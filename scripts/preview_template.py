import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_TEMPLATES = BASE_DIR / "app" / "templates" / "admin"

def load_dummy_data(template_name: str):
    """
    テンプレートごとのダミーデータ。
    必要に応じて増やしていく。
    """
    if template_name == "meal_order_register":
        return {
            "preview": {
                "filename": "dummy.xlsx",
                "arrival_date": "2025-12-07",
                "applicable_date": "2025-12-08",
                "result_rows_count": 3,
                "meals": [
                    {"excel_row": 6, "meal_id": "03001", "meal_name": "たらの牛だしあん", "qty": ""},
                    {"excel_row": 7, "meal_id": "03002", "meal_name": "豚バラ肉の豆乳ソースがけ", "qty": 4},
                    {"excel_row": 8, "meal_id": "03005", "meal_name": "鮭の塩焼き", "qty": 2},
                ]
            }
        }
    # 空辞書はテンプレートに変数が無い場合でも動く
    return {}

def main():
    if len(sys.argv) < 2:
        print("テンプレート名を指定してください。例: python preview.py meal_order_register")
        sys.exit(1)

    template_name = sys.argv[1]
    template_file = f"{template_name}.html"

    if not (ADMIN_TEMPLATES / template_file).exists():
        print(f"テンプレートが見つかりません: {template_file}")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(ADMIN_TEMPLATES), autoescape=True)
    template = env.get_template(template_file)

    context = load_dummy_data(template_name)
    context["preview_mode"] = True  # プレビュー用フラグ
    html = template.render(**context)

    output = BASE_DIR / f"preview_{template_name}.html"
    output.write_text(html, encoding="utf-8")

    print(f"✔ {output.name} を生成しました。ブラウザで開けます。")

if __name__ == "__main__":
    main()
