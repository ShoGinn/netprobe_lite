# Netprobe Service

import time

from loguru import logger

from netprobe_lite.config import Settings
from netprobe_lite.helpers.network_helper import NetworkCollector
from netprobe_lite.helpers.redis_helper import RedisConnect


def netprobe_service(config: Settings) -> None:
    # Global Variables

    collector = NetworkCollector(
        config.net_probe.sites,
        config.net_probe.count,
        config.net_probe.dns_test_site,
        config.net_probe.nameservers,
    )

    # Logging Config

    while True:
        try:
            stats = collector.collect()

        except Exception as e:
            logger.error("Error testing network")
            logger.error(e)
            continue

        # Connect to Redis

        try:
            cache = RedisConnect(config=config)

            # Save Data to Redis

            cache_interval = (
                config.net_probe.interval + 15
            )  # Set the redis cache TTL slightly longer than the probe interval

            cache.redis_write("netprobe", stats, cache_interval)

        except Exception as e:
            logger.error("Could not connect to Redis")
            logger.error(e)

        time.sleep(config.net_probe.interval)
