# app/models/weekly_menu.py

from sqlalchemy import Column, Integer, Date, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class WeeklyMenu(Base):
    __tablename__ = "weekly_menus"

    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(Date, nullable=False)

    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    meal = relationship("Meal")

    ext1 = Column(String(255), nullable=True)
    ext2 = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
