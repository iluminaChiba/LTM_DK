# app/models/meal.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    category = Column(String(100), nullable=True)
    initial_stock = Column(Integer, nullable=True)

    ext1 = Column(String(255), nullable=True)
    ext2 = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
