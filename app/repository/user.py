from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(self, data: UserCreate, hashed_password: str) -> User:
        user = User(**data.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update_user(self, user: User, data: UserUpdate, hashed_password: str | None = None) -> User:
        for field, value in data.model_dump(exclude_none=True, exclude={"password"}).items():
            setattr(user, field, value)
        if hashed_password:
            user.hashed_password = hashed_password
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()