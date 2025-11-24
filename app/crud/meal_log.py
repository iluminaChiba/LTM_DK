# app/crud/meal_log.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_meal_log(db: Session, data: schemas.MealLogCreate):
    # すでに同じ person_id + log_day が存在するか確認
    exists = (
        db.query(models.MealLog)
        .filter(
            models.MealLog.person_id == data.person_id,
            models.MealLog.log_day == data.log_day,
            models.MealLog.is_deleted == False,
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This person already has a meal log for the specified date.",
        )

    meal_log = models.MealLog(**data.model_dump())

    db.add(meal_log)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate meal log entry detected.",
        )

    db.refresh(meal_log)
    return meal_log


# ============================================================
# Read
# ============================================================
def get_meal_log(db: Session, log_id: int):
    return (
        db.query(models.MealLog)
        .filter(
            models.MealLog.id == log_id,
            models.MealLog.is_deleted == False
        )
        .first()
    )


def get_meal_logs(db: Session):
    return (
        db.query(models.MealLog)
        .filter(models.MealLog.is_deleted == False)
        .all()
    )


# ============================================================
# Update（通常は ext1/ext2 のみ変更、ビジネス制約なし）
# ============================================================
def update_meal_log(db: Session, meal_log: models.MealLog, data: schemas.MealLogUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meal_log, key, value)

    db.commit()
    db.refresh(meal_log)
    return meal_log


# ============================================================
# Logical Delete
# ============================================================
def delete_meal_log(db: Session, meal_log: models.MealLog):
    meal_log.is_deleted = True
    db.commit()
    return meal_log
