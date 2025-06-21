from aioredis import Redis

from app.config import config


# Redis connection dependency
async def get_redis():
    redis_client = Redis(
        host=config.redis.REDIS_HOST,
        port=config.redis.REDIS_PORT,
        decode_responses=True,
        password=config.redis.REDIS_PASSWORD,
    )
    try:
        yield redis_client  # Provide Redis instance to FastAPI
    finally:
        await redis_client.close()  # Ensure proper cleanup
