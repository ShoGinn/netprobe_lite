# __main__.py

import argparse

from loguru import logger

from netprobe_lite import __package_name__, __version__
from netprobe_lite.config import get_config
from netprobe_lite.logging.logging import setup_logger
from netprobe_lite.netprobe import netprobe_service
from netprobe_lite.presentation import start as presentation_service
from netprobe_lite.speedtest import speedtest_service


def main() -> None:
    settings = get_config()
    setup_logger()
    logger.info(f"Starting {__package_name__} version {__version__}")

    parser = argparse.ArgumentParser(description="Run netprobe services.")
    parser.add_argument("--netprobe", action="store_true", help="Run the netprobe service")
    parser.add_argument("--speedtest", action="store_true", help="Run the speedtest service")
    parser.add_argument("--presentation", action="store_true", help="Run the presentation service")

    args = parser.parse_args()

    if args.netprobe:
        netprobe_service(config=settings)

    if args.speedtest:
        speedtest_service(config=settings)

    if args.presentation:
        presentation_service(config=settings)


if __name__ == "__main__":
    main()
