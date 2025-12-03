from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pandas as pd
import tabula
import tempfile
from pathlib import Path

from app.core.preview_cache import PREVIEW_CACHE

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------------------------------------------------------
# ① /import ： UI を返すだけ（Excel と完全同じ）
# ---------------------------------------------------------
@router.get("/import", response_class=HTMLResponse)
def allergy_import_ui(request: Request):
    """
    アレルギー表取り込み画面（入口）
    Excel order importer と同じ構造で、UI を返すだけ。
    """
    return templates.TemplateResponse(
        "admin/allergy_import.html",
        {"request": request}
    )


# ---------------------------------------------------------
# ② /upload ： PDF → DataFrame → JSON → PREVIEW_CACHE
# ---------------------------------------------------------
@router.post("/upload")
async def allergy_upload(file: UploadFile = File(...)):
    """
    PDFUpload → Preview JSON を返す。
    Excel importer の upload(preview) と同位置の処理。
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "PDFファイルを選択してください")

    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        # PDF → DataFrame 抽出（lattice=True が重要）
        dfs = tabula.read_pdf(str(tmp_path), pages="1", lattice=True)
        dfs = tabula.read_pdf(str(tmp_path), pages="1", area=(300, 0, 9999, 9999), lattice=True)

        if not dfs or dfs[0].empty:
            raise HTTPException(400, "PDFから表を抽出できませんでした")

        df = dfs[0]

        # -------------------------
        # DataFrame 正規化処理
        # -------------------------
        df.columns = [f"col_{i}" for i in range(len(df.columns))]

        # ヘッダー行を削除（1行目が「卵」などのヘッダーの場合）
        # 最初の行にmeal_idが入っていない場合はスキップ
        if df.shape[0] > 0:
            try:
                # 試しに最初の行をintに変換してみる
                int(df.iloc[0]["col_1"])
            except (ValueError, KeyError):
                # 変換できない = ヘッダー行なので削除
                df = df.iloc[1:].reset_index(drop=True)

        # 不要列（行番号）を削除
        df = df.drop(columns=["col_0"], errors="ignore")
        # meal_id（数値に変換できない行はスキップ）
        df["meal_id"] = pd.to_numeric(df["col_1"], errors="coerce")
        df = df.dropna(subset=["meal_id"])  # NaNの行を削除
        df["meal_id"] = df["meal_id"].astype(int)

        # メニュー名
        df["name"] = df["col_2"].astype(str).str.strip()

        # ●→1変換（アレルギー28列）
        allergy_cols = [f"col_{i}" for i in range(3, 31)]
        allergy_matrix = df[allergy_cols].apply(
            lambda col: col.apply(lambda x: 1 if str(x).strip() == "●" else 0)
        )

        result_df = pd.concat(
            [df[["meal_id", "name"]], allergy_matrix],
            axis=1
        )

        # JSON 化
        preview_json = result_df.to_dict(orient="records")

        # confirm のために保存
        PREVIEW_CACHE["allergy_preview"] = preview_json

        return {
            "status": "ok",
            "rows": len(preview_json),
            "records": preview_json
        }

    except Exception as e:
        raise HTTPException(500, f"PDF解析中にエラー: {str(e)}")

    finally:
        tmp_path.unlink(missing_ok=True)
