from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.database.session import get_db
from app.core.security import decode_access_token
from app.services.user import UserService
from app.repository.user import UserRepository
from app.models.user import User
from app.core.redis import get_redis
from app.repository.todo import TodoRepository
from app.services.todo import TodoService
from app.services.cache import CacheService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # authorization button generates automatically because of this

def get_user_service(
    session: AsyncSession = Depends(get_db)
) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
) -> User:
    try:
        access_token = decode_access_token(token=token)
        user_id = int(access_token["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user

def get_cache_service(
        redis: Redis = Depends(get_redis)
) -> CacheService:
    return CacheService(redis)


def get_todo_service(
    session: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service)
) -> TodoService:
    repo = TodoRepository(session)
    return TodoService(repo, cache)