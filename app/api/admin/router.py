# app/api/admin/router.py

from fastapi import APIRouter
from app.api.admin import excel_import
from app.api.admin.excel_order.router import router as excel_order_router

admin_router = APIRouter()

# 管理画面ルーター統合
admin_router.include_router(excel_import.router, tags=["Admin - Excel Import"])
admin_router.include_router(excel_order_router, prefix="/excel_order", tags=["Admin - Excel Order"])
