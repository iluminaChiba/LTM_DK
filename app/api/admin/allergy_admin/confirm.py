from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db

from app.models.meal import Meal
from app.models.allergy import Allergy
from app.core.preview_cache import PREVIEW_CACHE

router = APIRouter()


# ---------------------------------------------------------
# アレルギー29項目（preview のキーと一致）
# ---------------------------------------------------------
ALLERGY_COLS = [
    "egg", "milk", "wheat", "soba", "peanut", "shrimp", "crab",
    "walnut", "abalone", "squid", "salmon_roe", "salmon", "mackerel",
    "seafood", "beef", "chicken", "pork", "orange", "kiwi", "apple",
    "peach", "banana", "soy", "cashew", "almond", "macadamia", "yam",
    "sesame", "gelatin",
]


# =========================================================
# commit endpoint
# =========================================================
@router.post("/confirm", response_model=None)
def allergy_commit(db: Session = Depends(get_db)):

    # -----------------------------------------------------
    # PREVIEW が存在するか？
    # -----------------------------------------------------
    preview = PREVIEW_CACHE.get("allergy_preview")
    if not preview:
        raise HTTPException(400, "PREVIEW が存在しません。先に /upload を実行してください。")

    # -----------------------------------------------------
    # 既存DBを取得（差分判定用）
    # -----------------------------------------------------
    stmt = select(Allergy)
    existing_rows = {row.meal_id: row for row in db.scalars(stmt).all()}

    new_ids = []
    updated_ids = []
    unchanged_ids = []

    # -----------------------------------------------------
    # PREVIEW の全レコードを処理
    # -----------------------------------------------------
    for item in preview:
        meal_id = item["meal_id"]
        name = item["name"]

        # meals 側に存在しなければ作る（必要に応じて）
        meal_obj = db.get(Meal, meal_id)
        if meal_obj is None:
            meal_obj = Meal(meal_id=meal_id, meal_name=name)
            db.add(meal_obj)
        else:
            # name の更新は任意。必要なら以下を有効化
            meal_obj.name = name

        # allergies 側
        old = existing_rows.get(meal_id)

        if old is None:
            # -------- 新規 INSERT --------
            new_allergy = Allergy(
                meal_id=meal_id,
                **{col: item[col] for col in ALLERGY_COLS}
            )
            db.add(new_allergy)
            new_ids.append(meal_id)

        else:
            # -------- UPDATE or UNCHANGED 判定 --------
            changed = False
            for col in ALLERGY_COLS:
                old_val = getattr(old, col)
                new_val = item[col]
                if old_val != new_val:
                    setattr(old, col, new_val)
                    changed = True

            if changed:
                updated_ids.append(meal_id)
            else:
                unchanged_ids.append(meal_id)

    # -----------------------------------------------------
    # DB に存在していたが、今回 PREVIEW にない => 消滅（必要なら返す）
    # -----------------------------------------------------
    preview_ids = {item["meal_id"] for item in preview}
    disappeared_ids = list(set(existing_rows.keys()) - preview_ids)

    # -----------------------------------------------------
    # トランザクション commit
    # -----------------------------------------------------
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"DB書き込み中にエラー: {e}")

    # -----------------------------------------------------
    # 完了レスポンス
    # -----------------------------------------------------
    return {
        "status": "ok",
        "total": len(preview),
        "new": new_ids,
        "updated": updated_ids,
        "unchanged": unchanged_ids,
        "disappeared": disappeared_ids,
    }
