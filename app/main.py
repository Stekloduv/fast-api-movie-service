from fastapi import FastAPI
from app.routers import movies, users
from app.database import engine
from app.models import Base

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(movies.router)
app.include_router(users.router)
