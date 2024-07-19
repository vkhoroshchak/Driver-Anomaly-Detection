import logging
import sys
from logging import Formatter, Handler, Logger


class BaseLogger:
    @staticmethod
    def get_console_handler(formatter: Formatter) -> Handler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        return console_handler

    def get_logger(self, logger_name: str) -> Logger:
        formatter = logging.Formatter(
            fmt="[%(levelname)s] %(asctime)s %(name)s.%(funcName)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(self.get_console_handler(formatter))
        return logger
