from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository.todo import TodoRepository
from app.services.todo import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


router = APIRouter(prefix="/todos", tags=["todos"])

# (response model or annotation)
@router.get("/", response_model=list[TodoResponse])
async def get_todos(session: AsyncSession = Depends(get_db)):
    service = TodoService(TodoRepository(session))
    return await service.get_all()

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_db)):
    service = TodoService(TodoRepository(session))
    return await service.get_by_id(todo_id)

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, session: AsyncSession = Depends(get_db)):
    service = TodoService(TodoRepository(session))
    return await service.create(todo)

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, data: TodoUpdate, session: AsyncSession = Depends(get_db)):
    service = TodoService(TodoRepository(session))
    return await service.update(todo_id, data)

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_db)):
    service = TodoService(TodoRepository(session))
    return await service.delete(todo_id)