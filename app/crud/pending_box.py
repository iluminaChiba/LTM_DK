# app/crud/pending_box.py
from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date


# ============================================================
# Create
# ============================================================
def create_pending_box(db: Session, data: schemas.PendingBoxCreate):
    pending_box = models.PendingBox(**data.model_dump())
    db.add(pending_box)
    db.commit()
    db.refresh(pending_box)
    return pending_box


def create_pending_boxes_bulk(db: Session, data_list: list[schemas.PendingBoxCreate]):
    """複数レコードを一括登録"""
    pending_boxes = [models.PendingBox(**data.model_dump()) for data in data_list]
    db.add_all(pending_boxes)
    db.commit()
    return pending_boxes


# ============================================================
# Read
# ============================================================
def get_pending_box(db: Session, pending_box_id: int):
    return (
        db.query(models.PendingBox)
        .filter(models.PendingBox.id == pending_box_id)
        .first()
    )


def get_pending_boxes(db: Session, status: str = None):
    """全件取得（statusでフィルタ可能）"""
    query = db.query(models.PendingBox)
    if status:
        query = query.filter(models.PendingBox.status == status)
    return query.order_by(models.PendingBox.created_at.desc()).all()


def get_pending_boxes_by_date(db: Session, applicable_date: date, status: str = None):
    """適用日で検索"""
    query = db.query(models.PendingBox).filter(
        models.PendingBox.applicable_date == applicable_date
    )
    if status:
        query = query.filter(models.PendingBox.status == status)
    return query.all()


# ============================================================
# Update
# ============================================================
def update_pending_box(db: Session, pending_box: models.PendingBox, data: schemas.PendingBoxUpdate):
    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(pending_box, key, value)

    db.commit()
    db.refresh(pending_box)
    return pending_box


def mark_as_applied(db: Session, pending_box_ids: list[int]):
    """複数レコードをappliedにする"""
    db.query(models.PendingBox).filter(
        models.PendingBox.id.in_(pending_box_ids)
    ).update({"status": "applied"}, synchronize_session=False)
    db.commit()


# ============================================================
# Delete
# ============================================================
def delete_pending_box(db: Session, pending_box: models.PendingBox):
    db.delete(pending_box)
    db.commit()
    return pending_box
