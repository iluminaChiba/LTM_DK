# app/api/allergy.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import schemas
from app.crud import allergy as crud_allergy

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.Allergy)
def create_allergy(allergy_in: schemas.AllergyCreate, db: Session = Depends(get_db)):
    # 既に存在するか確認
    existing = crud_allergy.get_allergy(db, allergy_in.meal_id)
    if existing:
        raise HTTPException(status_code=400, detail="Allergy info for this meal already exists")
    
    return crud_allergy.create_allergy(db, allergy_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{meal_id}", response_model=schemas.Allergy)
def read_allergy(meal_id: int, db: Session = Depends(get_db)):
    allergy = crud_allergy.get_allergy(db, meal_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy info not found")
    return allergy


# ============================================================
# Read (all)
# ============================================================
@router.get("/", response_model=list[schemas.Allergy])
def read_allergies(db: Session = Depends(get_db)):
    return crud_allergy.get_allergies(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{meal_id}", response_model=schemas.Allergy)
def update_allergy(
    meal_id: int,
    allergy_in: schemas.AllergyUpdate,
    db: Session = Depends(get_db),
):
    allergy = crud_allergy.get_allergy(db, meal_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy info not found")

    return crud_allergy.update_allergy(db, allergy, allergy_in)


# ============================================================
# Delete
# ============================================================
@router.delete("/{meal_id}", response_model=schemas.Allergy)
def delete_allergy(meal_id: int, db: Session = Depends(get_db)):
    allergy = crud_allergy.get_allergy(db, meal_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy info not found")

    return crud_allergy.delete_allergy(db, allergy)
