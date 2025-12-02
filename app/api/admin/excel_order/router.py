# app/api/admin/excel_order/router.py
from fastapi import APIRouter

# 各機能モジュールの router を取り込む
from .upload import router as upload_router
from .preview import router as preview_router
from .confirm import router as confirm_router
from .export import router as export_router

router = APIRouter()

# ここで Excel Order 系 API を統合
router.include_router(upload_router)
router.include_router(preview_router)
router.include_router(confirm_router)
router.include_router(export_router)
