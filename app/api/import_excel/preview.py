from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
from io import BytesIO
import pandas as pd
from datetime import datetime

router = APIRouter()

@router.post("/preview")
async def preview_excel(file: UploadFile = File(...)) -> Dict[str, Any]:

    # --- Step 1: 拡張子チェック ---
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Excelファイルをアップロードしてください。")

    # --- Step 2: バイナリ読み込み ---
    content = await file.read()

    try:
        df = pd.read_excel(BytesIO(content), sheet_name="取込用")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel読み込みに失敗しました: {str(e)}")

    # --- Step 3: 必要な列の存在確認 ---
    required_cols = ["商品コード", "商品名", "着日"]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"必要な列 '{col}' が見つかりません。")

    # --- Step 4: 型の正規化（文字列化） ---
    df["商品コード"] = df["商品コード"].astype("string")
    df["商品名"] = df["商品名"].astype("string")
    df["着日"] = df["着日"].astype("string")

    # --- Step 5: 商品コードが欠けている行を除外 ---
    df = df[df["商品コード"].notna()]

    # --- Step 6: 日付の正規化 ---
    def normalize_date(x: str):
        try:
            return datetime.strptime(x.strip(), "%Y年%m月%d日").date()
        except:
            return None

    df["parsed_date"] = df["着日"].apply(normalize_date)
    df = df[df["parsed_date"].notna()]

    # --- Step 7: 週の開始日 ---
    week_start = df["parsed_date"].min()

    # --- Step 8: vendor_item_id の正規化 ---
    # commit との整合性のため「int に変換」する
    def normalize_code(x):
        try:
            return int(float(x))
        except:
            return None

    # meals 用 DF
    meals_df = (
        df[["商品コード", "商品名"]]
            .drop_duplicates()
            .rename(columns={
                "商品コード": "vendor_item_id",
                "商品名": "name",
            })
    )

    # null の除去
    meals_df = meals_df.dropna(subset=["vendor_item_id", "name"])

    # vendor_item_id を int 化
    meals_df["vendor_item_id"] = meals_df["vendor_item_id"].apply(normalize_code)
    meals_df = meals_df.dropna(subset=["vendor_item_id"])

    meals_preview = meals_df.to_dict(orient="records")

    # --- Step 9: weekly_menu_items（vendor_item_id の一覧） ---
    codes = df["商品コード"].apply(normalize_code).dropna().astype(int)
    weekly_menu_preview = sorted(set(codes.tolist()))

    # --- Step 10: commit API に渡す形式で返却 ---
    result = {
        "filename": file.filename,
        "week": {
            "week_start": week_start.isoformat()
        },
        "meals": meals_preview,
        "weekly_menu_items": weekly_menu_preview  # ← List[int]
    }

    return result
