# routers/ui_meal_order_register.py
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
# from app.preview import run_preview  # TODO: preview関数の実装

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/admin")

@router.get("/admin/meal-order-register")
def ui_meal_order_register(request: Request):
    # TODO: 実際のpreview処理を実装
    preview_data = {"filename": "test.xlsx", "result_rows_count": 0, "meals": []}
    return templates.TemplateResponse(
        "meal_order_register.html",
        {"request": request, "preview": preview_data}
    )
