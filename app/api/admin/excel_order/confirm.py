# app/api/admin/excel_order/confirm.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from app.core.database import get_db
from app.crud import pending_box as crud_pending_box
from app.schemas.pending_box import PendingBoxCreate

router = APIRouter()


class OrderItem(BaseModel):
    meal_id: str
    meal_name: Optional[str]
    qty: int
    arrival_date: date
    applicable_date: date
    source_filename: str
    excel_row: int
    status: str


@router.post("/confirm")
def confirm_order(
    orders: List[OrderItem],
    db: Session = Depends(get_db)
):
    """
    注文確定：pending_boxテーブルに一括保存
    """
    try:
        # pending_box用のデータを作成
        pending_items = []
        for item in orders:
            if item.qty > 0:
                pending_items.append(
                    PendingBoxCreate(
                        arrival_date=item.arrival_date,
                        applicable_date=item.applicable_date,
                        meal_id=item.meal_id,
                        qty=item.qty,
                        source_filename=item.source_filename
                    )
                )

        # 一括挿入
        if pending_items:
            crud_pending_box.create_pending_boxes_bulk(db, pending_items)

        return {
            "status": "success",
            "inserted_count": len(pending_items),
            "message": f"{len(pending_items)}件をpending_boxに保存しました"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB保存エラー: {str(e)}")
