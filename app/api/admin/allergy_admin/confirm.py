# app/api/admin/allergy_admin/confirm.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.core.preview_cache import PREVIEW_CACHE
from app.models.allergy import Allergy
from app.models.meal import Meal
from app.core.templates import templates   # ← あなたの構成に合わせた
from app import schemas

router = APIRouter()

ALLERGY_COLS = [
    "egg","milk","wheat","soba","peanut","shrimp","crab","walnut",
    "abalone","squid","salmon_roe","salmon","mackerel","seafood",
    "beef","chicken","pork","orange","kiwi","apple","peach","banana",
    "soy","cashew","almond","macadamia","yam","sesame","gelatin"
]

@router.post("/confirm/{token}")
def confirm_allergy(token: str, request: Request, db: Session = Depends(get_db)):

    if token not in PREVIEW_CACHE:
        raise HTTPException(404, "指定されたトークンに対応する解析データが見つかりません。")

    cache = PREVIEW_CACHE[token]

    preview_rows = cache["rows"]
    meal_new = cache.get("meal_new", [])

    # DB 既存データ取得
    stmt = select(Allergy)
    existing = {row.meal_id: row for row in db.scalars(stmt).all()}

    inserted = []
    updated = []
    unchanged = []

    for row in preview_rows:
        meal_id = row["meal_id"]

        if meal_id in meal_new:
            # ここでは登録しない。new_meals で登録。
            continue

        old = existing.get(meal_id)

        if old is None:
            db.add(Allergy(
                meal_id=meal_id,
                **{col: row[col] for col in ALLERGY_COLS}
            ))
            inserted.append(meal_id)
            continue

        changed = False
        for col in ALLERGY_COLS:
            new_val = row[col]
            old_val = getattr(old, col)

            if new_val != old_val:
                setattr(old, col, new_val)
                changed = True

        if changed:
            updated.append(meal_id)
        else:
            unchanged.append(meal_id)

    db.commit()

    # ----------------------------
    # confirm 後のテーブル表示
    # ----------------------------
    return templates.TemplateResponse(
        "admin/allergy_table.html",
        {
            "request": request,
            "preview_data": preview_rows,

            "meal_new": meal_new,
            "meal_existing": cache.get("meal_existing", []),

            "allergy_new": inserted,
            "allergy_updated": updated,
            "allergy_unchanged": unchanged,

            "token": token,
            "is_after_confirm": True,
        }
    )
