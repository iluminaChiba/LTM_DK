# app/api/admin/excel_order/upload.py

import secrets
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.preview_cache import PREVIEW_CACHE
from .preview import parse_excel_order
from .ui import router as ui_router
from .confirm import router as confirm_router
from app.models.pending_box import PendingBox
from app.utils.excel_writer import generate_filled_excel
from pathlib import Path
import uuid

router = APIRouter()

# サブルーターは admin/router.py で個別に登録するため、ここでは統合しない


@router.post("/upload")
async def upload_excel_order(file: UploadFile = File(...)):
    """
    Excelファイルをアップロードしてプレビューデータを生成
    トークンを発行してメモリキャッシュに保存
    """
    try:
        content = await file.read()
        
        # Excel解析
        preview_data = await parse_excel_order(content, file.filename)
        
        # トークン発行してキャッシュに保存
        token = secrets.token_hex(8)
        PREVIEW_CACHE[token] = preview_data
        
        return {
            "status": "success",
            "token": token,
            "preview": preview_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel処理エラー: {str(e)}")
    
@router.get("/export_filled_excel")
def export_filled_excel(db: Session = Depends(get_db)):
    """
    pending_box に登録された数量を Excel に書き戻して返す。
    今は「直近の source_filename を使う」という想定。
    """

    # 1. pending の注文を取得
    items = db.query(PendingBox).filter(PendingBox.status == "pending").all()

    if not items:
        return {"message": "pending の注文がありません"}

    # 2. Excel 原本パスを決定（source_filename から生成）
    #    → 現在は resources/ に原本が保存されている前提
    source_filename = items[0].source_filename  # 全部同じ Excel の想定
    source_path = Path(f"app/resources/excels/{source_filename}")

    if not source_path.exists():
        return {"error": f"原本Excelが見つかりません: {source_path}"}

    # 3. 書き戻し先（output）を作成
    output_path = Path(f"/tmp/filled_{uuid.uuid4()}.xlsx")

    # 4. pending_box の行番号と数量だけ抽出
    pending_list = [
        {
            "excel_row": item.excel_row,
            "qty": item.qty
        }
        for item in items
    ]

    # 5. Excel を生成
    generated = generate_filled_excel(
        source_path=str(source_path),
        output_path=str(output_path),
        pending_items=pending_list
    )

    # 6. 生成されたファイルを返す
    return FileResponse(
        generated,
        filename=f"注文票_{items[0].arrival_date}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
