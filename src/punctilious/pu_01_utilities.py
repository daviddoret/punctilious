"""Miscellaneous utility functions.

"""

# special features
from __future__ import annotations

# external modules
import io
import yaml
import importlib.resources
import logging
import sys
import jinja2


def get_yaml_from_package(path: str, resource: str) -> dict:
    """Import a yaml file from a package.

    This method is called when processing imports with `source_type: python_package_resources`.

    :param path: A python importlib.resources.files folder, e.g. `data.operators`.
    :param resource: A yaml filename, e.g. `operators_1.yaml`.
    :return:
    """
    package_path = importlib.resources.files(path).joinpath(resource)
    with importlib.resources.as_file(package_path) as file_path:
        with open(file_path, 'r') as file:
            file: io.TextIOBase
            d: dict = yaml.safe_load(file)
            return d


def get_jinja2_template_from_package(path: str, resource: str) -> jinja2.Template:
    """Import a jinja2 template from a package.

    This method is called when processing imports with `source_type: python_package_resources`.

    :param path: A python importlib.resources.files folder, e.g. `data.operators`.
    :param resource: A jinja2 template filename, e.g. `operators_1_representations.jinja2`.
    :return:
    """
    package_path = importlib.resources.files(path).joinpath(resource)
    with importlib.resources.as_file(package_path) as file_path:
        with open(file_path, 'r') as file:
            file: io.TextIOBase
            template: str = file.read()
            template: jinja2.Template = jinja2.Template(template)
            return template


class Logger:
    # __slots__ = ('_native_logger')
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            self._native_logger = logging.getLogger('punctilious')
            self._native_logger.setLevel(logging.DEBUG)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.flush = lambda: sys.stdout.flush()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            self._native_logger.addHandler(stream_handler)
            self.__class__._singleton_initialized = True
            get_logger().debug(
                f'Logger singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(Logger, cls).__new__(cls)
        return cls._singleton

    def debug(self, msg: str):
        self._native_logger.debug(msg)

    def exception(self, msg: str):
        self._native_logger.exception(msg)

    def info(self, msg: str):
        self._native_logger.info(msg)

    def warning(self, msg: str):
        self._native_logger.warning(msg)


def get_logger():
    return Logger()


def kwargs_to_str(**kwargs) -> str:
    return '\n'.join(f'`{str(key)}`: ({type(value).__name__}) `{str(value)}`' for key, value in kwargs.items())


def debug(msg: str, **kwargs):
    get_logger().debug(msg + kwargs_to_str(**kwargs))


def exception(msg: str, **kwargs):
    get_logger().exception(msg + kwargs_to_str(**kwargs))


def warning(msg: str, **kwargs):
    get_logger().warning(msg + kwargs_to_str(**kwargs))


def info(msg: str, **kwargs):
    get_logger().info(msg + kwargs_to_str(**kwargs))


class PunctiliousError(Exception):
    def __init__(self, msg: str, **kwargs):
        self._msg: str = msg
        self._kwargs = kwargs
        self._description: str = msg + kwargs_to_str(**kwargs)
        exception(msg=msg, **kwargs)
        super().__init__()

    @property
    def description(self) -> str:
        return self._description

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def msg(self) -> str:
        return self._msg
