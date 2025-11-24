# app/api/meal_log.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.crud import meal_log as crud_meal_log

router = APIRouter()


# ============================================================
# Create（1日1食制約込み）
# ============================================================
@router.post("/", response_model=schemas.MealLog)
def create_meal_log(
    log_in: schemas.MealLogCreate,
    db: Session = Depends(get_db),
):
    return crud_meal_log.create_meal_log(db, log_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{log_id}", response_model=schemas.MealLog)
def read_meal_log(log_id: int, db: Session = Depends(get_db)):
    log = crud_meal_log.get_meal_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="MealLog not found")
    return log


# ============================================================
# Read (all)
# ============================================================
@router.get("/", response_model=list[schemas.MealLog])
def read_meal_logs(db: Session = Depends(get_db)):
    return crud_meal_log.get_meal_logs(db)


# ============================================================
# Update（ext1/ext2程度を扱う軽更新）
# ============================================================
@router.patch("/{log_id}", response_model=schemas.MealLog)
def update_meal_log(
    log_id: int,
    log_in: schemas.MealLogUpdate,
    db: Session = Depends(get_db),
):
    log = crud_meal_log.get_meal_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="MealLog not found")

    return crud_meal_log.update_meal_log(db, log, log_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{log_id}", response_model=schemas.MealLog)
def delete_meal_log(log_id: int, db: Session = Depends(get_db)):
    log = crud_meal_log.get_meal_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="MealLog not found")

    return crud_meal_log.delete_meal_log(db, log)
