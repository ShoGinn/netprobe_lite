# Network tests
import subprocess
import json
from threading import Thread
import dns.resolver
import speedtest  # type: ignore # Speedtest is not typed


class NetworkCollector(object):  # Main network collection class
    def __init__(self, sites, count, dns_test_site, nameservers_external):
        self.sites = sites  # List of sites to ping
        self.count = str(count)  # Number of pings
        self.stats = []  # List of stat dicts
        self.dns_stats = []  # List of stat dicts
        self.dns_test_site = dns_test_site  # Site used to test DNS response times
        self.nameservers = []
        self.nameservers = nameservers_external

    def ping_test(self, count, site):
        ping = subprocess.getoutput(
            f"ping -n -i 0.1 -c {count} {site} | grep 'rtt\\|loss'"
        )

        try:
            loss = ping.split(" ")[5].strip("%")
            latency = ping.split("/")[4]
            jitter = ping.split("/")[6].split(" ")[0]

            net_data = {
                "site": site,
                "latency": latency,
                "loss": loss,
                "jitter": jitter,
            }

            self.stats.append(net_data)

        except Exception as e:
            print(f"Error pinging {site} - {e}")
            return False

        return True

    def dns_test(self, site, name_server):
        my_resolver = dns.resolver.Resolver()

        server = [name_server[1]]
        try:
            my_resolver.nameservers = server
            my_resolver.timeout = 10

            answers = my_resolver.query(site, "A")

            dns_latency = round(answers.response.time * 1000, 2)

            dns_data = {
                "nameserver": name_server[0],
                "nameserver_ip": name_server[1],
                "latency": dns_latency,
            }

            self.dns_stats.append(dns_data)

        except Exception as e:
            print(f"Error performing DNS resolution on {name_server}")
            print(e)

            dns_data = {
                "nameserver": name_server[0],
                "nameserver_ip": name_server[1],
                "latency": 5000,
            }

            self.dns_stats.append(dns_data)

        return True

    def collect(self):
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


class Netprobe_Speedtest(object):  # Speed test class
    def __init__(self):
        self.speedtest_stats = {"download": None, "upload": None}

    def netprobe_speedtest(self):
        s = speedtest.Speedtest()
        s.get_best_server()
        download = s.download()
        upload = s.upload()

        self.speedtest_stats = {"download": download, "upload": upload}

    def collect(self):
        self.speedtest_stats = {"download": None, "upload": None}
        self.netprobe_speedtest()

        return json.dumps({"speed_stats": self.speedtest_stats})
