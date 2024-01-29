"""A wrapper module for logging, debugging, Exceptions management, warnings, etc."""

import logging


class Logger:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Logger, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        # Create a logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create a file handler and set the formatter
        file_handler = logging.FileHandler('punctilious.log', mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Create a console handler and set the formatter
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def debug(self, msg: str):
        self._logger.debug(msg=msg)

    def error(self, msg: str):
        self._logger.error(msg=msg)
        raise Exception(msg)

    def info(self, msg: str):
        self._logger.info(msg=msg)

    def warning(self, msg: str):
        self._logger.warning(msg=msg)
        warning(msg=msg)


logger = Logger()


def debug(msg: str):
    logger.debug(msg=msg)


def error(msg: str):
    logger.error(msg=msg)


def info(msg: str):
    logger.info(msg=msg)


def warning(msg: str):
    logger.warning(msg=msg)