# app/api/meal.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app import schemas
from app.crud import meal as crud_meal

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.Meal, status_code=201)
def create_meal(meal_in: schemas.MealCreate, db: Session = Depends(get_db)):
    # meal_idが既に存在する場合はエラー
    existing = crud_meal.get_meal(db, meal_in.meal_id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Meal with meal_id {meal_in.meal_id} already exists"
        )
    return crud_meal.create_meal(db, meal_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{meal_id}", response_model=schemas.Meal)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = crud_meal.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


# ============================================================
# Read (all / search by furigana)
# ============================================================
@router.get("/", response_model=list[schemas.Meal])
def read_meals(
    furigana: Optional[str] = Query(None, description="ふりがなの前方一致検索"),
    db: Session = Depends(get_db)
):
    if furigana:
        return crud_meal.get_meals_by_furigana(db, furigana)
    return crud_meal.get_meals(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{meal_id}", response_model=schemas.Meal)
def update_meal(
    meal_id: int,
    meal_in: schemas.MealUpdate,
    db: Session = Depends(get_db),
):
    meal = crud_meal.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    return crud_meal.update_meal(db, meal, meal_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{meal_id}", response_model=schemas.Meal)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = crud_meal.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    return crud_meal.delete_meal(db, meal)
