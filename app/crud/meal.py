# app/crud/meal.py
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any # 汎用的に Any を使うこともできます

# ============================================================
# Create
# ============================================================
def create_meal(db: Session, data: schemas.MealCreate):
    meal = models.Meal(**data.model_dump())
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


def create_meal_if_not_exists(db: Session, data: dict): #型ヒントを dict にしておく
    # existing_meal をチェックするために、辞書としてアクセス
    existing_meal = get_meal(db, data["meal_id"])
    
    if existing_meal:
        return False
    # create_meal に渡す直前に Pydantic モデルに変換する
    return create_meal(db, schemas.MealCreate(**data))

# ============================================================
# Read
# ============================================================
def get_meal(db: Session, meal_id: int):
    return (
        db.query(models.Meal)
        .filter(
            models.Meal.meal_id == meal_id,
            models.Meal.is_deleted == False
        )
        .first()
    )


def get_meals(db: Session):
    return (
        db.query(models.Meal)
        .filter(models.Meal.is_deleted == False)
        .order_by(models.Meal.furigana)  # ふりがな順でソート
        .all()
    )


def get_meals_by_furigana(db: Session, furigana_prefix: str):
    """ふりがなの前方一致検索"""
    return (
        db.query(models.Meal)
        .filter(
            models.Meal.furigana.like(f"{furigana_prefix}%"),
            models.Meal.is_deleted == False
        )
        .order_by(models.Meal.furigana)
        .all()
    )


# ============================================================
# Update
# ============================================================
def update_meal(db: Session, meal: models.Meal, data: schemas.MealUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meal, key, value)

    db.commit()
    db.refresh(meal)
    return meal


# ============================================================
# Delete（論理削除）
# ============================================================
def delete_meal(db: Session, meal: models.Meal):
    meal.is_deleted = True
    db.commit()
    return meal
