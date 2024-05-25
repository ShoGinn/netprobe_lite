# Netprobe Service

import time

from loguru import logger

from netprobe_lite.config import Settings
from netprobe_lite.helpers.network_helper import NetprobeSpeedTest
from netprobe_lite.helpers.redis_helper import RedisConnect


def speedtest_service(config: Settings) -> None:
    # Global Variables
    speedtest_enabled = config.speed_test.enabled
    if not speedtest_enabled:
        logger.info("Speedtest is not enabled")
        while True:
            time.sleep(60)  # Sleep for a minute before checking again

    if speedtest_enabled is True:
        collector = NetprobeSpeedTest()

        # Logging Config
        speedtest_interval = config.speed_test.interval

        while True:
            try:
                stats = collector.collect()

            except Exception as e:
                logger.error("Error running speedtest")
                logger.error(e)
                time.sleep(speedtest_interval)  # Pause before retrying
                continue

            # Connect to Redis

            try:
                cache = RedisConnect(config=config)

                # Save Data to Redis

                cache_interval = speedtest_interval * 2  # Set the redis cache 2x longer than the speedtest interval

                cache.redis_write("speedtest", stats, cache_interval)

                logger.debug(
                    "Stats successfully written to Redis for Speed Test",
                    extra={"stats": stats},
                )

            except Exception as e:
                logger.error("Could not connect to Redis")
                logger.error(e)

            time.sleep(speedtest_interval)
