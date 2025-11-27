from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date
from app.database import get_db
from app.models.meal import Meal
from app.models.weekly_menu import WeeklyMenu

router = APIRouter()

class ImportMealItem(BaseModel):
    vendor_item_id: int
    name: str


class ImportWeek(BaseModel):
    start_date: date
    end_date: date


class ImportPayload(BaseModel):
    week: ImportWeek
    meals: List[ImportMealItem]
    weekly_menu_items: List[int]   # vendor_item_id のリスト


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
    # Step 1: meals の upsert
    # ---------------------------------------------------------
    for item in payload.meals:

        # すでに vendor_item_id が存在するかチェック
        existing = (
            db.query(Meal)
              .filter(Meal.vendor_item_id == item.vendor_item_id)
              .first()
        )

        if existing:
            # 商品名が変わっている場合だけ UPDATE
            if existing.name != item.name:
                existing.name = item.name
                db.add(existing)
                updated_meals += 1
        else:
            # 新規 CREATE
            new_meal = Meal(
                name=item.name,
                vendor_item_id=item.vendor_item_id
            )
            db.add(new_meal)
            inserted_meals += 1

    db.commit()

    # ---------------------------------------------------------
    # Step 2: weekly_menus の登録（週単位）
    # ---------------------------------------------------------
    week_start = payload.week.start_date

    # vendor_item_id → meal.id への逆引き
    meal_map = {
        str(m.vendor_item_id): m.id
        for m in db.query(Meal).filter(
            Meal.vendor_item_id.in_([str(v) for v in payload.weekly_menu_items])
        )
    }

    for vendor_id in payload.weekly_menu_items:
        vendor_id_str = str(vendor_id)
        if vendor_id_str not in meal_map:
            raise HTTPException(status_code=400,
                                detail=f"vendor_item_id {vendor_id_str} が meals に見つかりません。")

        wm = WeeklyMenu(
            date=week_start,        # ← 日別処理は不要のため start_date で統一
            meal_id=meal_map[vendor_id_str]
        )
        db.add(wm)
        inserted_weekly += 1

    db.commit()

    # ---------------------------------------------------------
    # 結果を返す
    # ---------------------------------------------------------
    return {
        "status": "success",
        "meals_inserted": inserted_meals,
        "meals_updated": updated_meals,
        "weekly_menus_inserted": inserted_weekly
    }
