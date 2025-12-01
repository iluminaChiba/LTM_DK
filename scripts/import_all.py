import sys
import time
from pathlib import Path

# プロジェクトルートをPythonパスに追加
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import text
from app.core.database import SessionLocal

from scripts.import_sides import import_side_dishes
from scripts.import_meals import import_meals
from scripts.import_allergies import import_allergies


def wait_for_mysql():
    """MySQL が起動するまで待機（最大30秒）"""
    for _ in range(30):
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError("MySQL が起動しませんでした。")


def main():
    print("⏳ MySQL の起動を待っています…")
    wait_for_mysql()

    print("▶ 副菜（side_dishes）をインポートします…")
    import_side_dishes()

    print("▶ meals をインポートします…（副菜リンク生成付き）")
    import_meals()

    print("▶ allergies をインポートします…")
    import_allergies()

    print("🎉 すべての初期データ投入が完了しました！")


if __name__ == "__main__":
    main()
