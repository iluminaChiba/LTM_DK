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
# commit endpoint（最終形）
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
    # 既存アレルギー行を取得（差分判定用）
    # -----------------------------------------------------
    stmt = select(Allergy)
    existing_rows = {row.meal_id: row for row in db.scalars(stmt).all()}

    # 結果用
    new_ids = []          # allergies に新規追加された ID
    updated_ids = []      # allergies が更新された ID
    unchanged_ids = []    # 変更なしの ID
    new_meal_ids = []     # meals に存在しない新規メニュー ID（人間が登録すべき）
    
    # 既存 meals の ID セットを取得
    meals_stmt = select(Meal.meal_id)
    existing_meal_ids = set(db.scalars(meals_stmt).all())

    # -----------------------------------------------------
    # PREVIEW の全レコードを処理
    # -----------------------------------------------------
    for item in preview:
        meal_id = item["meal_id"]

        # -------------------------------------------------
        # meals に存在しない ID を検出（新規メニュー）
        # -------------------------------------------------
        if meal_id not in existing_meal_ids:
            new_meal_ids.append(meal_id)

        # -------------------------------------------------
        # allergies 側の差分処理
        # -------------------------------------------------
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
    # allergies には存在するが PREVIEW に無い ID
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
        "total_preview_rows": len(preview),
        "new_allergies": new_ids,
        "updated_allergies": updated_ids,
        "unchanged_allergies": unchanged_ids,
        "disappeared_allergies": disappeared_ids,

        # ★これが最重要：事務方が登録すべき新規メニュー
        "new_meal_ids": sorted(new_meal_ids),
    }
