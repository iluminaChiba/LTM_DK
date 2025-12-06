from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.meal import MealCreate
from app.core.database import get_db
from app.schemas.allergy_new_meals import NewMealRegisterRequest
from app.core.preview_cache import PREVIEW_CACHE
from app.crud.meal import create_meal_if_not_exists
from app.core.templates import templates

router = APIRouter()

@router.get("/new_meals/{token}")
def show_new_meals_ui(request: Request, token: str, db: Session = Depends(get_db)):
    if token not in PREVIEW_CACHE:
        raise HTTPException(404, detail="指定されたトークンに対応する解析データが見つかりません。")

    cache_data = PREVIEW_CACHE[token]
    new_ids = cache_data.get("meal_new", [])

    return templates.TemplateResponse(
        "admin/allergy/new_meal_register.html",
        {
            "request": request,
            "new_meal_ids": new_ids,
        }
    )


@router.post("/new_meals")
def register_new_meals(payload: NewMealRegisterRequest, db: Session = Depends(get_db)):

    results = []

    # PREVIEW_CACHE が必要
    token = payload.token  # ← フォーム側に token を hidden で入れる
    cache_data = PREVIEW_CACHE.get(token, {})

    for item in payload.items:
        created = create_meal_if_not_exists(
            db=db,
            data=MealCreate(
                meal_id=item.meal_id,
                meal_name=item.meal_name,
                furigana=item.furigana,
                kcal=item.kcal,
                protein=item.protein,
                fat=item.fat,
                carb=item.carb,
                salt=item.salt
            )
        )

        results.append({
            "meal_id": item.meal_id,
            "status": "created" if created else "exists"
        })
    # ------------------------------------------
    # ここが重要：allergies の INSERT
    # ------------------------------------------
    for item in payload.items:
        meal_id = item.meal_id
        row = next((r for r in cache_data.get("rows", []) if r["meal_id"] == meal_id), None)
        if row:
            create_allergy_from_row(db, row)  # あなたの環境の CRUD 名に合わせて書く

    return {
        "message": "登録が完了しました。",
        "results": results
    }
