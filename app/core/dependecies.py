from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.security import decode_access_token
from app.services.user import UserService
from app.repository.user import UserRepository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # authorization button generates automatically because of this

async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
):
    access_token = decode_access_token(token=token)
    user_id = int(access_token["sub"])
    service = UserService(UserRepository(session))
    return await service.get_by_id(user_id)