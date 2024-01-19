"""A wrapper module for logging, debugging, Exceptions management, warnings, etc."""

import logging

logging.basicConfig(level=logging.INFO)


def debug(msg: str):
    logging.debug(msg=msg)


def error(msg: str):
    logging.error(msg=msg)
    raise Exception(msg)


def warning(msg: str):
    logging.warning(msg=msg)
    warning(msg=msg)
