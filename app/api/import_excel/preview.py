from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

router = APIRouter()
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
from io import BytesIO
import pandas as pd
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/preview")
async def preview_excel(file: UploadFile = File(...)) -> Dict[str, Any]:

    # 拡張子チェック
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Excelファイルをアップロードしてください。")

    # バイナリ読み込み
    content = await file.read()

    try:
        df = pd.read_excel(BytesIO(content), sheet_name="取込用")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel読み込みに失敗しました: {str(e)}")

    # --- Step 1: 必要な列の存在確認 ---
    required_cols = ["商品コード", "商品名", "着日"]
    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"必要な列 '{col}' が見つかりません。")

    # --- Step 2: 文字列に変換して整形 ---
    df["商品コード"] = df["商品コード"].astype("string")
    df["商品名"] = df["商品名"].astype("string")
    df["着日"] = df["着日"].astype("string")

    # --- Step 3: 商品コードが欠けている行を除外 ---
    df = df[df["商品コード"].notna()]

    # --- Step 4: 着日の正規化（2025年12月9日 → 2025-12-09） ---
    def normalize_date(x: str):
        try:
            return datetime.strptime(x.strip(), "%Y年%m月%d日").date()
        except:
            return None

    df["parsed_date"] = df["着日"].apply(normalize_date)
    df = df[df["parsed_date"].notna()]

    # --- Step 5: 週の計算 ---
    # 同一ファイル内はすべて同じ週である前提（実際にそう）
    start_date = df["parsed_date"].min()
    end_date = df["parsed_date"].max()

    # --- Step 6: meals 用データ（重複削除） ---
    meals_preview = (
        df[["商品コード", "商品名"]]
        .drop_duplicates()
        .rename(columns={
            "商品コード": "vendor_item_id",
            "商品名": "name"
        })
        .to_dict(orient="records")
    )

    # --- Step 7: weekly_menus 用データ（vendor_item_id の一覧） ---
    weekly_menu_preview = sorted(set(df["商品コード"].tolist()))

    # --- Step 8: プレビューの返却構造（commit APIの入力形式と互換） ---
    result = {
        "filename": file.filename,
        "week": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        "meals": meals_preview,
        "weekly_menu_items": weekly_menu_preview
    }

    return result

