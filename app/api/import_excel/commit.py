from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date
from app.core.database import get_db
from app.models.meal import Meal
from app.models.weekly_menu import WeeklyMenu

router = APIRouter()

class ImportMealItem(BaseModel):
    meal_id: int
    name: str


class ImportWeek(BaseModel):
    week_start: date


class ImportPayload(BaseModel):
    week: ImportWeek
    meals: List[ImportMealItem]
    weekly_menu_items: List[int]   # meal_id のリスト


@router.post("/commit")
def commit_import(payload: ImportPayload,
                  db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    preview API の結果を受け取り、
    meals への upsert と、
    weekly_menus への「週単位」登録を行う。
    """
    print("=== COMMIT PAYLOAD ===", payload)

    inserted_meals = 0
    updated_meals = 0
    inserted_weekly = 0

    # ---------------------------------------------------------
    # Step 1: meals の upsert ここは書き直し
    # ---------------------------------------------------------
  
    

    # ---------------------------------------------------------
    # 結果を返す
    # ---------------------------------------------------------
    return {
        "status": "success",
        "meals_inserted": inserted_meals,
        "meals_updated": updated_meals,
        "weekly_menus_inserted": inserted_weekly
    }
