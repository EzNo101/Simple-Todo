from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(session))
    return await service.register(user)

@router.post("/login", response_model=Token, status_code=200)
async def login(data: UserLogin, session: AsyncSession = Depends(get_db)):
    service = UserService(UserRepository(session))
    token = await service.login(data.email, data.password)
    return {"access_token": token, "token_type": "bearer"}