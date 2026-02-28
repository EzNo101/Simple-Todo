import pytest_asyncio

@pytest_asyncio.fixture(scope="function")
async def create_todo(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    todo_data = {"title": "Test", "description": "desc"}
    create_resp = await async_client.post("/todos/", json=todo_data, headers=headers)
    assert create_resp.status_code == 201
    return create_resp.json()