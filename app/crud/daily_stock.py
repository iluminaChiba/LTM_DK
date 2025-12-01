# app/crud/daily_stock.py

from datetime import date
from sqlalchemy.orm import Session
from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_daily_stock(db: Session, data: schemas.DailyStockCreate):
    daily_stock = models.DailyStock(**data.model_dump())
    db.add(daily_stock)
    db.commit()
    db.refresh(daily_stock)
    return daily_stock


# ============================================================
# Read
# ============================================================
def get_daily_stock(db: Session, stock_id: int):
    return (
        db.query(models.DailyStock)
        .filter(
            models.DailyStock.id == stock_id,
            models.DailyStock.is_deleted == False
        )
        .first()
    )


def get_daily_stocks(db: Session):
    return (
        db.query(models.DailyStock)
        .filter(models.DailyStock.is_deleted == False)
        .order_by(models.DailyStock.stock_day.desc(), models.DailyStock.meal_id)
        .all()
    )


def get_daily_stocks_by_day(db: Session, stock_day: date):
    """特定日の在庫一覧を取得"""
    return (
        db.query(models.DailyStock)
        .filter(
            models.DailyStock.stock_day == stock_day,
            models.DailyStock.is_deleted == False
        )
        .order_by(models.DailyStock.meal_id)
        .all()
    )


def get_daily_stock_by_meal_and_day(db: Session, meal_id: int, stock_day: date):
    """特定の食事と日付の在庫を取得"""
    return (
        db.query(models.DailyStock)
        .filter(
            models.DailyStock.meal_id == meal_id,
            models.DailyStock.stock_day == stock_day,
            models.DailyStock.is_deleted == False
        )
        .first()
    )


# ============================================================
# Update
# ============================================================
def update_daily_stock(db: Session, daily_stock: models.DailyStock, data: schemas.DailyStockUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(daily_stock, key, value)

    db.commit()
    db.refresh(daily_stock)
    return daily_stock


# ============================================================
# Delete（論理削除）
# ============================================================
def delete_daily_stock(db: Session, daily_stock: models.DailyStock):
    daily_stock.is_deleted = True
    db.commit()
    return daily_stock
