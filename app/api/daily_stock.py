# app/api/daily_stock.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app import schemas
from app.crud import daily_stock as crud_daily_stock

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.DailyStock, status_code=201)
def create_daily_stock(stock_in: schemas.DailyStockCreate, db: Session = Depends(get_db)):
    # 同じmeal_idとstock_dayの組み合わせが既に存在する場合はエラー
    existing = crud_daily_stock.get_daily_stock_by_meal_and_day(
        db, stock_in.meal_id, stock_in.stock_day
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Daily stock for meal_id={stock_in.meal_id} on {stock_in.stock_day} already exists"
        )
    return crud_daily_stock.create_daily_stock(db, stock_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{stock_id}", response_model=schemas.DailyStock)
def read_daily_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = crud_daily_stock.get_daily_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Daily stock not found")
    return stock


# ============================================================
# Read (all / filter by date)
# ============================================================
@router.get("/", response_model=list[schemas.DailyStock])
def read_daily_stocks(
    stock_day: Optional[date] = Query(None, description="特定日の在庫を取得"),
    db: Session = Depends(get_db)
):
    if stock_day:
        return crud_daily_stock.get_daily_stocks_by_day(db, stock_day)
    return crud_daily_stock.get_daily_stocks(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{stock_id}", response_model=schemas.DailyStock)
def update_daily_stock(
    stock_id: int,
    stock_in: schemas.DailyStockUpdate,
    db: Session = Depends(get_db),
):
    stock = crud_daily_stock.get_daily_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Daily stock not found")

    return crud_daily_stock.update_daily_stock(db, stock, stock_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{stock_id}", response_model=schemas.DailyStock)
def delete_daily_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = crud_daily_stock.get_daily_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Daily stock not found")

    return crud_daily_stock.delete_daily_stock(db, stock)
