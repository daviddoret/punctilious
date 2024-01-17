import logging

logging.basicConfig(level=logging.INFO)


def debug(msg: str):
    logging.debug(msg=msg)


def error(msg: str):
    logging.error(msg=msg)
    raise Exception(msg)
