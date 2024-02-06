"""A wrapper module for logging, debugging, Exceptions management, warnings, etc."""

import logging


def force_kwargs_to_string(**kwargs) -> str:
    output = ''
    for k, v in kwargs.items():
        try:
            k = str(k)
            v = str(v)
            if output == '':
                output = output + ', '
            output = output + f'{k}: {v}'
        except Exception as e:
            output = output + f'{k}: {id(v)}'
    return output


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

    def debug(self, msg: str, **kwargs):
        self._logger.debug(msg=msg + '. ' + force_kwargs_to_string(kwargs=kwargs))

    def error(self, msg: str, **kwargs):
        self._logger.error(msg=msg + '. ' + force_kwargs_to_string(kwargs=kwargs))
        raise Exception(msg)

    def info(self, msg: str, **kwargs):
        self._logger.info(msg=msg + '. ' + force_kwargs_to_string(kwargs=kwargs))

    def warning(self, msg: str, **kwargs):
        self._logger.warning(msg=msg + '. ' + force_kwargs_to_string(kwargs=kwargs))
        warning(msg=msg)


logger = Logger()


def debug(msg: str, **kwargs):
    logger.debug(msg=msg, **kwargs)


def error(msg: str, **kwargs):
    logger.error(msg=msg, **kwargs)


def info(msg: str, **kwargs):
    logger.info(msg=msg, **kwargs)


def warning(msg: str, **kwargs):
    logger.warning(msg=msg, **kwargs)
