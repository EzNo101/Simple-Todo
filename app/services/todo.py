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

    async def create(self, data: TodoCreate) -> Todo:
        return await self.repo.create_todo(data)
    
    async def update(self, id: int, data: TodoUpdate) -> Todo:
        todo = await self.get_by_id(id)
        return await self.repo.update_todo(todo, data)

    async def delete(self, id: int) -> None:
        todo = await self.get_by_id(id)
        await self.repo.delete_todo(todo)