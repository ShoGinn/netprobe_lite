# Netprobe Service

import json
import time

from netprobe_lite.config import Config_Netprobe
from netprobe_lite.helpers.network_helper import Netprobe_Speedtest
from netprobe_lite.helpers.redis_helper import RedisConnect
from loguru import logger


def speedtest_service():
    # Global Variables

    speedtest_enabled = Config_Netprobe.speedtest_enabled
    if not speedtest_enabled:
        logger.info("Speedtest is not enabled")
        while True:
            time.sleep(60)  # Sleep for a minute before checking again

    if speedtest_enabled is True:
        collector = Netprobe_Speedtest()

        # Logging Config
        speedtest_interval = Config_Netprobe.speedtest_interval

        while True:
            try:
                stats = collector.collect()

            except Exception as e:
                print("Error running speedtest")
                logger.error("Error running speedtest")
                logger.error(e)
                time.sleep(speedtest_interval)  # Pause before retrying
                continue

            # Connect to Redis

            try:
                cache = RedisConnect()

                # Save Data to Redis

                cache_interval = (
                    speedtest_interval * 2
                )  # Set the redis cache 2x longer than the speedtest interval

                cache.redis_write("speedtest", json.dumps(stats), cache_interval)

                logger.debug(
                    f"Stats successfully written to Redis for Speed Test, {stats}"
                )

            except Exception as e:
                logger.error("Could not connect to Redis")
                logger.error(e)

            time.sleep(speedtest_interval)


def main():
    speedtest_service()


if __name__ == "__main__":
    main()
