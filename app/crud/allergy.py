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


def create_allergy_from_row(db: Session, row: dict):

    allergy_data = schemas.AllergyCreate(
        meal_id=row["meal_id"],

        # --- 特定原材料（表示義務）7品目 ---
        egg=row.get("egg", False),
        milk=row.get("milk", False),
        wheat=row.get("wheat", False),
        soba=row.get("soba", False),
        peanut=row.get("peanut", False),
        shrimp=row.get("shrimp", False),
        crab=row.get("crab", False),

        # --- 特定原材料に準ずるもの 22品目 ---
        walnut=row.get("walnut", False),
        abalone=row.get("abalone", False),
        squid=row.get("squid", False),
        salmon_roe=row.get("salmon_roe", False),
        salmon=row.get("salmon", False),
        mackerel=row.get("mackerel", False),
        seafood=row.get("seafood", False),  # ← fish ではなく seafood が正しい
        beef=row.get("beef", False),
        chicken=row.get("chicken", False),
        pork=row.get("pork", False),
        orange=row.get("orange", False),
        kiwi=row.get("kiwi", False),
        apple=row.get("apple", False),
        peach=row.get("peach", False),
        banana=row.get("banana", False),
        soy=row.get("soy", False),  # soybean ではない。モデル名に合わせる
        cashew=row.get("cashew", False),
        almond=row.get("almond", False),
        macadamia=row.get("macadamia", False),
        yam=row.get("yam", False),
        sesame=row.get("sesame", False),
        gelatin=row.get("gelatin", False),
    )

    return create_allergy(db, allergy_data)


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
