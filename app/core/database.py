# app/core/database.py
"""
core/database.py
アプリケーションの根幹となる ＤＢセッション管理を提供します。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://ltm_user:ltm_pass@db:3306/ltm_db"

# Base class for models
Base = declarative_base()

# Engine（同期版）
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,        # 必要なら True
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Dependency（同期版）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
