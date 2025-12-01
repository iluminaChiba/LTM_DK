# scripts/migrate_sides.py

import sys
from pathlib import Path

# プロジェクトルートをPYTHONPATHに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.meal import Meal
from app.models.side_dish import SideDish
from app.models.meal_side_dish import MealSideDish


def extract_unique_sides(db: Session) -> set[str]:
    unique = set()

    meals = db.query(Meal).all()

    for meal in meals:
        for s in [meal.side1, meal.side2, meal.side3]:
            if s is not None and s.strip() != "":
                unique.add(s.strip())

    return unique


def register_side_dishes(db: Session, sides: set[str]) -> dict[str, int]:
    name_to_id = {}

    for name in sorted(sides):
        sd = SideDish(name=name)
        db.add(sd)
        db.flush()  # INSERT を確定させ ID を取得
        name_to_id[name] = sd.side_dish_id

    db.commit()
    return name_to_id


def create_meal_side_links(db: Session, name_to_id: dict[str, int]):
    meals = db.query(Meal).all()

    for meal in meals:
        for idx, s in enumerate([meal.side1, meal.side2, meal.side3], start=1):
            if s is not None and s.strip() != "":
                side_id = name_to_id[s.strip()]
                link = MealSideDish(
                    meal_id=meal.meal_id,
                    side_dish_id=side_id,
                    position=idx,
                )
                db.add(link)

    db.commit()


def migrate_sides(db: Session):
    """副菜をmealsテーブルから分離してside_dishesテーブルへ移行"""
    # 1. 副菜抽出
    sides = extract_unique_sides(db)
    print(f"抽出された副菜: {len(sides)}種類")

    # 2. 副菜マスターへ登録 → ID辞書作成
    name_to_id = register_side_dishes(db, sides)
    print(f"side_dishesテーブルへ登録完了")

    # 3. meals → meal_side_dish の関連を作成
    create_meal_side_links(db, name_to_id)
    print(f"meal_side_dishテーブルへリンク作成完了")

    print("副菜分離マイグレーション完了")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        migrate_sides(db)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

