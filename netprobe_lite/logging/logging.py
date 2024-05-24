"""Logging module provides functionality for setting up the logger for the app."""

import json
import sys

import loguru
from loguru import logger


def structured_formatter(record: "loguru.Record") -> str:
    """Format the log record in a structured way.

    Args:
        record (dict): The log record.

    Returns:
        str: The formatted log record.
        _type_: _description_
    """
    record["extra"]["__json_serialized"] = json.dumps(
        {
            "timestamp": record["time"].timestamp(),
            "level": record["level"].name,
            "message": record["message"],
            "source": f"{record['file'].path}:{record['line']}",
            "extra": record["extra"],
        }
    )

    return "{extra[__json_serialized]}\n"


def setup_logger(app_env: str = "local", app_log_level: str = "DEBUG") -> None:
    """
    Set up the logger based on the specified log level.

    Raises:
        RuntimeError: If the environment is unknown.

    """

    logger.remove()
    logger.bind().info("Setting up logger")
    # deployment mode
    if app_env == "production":
        logger.add(
            sys.stdout,
            level=app_log_level,
            format=structured_formatter,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
        # local mode ot test mode
    elif app_env == "local":
        logger.add(
            sys.stdout,
            level=app_log_level,
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | "
            "<level>{level}</level> | <cyan>{name}</cyan>"
            ":<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            " - <yellow>{message}</yellow>",
            colorize=True,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
    else:
        raise RuntimeError(f"Unknown environment: {app_env}, Exiting...")
    logger.debug(f"Logger set up for {app_env} environment. Log level: {app_log_level}")
