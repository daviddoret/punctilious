import logging
import typing

# import warnings

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


def prettify_kwargs(**kwargs) -> str:
    return '\n\t'.join(f'{key}: {force_str(o=value)}' for key, value in kwargs)


def log_info(msg: str, **kwargs):
    global logger
    pretty_msg: str = f'{msg}{prettify_kwargs(**kwargs)}'
    logger.info(pretty_msg)
    print(pretty_msg, flush=True)


def log_debug(msg: str, **kwargs):
    global logger
    pretty_msg: str = f'{msg}{prettify_kwargs(**kwargs)}'
    logger.debug(pretty_msg)
    print(pretty_msg, flush=True)


class ApplicativeException(Exception):
    def __init__(self, code: str | None = None, msg: str | None = None, **kwargs):
        self.code: str = code
        self.msg: str = msg
        self.kwargs: dict[str, typing.Any] = kwargs
        super().__init__(msg)
        log_error(e=self)

    def __str__(self) -> str:
        report: str = f'Error {self.code}: ' if self.code is not None else f'Error: '
        report: str = f'{report}{self.msg}'
        return report

    def __repr__(self) -> str:
        return self.__str__()


def log_error(e: ApplicativeException):
    global logger
    logger.error(str(e))
    print(f'{e}', flush=True)
