import json
from pathlib import Path

def load_side_map(sides_path="app/resources/sides.json"):
    """副菜JSONから名前→IDのマッピングを作成"""
    sides_file = Path(sides_path)
    if not sides_file.exists():
        raise FileNotFoundError(f"副菜JSONファイルが見つかりません: {sides_file}")
    
    with open(sides_file, encoding="utf-8") as f:
        sides = json.load(f)
    return { s["name"]: s["side_dish_id"] for s in sides }

def convert_meals(old_path="app/resources/monthly_menu.json", new_path="app/resources/meals_converted.json"):
    """古いmeals.jsonを新形式（副菜ID配列）に変換"""
    old_file = Path(old_path)
    if not old_file.exists():
        raise FileNotFoundError(f"monthly_menu.jsonが見つかりません: {old_file}")
    
    side_map = load_side_map()

    with open(old_file, encoding="utf-8") as f:
        meals = json.load(f)

    new_meals = []
    for m in meals:
        sides = []
        for s in [m.get("side1"), m.get("side2"), m.get("side3")]:
            if s and s in side_map:
                sides.append(side_map[s])

        new_meals.append({
            "meal_id": m["meal_id"],
            "name": m["meal_name"],
            "sides": sides,
            "kcal": m["kcal"],
            "protein": m["protein"],
            "fat": m["fat"],
            "carb": m["carb"],
            "salt": m["salt"],
        })

    # 出力ディレクトリを作成
    new_file = Path(new_path)
    new_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(new_file, "w", encoding="utf-8") as f:
        json.dump(new_meals, f, ensure_ascii=False, indent=2)

    print(f"meals.json を新形式に変換しました: {new_file} ({len(new_meals)}件)")

if __name__ == "__main__":
    try:
        convert_meals()
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        print("先に export_sides.py を実行して sides.json を生成してください。")
    except Exception as e:
        print(f"予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
