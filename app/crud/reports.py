from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_today_logs(db: Session, target_date):
    """
    当日の meal_logs を person / meal と JOIN した一覧を返す
    """
    return (
        db.query(
            models.MealLog.id.label("log_id"),
            models.Person.id.label("person_id"),
            models.Person.name.label("person_name"),
            models.Meal.id.label("meal_id"),
            models.Meal.name.label("meal_name"),
            models.MealLog.log_day.label("log_day"),
        )
        .join(models.Person, models.Person.id == models.MealLog.person_id)
        .join(models.Meal, models.Meal.id == models.MealLog.meal_id)
        .filter(
            models.MealLog.log_day == target_date,
            models.MealLog.is_deleted == False,
        )
        .order_by(models.Person.name.asc())
        .all()
    )
