from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import pandas as pd
import openpyxl
from io import BytesIO

router = APIRouter()


def has_border(cell):
    """セルに上下左右どれかの罫線があるかどうか"""
    b = cell.border
    return any([
        b.top.style,
        b.bottom.style,
        b.left.style,
        b.right.style,
    ])


def is_effectively_blank(value):
    """Excel の '見た目が空' を正しく検出する強化版"""
    if value is None:
        return True

    if isinstance(value, float) and pd.isna(value):
        return True

    if isinstance(value, str):
        cleaned = (
            value.replace("\u3000", "")   # 全角空白（Mac/Win共通）
                 .replace("\xa0", "")    # NBSP（主にMacやWeb系）
                 .replace("\n", "")
                 .replace("\r", "")
                 .strip()
        )
        return cleaned == ""

    return False


@router.post("/preview")
async def preview_excel(file: UploadFile = File(...)):
    try:
        content = await file.read()
        wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
        ws = wb.active

        # ---------------------------------------------------------
        # 1) 週開始日（I1）を取得
        # ---------------------------------------------------------
        raw_date = ws["I1"].value
        if isinstance(raw_date, str):
            week_start = datetime.strptime(raw_date.strip(), "%Y年%m月%d日").date()
        elif isinstance(raw_date, datetime):
            week_start = raw_date.date()
        else:
            raise HTTPException(
                status_code=400,
                detail="Excel解析エラー：着日セル(I1)から日付が読み取れません。",
            )

        # ---------------------------------------------------------
        # 2) C列に「健康管理食選択型」がある行をヘッダ行とみなす
        #    （= 商品名カラムのヘッダ）
        # ---------------------------------------------------------
        header_excel_row = None
        for row in range(1, ws.max_row + 1):
            val = ws.cell(row=row, column=3).value  # C列
            if isinstance(val, str) and "健康管理食選択型" in val:
                header_excel_row = row
                break

        if header_excel_row is None:
            raise HTTPException(
                status_code=400,
                detail="Excel解析エラー：C列に「健康管理食選択型」を持つヘッダ行が見つかりません。",
            )

        # pandas の header は 0-based 行番号なので -1
        pandas_header_idx = header_excel_row - 1

        # ---------------------------------------------------------
        # 3) pandas でヘッダ付きとして読み込み
        #    A列: 謎の数字, B列: コード, C列: 健康管理食選択型(=商品名)
        # ---------------------------------------------------------
        df_raw = pd.read_excel(BytesIO(content), header=pandas_header_idx, dtype=str)

        # 少なくとも B,C 列までは存在してほしい
        if len(df_raw.columns) < 3:
            raise HTTPException(
                status_code=400,
                detail="Excel解析エラー：列数が不足しています。（少なくとも3列必要）",
            )

        # 列位置で商品コード・商品名を決め打ち
        code_col = df_raw.columns[1]  # B列
        name_col = df_raw.columns[2]  # C列（健康管理食選択型）

        df = df_raw.copy()
        df = df.rename(columns={
            code_col: "商品コード",
            name_col: "商品名",
        })

        # ---------------------------------------------------------
        # 4) openpyxl 側で行情報を収集
        #    コードは B列, 名称は C列 から取得
        # ---------------------------------------------------------
        excel_info = {}
        for row in range(1, ws.max_row + 1):
            code_cell = ws.cell(row=row, column=2)  # B列: コード
            name_cell = ws.cell(row=row, column=3)  # C列: 商品名

            excel_info[row] = {
                "code": code_cell.value,
                "name": name_cell.value,
                "height": ws.row_dimensions[row].height,
                "hidden": ws.row_dimensions[row].hidden,
                "invisible": (ws.row_dimensions[row].height == 0),
                "border_code": has_border(code_cell),
                "border_name": has_border(name_cell),
            }

        # ---------------------------------------------------------
        # 5) df の各行に対応する Excel の行番号(excel_row)を紐づける
        # ---------------------------------------------------------
        excel_rows = []
        for j in range(len(df)):
            code = df.iloc[j]["商品コード"]
            row_found = None

            if not is_effectively_blank(code):
                for r, info in excel_info.items():
                    if str(info["code"]) == str(code):
                        row_found = r
                        break

            excel_rows.append(row_found)

        df["excel_row"] = excel_rows




        for i in range(len(df)):
            erow = df.iloc[i]["excel_row"]
            code = df.iloc[i]["商品コード"]
            name = df.iloc[i]["商品名"]

            # ★ NaN 対策（ここでスキップ）
            if pd.isna(erow):
                continue

            # --- デバッグ出力 ------------------------
            info = excel_info.get(erow, {})
            name_cell = ws.cell(row=erow, column=3) if erow else None

            safe_hex = (
                " ".join(f"{ord(ch):04x}" for ch in str(name))
                if isinstance(name, str) else "None"
            )

            print(f"[CHECK] excel_row={erow}, code={code}, "
                f"name='{name}', HEX={safe_hex}, "
                f"font_color={getattr(name_cell.font, 'color', None) if name_cell else None}, "
                f"border={info.get('border_name') if info else None}, "
                f"hidden={info.get('hidden') if info else None}, "
                f"invisible={info.get('invisible') if info else None}")
            # ------------------------------------------





        # ---------------------------------------------------------
        # 6) データ行フィルタ
        #    - excel_row が取れている
        #    - 行が非表示/高さ0 ではない
        #    - 商品名が空でない
        #    - 商品名セルに罫線がある（=本物の行）
        # ---------------------------------------------------------
        def is_valid_row(idx: int) -> bool:
            erow = df.iloc[idx]["excel_row"]
            name = df.iloc[idx]["商品名"]

            if erow is None:
                return False

            info = excel_info.get(erow, {})

            if info.get("hidden") or info.get("invisible"):
                return False

            if is_effectively_blank(name):
                return False

            if not info.get("border_name"):
                return False

            return True

        # ---------------------------------------------------------
        # 7) 抽出
        # ---------------------------------------------------------
        meals = []
        weekly_menu_preview = []


        for i in range(len(df)):
            if is_valid_row(i):
                code = df.iloc[i]["商品コード"]
                name = df.iloc[i]["商品名"]

                try:
                    vid = int(str(code))
                except ValueError:
                    # 数値化できないコードはスキップ
                    continue


                meals.append({
                    "vendor_item_id": vid,
                    "name": name,
                })
                weekly_menu_preview.append(vid)

        return {
            "filename": file.filename,
            "week": {"week_start": week_start.isoformat()},
            "meals": meals,
            "weekly_menu_preview": weekly_menu_preview,
        }

    except HTTPException:
        # そのまま投げ直し
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel解析エラー: {str(e)}")
