# app/api/admin/excel_import.py

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.core.dependencies import get_template_manager
from app.template_manager import TemplateManager

router = APIRouter()


@router.get("/excel_import", response_class=HTMLResponse)
def admin_excel_import(
    request: Request,
    tm: TemplateManager = Depends(get_template_manager)
):
    """管理者用Excelインポート画面"""
    return tm.render("admin/excel_import.html", {})
