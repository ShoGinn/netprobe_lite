# Netprobe Service

import json
import time

from netprobe_lite.config import Config_Netprobe
from netprobe_lite.helpers.network_helper import NetworkCollector
from netprobe_lite.helpers.redis_helper import RedisConnect
from loguru import logger


def netprobe_service():
    # Global Variables

    probe_interval = Config_Netprobe.probe_interval
    probe_count = Config_Netprobe.probe_count
    sites = Config_Netprobe.sites
    dns_test_site = Config_Netprobe.dns_test_site
    nameservers_external = Config_Netprobe.nameservers

    collector = NetworkCollector(
        sites, probe_count, dns_test_site, nameservers_external
    )

    # Logging Config

    while True:
        try:
            stats = collector.collect()

        except Exception as e:
            print("Error testing network")
            logger.error("Error testing network")
            logger.error(e)
            continue

        # Connect to Redis

        try:
            cache = RedisConnect()

            # Save Data to Redis

            cache_interval = (
                probe_interval + 15
            )  # Set the redis cache TTL slightly longer than the probe interval

            cache.redis_write("netprobe", json.dumps(stats), cache_interval)

            # logger.info(f"Stats successfully written to Redis from device ID for Netprobe")

        except Exception as e:
            logger.error("Could not connect to Redis")
            logger.error(e)

        time.sleep(probe_interval)


def main():
    netprobe_service()


if __name__ == "__main__":
    main()
