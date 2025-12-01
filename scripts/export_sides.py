import json
import sys
from pathlib import Path

# プロジェクトルートをPYTHONPATHに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models.side_dish import SideDish

def export_sides_json(output_path="app/resources/sides.json"):
    db = SessionLocal()
    try:
        sides = db.query(SideDish).order_by(SideDish.side_dish_id).all()

        data = []
        for s in sides:
            data.append({
                "side_dish_id": s.side_dish_id,
                "name": s.name
            })

        # 出力ディレクトリを作成
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"副菜一覧を JSON にエクスポートしました: {output_file} ({len(data)}件)")
    finally:
        db.close()

if __name__ == "__main__":
    export_sides_json()
