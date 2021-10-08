import logging
import os
import sys
from pathlib import Path

from loguru import logger
import json

from app.core.settings import settings

LOG_LEVEL_MAP = {
    50: 'CRITICAL',
    40: 'ERROR',
    30: 'WARNING',
    20: 'INFO',
    10: 'DEBUG',
    0: 'NOTSET',
}


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = LOG_LEVEL_MAP[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='fastApi')
        log.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class CustomizeLogger:

    @classmethod
    def make_logger(cls):
        config = cls.load_logging_config(Path(settings.logging_config_path))
        logging_config = config.get('logger')
        filepath = Path(os.path.join(logging_config.get('path'), logging_config.get('filename')))

        logger = cls.customize_logging(
            filepath,
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            logger_format=logging_config.get('format')
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        logger_format: str
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=logger_format
        )
        if settings.environment == "dev":
            logger.add(
                filepath,
                rotation=rotation,
                retention=retention,
                enqueue=True,
                backtrace=True,
                level=level.upper(),
                format=logger_format
            )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn', 'uvicorn.error', 'fastApi']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
