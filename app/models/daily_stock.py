# app/models/daily_stock.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class DailyStock(Base):
    __tablename__ = "daily_stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meal_id = Column(Integer, ForeignKey("meals.meal_id"), nullable=False)
    stock_day = Column(Date, nullable=False)
    stock = Column(Integer, nullable=False)
    
    # 拡張フィールド
    ext1 = Column(String(255), nullable=True)
    ext2 = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<DailyStock(id={self.id}, meal_id={self.meal_id}, stock_day={self.stock_day}, stock={self.stock})>"
