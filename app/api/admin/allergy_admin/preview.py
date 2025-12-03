from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pandas as pd
import tempfile
from pathlib import Path
import camelot

from app.core.preview_cache import PREVIEW_CACHE

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------------------------------------------------------
# ① /import ： UI を返すだけ
# ---------------------------------------------------------
@router.get("/import", response_class=HTMLResponse)
def allergy_import_ui(request: Request):
    return templates.TemplateResponse(
        "admin/allergy_import.html",
        {"request": request}
    )


# ---------------------------------------------------------
# ② /upload ： PDF → Camelot(stream) → DataFrame → JSON
# ---------------------------------------------------------
@router.post("/upload")
async def allergy_upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "PDFファイルを選択してください")

    # 一時保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        # -------------------------
        # Camelot(stream) で PDF を解析
        # このPDFはlatticeモードでは正しく解析できないため、streamを使用
        # 列ズレは後処理で対応
        # -------------------------
        tables = camelot.read_pdf(
            str(tmp_path),
            pages="1",
            flavor="stream",
        )

        if tables.n == 0:
            raise HTTPException(
                400,
                "PDF から表を検出できませんでした。レイアウトが変わった可能性があります。"
            )

        raw_df = tables[0].df

        # -------------------------
        # DataFrame の基本正規化
        # -------------------------
        raw_df.columns = [f"col_{i}" for i in range(len(raw_df.columns))]
        df = raw_df.copy()

        # col_0 が行番号等の場合は削除
        df = df.drop(columns=["col_0"], errors="ignore")

        # ヘッダー行（空行）を削除
        df = df[df["col_1"].astype(str).str.strip() != ""]

        # -------------------------
        # meal_id と name の分割（col_1 から）
        # -------------------------
        if "col_1" not in df.columns:
            raise HTTPException(
                400,
                f"PDF の列構造が想定と異なります。検出された列: {list(df.columns)}"
            )

        # col_1 から meal_id と name を抽出
        # 例: "8118 タラの牛だしあん" → meal_id=8118, name="タラの牛だしあん"
        df["col_1"] = df["col_1"].astype(str).str.strip()
        
        # スペースで分割して最初の部分をmeal_id、残りをnameとする
        split_data = df["col_1"].str.split(n=1, expand=True)
        
        if split_data.shape[1] < 2:
            raise HTTPException(
                400,
                f"col_1からmeal_idとnameを分割できません。サンプル: {df['col_1'].head(3).tolist()}"
            )
        
        df["meal_id"] = pd.to_numeric(split_data[0], errors="coerce")
        df["name"] = split_data[1].fillna("").astype(str).str.strip()

        if df["meal_id"].isna().all():
            raise HTTPException(
                400,
                f"PDF から meal_id を抽出できません。col_1の内容: {df['col_1'].head(10).tolist()}"
            )

        df = df.dropna(subset=["meal_id"])
        df["meal_id"] = df["meal_id"].astype(int)

        # -------------------------
        # アレルギー列の自動検出
        # col_1がmeal_id+nameなので、アレルギー列はcol_2から開始
        # -------------------------
        # まず全列を確認
        total_cols = len(df.columns)
        print(f"\n=== DEBUG: 総列数 = {total_cols}, 列名: {list(df.columns)} ===\n")
        
        # col_2以降を全てアレルギー列として扱う
        allergy_cols = [f"col_{i}" for i in range(2, total_cols)]
        existing = [c for c in allergy_cols if c in df.columns]
        
        print(f"=== DEBUG: アレルギー列数 = {len(existing)} ===\n")

        if len(existing) < 28:
            raise HTTPException(
                400,
                f"アレルギー列が不足しています（{len(existing)}列検出、最低28列必要）。PDFレイアウトを確認してください。"
            )

        # アレルギー名は検出された列数に応じて調整
        base_allergy_names = [
            "egg", "milk", "wheat", "soba", "peanut", "shrimp", "crab",
            "walnut", "abalone", "squid", "salmon_roe", "salmon",
            "mackerel", "seafood", "beef", "chicken", "pork",
            "orange", "kiwi", "apple", "peach", "banana", "soy",
            "cashew", "almond", "macadamia", "yam", "sesame", "gelatin"
        ]
        
        # 検出された列数に合わせてallergy_namesを調整
        allergy_names = base_allergy_names[:len(existing)]
        if len(existing) > len(base_allergy_names):
            # 予想外に列が多い場合は、extra_1, extra_2... で埋める
            allergy_names.extend([f"extra_{i}" for i in range(1, len(existing) - len(base_allergy_names) + 1)])

        print(f"=== DEBUG: allergy_cols length = {len(allergy_cols)}, existing length = {len(existing)} ===")
        print(f"=== DEBUG: allergy_names length = {len(allergy_names)} ===")
        
        # meal_id 8118 の全列データを確認
        sample_row = df[df["meal_id"] == 8118]
        if not sample_row.empty:
            print("\n=== DEBUG: meal_id=8118 の全列データ ===")
            marked_cols = []
            for col in existing:
                val = sample_row[col].iloc[0]
                if str(val).strip() == "●":
                    marked_cols.append(col)
                print(f"{col}: [{repr(val)}]")
            print(f"\n●がある列: {marked_cols}")
            print("=" * 60 + "\n")
        
        allergy_matrix = df[existing].apply(  # allergy_colsではなくexistingを使う
            lambda col: col.apply(lambda x: 1 if str(x).strip() == "●" else 0)
        )
        
        print(f"=== DEBUG: allergy_matrix shape = {allergy_matrix.shape} ===")
        
        allergy_matrix.columns = allergy_names
        
        # 警告メッセージを追加（検出列数が29未満の場合）
        if len(existing) < 29:
            print(f"\n⚠️ 警告: アレルギー列が{len(existing)}列しか検出されませんでした（期待値: 29列）")
            print(f"   最後の列（{base_allergy_names[len(existing):]}）が欠落している可能性があります\n")

        # -------------------------
        # 結合して JSON 化
        # -------------------------
        result_df = pd.concat(
            [df[["meal_id", "name"]], allergy_matrix],
            axis=1
        )

        preview_json = result_df.where(
            pd.notnull(result_df), None
        ).to_dict(orient="records")

        PREVIEW_CACHE["allergy_preview"] = preview_json

        return {
            "status": "ok",
            "rows": len(preview_json),
            "records": preview_json
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            500,
            f"予期しないエラーが発生しました：{str(e)}"
        )
    finally:
        tmp_path.unlink(missing_ok=True)
