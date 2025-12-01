import json
import sys
from pathlib import Path

# プロジェクトルート設定
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.meal import Meal
from app.models.meal_side_dish import MealSideDish


JSON_PATH = BASE_DIR / "app" / "resources" / "monthly_menu.json"


def import_meals():
    db = SessionLocal()

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            meals = json.load(f)

        for item in meals:
            meal_id = item["meal_id"]
            
            # ---- 既存チェック ----
            existing_meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
            if existing_meal:
                print(f"⏩ meal_id={meal_id} は既に存在するのでスキップ")
                continue

            # ---- Meal 本体の作成 ----
            meal = Meal(
                meal_id=meal_id,
                meal_name=item["meal_name"],
                furigana=item.get("furigana"),
                kcal=item.get("kcal"),
                protein=item.get("protein"),
                fat=item.get("fat"),
                carb=item.get("carb"),
                salt=item.get("salt"),
            )

            db.add(meal)
            db.commit()
            db.refresh(meal)

            # ---- 副菜リレーションの作成 ----
            sides = item.get("sides", [])

            for idx, side_id in enumerate(sides, start=1):
                link = MealSideDish(
                    meal_id=meal.meal_id,
                    side_dish_id=side_id,
                    position=idx
                )
                db.add(link)

            db.commit()

        print(f"✅ {len(meals)}件のメニューをインポートしました")

    except Exception as e:
        db.rollback()
        print("❌ エラー:", e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_meals()
