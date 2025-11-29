# app/api/person.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import schemas
from app.crud import person as crud_person

router = APIRouter()


# ============================================================
# Create
# ============================================================
@router.post("/", response_model=schemas.Person)
def create_person(person_in: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud_person.create_person(db, person_in)


# ============================================================
# Read (one)
# ============================================================
@router.get("/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = crud_person.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


# ============================================================
# Read (all)
# ============================================================
@router.get("/", response_model=list[schemas.Person])
def read_people(furigana: str | None = None, db: Session = Depends(get_db)):
    if furigana:
        return crud_person.get_people_by_furigana(db, furigana)
    return crud_person.get_people(db)


# ============================================================
# Update
# ============================================================
@router.patch("/{person_id}", response_model=schemas.Person)
def update_person(
    person_id: int,
    person_in: schemas.PersonUpdate,
    db: Session = Depends(get_db),
):
    person = crud_person.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return crud_person.update_person(db, person, person_in)


# ============================================================
# Delete（論理削除）
# ============================================================
@router.delete("/{person_id}", response_model=schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = crud_person.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return crud_person.delete_person(db, person)
