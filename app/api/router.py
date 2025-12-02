# app/api/router.py

from fastapi import APIRouter
from app.api import person, meal, meal_log, supply, reports, entry, ui_test, ui_allergy, allergy, pending_box, daily_stock, order, stock
from app.api.admin.router import admin_router


api_router = APIRouter()

# データAPI
api_router.include_router(person.router, prefix="/persons", tags=["Persons"])
api_router.include_router(meal.router, prefix="/meals", tags=["Meals"])
api_router.include_router(allergy.router, prefix="/allergy", tags=["Allergy"])
api_router.include_router(meal_log.router, prefix="/meal_logs", tags=["MealLogs"])
api_router.include_router(supply.router, prefix="/supplies", tags=["Supplies"])
api_router.include_router(pending_box.router, prefix="/pending_box", tags=["PendingBox"])
api_router.include_router(daily_stock.router, prefix="/daily_stocks", tags=["DailyStocks"])
api_router.include_router(order.router, prefix="/orders", tags=["Orders"])
api_router.include_router(stock.router, prefix="/stock", tags=["Stock"])

# レポート・エントリー
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(entry.router, prefix="/entry", tags=["Entry"])

# UI関連
api_router.include_router(ui_allergy.router, prefix="/allergies", tags=["Allergies"])

# 管理画面（Excel注文フローを含む） - タグは各サブルーターで指定
api_router.include_router(admin_router, prefix="/admin")

# DEBUG Statics 
api_router.include_router(ui_test.router, prefix="/statics", tags=["Statics"])
# END DEBUG
