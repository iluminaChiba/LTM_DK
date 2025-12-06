from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse
import pandas as pd
import tempfile
from pathlib import Path
import pdfplumber
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.preview_cache import PREVIEW_CACHE
from app.core.templates import templates
from app.core.database import get_db
from app.models.meal import Meal
from app.models.allergy import Allergy

router = APIRouter()

# ---------------------------------------------------------
# 公式アレルゲン29列（labels.csv 順）
# ---------------------------------------------------------
BASE_ALLERGY_NAMES = [
    "egg",                 # 卵
    "milk",                # 乳成分
    "wheat",               # 小麦
    "soba",                # そば
    "peanut",              # 落花生
    "shrimp",              # えび
    "crab",                # かに
    "walnut",              # くるみ
    "abalone",             # あわび
    "squid",               # いか
    "salmon_roe",          # いくら
    "salmon",              # さけ
    "mackerel",            # さば
    "seafood",             # 魚介類
    "beef",                # 牛肉
    "chicken",             # 鶏肉
    "pork",                # 豚肉
    "orange",              # オレンジ
    "kiwi",                # キウイフルーツ
    "apple",               # りんご
    "peach",               # もも
    "banana",              # バナナ
    "soy",                 # 大豆
    "cashew",              # カシューナッツ
    "almond",              # アーモンド
    "macadamia",           # マカダミアナッツ
    "yam",                 # やまいも
    "sesame",              # ごま
    "gelatin",             # ゼラチン
]

REQUIRED_COLS = len(BASE_ALLERGY_NAMES)  # = 29


# =========================================================
# 共通ユーティリティ
# =========================================================
def group_rows(words, row_tol: float = 2.5):
    """
    pdfplumber の words を top 座標で行ごとにまとめる。
    """
    if not words:
        return []

    words_sorted = sorted(words, key=lambda w: (w["top"], w["x0"]))
    rows = []
    current = []
    current_top = None

    for w in words_sorted:
        y = float(w["top"])
        if current_top is None:
            current_top = y
            current = [w]
            continue

        if abs(y - current_top) <= row_tol:
            current.append(w)
        else:
            rows.append(current)
            current = [w]
            current_top = y

    if current:
        rows.append(current)

    return rows


def is_menu_row(row_words):
    """
    行内に 3〜5 桁の数字があれば meal_id 行とみなす。
    """
    for w in row_words:
        t = w["text"].strip()
        if t.isdigit() and 3 <= len(t) <= 5:
            return True
    return False


def cluster_positions(xs, max_gap: float = 1.5):
    """
    近接した x 座標をクラスタリングし、中心値リストを返す。
    """
    if not xs:
        return []

    xs = sorted(xs)
    clusters = []
    cluster = [xs[0]]

    for x in xs[1:]:
        if x - cluster[-1] <= max_gap:
            cluster.append(x)
        else:
            clusters.append(cluster)
            cluster = [x]
    clusters.append(cluster)

    return [sum(c) / len(c) for c in clusters]


def extract_dots(page):
    """
    ● の位置を chars + images から取得し、(x, y) のリストで返す。
    """
    dots = []

    # ● が文字として描かれている場合
    for c in page.chars:
        if c.get("text") == "●":
            x = (float(c["x0"]) + float(c["x1"])) / 2.0
            y = (float(c["top"]) + float(c["bottom"])) / 2.0
            dots.append({"x": x, "y": y})

    # ● が小さな画像として貼られている場合
    for img in page.images:
        w = float(img.get("width", 0))
        h = float(img.get("height", 0))

        # 小さな正方形〜円っぽい画像だけを候補にする
        if 3 <= w <= 15 and 3 <= h <= 15:
            x = (float(img["x0"]) + float(img["x1"])) / 2.0
            # pdfplumber では top/bottom が無い場合があるので y0/y1 から補う
            top = float(img.get("top", img.get("y0", 0)))
            bottom = float(img.get("bottom", img.get("y1", top + h)))
            y = (top + bottom) / 2.0
            dots.append({"x": x, "y": y})

    return dots


def estimate_allergy_columns(page, dots):
    """
    縦罫線(page.lines)と●の分布から、
    アレルギー29列の列中心座標と、アレルギー領域の左境界・右境界を推定する。
    """

    # --- 1) 縦罫線の x 座標を取得 ---
    v_lines = [
        ln for ln in page.lines
        if abs(float(ln["x0"]) - float(ln["x1"])) < 0.5
        and (float(ln["bottom"]) - float(ln["top"])) > 20  # ある程度の高さを持つ線だけ
    ]
    v_xs_raw = [float(ln["x0"]) for ln in v_lines]

    v_centers = cluster_positions(v_xs_raw, max_gap=1.5)
    v_centers = sorted(v_centers)

    if not v_centers:
        raise HTTPException(400, "PDF内の縦罫線を検出できませんでした。レイアウトを確認してください。")

    # --- 2) ● の x 範囲を取得 ---
    if not dots:
        raise HTTPException(400, "PDF内にアレルギー ● が検出できませんでした。")

    dot_xs = [d["x"] for d in dots]
    min_dot = min(dot_xs)
    max_dot = max(dot_xs)

    # ● の範囲より少し余裕をもたせて境界候補を抽出
    margin = 5.0
    allergy_boundaries = [
        x for x in v_centers if (min_dot - margin) <= x <= (max_dot + margin)
    ]

    allergy_boundaries = sorted(allergy_boundaries)

    # 理想は 29列 → 30 本の境界
    expected_boundaries = REQUIRED_COLS + 1

    if len(allergy_boundaries) >= expected_boundaries:
        # 多過ぎる場合は中央部分を取り出す
        extra = len(allergy_boundaries) - expected_boundaries
        drop_left = extra // 2
        drop_right = extra - drop_left
        allergy_boundaries = allergy_boundaries[drop_left:len(allergy_boundaries) - drop_right]
    else:
        # 足りない場合は、●の範囲を等分して補完
        left = min_dot - 3.0
        right = max_dot + 3.0
        step = (right - left) / REQUIRED_COLS
        allergy_boundaries = [left + step * i for i in range(REQUIRED_COLS + 1)]

    if len(allergy_boundaries) != expected_boundaries:
        raise HTTPException(
            400,
            f"アレルギー列の境界数が不正です（{len(allergy_boundaries)}本検出、期待値 {expected_boundaries}）。"
        )

    allergy_boundaries = sorted(allergy_boundaries)
    allergy_left = allergy_boundaries[0]
    allergy_right = allergy_boundaries[-1]

    # 列中心
    col_centers = [
        (allergy_boundaries[i] + allergy_boundaries[i + 1]) / 2.0
        for i in range(REQUIRED_COLS)
    ]

    return col_centers, allergy_left, allergy_right


def detect_column(x0: float, col_centers):
    """
    x0 が属するアレルギー列 index (0〜28) を返す。
    """
    return min(range(len(col_centers)), key=lambda i: abs(col_centers[i] - x0))


def get_all_meal_ids_from_db(db: Session) -> set[int]:
    """
    データベースから全てのmeal_idを取得してセットで返す
    """
    stmt = select(Meal.meal_id)
    result = db.scalars(stmt).all()
    result_list = list(result)
    print(f"DEBUG [get_all_meal_ids_from_db]: result count = {len(result_list)}")
    print(f"DEBUG [get_all_meal_ids_from_db]: first 10 = {result_list[:10]}")
    result_set = set(result_list)
    print(f"DEBUG [get_all_meal_ids_from_db]: set size = {len(result_set)}")
    return result_set


# =========================================================
# ルーティング
# =========================================================
@router.get("/import", response_class=HTMLResponse)
def allergy_ui(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("admin/allergy_import.html", context)


@router.post("/upload")
async def allergy_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "PDFファイルを指定してください。")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        with pdfplumber.open(str(tmp_path)) as pdf:
            if not pdf.pages:
                raise HTTPException(400, "PDF にページが存在しません。")

            page = pdf.pages[0]

            # words 抽出 → 行構成
            words = page.extract_words()
            if not words:
                raise HTTPException(400, "PDF からテキストを抽出できませんでした。")

            rows = group_rows(words)

            # メニュー行だけ抜き出す
            menu_rows = [sorted(r, key=lambda w: w["x0"]) for r in rows if is_menu_row(r)]

            if not menu_rows:
                raise HTTPException(400, "メニュー行が抽出できませんでした。")

            # ● の位置
            dots = extract_dots(page)

            # アレルギー29列の中心と左右境界を、縦罫線＋● から推定
            col_centers, allergy_left, allergy_right = estimate_allergy_columns(page, dots)

            # 行ごとの y 範囲も保持しておく
            menu_rows_with_bounds = []
            for r in menu_rows:
                tops = [float(w["top"]) for w in r]
                bottoms = [float(w["bottom"]) for w in r]
                row_top = min(tops)
                row_bottom = max(bottoms)
                menu_rows_with_bounds.append((r, row_top, row_bottom))

            results = []

            # 各メニュー行を解析
            for row_words, row_top, row_bottom in menu_rows_with_bounds:
                # meal_id と name 抽出
                meal_id = None
                meal_id_x = None
                name_parts = []

                for w in row_words:
                    t = w["text"].strip()
                    x = float(w["x0"])

                    # meal_id: 左側、3〜5桁の数字
                    if meal_id is None and t.isdigit() and 3 <= len(t) <= 5 and x < allergy_left - 10:
                        meal_id = int(t)
                        meal_id_x = x
                        continue

                if meal_id is None:
                    # 想定外行はスキップ
                    continue

                # name: meal_id より右、アレルギー領域より左の文字を結合
                for w in row_words:
                    t = w["text"]
                    x = float(w["x0"])
                    if meal_id_x is not None and meal_id_x < x < allergy_left - 5:
                        # 全角スペースなどもまとめておく
                        if t != "●":
                            name_parts.append(t)

                name = "".join(name_parts).strip()

                # 行に属する ● を dots から拾う（y 近傍で判定）
                row_center_y = (row_top + row_bottom) / 2.0
                row_dots = [
                    d for d in dots
                    if (row_top - 2.0) <= d["y"] <= (row_bottom + 2.0)
                ]

                vec = [0] * REQUIRED_COLS

                for d in row_dots:
                    if not (allergy_left <= d["x"] <= allergy_right):
                        continue
                    col_index = detect_column(d["x"], col_centers)
                    if 0 <= col_index < REQUIRED_COLS:
                        vec[col_index] = 1

                rec = {
                    "meal_id": meal_id,
                    "name": name,
                }
                rec.update({BASE_ALLERGY_NAMES[i]: vec[i] for i in range(REQUIRED_COLS)})
                results.append(rec)

            df = pd.DataFrame(results)

            preview_json = df.where(pd.notnull(df), None).to_dict(orient="records")
            
            # ------------------------------------------------------------
            # 2. allergies × PDF の比較（アレルギー差分）
            # ------------------------------------------------------------
            existing_allergies = {
                row.meal_id: row for row in db.scalars(select(Allergy)).all()
            }

            incoming_ids = { row["meal_id"] for row in preview_json }

            allergy_new = []
            allergy_updated = []
            allergy_unchanged = []

            for row in preview_json:
                meal_id = row["meal_id"]
                if meal_id not in existing_allergies:
                    allergy_new.append(meal_id)
                else:
                    # 既存レコードと比較 → 変更あり？
                    model = existing_allergies[meal_id]
                    # model.__dict__ と row の一致チェック
                    changed = False
                    for key, value in row.items():
                        if hasattr(model, key) and getattr(model, key) != value:
                            changed = True
                            break
                    if changed:
                        allergy_updated.append(meal_id)
                    else:
                        allergy_unchanged.append(meal_id)

            # ------------------------------------------------------------
            # 3. meals × PDF の比較（新規メニュー差分）
            # ------------------------------------------------------------
            existing_meals = set(db.scalars(select(Meal.meal_id)).all())

            meal_new = sorted(incoming_ids - existing_meals)
            meal_existing = sorted(incoming_ids & existing_meals)

            token = str(uuid4()) # シンプルなトークンを生成
            
            # ------------------------------------------------------------
            # 4. PREVIEW_CACHE の正式形
            # ------------------------------------------------------------
            PREVIEW_CACHE[token] = {
                "rows": preview_json,

                # アレルギー差分
                "allergy_new": allergy_new,
                "allergy_updated": allergy_updated,
                "allergy_unchanged": allergy_unchanged,

                # メニュー差分
                "meal_new": meal_new,
                "meal_existing": meal_existing,
            }
            # ------------------------------------------------------------
            # 5. フロント側への返り値 — 人間確認用
            # ------------------------------------------------------------
            return {
                "status": "ok",
                "token": token,
                "total_preview_rows": len(preview_json),

                # アレルギー差分
                "allergy_new": allergy_new,
                "allergy_updated": allergy_updated,
                "allergy_unchanged": allergy_unchanged,

                # メニュー差分
                "meal_new": meal_new,
                "meal_existing": meal_existing,

                "records": preview_json,
            }            
    except HTTPException:
        raise
    except Exception as e:
        # ログ出力（デバッグ用）
        print(f"Internal Error in PDF processing: {e}")
        raise HTTPException(500, f"内部エラーが発生しました: {e}")
    finally:
        tmp_path.unlink(missing_ok=True)

