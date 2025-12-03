import os
import sys
from loguru import logger


def setup_logging() -> None:
    log_level = os.getenv('MCP_LOG_LEVEL', 'INFO').upper()
    logger.remove()
    logger.add(sys.stderr, level=log_level, colorize=True)
