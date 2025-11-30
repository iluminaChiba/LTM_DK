# app/models/pending_box.py
from sqlalchemy import Column, BigInteger, String, Integer, Date, Enum, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class StatusEnum(str, enum.Enum):
    pending = "pending"
    applied = "applied"


class PendingBox(Base):
    __tablename__ = "pending_box"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    meal_id = Column(String(10), nullable=False, index=True)
    meal_name = Column(String(255), nullable=True)
    qty = Column(Integer, nullable=False)
    arrival_date = Column(Date, nullable=False)
    applicable_date = Column(Date, nullable=False)
    source_filename = Column(String(255), nullable=True)
    excel_row = Column(Integer, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, server_default="pending")
    
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PendingBox(id={self.id}, meal_id={self.meal_id}, meal_name={self.meal_name}, status={self.status})>"
