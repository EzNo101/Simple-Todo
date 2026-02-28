import pytest

from tests.fixtures.users import user_token, user_factory
from tests.fixtures.todos import create_todo

@pytest.mark.asyncio
async def test_get_todos(async_client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}

        response = await async_client.get("/todos/", headers=headers)
        print(response.json())
        assert response.status_code == 200

@pytest.mark.asyncio 
async def test_get_by_id(async_client, user_token, create_todo):
        headers = {"Authorization": f"Bearer {user_token}"}
        todo = create_todo["id"]

        response = await async_client.get(f"/todos/{todo}", headers=headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Test"
        
@pytest.mark.asyncio
async def test_create_todo(async_client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        data = {"title": "Todo test", "description": "Test desc"}

        response = await async_client.post("/todos/", json=data, headers=headers)
        assert response.status_code == 201
        resp_data = response.json()
        assert resp_data["title"] == "Todo test"
        assert resp_data["description"] == "Test desc"

@pytest.mark.asyncio
async def test_update_todo(async_client, user_token, create_todo):
        headers = {"Authorization": f"Bearer {user_token}"}
        todo = create_todo["id"]

        update_data = {"title": "Updated Title", "description": "Updated Description", "completed": True}
        response = await async_client.patch(f"/todos/{todo}", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_delete_todo(async_client, user_token, create_todo):
        headers = {"Authorization": f"Bearer {user_token}"}
        todo = create_todo["id"]

        response = await async_client.delete(f"/todos/{todo}", headers=headers)
        assert response.status_code == 204

@pytest.mark.asyncio
async def test_cannot_access(async_client, user_token, user_factory):
        # user2
        user2_data = user_factory.build().model_dump()
        await async_client.post("/auth/register", json=user2_data)
        login_resp = await async_client.post("/auth/login", data={
                "username": user2_data["email"],
                "password": user2_data["password"]
        })
        user2_token = login_resp.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        user1_headers = {"Authorization": f"Bearer {user_token}"}
        todo_resp = await async_client.post(
                "/todos/",
                json={"title": "Test", "description": "Test desc"},
                headers=user1_headers 
        )
        todo_id = todo_resp.json()["id"]

        # user2 try to get, update, delete user1's todo
        resp = await async_client.get(f"/todos/{todo_id}", headers=user2_headers)
        assert resp.status_code in (403, 404)
        resp = await async_client.patch(
                f"/todos/{todo_id}",
                json={"title": "Hacked"},
                headers=user2_headers
        )
        assert resp.status_code in (403, 404)
        resp = await async_client.delete(f"/todos/{todo_id}", headers=user2_headers)
        assert resp.status_code in (403, 404)