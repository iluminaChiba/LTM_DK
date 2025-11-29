import json
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
BASE_DIR = Path(__file__).resolve().parent.parent  # プロジェクトルート
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.meal import Meal

JSON_PATH = BASE_DIR / "app" / "resources" / "monthly_menu.json"

def import_meals():
    db = SessionLocal()
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            meals = json.load(f)

        for item in meals:
            meal = Meal(
                meal_id=item["meal_id"],
                meal_name=item["meal_name"],
                furigana=item.get("furigana"),
                side1=item.get("side1"),
                side2=item.get("side2"),
                side3=item.get("side3"),
                kcal=item.get("kcal"),
                protein=item.get("protein"),
                fat=item.get("fat"),
                carb=item.get("carb"),
                salt=item.get("salt"),
            )
            db.add(meal)

        db.commit()
        print(f"✅ {len(meals)}件のメニューをインポートしました")
    except Exception as e:
        db.rollback()
        print(f"❌ エラー: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_meals()
