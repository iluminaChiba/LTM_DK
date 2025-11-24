from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.crud import reports as crud_reports

router = APIRouter()


@router.get("/today", summary="Get Today's Meal Logs (JOIN)")
def get_today_logs(db: Session = Depends(get_db)):
    today = date.today()
    results = crud_reports.get_today_logs(db, today)

    # FastAPI は辞書リストをそのまま返してもOK
    return [
        {
            "log_id": r.log_id,
            "person_id": r.person_id,
            "person_name": r.person_name,
            "meal_id": r.meal_id,
            "meal_name": r.meal_name,
            "log_day": r.log_day,
        }
        for r in results
    ]



@router.get("/today_counts", summary="Get Meal Counts for Today")
def get_today_counts(db: Session = Depends(get_db)):
    today = date.today()
    results = crud_reports.get_today_meal_counts(db, today)

    return [
        {
            "meal_id": r.meal_id,
            "meal_name": r.meal_name,
            "count": r.count,
        }
        for r in results
    ]


@router.get("/today_unanswered", summary="Get Persons Without Today's MealLog")
def get_today_unanswered(db: Session = Depends(get_db)):
    today = date.today()
    results = crud_reports.get_today_unanswered(db, today)

    return [
        {
            "person_id": r.person_id,
            "person_name": r.person_name,
        }
        for r in results
    ]
