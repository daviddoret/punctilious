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

    def error(self, msg: str, e: Exception):
        self._native_logger.error(msg, exc_info=e)

    def info(self, msg: str):
        self._native_logger.info(msg)

    def warning(self, msg: str):
        self._native_logger.warning(msg)


def get_logger():
    return Logger()


def kwargs_to_str(**kwargs) -> str:
    return '\n\t'.join(
        f'`{coerce_to_str(key)}`: ({type(value).__name__}) `{str(value)}`' for key, value in kwargs.items())


def coerce_to_str(o: object) -> str:
    try:
        return str(o)
    except:
        pass
    try:
        return repr(o)
    except:
        pass
    try:
        return f'python-object-{str(id(o))}'
    except:
        pass
    return '[no string representation available]'


def friendly_report(title: str, report: str, **kwargs) -> str:
    if report is not None:
        report: str = f'\n\t{report}'
    else:
        report: str = ''
    if len(kwargs) > 0:
        kwargs: str = f'\n\t{kwargs_to_str(**kwargs)}'
    else:
        kwargs = ''
    return f'{title}{report}{kwargs}'


def debug(title: str, details: str, **kwargs):
    get_logger().debug(friendly_report(title=title, report=details, **kwargs))


def _error(title: str, details: str, exception: Exception, **kwargs):
    """Internal function. Called internally by PunctiliousError.__init__."""
    get_logger().error(friendly_report(title=title, report=details, **kwargs), e=exception)


def warning(title: str, details: str, **kwargs):
    get_logger().warning(friendly_report(title=title, report=details, **kwargs))


def info(title: str, details: str, **kwargs):
    get_logger().info(friendly_report(title=title, report=details, **kwargs))


class PunctiliousError(Exception):
    def __init__(self, title: str, details: str | None = None, **kwargs):
        self._title: str = title
        self._details: str = details
        self._kwargs = kwargs
        self._friendly_report: str = 'ERROR: ' + friendly_report(title=title, report=details, **kwargs)
        super().__init__(self.friendly_report)
        # _error(title=title, details=details, exception=self, **kwargs)

    def __repr__(self):
        return self.friendly_report

    def __str__(self):
        return self.friendly_report

    @property
    def friendly_report(self) -> str:
        return self._friendly_report

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def title(self) -> str:
        return self._title
