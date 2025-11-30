# app/schemas/pending_box.py
from datetime import datetime, date
from typing import Optional, Literal
from pydantic import BaseModel


# ============================================================
# Base
# ============================================================
class PendingBoxBase(BaseModel):
    meal_id: str
    meal_name: Optional[str] = None
    qty: int
    arrival_date: date
    applicable_date: date
    source_filename: Optional[str] = None
    excel_row: int
    status: Literal['pending', 'applied'] = 'pending'


# ============================================================
# Create（API入力用）
# ============================================================
class PendingBoxCreate(PendingBoxBase):
    pass


# ============================================================
# Update（PATCH 用）
# ============================================================
class PendingBoxUpdate(BaseModel):
    meal_id: Optional[str] = None
    meal_name: Optional[str] = None
    qty: Optional[int] = None
    arrival_date: Optional[date] = None
    applicable_date: Optional[date] = None
    source_filename: Optional[str] = None
    excel_row: Optional[int] = None
    status: Optional[Literal['pending', 'applied']] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class PendingBox(PendingBoxBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
