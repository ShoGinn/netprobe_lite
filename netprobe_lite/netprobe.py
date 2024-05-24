# Netprobe Service

import json
import time

from loguru import logger

from netprobe_lite.config import ConfigNetProbe
from netprobe_lite.helpers.network_helper import NetworkCollector
from netprobe_lite.helpers.redis_helper import RedisConnect


def netprobe_service() -> None:
    # Global Variables

    probe_interval = ConfigNetProbe.probe_interval
    probe_count = ConfigNetProbe.probe_count
    sites = ConfigNetProbe.sites
    dns_test_site = ConfigNetProbe.dns_test_site
    nameservers_external = ConfigNetProbe.nameservers

    collector = NetworkCollector(sites, probe_count, dns_test_site, nameservers_external)

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
            cache = RedisConnect()

            # Save Data to Redis

            cache_interval = probe_interval + 15  # Set the redis cache TTL slightly longer than the probe interval

            cache.redis_write("netprobe", json.dumps(stats), cache_interval)

        except Exception as e:
            logger.error("Could not connect to Redis")
            logger.error(e)

        time.sleep(probe_interval)


def main() -> None:
    netprobe_service()


if __name__ == "__main__":
    main()
