# app/schemas/meal_log.py
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class MealLogBase(BaseModel):
    person_id: int
    meal_id: int
    log_day: date
    ext1: Optional[str] = None
    ext2: Optional[str] = None


class MealLogCreate(MealLogBase):
    pass


class MealLogUpdate(BaseModel):
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    is_deleted: Optional[bool] = None


class MealLog(MealLogBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

        
class MealResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    
    class Config:
        from_attributes = True