from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.meal import MealCreate
from app.core.database import get_db
from app.schemas.allergy_new_meals import NewMealRegisterRequest
from app.core.preview_cache import PREVIEW_CACHE
from app.crud.meal import create_meal_if_not_exists
from app.core.templates import templates
from app.crud.allergy import create_allergy_from_row


router = APIRouter()



@router.get("/new_meals/{token}")
def show_new_meals_ui(request: Request, token: str, db: Session = Depends(get_db)):
    if token not in PREVIEW_CACHE:
        raise HTTPException(404, detail="指定されたトークンに対応する解析データが見つかりません。")

    cache_data = PREVIEW_CACHE[token]
    new_ids = cache_data.get("meal_new", [])

    return templates.TemplateResponse(
        "admin/new_meals.html",
        {
            "request": request,
            "new_meal_ids": new_ids,
            "token": token,
        }
    )


@router.post("/new_meals")
async def register_new_meals(request: Request, db: Session = Depends(get_db)):

    # ------------------------------------
    # 1) FormData を受け取る
    # ------------------------------------
    form = await request.form()

    # token 取得
    token = form.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="token が存在しません。")

    cache_data = PREVIEW_CACHE.get(token)
    if not cache_data:
        raise HTTPException(status_code=404, detail="PREVIEW_CACHE に該当 token がありません。")

    # ------------------------------------
    # 2) items[...] を Python の list に復元
    # ------------------------------------
    items = []
    index = 0

    while True:
        base = f"items[{index}]"

        meal_id_key = f"{base}[meal_id]"
        if meal_id_key not in form:
            break  # もう項目が無い

        try:
            meal_id = int(form.get(meal_id_key))
        except:
            raise HTTPException(400, f"meal_id の形式が不正です（index={index}）")
        
        def get_float_or_none(key):
            val = form.get(key)
            if val is not None and val != '':
                try:
                # Decimalに変換しやすいように、文字列ではなくfloatに変換してから渡す
                    return float(val) 
                except ValueError:
                # 数値として不正な場合は400エラー (念のため)
                    raise HTTPException(400, f"{key} の値の形式が不正です")
            return None # 空文字列やNoneの場合はNoneを返す

        item = {
            "meal_id": meal_id,
            "meal_name": form.get(f"{base}[meal_name]"),
            "furigana": form.get(f"{base}[furigana]"),
            "kcal": get_float_or_none(f"{base}[kcal]"),
            "protein": get_float_or_none(f"{base}[protein]"),
            "fat": get_float_or_none(f"{base}[fat]"),
            "carb": get_float_or_none(f"{base}[carb]"),
            "salt": get_float_or_none(f"{base}[salt]"),
        }

        items.append(item)
        index += 1

    if not items:
        raise HTTPException(400, "items が 0 件でした。")

    # ------------------------------------
    # 3) meals 登録
    # ------------------------------------
    register_results = []

    for item in items:
        created = create_meal_if_not_exists(
            db=db,
            data={
                "meal_id": item["meal_id"],
                "meal_name": item["meal_name"],
                "furigana": item["furigana"],
                "kcal": item["kcal"],
                "protein": item["protein"],
                "fat": item["fat"],
                "carb": item["carb"],
                "salt": item["salt"],
            }
        )
        register_results.append({
            "meal_id": item["meal_id"],
            "status": "created" if created else "exists",
        })

    # ------------------------------------
    # 4) アレルギー情報も PREVIEW_CACHE の rows から登録
    # ------------------------------------
    for item in items:
        meal_id = item["meal_id"]
        # rows から meal_id に一致する行を探す
        row = next((r for r in cache_data.get("rows", []) if r["meal_id"] == meal_id), None)
        if row:
            create_allergy_from_row(db, row)

    db.commit()

    # ------------------------------------
    # 5) 戻り値（後で TemplateResponse にしても良い）
    # ------------------------------------
    return {
        "message": "登録が完了しました。",
        "results": register_results,
        "count": len(register_results),
    }
