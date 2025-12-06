from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.core.preview_cache import PREVIEW_CACHE
from app.core.templates import templates

router = APIRouter()

@router.get("/table-view/{token}", response_class=HTMLResponse)
def allergy_table_view(token: str, request: Request):
    """
    トークンを受け取り、allergy_table.html をレンダリングする。
    """
    print(f"DEBUG [table_view.py]: Received token = {token}")
    print(f"DEBUG [table_view.py]: CACHE keys count = {len(PREVIEW_CACHE)}")
    print(f"DEBUG [table_view.py]: Token in CACHE? {token in PREVIEW_CACHE}")
    
    if token not in PREVIEW_CACHE:
        raise HTTPException(404, detail="指定されたトークンに対応する解析データが見つかりません。")

    cache_data = PREVIEW_CACHE[token]
    
    print(f"DEBUG [table_view.py]: cache_data keys = {cache_data.keys()}")
    print(f"DEBUG [table_view.py]: new_allergies = {cache_data.get('new_allergies', [])}")
    print(f"DEBUG [table_view.py]: new_allergies length = {len(cache_data.get('new_allergies', []))}")
    
    context = {
        "request": request,
        "token": token,
        "preview_data": cache_data["rows"],
        # アレルギー側の差分
        "allergy_new": cache_data.get("allergy_new", []),
        "allergy_updated": cache_data.get("allergy_updated", []),
        "allergy_unchanged": cache_data.get("allergy_unchanged", []),
        # メニュー側の差分(新規登録ボタンの表示判定に使います)
        "meal_new": cache_data.get("meal_new", []),
    }
    
    if not cache_data.get("rows"):
        context["error_message"] = "指定されたトークンに対応するデータが見つかりません。"
        
    return templates.TemplateResponse("admin/allergy_table.html", context)