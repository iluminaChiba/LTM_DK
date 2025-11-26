# app/api/ui_test.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
async def meal_logs_uitest(request: Request):
    payload = await request.json()
    menu_id = payload.get("menu_id")
    token = request.headers.get("X-Auth-Token")

    print("=== SIMPLE LOG ===")
    print("menu_id:", menu_id)
    print("token  :", token)
    print("===================")

    return {"status": "ok"}
