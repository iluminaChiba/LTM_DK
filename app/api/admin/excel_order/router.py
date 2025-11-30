# app/api/admin/excel_order/router.py

import secrets
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.preview_cache import PREVIEW_CACHE
from .preview import parse_excel_order
from .ui import router as ui_router
from .confirm import router as confirm_router

router = APIRouter()

# サブルーターを統合
router.include_router(ui_router)
router.include_router(confirm_router)


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
