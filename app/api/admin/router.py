# app/api/admin/router.py
from fastapi import APIRouter
from app.api.admin.excel_order.router import router as excel_order_router
from app.api.admin.allergy_admin.router import router as allergy_admin_router

admin_router = APIRouter()

admin_router.include_router(
    excel_order_router,
    prefix="/excel_order",
    tags=["Admin - Excel Order"]
)

admin_router.include_router(
    allergy_admin_router,
    prefix="/allergy_admin",
    tags=["Admin - Allergy"]
)
