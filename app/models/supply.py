# app/models/supply.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base


class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, index=True)

    meal_id = Column(Integer, ForeignKey("meals.meal_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    supplied_at = Column(Date, nullable=False)

    ext1 = Column(String(255), nullable=True)
    ext2 = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
