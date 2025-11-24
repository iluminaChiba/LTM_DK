# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://ltm_user:ltm_pass@db:3306/ltm_db"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True,
    future=True,
)

# セッションファクトリ
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# FastAPI dependency
async def get_session():
    async with async_session() as session:
        yield session
