# Network tests
import json
import re
import subprocess
from threading import Thread

import dns.resolver
import speedtest  # type: ignore[import-untyped]
from loguru import logger


class NetworkCollector:  # Main network collection class
    def __init__(self, sites: list[str], count: int | str, dns_test_site: str, nameservers_external: list) -> None:
        self.sites = sites  # List of sites to ping
        self.count = str(count)  # Number of pings
        self.stats: list[dict[str, str | float | int]] = []  # List of stat dicts
        self.dns_stats: list[dict[str, str | float | int]] = []  # List of stat dicts
        self.dns_test_site = dns_test_site  # Site used to test DNS response times
        self.nameservers = []
        self.nameservers = nameservers_external

    def ping_test(self, count: int, site: str) -> bool:
        ping = subprocess.getoutput(f"ping -n -i 0.1 -c {count} {site} | grep 'max\\|loss'")
        try:
            self.ping_parse(ping, site)
        except Exception as e:
            logger.error(f"Error pinging {site} - {e}")
            return False

        return True

    def ping_parse(self, ping: str, site: str) -> None:
        loss_match = re.search(r"(\d+(\.\d+)?)%? packet loss", ping)
        loss = loss_match[1] if loss_match else 5000.0

        latency_jitter_match = re.search(r"([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms", ping)
        latency = latency_jitter_match[3] if latency_jitter_match else 5000.0
        jitter = latency_jitter_match[4] if latency_jitter_match else 5000.0

        net_data = {
            "site": site,
            "latency": latency,
            "loss": loss,
            "jitter": jitter,
        }
        logger.debug(f"Netprobe: {net_data}")
        self.stats.append(net_data)

    def dns_test(self, site: str, name_server: str) -> bool:
        my_resolver = dns.resolver.Resolver()

        server = [name_server[1]]
        try:
            my_resolver.nameservers = server
            my_resolver.timeout = 10

            answers = my_resolver.query(site, "A")

            dns_latency = round(answers.response.time * 1000, 2)

            dns_data: dict[str, str | float | int] = {
                "nameserver": name_server[0],
                "nameserver_ip": name_server[1],
                "latency": dns_latency,
            }

            self.dns_stats.append(dns_data)

        except Exception as e:
            logger.error(f"Error performing DNS resolution on {name_server}")
            logger.error(e)

            dns_data = {
                "nameserver": name_server[0],
                "nameserver_ip": name_server[1],
                "latency": 5000.0,
            }

            self.dns_stats.append(dns_data)

        return True

    def collect(self) -> str:
        # Empty previous results
        self.stats = []
        self.dns_stats = []

        # Create threads, start them
        threads = []

        for item in self.sites:
            t = Thread(
                target=self.ping_test,
                args=(
                    self.count,
                    item,
                ),
            )
            threads.append(t)
            t.start()

        # Wait for threads to complete
        for t in threads:
            t.join()

        # Create threads, start them
        threads = []
        for item in self.nameservers:
            s = Thread(
                target=self.dns_test,
                args=(
                    self.dns_test_site,
                    item,
                ),
            )
            threads.append(s)
            s.start()

        # Wait for threads to complete
        for s in threads:
            s.join()

        return json.dumps({"stats": self.stats, "dns_stats": self.dns_stats})


class NetprobeSpeedTest:  # Speed test class
    def __init__(self) -> None:
        self.speedtest_stats = {"download": None, "upload": None}

    def netprobe_speedtest(self) -> None:
        s = speedtest.Speedtest()
        s.get_best_server()
        download = s.download()
        upload = s.upload()

        self.speedtest_stats = {"download": download, "upload": upload}

    def collect(self) -> str:
        self.speedtest_stats = {"download": None, "upload": None}
        self.netprobe_speedtest()

        return json.dumps({"speed_stats": self.speedtest_stats})
