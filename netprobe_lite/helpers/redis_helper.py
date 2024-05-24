# Redis helper
#
# Functions to help read and write from Redis


import json

import redis

from netprobe_lite.config import ConfigRedis


class RedisConnect:
    def __init__(self) -> None:
        # Load global variables

        self.redis_url = ConfigRedis.redis_url
        self.redis_port = ConfigRedis.redis_port
        self.redis_password = ConfigRedis.redis_password

        self.r = redis.Redis(  # Connect to Redis
            host=self.redis_url, port=self.redis_port
        )

    def redis_read(self, key: str) -> str:  # Read data from Redis
        results = self.r.get(key)
        return str(results) if results else ""

    def redis_write(self, key: str, data: str, ttl: int) -> None:  # Write data to Redis
        self.r.set(key, json.dumps(data), ttl)
