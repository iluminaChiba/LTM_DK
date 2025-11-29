# app/core/dependencies.py
"""
core/dependencies.py
FastAPI の依存注入（Depends 用関数）を提供します。
"""
from app.template_manager import TemplateManager


def get_template_manager() -> TemplateManager:
    """Jinja2テンプレートマネージャーを提供する依存性注入関数"""
    return TemplateManager("app/templates")
