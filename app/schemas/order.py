# app/schemas/order.py
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


# ============================================================
# Base
# ============================================================
class OrderBase(BaseModel):
    person_id: int
    meal_id: int
    order_day: date
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Create（API入力用）
# ============================================================
class OrderCreate(OrderBase):
    pass


# ============================================================
# Update（PATCH 用）
# ============================================================
class OrderUpdate(BaseModel):
    meal_id: Optional[int] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class Order(OrderBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
