# app/dependencies.py
from app.template_manager import TemplateManager


def get_template_manager() -> TemplateManager:
    """Jinja2テンプレートマネージャーを提供する依存性注入関数"""
    return TemplateManager("app/templates")
