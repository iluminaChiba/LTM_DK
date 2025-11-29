# app/crud/person.py
import secrets
from sqlalchemy.orm import Session
from app import models, schemas


# ============================================================
# Create
# ============================================================
def create_person(db: Session, data: schemas.PersonCreate):
    person = models.Person(**data.model_dump())
    # 64文字のランダム token を自動生成
    token = secrets.token_hex(32)
    person = models.Person(
        **data.model_dump(),
        token=token
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
# ============================================================
# Read
# ============================================================
def get_person(db: Session, person_id: int):
    return (
        db.query(models.Person)
        .filter(
            models.Person.id == person_id,
            models.Person.is_deleted == False
        )
        .first()
    )


def get_people(db: Session):
    return (
        db.query(models.Person)
        .filter(models.Person.is_deleted == False)
        .order_by(models.Person.furigana)
        .all()
    )


def get_people_by_furigana(db: Session, furigana: str):
    """ふりがなで部分一致検索"""
    return (
        db.query(models.Person)
        .filter(
            models.Person.is_deleted == False,
            models.Person.furigana.contains(furigana)
        )
        .order_by(models.Person.furigana)
        .all()
    )


# ============================================================
# Update
# ============================================================
def update_person(db: Session, person: models.Person, data: schemas.PersonUpdate):
    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(person, key, value)

    db.commit()
    db.refresh(person)
    return person


# ============================================================
# Logical Delete
# ============================================================
def delete_person(db: Session, person: models.Person):
    person.is_deleted = True
    db.commit()
    return person

