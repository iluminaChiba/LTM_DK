
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/table-view/{token}", response_class=HTMLResponse)
def allergy_table_view(token: str, request: Request):
    """
    トークンを受け取り、allergy_table.html をレンダリングする。
    """
    from app.core.preview_cache import PREVIEW_CACHE
    
    preview_data = PREVIEW_CACHE.get(token)
    
    context = {
        "request": request,
        "css_root": "/api/admin/css",
        "js_root": "/api/admin/js",
        "token": token,
        "preview_data": preview_data,
    }
    
    if not preview_data:
        context["error_message"] = "指定されたトークンに対応するデータが見つかりません。"
        
    return templates.TemplateResponse("admin/allergy_table.html", context)