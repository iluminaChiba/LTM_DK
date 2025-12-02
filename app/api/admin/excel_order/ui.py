# app/api/admin/excel_order/ui.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.core.preview_cache import PREVIEW_CACHE

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/import")
def excel_import_ui(request: Request):
    """Excelアップロード画面（入口）"""
    return templates.TemplateResponse(
        "admin/excel_import.html",
        {"request": request}
    )


@router.get("/register")
def excel_order_register_ui(token: str, request: Request):
    """注文登録画面（トークン経由でプレビューデータを表示）"""
    preview = PREVIEW_CACHE.get(token)
    if preview is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return templates.TemplateResponse(
        "admin/meal_order_register.html",
        {
            "request": request,
            "preview": preview
        }
    )
