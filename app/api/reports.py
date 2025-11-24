import io
import csv
from fastapi import APIRouter, Depends, Response
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


@router.get("/today_csv", summary="Download Today's Meal Logs as CSV")
def get_today_csv(db: Session = Depends(get_db)):
    today = date.today()
    results = crud_reports.get_today_logs(db, today)

    # Row オブジェクト → dict へ変換
    data = [
        {
            "log_id": r.log_id,
            "person_id": r.person_id,
            "person_name": r.person_name,
            "meal_id": r.meal_id,
            "meal_name": r.meal_name,
            "log_day": str(r.log_day),
        }
        for r in results
    ]

    # データが無い場合は空の CSV
    if not data:
        return Response(
            content="log_id,person_id,person_name,meal_id,meal_name,log_day\n",
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=today_meal_logs.csv"}
        )

    # CSV の列名は dict のキーで OK
    fieldnames = list(data[0].keys())

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

    csv_data = output.getvalue()
    output.close()
    csv_data = "\ufeff" + csv_data  # BOM付与（Excel対策）
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=today_meal_logs.csv"}
    )
