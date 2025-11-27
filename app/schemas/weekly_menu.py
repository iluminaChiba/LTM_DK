# app/schemas/weekly_menu.py

from pydantic import BaseModel
from datetime import date
from app.schemas.meal import MealResponse

class WeeklyMenuCreate(BaseModel):
    week_start: date
    meal_id: int
    ext1: str | None = None
    ext2: str | None = None


class WeeklyMenuUpdate(BaseModel):
    week_start: date | None = None
    meal_id: int | None = None
    ext1: str | None = None
    ext2: str | None = None


class WeeklyMenuResponse(BaseModel):
    id: int
    week_start: date
    meal: MealResponse | None
    ext1: str | None = None
    ext2: str | None = None

    class Config:
        from_attributes = True

