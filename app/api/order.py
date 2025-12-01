# app/api/order.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app import schemas
from app.crud import order as crud_order

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.Order, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 同じperson_idとorder_dayの組み合わせが既に存在する場合はエラー
    existing = crud_order.get_order_by_person_and_day(
        db, order_in.person_id, order_in.order_day
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Order for person_id={order_in.person_id} on {order_in.order_day} already exists"
        )
    return crud_order.create_order(db, order_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ============================================================
# Read (all / filter by date or person)
# ============================================================
@router.get("/", response_model=list[schemas.Order])
def read_orders(
    order_day: Optional[date] = Query(None, description="特定日の注文を取得"),
    person_id: Optional[int] = Query(None, description="特定の人の注文履歴を取得"),
    db: Session = Depends(get_db)
):
    if order_day:
        return crud_order.get_orders_by_day(db, order_day)
    elif person_id:
        return crud_order.get_orders_by_person(db, person_id)
    return crud_order.get_orders(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{order_id}", response_model=schemas.Order)
def update_order(
    order_id: int,
    order_in: schemas.OrderUpdate,
    db: Session = Depends(get_db),
):
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return crud_order.update_order(db, order, order_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return crud_order.delete_order(db, order)
