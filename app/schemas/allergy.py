# app/schemas/allergy.py
from typing import Optional
from pydantic import BaseModel


# ============================================================
# Base
# ============================================================
class AllergyBase(BaseModel):
    # 特定原材料（表示義務）7品目
    egg: bool = False
    milk: bool = False
    wheat: bool = False
    soba: bool = False
    peanut: bool = False
    shrimp: bool = False
    crab: bool = False
    
    # 特定原材料に準ずるもの（推奨表示）22品目
    walnut: bool = False
    abalone: bool = False
    squid: bool = False
    salmon_roe: bool = False
    salmon: bool = False
    mackerel: bool = False
    seafood: bool = False
    beef: bool = False
    chicken: bool = False
    pork: bool = False
    orange: bool = False
    kiwi: bool = False
    apple: bool = False
    peach: bool = False
    banana: bool = False
    soy: bool = False
    cashew: bool = False
    almond: bool = False
    macadamia: bool = False
    yam: bool = False
    sesame: bool = False
    gelatin: bool = False


# ============================================================
# Create（API入力用）
# ============================================================
class AllergyCreate(AllergyBase):
    meal_id: int


# ============================================================
# Update（PATCH 用）
# ============================================================
class AllergyUpdate(BaseModel):
    egg: Optional[bool] = None
    milk: Optional[bool] = None
    wheat: Optional[bool] = None
    soba: Optional[bool] = None
    peanut: Optional[bool] = None
    shrimp: Optional[bool] = None
    crab: Optional[bool] = None
    walnut: Optional[bool] = None
    abalone: Optional[bool] = None
    squid: Optional[bool] = None
    salmon_roe: Optional[bool] = None
    salmon: Optional[bool] = None
    mackerel: Optional[bool] = None
    seafood: Optional[bool] = None
    beef: Optional[bool] = None
    chicken: Optional[bool] = None
    pork: Optional[bool] = None
    orange: Optional[bool] = None
    kiwi: Optional[bool] = None
    apple: Optional[bool] = None
    peach: Optional[bool] = None
    banana: Optional[bool] = None
    soy: Optional[bool] = None
    cashew: Optional[bool] = None
    almond: Optional[bool] = None
    macadamia: Optional[bool] = None
    yam: Optional[bool] = None
    sesame: Optional[bool] = None
    gelatin: Optional[bool] = None


# ============================================================
# Response（DB出力用）
# ============================================================
class Allergy(AllergyBase):
    meal_id: int

    class Config:
        from_attributes = True
