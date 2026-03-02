import time
from fastapi import FastAPI, Request

from app.api import router
from app.core.redis import get_redis

app = FastAPI()

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} - {duration:.2f}ms")
    return response

app.include_router(router)

@app.router.post("/redis-test")
async def redis_test():
    redis = await get_redis()
    await redis.set("test", "hello")
    return await redis.get("test")