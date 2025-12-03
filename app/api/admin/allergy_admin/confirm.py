from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.models.allergy import Allergy
from app.models.meal import Meal
from app.core.preview_cache import PREVIEW_CACHE

router = APIRouter()


@router.post("/confirm")
def allergy_confirm():
    """
    PREVIEW_CACHE に保存されたプレビュー結果を
    allergies テーブルへ登録する。
    Excel importer と同様の責務分離を行う。
    """

    preview_data = PREVIEW_CACHE.get("allergy_preview")
    if preview_data is None:
        raise HTTPException(status_code=400, detail="プレビュー結果が見つかりません")

    db = SessionLocal()

    inserted = 0
    skipped = 0
    errors = []

    try:
        for row in preview_data:
            meal_id = row["meal_id"]

            # meals テーブルに存在しない場合はスキップ（要件通り）
            meal_exists = db.query(Meal).filter(Meal.meal_id == meal_id).first()
            if not meal_exists:
                skipped += 1
                errors.append(f"meal_id {meal_id} は meals テーブルに存在しないためスキップ")
                continue

            # 既存のレコードはスキップ
            exist = db.query(Allergy).filter(Allergy.meal_id == meal_id).first()
            if exist:
                skipped += 1
                continue

            # アレルギー 28 カラムの並び
            ALLERGY_COLS = [
                "egg","milk","wheat","soba","peanut","shrimp","crab","walnut",
                "abalone","squid","salmon_roe","salmon","mackerel","seafood",
                "beef","chicken","pork","orange","kiwi","apple","peach",
                "banana","soy","cashew","almond","macadamia","yam","sesame","gelatin"
            ]

            values = {col: row[f"col_{i+3}"] for i, col in enumerate(ALLERGY_COLS)}

            entry = Allergy(
                meal_id = meal_id,
                **values
            )

            db.add(entry)
            inserted += 1

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB登録中にエラー: {e}")

    finally:
        db.close()

    return {
        "status": "ok",
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors,
    }
