import asyncio
import time

from aioredis import create_redis
from functional.settings import settings


async def main() -> bool:
    try:
        redis = await create_redis(
            (settings.redis_host, settings.redis_port)
        )

    except ConnectionRefusedError:
        return False

    redis.close()
    await redis.wait_closed()
    return True


while True:
    res = asyncio.run(main())
    if res:
        break
    print('could not connect to redis')
    time.sleep(1)
