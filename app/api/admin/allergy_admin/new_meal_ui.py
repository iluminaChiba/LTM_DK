from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/new_meals")
def new_meals_page(request: Request):
    """
    新規メニュー登録画面。
    ここではまだ meal_id や名前は受け取らず、
    フロント側 JS から埋め込む方式にする。
    """
    return templates.TemplateResponse(
        "admin/new_meal_register.html",
        {"request": request}
    )
