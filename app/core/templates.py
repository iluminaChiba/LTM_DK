# app/core/templates.py

from fastapi.templating import Jinja2Templates

# Jinja2テンプレートエンジンの共通インスタンス
templates = Jinja2Templates(directory="app/templates")

# グローバル変数を設定（全テンプレートで利用可能）
templates.env.globals.update({
    "css_root": "/api/admin/css",
    "js_root": "/api/admin/js"
})
