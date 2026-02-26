from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository.todo import TodoRepository
from app.services.todo import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.core.dependecies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["todos"])

# (response model or annotation)
@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(TodoRepository(session))
    return await service.get_all_by_user(current_user.id)

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int, session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(TodoRepository(session))
    return await service.get_by_id_and_user(todo_id, current_user.id)

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(TodoRepository(session))
    return await service.create(todo, current_user.id)

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    data: TodoUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(TodoRepository(session))
    return await service.update(todo_id, data, current_user.id)

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(TodoRepository(session))
    return await service.delete(todo_id, current_user.id)