# app/schemas/person.py
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


# ============================================================
# Base
# ============================================================
class PersonBase(BaseModel):
    person_name: str
    furigana: Optional[str] = None
    fee_category: Literal['visitor', 'trainee', 'normal'] = 'normal'
    is_present: bool = False
    ext1: Optional[str] = None
    ext2: Optional[str] = None


# ============================================================
# Create（API入力用）
# ============================================================
class PersonCreate(PersonBase):
    pass


# ============================================================
# Update（PATCH 用）
# ============================================================
class PersonUpdate(BaseModel):
    person_name: Optional[str] = None
    furigana: Optional[str] = None
    fee_category: Optional[
        Literal['visitor', 'trainee', 'normal']
    ] = None
    is_present: Optional[bool] = None
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    is_deleted: Optional[bool] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class Person(BaseModel):
    id: int
    person_name: str
    furigana: Optional[str] = None
    fee_category: str   #  出力は文字列じゃないとエラーになります。
    is_present: bool
    ext1: Optional[str] = None
    ext2: Optional[str] = None
    token: Optional[str] = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# UI用レスポンス（トークンから人名取得）
# ============================================================
class PersonByTokenResponse(BaseModel):
    """トークンから取得した人物情報（UI表示用）"""
    id: int
    person_name: str
    furigana: Optional[str] = None
    fee_category: str
    is_present: bool
    token: str

    class Config:
        from_attributes = True
