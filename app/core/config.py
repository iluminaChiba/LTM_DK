# app/core/config.py
# まだ未稼働ですが、将来的に設定管理用に使用する予定です。
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    # 必要に応じて追加

    class Config:
        env_file = ".env"

settings = Settings()
"""
#上記の設定を有効化し、適切に整えれば、以下のように各ファイルからの呼び出しを一元化できます。
# from app.core.config import settings