from fastapi import HTTPException

from app.repository.todo import TodoRepository
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def get_all(self) -> list[Todo]:
        return await self.repo.get_all()
    
    async def get_by_id(self, id: int) -> Todo:
        todo = await self.repo.get_by_id(id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return todo

    async def get_all_by_user(self, user_id: int) -> list[Todo]:
        return await self.repo.get_all_by_user(user_id)
    
    async def get_by_id_and_user(self, todo_id: int, user_id: int) -> Todo:
        todo = await self.repo.get_by_id_and_user(todo_id, user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return todo

    async def create(self, data: TodoCreate, user_id: int) -> Todo:
        return await self.repo.create_todo(data, user_id)
    
    async def update(self, id: int, data: TodoUpdate, user_id: int) -> Todo:
        todo = await self.get_by_id_and_user(id, user_id)
        return await self.repo.update_todo(todo, data)

    async def delete(self, id: int, user_id: int) -> None:
        todo = await self.get_by_id_and_user(id, user_id)
        await self.repo.delete_todo(todo)