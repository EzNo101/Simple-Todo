from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

# repository works only with session(not with db)
class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Todo]:
        result = await self.session.execute(select(Todo))
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Todo | None: # sqlalchemy will return object for python
        result = await self.session.execute(select(Todo).where(Todo.id == id))
        return result.scalar_one_or_none()
    
    async def create_todo(self, data: TodoCreate) -> Todo:
        todo = Todo(**data.model_dump()) # in session we can transfer only sqlalchemy model (we create it from pydantic schema)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
    
    async def update_todo(self, todo: Todo, data: TodoUpdate) -> Todo:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(todo, field, value) # dynamically set items which are not None
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
    
    async def delete_todo(self, todo: Todo) -> None:
        await self.session.delete(todo)
        await self.session.commit()