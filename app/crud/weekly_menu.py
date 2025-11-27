from sqlalchemy.orm import Session
from app.models.weekly_menu import WeeklyMenu
from datetime import date


def get_today_menus(db: Session, today: date):
    return (
        db.query(WeeklyMenu)
        .filter(WeeklyMenu.start_date <= today, WeeklyMenu.end_date >= today)
        .all()
    )

def get_week_menus(db: Session, start: date, end: date):
    return (
        db.query(WeeklyMenu)
        .filter(WeeklyMenu.start_date == start, WeeklyMenu.end_date == end)
        .all()
    )
