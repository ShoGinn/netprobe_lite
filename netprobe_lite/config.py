import contextlib
import os
from typing import ClassVar

from dotenv import load_dotenv

from netprobe_lite.logging.logging import setup_logger

# Load configs from env

with contextlib.suppress(IOError):
    load_dotenv()

app_env = os.getenv("APP_ENV", "local")
app_log_level = os.getenv("NETPROBE_LOG_LEVEL", "DEBUG")

setup_logger(app_env=app_env, app_log_level=app_log_level)


class ConfigNetProbe:
    probe_interval = int(os.getenv("PROBE_INTERVAL", "30"))
    probe_count = int(os.getenv("PROBE_COUNT", "50"))
    sites = os.getenv("SITES", "google.com,facebook.com,twitter.com,youtube.com,amazon.com").split(",")
    dns_test_site = os.getenv("DNS_TEST_SITE", "google.com")
    speedtest_enabled = os.getenv("SPEEDTEST_ENABLED", "False").lower() in (
        "true",
        "1",
        "t",
    )
    speedtest_interval = int(os.getenv("SPEEDTEST_INTERVAL", "937"))

    DNS_NAMESERVER_1 = os.getenv("DNS_NAMESERVER_1", "Google_DNS")
    DNS_NAMESERVER_1_IP = os.getenv("DNS_NAMESERVER_1_IP", "8.8.8.8")
    DNS_NAMESERVER_2 = os.getenv("DNS_NAMESERVER_2", "Quad9_DNS")
    DNS_NAMESERVER_2_IP = os.getenv("DNS_NAMESERVER_2_IP", "9.9.9.9")
    DNS_NAMESERVER_3 = os.getenv("DNS_NAMESERVER_3", "Cloudflare_DNS")
    DNS_NAMESERVER_3_IP = os.getenv("DNS_NAMESERVER_3_IP", "1.1.1.1")
    DNS_NAMESERVER_4 = os.getenv("DNS_NAMESERVER_4", "My_DNS_Server")
    DNS_NAMESERVER_4_IP = os.getenv("DNS_NAMESERVER_4_IP", "8.8.8.8")

    nameservers: ClassVar[list[tuple[str, str]]] = [
        (DNS_NAMESERVER_1, DNS_NAMESERVER_1_IP),
        (DNS_NAMESERVER_2, DNS_NAMESERVER_2_IP),
        (DNS_NAMESERVER_3, DNS_NAMESERVER_3_IP),
        (DNS_NAMESERVER_4, DNS_NAMESERVER_4_IP),
    ]


class ConfigRedis:
    redis_url = os.getenv("REDIS_URL", "netprobe-redis")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis_password = os.getenv("REDIS_PASSWORD", "password")


class ConfigPresentation:
    presentation_port = int(os.getenv("PRESENTATION_PORT", "49500"))
    presentation_interface = os.getenv("PRESENTATION_INTERFACE", "0.0.0.0")

    weight_loss = float(os.getenv("WEIGHT_LOSS", "0.6"))
    weight_latency = float(os.getenv("WEIGHT_LATENCY", "0.15"))
    weight_jitter = float(os.getenv("WEIGHT_JITTER", "0.2"))
    weight_dns_latency = float(os.getenv("WEIGHT_DNS_LATENCY", "0.05"))

    threshold_loss = int(os.getenv("THRESHOLD_LOSS", "5"))
    threshold_latency = int(os.getenv("THRESHOLD_LATENCY", "100"))
    threshold_jitter = int(os.getenv("THRESHOLD_JITTER", "30"))
    threshold_dns_latency = int(os.getenv("THRESHOLD_DNS_LATENCY", "100"))
