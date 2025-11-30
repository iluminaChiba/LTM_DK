from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO
from datetime import datetime
import math

import openpyxl
import pandas as pd

router = APIRouter()


def safe_json_value(val):
    """JSON変換できない値（NaN, Inf）をNoneに変換"""
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
    return val


def has_border(cell) -> bool:
    """セルに上下左右どれかの罫線があるかどうか"""
    b = cell.border
    if b is None:
        return False
    return any([
        b.top and b.top.style,
        b.bottom and b.bottom.style,
        b.left and b.left.style,
        b.right and b.right.style,
    ])


def is_blank_like(val) -> bool:
    """pandasが読んだ値が「実質空白」かどうか"""
    if val is None:
        return True
    if pd.isna(val):
        return True
    if isinstance(val, str) and val.strip() == "":
        return True
    return False


@router.post("/preview")
async def preview(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # ============================================
        # STEP0: まず Excel の範囲を決める（6〜63）
        # ============================================
        START_ROW = 6
        END_ROW = 63

        # openpyxl(data_only=False) — 罫線や hidden を見る用
        wb = openpyxl.load_workbook(BytesIO(content), data_only=False)
        ws = wb.active

        # pandas(data_only=True 相当) — 実体値を見る用
        df = pd.read_excel(BytesIO(content), engine="openpyxl", sheet_name=0, header=None)

        # ============================================
        # STEP1: C列（3列目）の罫線で候補を絞る
        # ============================================
        def has_border(cell) -> bool:
            b = cell.border
            if not b:
                return False
            return any([
                b.top and b.top.style,
                b.bottom and b.bottom.style,
                b.left and b.left.style,
                b.right and b.right.style,
            ])

        candidate_rows = []
        for r in range(START_ROW, END_ROW + 1):
            if has_border(ws.cell(row=r, column=3)):
                candidate_rows.append(r)

        # ============================================
        # STEP2: pandas(data_only=True) で名前が空白でない行だけ残す
        # ============================================
        def is_blank_like(v) -> bool:
            if v is None:
                return True
            try:
                if pd.isna(v):
                    return True
            except Exception:
                pass

            if isinstance(v, (int, float)):
                return False

            if isinstance(v, str):
                cleaned = (
                    v.replace("\u3000", "")
                     .replace("\xa0", "")
                     .replace("\n", "")
                     .replace("\r", "")
                     .strip()
                )
                return cleaned == ""
            return False

        rows_after_step2 = []
        for r in candidate_rows:
            idx = r - 1
            if idx < 0 or idx >= len(df):
                continue

            # --- STEP2 で NaN をすべて None に正規化する ---
            raw_meal_id  = df.iat[idx, 1] if df.shape[1] > 1 else None
            raw_meal_name = df.iat[idx, 2] if df.shape[1] > 2 else None
            raw_qty       = df.iat[idx, 3] if df.shape[1] > 3 else None

            meal_id = safe_json_value(raw_meal_id)
            meal_name = safe_json_value(raw_meal_name)
            qty = safe_json_value(raw_qty)

            # 名前が実質空行は除外（STEP2）
            if is_blank_like(meal_name):
                continue

            rows_after_step2.append((r, meal_id, meal_name, qty))

        # ============================================
        # STEP3: hidden=true の行は除外（あなたの観測に基づく）
        # ============================================
        final_rows = []
        for (r, meal_id, meal_name, qty) in rows_after_step2:
            row_dim = ws.row_dimensions[r]
            if bool(row_dim.hidden):   # hidden=True → 除外
                continue

            # STEP2 で safe_json_value 済なのでここはそのまま入れて良い
            final_rows.append({
                "excel_row": r,
                "meal_id": meal_id,
                "meal_name": meal_name,
                "qty": qty,
            })

        # ============================================
        # rice（お米パック）の取得（既存処理のまま）
        # ここはあなたの過去のコードに合わせておきます
        # ============================================
        try:
            rice_val = df.iat[6, 17] if df.shape[1] > 17 else None
            rice_total = int(rice_val) if not pd.isna(rice_val) else None
        except:
            rice_total = None

        return {
            "filename": file.filename,
            "rows_range": [START_ROW, END_ROW],
            "candidate_rows_count": len(candidate_rows),
            "after_step2_count": len(rows_after_step2),
            "result_rows_count": len(final_rows),
            "rice": {
                "total": safe_json_value(rice_total),
            },
            "meals": final_rows,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"preview処理エラー: {str(e)}")
