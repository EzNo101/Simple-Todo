import pytest

from tests.fixtures.users import user_token

@pytest.mark.asyncio
async def test_get_todos(async_client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}

        response = await async_client.get("/todos/", headers=headers)
        print(response.json())
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_todo(async_client, user_token):
        ...