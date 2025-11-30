# api/order_register.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class OrderItem(BaseModel):
    meal_id: str
    qty: int | None

class OrderConfirm(BaseModel):
    filename: str
    orders: list[OrderItem]

@router.post("/confirm")
def order_confirm(payload: OrderConfirm):
    # pending_import テーブルに保存する想定（疑似コード）
    data = {
        "filename": payload.filename,
        "orders_json": [item.model_dump() for item in payload.orders],
        "created_at": datetime.now(),
        "processed": False,
    }

    # insert_pending_import(data)  ← 実装予定のCRUD関数
    print("DEBUG pending_import:", data)

    return {"status": "ok"}
