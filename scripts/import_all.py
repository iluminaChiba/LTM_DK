import sys
import time
from pathlib import Path

# プロジェクトルートをPythonパスに追加
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from scripts.import_meals import import_meals
from scripts.import_allergies import import_allergies

def wait_for_mysql():
    """MySQL が起動するまで待機する。最大30秒。"""
    for _ in range(30):
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return True
        except Exception:
            time.sleep(1)
    raise RuntimeError("MySQL が起動しませんでした。")

def main():
    print("⏳ MySQL の起動を待機しています...")
    wait_for_mysql()

    print("▶ meals の初期データをインポートします...")
    import_meals()

    print("▶ allergies の初期データをインポートします...")
    import_allergies()

    print("🎉 すべての初期データ投入が完了しました。")

if __name__ == "__main__":
    main()
