# app/models/meal_side_dish.py

from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class MealSideDish(Base):
    __tablename__ = "meal_side_dish"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meal_id = Column(Integer, ForeignKey("meals.meal_id"), nullable=False)
    side_dish_id = Column(Integer, ForeignKey("side_dishes.side_dish_id"), nullable=False)
    position = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<MealSideDish(meal_id={self.meal_id}, side_dish_id={self.side_dish_id}, position={self.position})>"
