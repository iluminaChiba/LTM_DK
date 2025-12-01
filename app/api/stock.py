# app/api/stock.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app import models

router = APIRouter()


# ============================================================
# Response Schema
# ============================================================
class StockRemaining(BaseModel):
    meal_id: int
    meal_name: str
    stock: int
    ordered_count: int
    remaining: int

    class Config:
        from_attributes = True


# ============================================================
# GET /stock/remaining
# ============================================================
@router.get("/remaining", response_model=List[StockRemaining])
def get_remaining_stock(
    date: date = Query(..., description="在庫確認日 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    指定日の各メニューの在庫・注文数・残数を取得
    
    - stock: daily_stockテーブルの在庫数
    - ordered_count: ordersテーブルの注文数
    - remaining: stock - ordered_count
    """
    
    # 1. 指定日の在庫データを取得
    stocks = (
        db.query(
            models.DailyStock.meal_id,
            models.Meal.meal_name,
            models.DailyStock.stock
        )
        .join(models.Meal, models.DailyStock.meal_id == models.Meal.meal_id)
        .filter(
            models.DailyStock.stock_day == date,
            models.DailyStock.is_deleted == False,
            models.Meal.is_deleted == False
        )
        .all()
    )
    
    # 2. 指定日の注文数を集計
    order_counts = (
        db.query(
            models.Order.meal_id,
            func.count(models.Order.id).label("ordered_count")
        )
        .filter(
            models.Order.order_day == date,
            models.Order.is_deleted == False
        )
        .group_by(models.Order.meal_id)
        .all()
    )
    
    # 注文数を辞書化
    order_dict = {order.meal_id: order.ordered_count for order in order_counts}
    
    # 3. 結果を組み立て
    results = []
    for stock in stocks:
        ordered = order_dict.get(stock.meal_id, 0)
        results.append(
            StockRemaining(
                meal_id=stock.meal_id,
                meal_name=stock.meal_name,
                stock=stock.stock,
                ordered_count=ordered,
                remaining=stock.stock - ordered
            )
        )
    
    # meal_idでソート
    results.sort(key=lambda x: x.meal_id)
    
    return results
