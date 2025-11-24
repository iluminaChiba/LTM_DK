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


def get_today_meal_counts(db: Session, target_date):
    """
    メニューごとの当日件数を返す
    """
    return (
        db.query(
            models.Meal.id.label("meal_id"),
            models.Meal.name.label("meal_name"),
            func.count(models.MealLog.id).label("count"),
        )
        .join(models.MealLog, models.Meal.id == models.MealLog.meal_id)
        .filter(
            models.MealLog.log_day == target_date,
            models.MealLog.is_deleted == False,
        )
        .group_by(models.Meal.id, models.Meal.name)
        .order_by(models.Meal.id.asc())
        .all()
    )


def get_today_unanswered(db: Session, target_date):
    """
    今日の meal_log を提出していない persons 一覧
    """
    subq = (
        db.query(models.MealLog.person_id)
        .filter(
            models.MealLog.log_day == target_date,
            models.MealLog.is_deleted == False,
        )
        .subquery()
    )

    return (
        db.query(
            models.Person.id.label("person_id"),
            models.Person.name.label("person_name"),
        )
        .filter(
            models.Person.is_deleted == False,
            ~models.Person.id.in_(subq),
        )
        .order_by(models.Person.name.asc())
        .all()
    )
