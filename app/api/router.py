# app/api/router.py

from fastapi import APIRouter, Depends, Request
from app.api import person, meal, meal_log, supply, reports, entry, ui_test, import_excel, ui_allergy, allergy
from app.core.dependencies import get_template_manager
from fastapi.responses import HTMLResponse
from app.template_manager import TemplateManager


api_router = APIRouter()

api_router.include_router(person.router, prefix="/persons", tags=["Persons"])
api_router.include_router(meal.router, prefix="/meals", tags=["Meals"])
api_router.include_router(allergy.router, prefix="/allergy", tags=["Allergy"])
api_router.include_router(meal_log.router, prefix="/meal_logs", tags=["MealLogs"])
api_router.include_router(supply.router, prefix="/supplies", tags=["Supplies"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(entry.router, prefix="/entry", tags=["Entry"])
api_router.include_router(import_excel.preview_router, prefix="/preview", tags=["Preview"])
api_router.include_router(ui_allergy.router, prefix="/allergies", tags=["Allergies"])
api_router.include_router(import_excel.commit_router, prefix="/commit", tags=["Commit"])
# DEBUG Statics 
api_router.include_router(ui_test.router, prefix="/statics", tags=["Statics"])
# END DEBUG


# DEBUG 管理者用Excelインポート画面のルーティングのテスト用 あくまで臨時の配置です！
@api_router.get("/admin/excel_import", response_class=HTMLResponse)
def admin_excel_import(
    request: Request,
    tm: TemplateManager = Depends(get_template_manager)
):
    return tm.render("admin/excel_import.html", {})
# END DEBUG

