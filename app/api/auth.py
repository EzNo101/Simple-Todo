from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.register(user)

@router.post("/login", response_model=Token, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    token = await service.login(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}