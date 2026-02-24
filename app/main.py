from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import router
from app.database.base import Base
from app.database.session import engine
from app.models.todo import Todo


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)