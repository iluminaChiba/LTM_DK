# app/crud/allergy.py
from sqlalchemy.orm import Session
from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_allergy(db: Session, data: schemas.AllergyCreate):
    allergy = models.Allergy(**data.model_dump())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy


# ============================================================
# Read
# ============================================================
def get_allergy(db: Session, meal_id: int):
    return (
        db.query(models.Allergy)
        .filter(models.Allergy.meal_id == meal_id)
        .first()
    )


def get_allergies(db: Session):
    return db.query(models.Allergy).all()


# ============================================================
# Update
# ============================================================
def update_allergy(db: Session, allergy: models.Allergy, data: schemas.AllergyUpdate):
    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(allergy, key, value)

    db.commit()
    db.refresh(allergy)
    return allergy


# ============================================================
# Delete
# ============================================================
def delete_allergy(db: Session, allergy: models.Allergy):
    db.delete(allergy)
    db.commit()
    return allergy
