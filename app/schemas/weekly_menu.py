# app/schemas/weekly_menu.py

from pydantic import BaseModel
from datetime import date
from app.schemas.meal import MealResponse

class WeeklyMenuCreate(BaseModel):
    start_date: date
    end_date: date
    meal_id: int
    ext1: str | None = None
    ext2: str | None = None


class WeeklyMenuUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    meal_id: int | None = None
    ext1: str | None = None
    ext2: str | None = None


class WeeklyMenuResponse(BaseModel):
    id: int
    start_date: date
    end_date: date
    meal: MealResponse | None
    ext1: str | None = None
    ext2: str | None = None

    class Config:
        from_attributes = True

