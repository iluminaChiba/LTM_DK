# app/schemas/meal.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MealBase(BaseModel):
    name: str
    category: Optional[str] = None
    initial_stock: Optional[int] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    initial_stock: Optional[int] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    is_deleted: Optional[bool] = None


class Meal(MealBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
