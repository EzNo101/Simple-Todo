import pytest_asyncio
from tests.factories.user_factory import UserFactory

@pytest_asyncio.fixture(scope="function")
async def user_token(async_client):
    # register
    user_data = UserFactory().model_dump()
    register_response = await async_client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201
    # login for get a token
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    login_response = await  async_client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    return token