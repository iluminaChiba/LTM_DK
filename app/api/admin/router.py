# app/api/admin/router.py

from fastapi import APIRouter
from app.api.admin.excel_order.upload import router as excel_order_upload_router
from app.api.admin.excel_order.ui import router as excel_order_ui_router
from app.api.admin.excel_order.confirm import router as excel_order_confirm_router

admin_router = APIRouter()

# 管理画面ルーター統合（タグで分離）
admin_router.include_router(excel_order_upload_router, prefix="/excel_order", tags=["Admin - Excel Order"])
admin_router.include_router(excel_order_ui_router, prefix="/excel_order", tags=["Admin - Excel Order"])
admin_router.include_router(excel_order_confirm_router, prefix="/excel_order", tags=["Admin - Excel Order"])