# Data presentation service (prometheus)

import time
from collections.abc import Iterable

from loguru import logger
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily, Metric
from prometheus_client.registry import Collector

from netprobe_lite.config import ConfigPresentation
from netprobe_lite.helpers.redis_helper import RedisConnect


class CustomCollector(Collector):
    def __init__(self) -> None:
        pass

    def collect(self) -> Iterable[Metric]:
        try:
            cache = RedisConnect()
        except Exception as e:
            logger.error("Could not connect to Redis")
            logger.error(e)
            return

        if not cache:
            return

        if results_netprobe := cache.redis_read("netprobe"):
            stats_netprobe = results_netprobe
        else:
            return

        g = GaugeMetricFamily(
            "Network_Stats",
            "Network statistics for latency and loss from the probe to the destination",
            labels=["type", "target"],
        )

        total_latency, total_loss, total_jitter = 0.0, 0.0, 0.0

        for item in stats_netprobe["stats"]:
            g.add_metric(["latency", item["site"]], item["latency"])
            g.add_metric(["loss", item["site"]], item["loss"])
            g.add_metric(["jitter", item["site"]], item["jitter"])

            total_latency += float(item["latency"])
            total_loss += float(item["loss"])
            total_jitter += float(item["jitter"])

        average_latency = total_latency / len(stats_netprobe["stats"])
        average_loss = total_loss / len(stats_netprobe["stats"])
        average_jitter = total_jitter / len(stats_netprobe["stats"])

        g.add_metric(["latency", "all"], average_latency)
        g.add_metric(["loss", "all"], average_loss)
        g.add_metric(["jitter", "all"], average_jitter)

        h = GaugeMetricFamily(
            "DNS_Stats",
            "DNS performance statistics for various DNS servers",
            labels=["server"],
        )

        my_dns_latency = 0.0
        for item in stats_netprobe["dns_stats"]:
            h.add_metric([item["nameserver"]], item["latency"])
            if item["nameserver"] == "My_DNS_Server":
                my_dns_latency = float(item["latency"])

        if results_speedtest := cache.redis_read("speedtest"):
            stats_speedtest = results_speedtest

            s = GaugeMetricFamily(
                "Speed_Stats",
                "Speedtest performance statistics from speedtest.net",
                labels=["direction"],
            )

            for key, value in stats_speedtest["speed_stats"].items():
                if value:
                    s.add_metric([key], value)

        weight_loss, weight_latency, weight_jitter, weight_dns_latency = (
            ConfigPresentation.weight_loss,
            ConfigPresentation.weight_latency,
            ConfigPresentation.weight_jitter,
            ConfigPresentation.weight_dns_latency,
        )

        threshold_loss, threshold_latency, threshold_jitter, threshold_dns_latency = (
            ConfigPresentation.threshold_loss,
            ConfigPresentation.threshold_latency,
            ConfigPresentation.threshold_jitter,
            ConfigPresentation.threshold_dns_latency,
        )

        eval_loss = min(average_loss / threshold_loss, 1)
        eval_latency = min(average_latency / threshold_latency, 1)
        eval_jitter = min(average_jitter / threshold_jitter, 1)
        eval_dns_latency = min(my_dns_latency / threshold_dns_latency, 1)

        score = 1 - (
            weight_loss * eval_loss
            + weight_jitter * eval_jitter
            + weight_latency * eval_latency
            + weight_dns_latency * eval_dns_latency
        )

        i = GaugeMetricFamily("Health_Stats", "Overall internet health function")
        i.add_metric(["health"], score)

        yield g
        yield h
        yield s
        yield i


def main() -> None:
    start_http_server(
        ConfigPresentation.presentation_port,
        addr=ConfigPresentation.presentation_interface,
    )

    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(15)


if __name__ == "__main__":
    main()
