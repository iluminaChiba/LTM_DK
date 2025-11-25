# app/api/entry.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app import schemas
from app.crud import meal_log as crud_meal_log
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/entry/{token}")
def identify_person(token: str, db: Session = Depends(get_db)):
    person = (
        db.query(models.Person)
        .filter(models.Person.token == token)
        .filter(models.Person.is_deleted == False)
        .first()
    )

    if not person:
        raise HTTPException(status_code=404, detail="Invalid token")

    return {
        "person_id": person.id,
        "name": person.name,
        "fee_category": person.fee_category,
    }




# ============================================================
# Lunch Log Registration（URL認証 → そのままmeal_log登録）
# ============================================================
@router.get("/entry/{token}/lunch")
def register_lunch(token: str, db: Session = Depends(get_db)):
    # 1. token -> person を同定
    person = (
        db.query(models.Person)
        .filter(models.Person.token == token)
        .filter(models.Person.is_deleted == False)
        .first()
    )
    if not person:
        raise HTTPException(status_code=404, detail="Invalid token")

    # 2. 今日の日付
    today = date.today()

    # 3. meal_log を作成（meal_id は暫定で1番とする）
    log_in = schemas.MealLogCreate(
        person_id=person.id,
        meal_id=1,        # ★ 必要に応じて後で動的化
        log_day=today
    )
    created_log = crud_meal_log.create_meal_log(db, log_in)

    # 4. レスポンス
    return {
        "status": "ok",
        "registered": created_log.log_day.isoformat(),
        "person_id": person.id,
        "name": person.name,
        "meal_id": created_log.meal_id,
    }