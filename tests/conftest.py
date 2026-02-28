import os
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.database.base import Base
from app.database.session import get_db

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

@pytest_asyncio.fixture(scope="function")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine

@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

#override fastapi dependency
@pytest_asyncio.fixture
async def override_get_db(engine):
    TestSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )
    async def _override(): # dependency function for fastapi
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def async_client(override_get_db):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000"
    ) as client:
        yield client
