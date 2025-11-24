from fastapi import FastAPI, Depends
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import time

app = FastAPI()

@app.get("/")
async def db_test(session: AsyncSession = Depends(get_session)):
    start_time = time.time()

    result = await session.execute(text("SELECT 1"))
    
    elapsed_time = time.time() - start_time
    return {
        "message": "Database connection successful!",
        "elapsed_time": elapsed_time,
        "result": result.scalar()
    }
