import typing

import log


class Config:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Config, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_dictionary = dict()

    def get(self, key: str, default: typing.Optional[object] = None) -> object:
        if key not in self._internal_dictionary.keys():
            log.warning(msg=f"Config: key '{key}' not found. Use default instead.")
            return default
        else:
            return self._internal_dictionary[key]

    def set(self, key: str, value: object) -> None:
        self._internal_dictionary[key] = value


def get_config() -> Config:
    return Config()


config = get_config()
