# app/models/allergy.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.core.database import Base


class Allergy(Base):
    __tablename__ = "allergies"

    meal_id = Column(Integer, ForeignKey("meals.meal_id", ondelete="CASCADE"), primary_key=True)
    
    # 特定原材料（表示義務）7品目
    egg = Column(Boolean, nullable=False, server_default="0")
    milk = Column(Boolean, nullable=False, server_default="0")
    wheat = Column(Boolean, nullable=False, server_default="0")
    soba = Column(Boolean, nullable=False, server_default="0")
    peanut = Column(Boolean, nullable=False, server_default="0")
    shrimp = Column(Boolean, nullable=False, server_default="0")
    crab = Column(Boolean, nullable=False, server_default="0")
    
    # 特定原材料に準ずるもの（推奨表示）21品目
    walnut = Column(Boolean, nullable=False, server_default="0")
    abalone = Column(Boolean, nullable=False, server_default="0")
    squid = Column(Boolean, nullable=False, server_default="0")
    salmon_roe = Column(Boolean, nullable=False, server_default="0")
    salmon = Column(Boolean, nullable=False, server_default="0")
    mackerel = Column(Boolean, nullable=False, server_default="0")
    seafood = Column(Boolean, nullable=False, server_default="0")
    beef = Column(Boolean, nullable=False, server_default="0")
    chicken = Column(Boolean, nullable=False, server_default="0")
    pork = Column(Boolean, nullable=False, server_default="0")
    orange = Column(Boolean, nullable=False, server_default="0")
    kiwi = Column(Boolean, nullable=False, server_default="0")
    apple = Column(Boolean, nullable=False, server_default="0")
    peach = Column(Boolean, nullable=False, server_default="0")
    banana = Column(Boolean, nullable=False, server_default="0")
    soy = Column(Boolean, nullable=False, server_default="0")
    cashew = Column(Boolean, nullable=False, server_default="0")
    almond = Column(Boolean, nullable=False, server_default="0")
    macadamia = Column(Boolean, nullable=False, server_default="0")
    yam = Column(Boolean, nullable=False, server_default="0")
    sesame = Column(Boolean, nullable=False, server_default="0")
    gelatin = Column(Boolean, nullable=False, server_default="0")

    def __repr__(self):
        allergens = []
        if self.egg: allergens.append("卵")
        if self.milk: allergens.append("乳")
        if self.wheat: allergens.append("小麦")
        if self.soba: allergens.append("そば")
        if self.peanut: allergens.append("落花生")
        if self.shrimp: allergens.append("えび")
        if self.crab: allergens.append("かに")
        
        allergen_str = ", ".join(allergens) if allergens else "なし"
        return f"<Allergy(meal_id={self.meal_id}, allergens={allergen_str})>"
