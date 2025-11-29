# app/models/person.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class FeeCategory(enum.Enum):
    visitor = "visitor"
    trainee = "trainee"
    normal = "normal"


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String(255), nullable=False)
    furigana = Column(String(255), nullable=False)

    token = Column(String(64), unique=True, nullable=True)

    fee_category = Column(
        Enum(FeeCategory),
        nullable=False,
        default=FeeCategory.normal,
    )
    
    is_present = Column(Boolean, nullable=False, default=False)

    ext1 = Column(String(255), nullable=True)
    ext2 = Column(String(255), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
