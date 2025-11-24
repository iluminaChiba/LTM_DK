# app/schemas/supply.py
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class SupplyBase(BaseModel):
    meal_id: int
    quantity: int
    supplied_at: date
    ext1: Optional[str] = None
    ext2: Optional[str] = None


class SupplyCreate(SupplyBase):
    pass


class SupplyUpdate(BaseModel):
    meal_id: Optional[int] = None
    quantity: Optional[int] = None
    supplied_at: Optional[date] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    is_deleted: Optional[bool] = None


class Supply(SupplyBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
