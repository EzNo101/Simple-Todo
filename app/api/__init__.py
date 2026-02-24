from fastapi import APIRouter

from app.api.todos import router as todos_router

router = APIRouter()
router.include_router(todos_router)