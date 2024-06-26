import logging
import typing
import warnings

logger = logging.getLogger(__name__)


def force_str(o: object):
    if isinstance(o, typing.Dict):
        '(' + ', '.join(f'{force_str(key)}: {force_str(value)}' for key, value in o.items()) + ')'
    elif isinstance(o, typing.Iterable):
        '(' + ', '.join(f'{force_str(element)}' for element in o) + ')'
    else:
        try:
            return str(o)
        except Exception:
            return f'object-{id(o)} of type {str(type(o))}'


def log_info(msg: str, **kwargs):
    global logger
    logger.info(msg)
    # warnings.warn('{msg} :{force_str(kwargs)}.')
    print(f'{msg}', flush=True)


def log_debug(msg: str, **kwargs):
    global logger
    logger.debug(msg)
    # warnings.warn('{msg} :{force_str(kwargs)}.')
    print(f'{msg}', flush=True)


class ApplicativeException(Exception):
    def __init__(self, code: str | None = None, msg: str | None = None, **kwargs):
        self.code: str = code
        self.msg: str = msg
        self.kwargs: tuple[tuple, ...] = kwargs
        super().__init__(msg)
        log_error(e=self)

    def __str__(self) -> str:
        report: str = f'Error {self.code}: ' if self.code is not None else f'Error: '
        report: str = f'{report}{self.msg}'
        for key, value in self.kwargs:
            kwarg: str = f'\n\t{key}: {force_str(o=value)}'
            report: str = f'{report}{kwarg}'
        return report

    def __repr__(self):
        return self.__str__()


def log_error(e: ApplicativeException):
    global logger
    logger.error(e)
    print(f'{e}', flush=True)
