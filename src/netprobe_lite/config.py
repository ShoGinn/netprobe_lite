import os
from enum import Enum

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(str, Enum):
    """Enumeration representing the different application environments.

    Attributes:
        local (str): Local development environment.
        test (str): Testing environment.
        dev (str): Development environment.
        qa (str): Quality assurance environment.
        stage (str): Staging environment.
        prod (str): Production environment.
    """

    local = "local"
    test = "test"
    dev = "dev"
    qa = "qa"
    stage = "stage"
    prod = "prod"


class LogLevel(str, Enum):
    """Represents the log levels for logging messages.

    The available log levels are:
    - trace: For very detailed logging, typically used for debugging purposes.
    - debug: For debugging information.
    - info: For general information.
    - success: For successful operations.
    - warning: For warnings that may indicate potential issues.
    - error: For errors that occurred but did not prevent the program from continuing.
    - critical: For critical errors that may cause the program to terminate.

    Each log level is represented by a string value.
    """

    trace = "TRACE"
    debug = "DEBUG"
    info = "INFO"
    success = "SUCCESS"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


class ConfigSpeedTest(BaseModel):
    interval: int = 937
    enabled: bool = False


class ConfigNetProbe(BaseModel):
    interval: int = 30
    count: int = 50
    sites: list[str] = ["google.com", "facebook.com", "twitter.com", "youtube.com", "amazon.com"]

    dns_test_site: str = "google.com"

    DNS_NAMESERVER_1: str = "Google_DNS"
    DNS_NAMESERVER_1_IP: str = "8.8.8.8"
    DNS_NAMESERVER_2: str = "Quad9_DNS"
    DNS_NAMESERVER_2_IP: str = "9.9.9.9"
    DNS_NAMESERVER_3: str = "Cloudflare_DNS"
    DNS_NAMESERVER_3_IP: str = "1.1.1.1"
    DNS_NAMESERVER_4: str = "My_DNS_Server"
    DNS_NAMESERVER_4_IP: str = "8.8.8.8"

    nameservers: list[tuple[str, str]] = [
        (DNS_NAMESERVER_1, DNS_NAMESERVER_1_IP),
        (DNS_NAMESERVER_2, DNS_NAMESERVER_2_IP),
        (DNS_NAMESERVER_3, DNS_NAMESERVER_3_IP),
        (DNS_NAMESERVER_4, DNS_NAMESERVER_4_IP),
    ]


class ConfigRedis(BaseModel):
    url: str = "netprobe-redis"
    port: str = "6379"
    password: str = "password"


class ConfigPresentation(BaseModel):
    port: int = 49500
    interface: str = "0.0.0.0"
    weight_loss: float = 0.6
    weight_latency: float = 0.15
    weight_jitter: float = 0.2
    weight_dns_latency: float = 0.05
    threshold_loss: int = 5
    threshold_latency: int = 100
    threshold_jitter: int = 30
    threshold_dns_latency: int = 100


class Settings(BaseSettings):
    """Represents the settings for the x2webhook application."""

    model_config = SettingsConfigDict(env_prefix="NETPROBE_", env_nested_delimiter="__")
    app_env: AppEnv = AppEnv.local
    log_level: LogLevel = LogLevel.debug

    net_probe: ConfigNetProbe = ConfigNetProbe()
    redis: ConfigRedis = ConfigRedis()
    presentation: ConfigPresentation = ConfigPresentation()
    speed_test: ConfigSpeedTest = ConfigSpeedTest()


def get_config() -> Settings:
    """Return the configuration settings.

    Returns:
        Settings: An instance of the Settings class representing the configuration.
    """
    env_file = None if "PYTEST_CURRENT_TEST" in os.environ else ".env"
    env_file_encoding = None if "PYTEST_CURRENT_TEST" in os.environ else "utf-8"
    return Settings(_env_file=env_file, _env_file_encoding=env_file_encoding)  # type: ignore[call-arg]
