# app/schemas/meal.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


# ============================================================
# Base
# ============================================================
class MealBase(BaseModel):
    meal_name: str
    furigana: str
    side1: Optional[str] = None
    side2: Optional[str] = None
    side3: Optional[str] = None
    kcal: Optional[Decimal] = None
    protein: Optional[Decimal] = None
    fat: Optional[Decimal] = None
    carb: Optional[Decimal] = None
    salt: Optional[Decimal] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Create（API入力用）
# ============================================================
class MealCreate(MealBase):
    meal_id: int


# ============================================================
# Update（PATCH 用）
# ============================================================
class MealUpdate(BaseModel):
    meal_name: Optional[str] = None
    furigana: Optional[str] = None
    side1: Optional[str] = None
    side2: Optional[str] = None
    side3: Optional[str] = None
    kcal: Optional[Decimal] = None
    protein: Optional[Decimal] = None
    fat: Optional[Decimal] = None
    carb: Optional[Decimal] = None
    salt: Optional[Decimal] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class Meal(BaseModel):
    meal_id: int
    meal_name: str
    furigana: str
    side1: Optional[str] = None
    side2: Optional[str] = None
    side3: Optional[str] = None
    kcal: Optional[Decimal] = None
    protein: Optional[Decimal] = None
    fat: Optional[Decimal] = None
    carb: Optional[Decimal] = None
    salt: Optional[Decimal] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# UI用レスポンス（簡易表示用）
# ============================================================
class MealResponse(BaseModel):
    meal_id: int
    meal_name: str
    furigana: str
    kcal: Optional[Decimal] = None
    
    class Config:
        from_attributes = True        
