# app/api/admin/router.py
from fastapi import APIRouter
from app.api.admin.excel_order.router import router as excel_order_router

admin_router = APIRouter()

admin_router.include_router(
    excel_order_router,
    prefix="/excel_order",
    tags=["Admin - Excel Order"]
)
