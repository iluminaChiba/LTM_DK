# app/template_manager/__init__.py
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape
from pathlib import Path
from typing import Dict, Any

class TemplateManager:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir).resolve()
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )


    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except TemplateNotFound:
            raise TemplateNotFound(f"Template '{template_name}' not found in '{self.template_dir}'")
        except Exception as e:
            raise RuntimeError(f"Render error '{template_name}': {e}")
    
        
    def add_filter(self, name: str, filter_func):
        self.env.filters[name] = filter_func
    

    def add_global(self, name: str, global_func):
        self.env.globals[name] = global_func


    def render_to_file(self, template_name: str, context: Dict[str, Any], output_path: str) -> None:
        rendered = self.render(template_name, context)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding='utf-8')


__all__ = ["TemplateManager"]
