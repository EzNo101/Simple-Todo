from fastapi import APIRouter

from app.api.todos import router as todos_router
from app.api.auth import router as auth_router

router = APIRouter()
router.include_router(todos_router)
router.include_router(auth_router)