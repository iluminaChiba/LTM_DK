# app/schemas/daily_stock.py
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


# ============================================================
# Base
# ============================================================
class DailyStockBase(BaseModel):
    meal_id: int
    stock_day: date
    stock: int
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Create（API入力用）
# ============================================================
class DailyStockCreate(DailyStockBase):
    pass


# ============================================================
# Update（PATCH 用）
# ============================================================
class DailyStockUpdate(BaseModel):
    stock: Optional[int] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class DailyStock(DailyStockBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
