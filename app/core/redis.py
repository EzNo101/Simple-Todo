import redis.asyncio as aioredis

# function for create Redis client
async def get_redis():
    # create client (connection to the Redis)
    redis = aioredis.from_url("redis://localhost")
    return redis