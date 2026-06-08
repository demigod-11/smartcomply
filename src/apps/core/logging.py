import logging
import sys

from loguru import logger


def _is_benign_websocket_redis_timeout(record: logging.LogRecord) -> bool:
    """Daphne logs Redis read timeouts when a WS client closes mid-poll."""
    if record.name != "daphne.server" or not record.exc_info:
        return False
    exc_type, exc_value, _ = record.exc_info
    if exc_type is None:
        return False
    name = f"{exc_type.__module__}.{exc_type.__name__}"
    if name == "redis.exceptions.TimeoutError":
        return True
    return "Timeout reading from redis" in str(exc_value)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        if record.name == "django.request" and record.levelno <= logging.WARNING:
            return
        if _is_benign_websocket_redis_timeout(record):
            return
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def configure_loguru():
    logger.remove()
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[request_id]} | {extra[actor_name]} | {message}",
        level="INFO",
        filter=lambda record: "request_id" in record["extra"],
    )
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | - | - | {message}",
        level="INFO",
        filter=lambda record: "request_id" not in record["extra"],
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
    for logger_name in ("django.request", "asyncio"):
        logging.getLogger(logger_name).setLevel(logging.ERROR)
