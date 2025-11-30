# app/api/admin/excel_order/preview.py

import math
import openpyxl
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta


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


async def parse_excel_order(file_content: bytes, filename: str) -> dict:
    """
    Excelファイルを解析して注文データを抽出
    
    Returns:
        dict: プレビューデータ（filename, meals, rice, etc.）
    """
    START_ROW = 6
    END_ROW = 63

    # openpyxl(data_only=False) — 罫線や hidden を見る用
    wb = openpyxl.load_workbook(BytesIO(file_content), data_only=False)
    ws = wb.active

    # pandas(data_only=True 相当) — 実体値を見る用
    df = pd.read_excel(BytesIO(file_content), engine="openpyxl", sheet_name=0, header=None)

    # ============================================
    # STEP1: C列（3列目）の罫線で候補を絞る
    # ============================================
    candidate_rows = []
    for r in range(START_ROW, END_ROW + 1):
        if has_border(ws.cell(row=r, column=3)):
            candidate_rows.append(r)

    # ============================================
    # STEP2: pandas で名前が空白でない行だけ残す
    # ============================================
    def is_blank_like_extended(v) -> bool:
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

        raw_meal_id = df.iat[idx, 1] if df.shape[1] > 1 else None
        raw_meal_name = df.iat[idx, 2] if df.shape[1] > 2 else None
        raw_qty = df.iat[idx, 3] if df.shape[1] > 3 else None

        meal_id = safe_json_value(raw_meal_id)
        meal_name = safe_json_value(raw_meal_name)
        qty = safe_json_value(raw_qty)

        # 名前が実質空行は除外（STEP2）
        if is_blank_like_extended(meal_name):
            continue

        rows_after_step2.append((r, meal_id, meal_name, qty))

    # ============================================
    # STEP3: hidden=true の行は除外
    # ============================================
    final_rows = []
    for (r, meal_id, meal_name, qty) in rows_after_step2:
        row_dim = ws.row_dimensions[r]
        if bool(row_dim.hidden):
            continue

        final_rows.append({
            "excel_row": r,
            "meal_id": meal_id,
            "meal_name": meal_name,
            "qty": qty,
        })

    # ============================================
    # rice（お米パック）の取得
    # ============================================
    try:
        rice_val = df.iat[6, 17] if df.shape[1] > 17 else None
        rice_total = int(rice_val) if not pd.isna(rice_val) else None
    except:
        rice_total = None

    # 日付情報の取得（着日はI1）
    try:
        arrival_date_val = df.iat[0, 8] if df.shape[1] > 8 else None  # I1
        
        if pd.notna(arrival_date_val):
            # pandas Timestamp を date に変換
            if hasattr(arrival_date_val, 'date'):
                # pandasのTimestamp型の場合
                arrival_dt = arrival_date_val.date()
            else:
                # 文字列の場合（日本語形式: "2025年12月9日"）
                import re
                date_str = str(arrival_date_val)
                match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
                if match:
                    year, month, day = match.groups()
                    arrival_dt = datetime(int(year), int(month), int(day)).date()
                else:
                    # YYYY-MM-DD形式も試す
                    arrival_dt = datetime.strptime(date_str[:10], '%Y-%m-%d').date()
            
            arrival_date = arrival_dt.isoformat()
            # 着日 + 1日 = 適用日
            applicable_date = (arrival_dt + timedelta(days=1)).isoformat()
        else:
            arrival_date = None
            applicable_date = None
            
    except Exception as e:
        print(f"日付取得エラー: {e}")
        import traceback
        traceback.print_exc()
        arrival_date = None
        applicable_date = None
        
    return {
        "filename": filename,
        "arrival_date": arrival_date,
        "applicable_date": applicable_date,
        "rows_range": [START_ROW, END_ROW],
        "candidate_rows_count": len(candidate_rows),
        "after_step2_count": len(rows_after_step2),
        "result_rows_count": len(final_rows),
        "rice": {
            "total": safe_json_value(rice_total),
        },
        "meals": final_rows,
    }
