# app/models/meal.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL
from sqlalchemy.sql import func
from app.core.database import Base


class Meal(Base):
    __tablename__ = "meals"

    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String(255), nullable=False)
    furigana = Column(String(255), nullable=False, index=True)
    
    # 栄養成分
    kcal = Column(DECIMAL(6, 1), nullable=True)
    protein = Column(DECIMAL(6, 1), nullable=True)
    fat = Column(DECIMAL(6, 1), nullable=True)
    carb = Column(DECIMAL(6, 1), nullable=True)
    salt = Column(DECIMAL(6, 2), nullable=True)
    
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
