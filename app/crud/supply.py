# app/crud/supply.py

from sqlalchemy.orm import Session
from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_supply(db: Session, data: schemas.SupplyCreate):
    supply = models.Supply(**data.model_dump())
    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply


# ============================================================
# Read
# ============================================================
def get_supply(db: Session, supply_id: int):
    return (
        db.query(models.Supply)
        .filter(
            models.Supply.id == supply_id,
            models.Supply.is_deleted == False
        )
        .first()
    )


def get_supplies(db: Session):
    return (
        db.query(models.Supply)
        .filter(models.Supply.is_deleted == False)
        .all()
    )


# ============================================================
# Update
# ============================================================
def update_supply(db: Session, supply: models.Supply, data: schemas.SupplyUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(supply, key, value)

    db.commit()
    db.refresh(supply)
    return supply


# ============================================================
# Delete（論理削除）
# ============================================================
def delete_supply(db: Session, supply: models.Supply):
    supply.is_deleted = True
    db.commit()
    return supply
