import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.side_dish import SideDish

JSON_PATH = BASE_DIR / "app" / "resources" / "sides.json"

def import_side_dishes():
    db = SessionLocal()
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            sides = json.load(f)

        for item in sides:
            side_dish_id = item["side_dish_id"]
            
            # 既存チェック
            existing = db.query(SideDish).filter(SideDish.side_dish_id == side_dish_id).first()
            if existing:
                print(f"⏩ side_dish_id={side_dish_id} は既に存在するのでスキップ")
                continue
            
            sd = SideDish(
                side_dish_id=side_dish_id,
                name=item["name"],
            )
            db.add(sd)

        db.commit()
        print(f"✅ {len(sides)}件の副菜マスターをインポートしました")
    except Exception as e:
        db.rollback()
        print("❌ エラー:", e)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_side_dishes()
