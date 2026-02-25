from fastapi import HTTPException

from app.repository.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password, create_access_token

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        existing_user = await self.repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(data.password)
        return await self.repo.create_user(data, hashed_password)

    async def get_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def login(self, email: str, password: str) -> str: # will return token
        user = await self.get_by_email(email)
        verify = verify_password(password, user.hashed_password)
        if not verify:
            raise HTTPException(status_code=401, detail="Incorrect password")
        return create_access_token(user.id)
