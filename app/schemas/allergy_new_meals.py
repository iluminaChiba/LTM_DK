# app/schemas/allergy_new_meals.py

from pydantic import BaseModel
from typing import List, Optional

class NewMealItem(BaseModel):
    meal_id: int
    meal_name: str
    furigana: Optional[str] = None
    kcal: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carb: Optional[float] = None
    salt: Optional[float] = None


class NewMealRegisterRequest(BaseModel):
    items: List[NewMealItem]
