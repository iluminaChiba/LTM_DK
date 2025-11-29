# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.api.router import api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# /api 配下のルーティング
app.include_router(api_router, prefix="/api")

# DEBUG テスト用の静的ファイル あとで使いまわすかも
app.mount("/statics", StaticFiles(directory="app/api/statics"), name="statics")
# END DEBUG

# # データベース接続テスト（同期版）
# @app.get("/")
# def db_test(db: Session = Depends(get_db)):
#     result = db.execute(text("SELECT 1"))
#     return {
#         "message": "Database connection successful!",
#         "result": result.scalar()
#     }
