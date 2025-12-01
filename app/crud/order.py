# app/crud/order.py

from datetime import date
from sqlalchemy.orm import Session
from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_order(db: Session, data: schemas.OrderCreate):
    order = models.Order(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# ============================================================
# Read
# ============================================================
def get_order(db: Session, order_id: int):
    return (
        db.query(models.Order)
        .filter(
            models.Order.id == order_id,
            models.Order.is_deleted == False
        )
        .first()
    )


def get_orders(db: Session):
    return (
        db.query(models.Order)
        .filter(models.Order.is_deleted == False)
        .order_by(models.Order.order_day.desc(), models.Order.person_id)
        .all()
    )


def get_orders_by_day(db: Session, order_day: date):
    """特定日の注文一覧を取得"""
    return (
        db.query(models.Order)
        .filter(
            models.Order.order_day == order_day,
            models.Order.is_deleted == False
        )
        .order_by(models.Order.person_id)
        .all()
    )


def get_orders_by_person(db: Session, person_id: int):
    """特定の人の注文履歴を取得"""
    return (
        db.query(models.Order)
        .filter(
            models.Order.person_id == person_id,
            models.Order.is_deleted == False
        )
        .order_by(models.Order.order_day.desc())
        .all()
    )


def get_order_by_person_and_day(db: Session, person_id: int, order_day: date):
    """特定の人の特定日の注文を取得"""
    return (
        db.query(models.Order)
        .filter(
            models.Order.person_id == person_id,
            models.Order.order_day == order_day,
            models.Order.is_deleted == False
        )
        .first()
    )


# ============================================================
# Update
# ============================================================
def update_order(db: Session, order: models.Order, data: schemas.OrderUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


# ============================================================
# Delete（論理削除）
# ============================================================
def delete_order(db: Session, order: models.Order):
    order.is_deleted = True
    db.commit()
    return order
