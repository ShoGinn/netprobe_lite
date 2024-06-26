# Redis helper
#
# Functions to help read and write from Redis


import json

import redis

from netprobe_lite.config import Settings


class RedisConnect:
    def __init__(self, config: Settings) -> None:
        # Load global variables

        self.redis_url = config.redis.url
        self.redis_port = config.redis.port
        self.redis_password = config.redis.password

        self.r = redis.Redis(  # Connect to Redis
            host=self.redis_url, port=self.redis_port
        )

    def redis_read(self, key: str) -> dict:  # Read data from Redis
        results = self.r.get(key)
        return json.loads(results) if results else {}  # type: ignore[no-any-return, arg-type]

    def redis_write(self, key: str, data: str, ttl: int) -> None:  # Write data to Redis
        self.r.set(key, data, ttl)
