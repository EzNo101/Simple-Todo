from fastapi import HTTPException

from app.repository.todo import TodoRepository
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services.cache import CacheService
from app.core.config import settings


class TodoService:
    def __init__(self, repo: TodoRepository, cache: CacheService):
        self.repo = repo
        self.cache = cache

    async def get_all(self) -> list[Todo]:
        return await self.repo.get_all()
    
    async def get_by_id(self, id: int) -> Todo:
        todo = await self.repo.get_by_id(id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return todo

    async def get_all_by_user(self, user_id: int) -> list[Todo]:
        cached_key = f"user:{user_id}:todos"
        
        cached = await self.cache.get(cached_key)
        if cached:
            return [TodoResponse(**todo) for todo in cached]
        
        todos =  await self.repo.get_all_by_user(user_id)
        todos_data = [TodoResponse.model_validate(todo).model_dump() for todo in todos]
        await self.cache.set(cached_key, todos_data, ttl=settings.CACHE_TTL)
        return [TodoResponse.model_validate(todo) for todo in todos]
    
    async def get_by_id_and_user(self, todo_id: int, user_id: int) -> Todo:
        cache_key = f"user:{user_id}:todo:{todo_id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return TodoResponse(**cached)
        
        todo = await self.repo.get_by_id_and_user(todo_id, user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        todo_data = TodoResponse.model_validate(todo).model_dump()
        await self.cache.set(cache_key, todo_data, ttl=settings.CACHE_TTL)
        return TodoResponse.model_validate(todo)

    async def create(self, data: TodoCreate, user_id: int) -> Todo:
        todo = await self.repo.create_todo(data, user_id)
        
        # cache invalidation
        await self.cache.delete(f"user:{user_id}:todos")
        return todo
    
    async def update(self, id: int, data: TodoUpdate, user_id: int) -> Todo:
        todo = await self.repo.get_by_id_and_user(id, user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        updated_todo = await self.repo.update_todo(todo, data)        
        await self.cache.delete(f"user:{user_id}:todos")
        await self.cache.delete(f"user:{user_id}:todo:{id}")
        return updated_todo

    async def delete(self, id: int, user_id: int) -> None:
        todo = await self.repo.get_by_id_and_user(id, user_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Task not found")
        await self.repo.delete_todo(todo)

        await self.cache.delete(f"user:{user_id}:todos")
        await self.cache.delete(f"user:{user_id}:todo:{id}")