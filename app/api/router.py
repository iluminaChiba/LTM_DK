# app/api/router.py

from fastapi import APIRouter
from app.api import person, meal, meal_log, supply, reports

api_router = APIRouter()

api_router.include_router(person.router, prefix="/persons", tags=["Persons"])
api_router.include_router(meal.router, prefix="/meals", tags=["Meals"])
api_router.include_router(meal_log.router, prefix="/meal_logs", tags=["MealLogs"])
api_router.include_router(supply.router, prefix="/supplies", tags=["Supplies"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
