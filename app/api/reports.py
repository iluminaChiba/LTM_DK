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
