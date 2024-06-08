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
    print(f'{msg}')
