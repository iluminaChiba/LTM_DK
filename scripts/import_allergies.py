import csv
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
BASE_DIR = Path(__file__).resolve().parent.parent  # プロジェクトルート
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.allergy import Allergy
from app.models.meal import Meal

CSV_PATH = BASE_DIR / "app" / "resources" / "allergies" / "allergy_raw_2025_12.csv"

# allergiesテーブルの28項目（DBのカラム順と完全一致）
COLUMNS = [
    "egg","milk","wheat","soba","peanut","shrimp","crab","walnut","abalone",
    "squid","salmon_roe","salmon","mackerel","seafood","beef","chicken","pork",
    "orange","kiwi","apple","peach","banana","soy","cashew","almond",
    "macadamia","yam","sesame","gelatin"
]

def import_allergies():
    db = SessionLocal()

    try:
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"CSVファイルが見つかりません: {CSV_PATH}")

        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            count = 0
            skip_count = 0
            for row_num, row in enumerate(reader, start=1):
                # 空行をスキップ
                if not row or not row[0].strip():
                    continue

                # ヘッダー行をスキップ（meal_idが数字でない場合）
                try:
                    meal_id = int(row[0])
                except ValueError:
                    print(f"⚠️ {row_num}行目をスキップ（ヘッダー or 無効なmeal_id）: {row[0]}")
                    skip_count += 1
                    continue

                # 行の長さチェック（最低30列必要: meal_id + 1列 + 28アレルギー項目）
                if len(row) < 30:
                    print(f"⚠️ {row_num}行目をスキップ（列数不足: {len(row)}列）")
                    skip_count += 1
                    continue

                # mealsテーブルに存在するか確認（外部キー制約対策）
                meal_exists = db.query(Meal).filter(Meal.meal_id == meal_id).first()
                if not meal_exists:
                    print(f"⚠️ meal_id={meal_id} はmealsテーブルに存在しないためスキップ")
                    skip_count += 1
                    continue

                # 既存データがあればスキップ（重複防止）
                existing = db.query(Allergy).filter(Allergy.meal_id == meal_id).first()
                if existing:
                    print(f"⚠️ meal_id={meal_id} のアレルギー情報は既に存在するためスキップ")
                    skip_count += 1
                    continue

                # 3〜30列目がアレルギー（28個）
                raw = row[2:30]
                data = [1 if cell.strip() == "●" else 0 for cell in raw]

                allergy = Allergy(
                    meal_id=meal_id,
                    **dict(zip(COLUMNS, data))
                )
                db.add(allergy)
                count += 1

        db.commit()
        print(f"✅ {count}件のアレルギー情報をインポートしました")
        if skip_count > 0:
            print(f"ℹ️ {skip_count}件をスキップしました")

    except Exception as e:
        db.rollback()
        print(f"❌ エラー: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_allergies()
