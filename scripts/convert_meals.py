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
            "meal_name": m["meal_name"],
            "furigana": m.get("furigana"),
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
    
    # sides配列を1行にするため、カスタム整形
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, meal in enumerate(new_meals):
            # sides配列を1行で出力
            sides_str = json.dumps(meal["sides"], ensure_ascii=False)
            f.write("  {\n")
            f.write(f'    "meal_id": {meal["meal_id"]},\n')
            f.write(f'    "meal_name": "{meal["meal_name"]}",\n')
            f.write(f'    "furigana": "{meal.get("furigana", "")}",\n')
            f.write(f'    "sides": {sides_str},\n')
            f.write(f'    "kcal": {meal["kcal"]},\n')
            f.write(f'    "protein": {meal["protein"]},\n')
            f.write(f'    "fat": {meal["fat"]},\n')
            f.write(f'    "carb": {meal["carb"]},\n')
            f.write(f'    "salt": {meal["salt"]}\n')
            f.write("  }" + ("," if i < len(new_meals) - 1 else "") + "\n")
        f.write("]\n")

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
