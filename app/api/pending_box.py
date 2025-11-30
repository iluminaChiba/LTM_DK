# app/api/pending_box.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app import schemas
from app.crud import pending_box as crud_pending_box

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.PendingBox)
def create_pending_box(
    pending_box_in: schemas.PendingBoxCreate,
    db: Session = Depends(get_db)
):
    return crud_pending_box.create_pending_box(db, pending_box_in)


@router.post("/bulk", response_model=list[schemas.PendingBox])
def create_pending_boxes_bulk(
    pending_boxes_in: list[schemas.PendingBoxCreate],
    db: Session = Depends(get_db)
):
    """複数レコードを一括登録"""
    return crud_pending_box.create_pending_boxes_bulk(db, pending_boxes_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{pending_box_id}", response_model=schemas.PendingBox)
def read_pending_box(pending_box_id: int, db: Session = Depends(get_db)):
    pending_box = crud_pending_box.get_pending_box(db, pending_box_id)
    if not pending_box:
        raise HTTPException(status_code=404, detail="Pending box not found")
    return pending_box


# ============================================================
# Read (all)
# ============================================================
@router.get("/", response_model=list[schemas.PendingBox])
def read_pending_boxes(
    status: Optional[str] = None,
    applicable_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if applicable_date is not None:
        # 日付とステータスを両方考慮した取得
        return crud_pending_box.get_pending_boxes_by_date(db, applicable_date, status)

    # 日付指定なし → 全件or statusで取得
    return crud_pending_box.get_pending_boxes(db, status)


# ============================================================
# Update
# ============================================================
@router.patch("/{pending_box_id}", response_model=schemas.PendingBox)
def update_pending_box(
    pending_box_id: int,
    pending_box_in: schemas.PendingBoxUpdate,
    db: Session = Depends(get_db),
):
    pending_box = crud_pending_box.get_pending_box(db, pending_box_id)
    if not pending_box:
        raise HTTPException(status_code=404, detail="Pending box not found")

    return crud_pending_box.update_pending_box(db, pending_box_id, pending_box_in)



@router.post("/mark-applied")
def mark_as_applied(
    pending_box_ids: list[int],
    db: Session = Depends(get_db)
):
    """複数レコードをappliedにする"""
    crud_pending_box.mark_as_applied(db, pending_box_ids)
    return {"status": "ok", "count": len(pending_box_ids)}


# ============================================================
# Delete
# ============================================================
@router.delete("/{pending_box_id}", response_model=schemas.PendingBox)
def delete_pending_box(pending_box_id: int, db: Session = Depends(get_db)):
    pending_box = crud_pending_box.get_pending_box(db, pending_box_id)
    if not pending_box:
        raise HTTPException(status_code=404, detail="Pending box not found")

    return crud_pending_box.delete_pending_box(db, pending_box_id)
