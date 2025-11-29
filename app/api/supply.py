# app/api/supply.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import schemas
from app.crud import supply as crud_supply

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.Supply)
def create_supply(
    supply_in: schemas.SupplyCreate,
    db: Session = Depends(get_db),
):
    return crud_supply.create_supply(db, supply_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{supply_id}", response_model=schemas.Supply)
def read_supply(
    supply_id: int,
    db: Session = Depends(get_db),
):
    supply = crud_supply.get_supply(db, supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply


# ============================================================
# Read (all)
# ============================================================
@router.get("/", response_model=list[schemas.Supply])
def read_supplies(
    db: Session = Depends(get_db),
):
    return crud_supply.get_supplies(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{supply_id}", response_model=schemas.Supply)
def update_supply(
    supply_id: int,
    supply_in: schemas.SupplyUpdate,
    db: Session = Depends(get_db),
):
    supply = crud_supply.get_supply(db, supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    return crud_supply.update_supply(db, supply, supply_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{supply_id}", response_model=schemas.Supply)
def delete_supply(
    supply_id: int,
    db: Session = Depends(get_db),
):
    supply = crud_supply.get_supply(db, supply_id)
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    return crud_supply.delete_supply(db, supply)
