from __future__ import annotations

import typing
import tomllib
import pathlib


class ConfigurationSettings(dict):
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(ConfigurationSettings, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self.load()

    def load(self, configuration_file_path: typing.Optional[str] = None):
        module_path: str = __file__
        module_folder: pathlib.Path = pathlib.Path(module_path).parent
        configuration_file_path: pathlib.Path = module_folder.joinpath('presentation_1.toml')
        with open(file=configuration_file_path, mode='rb') as f:
            configuration: dict[str, typing.Any] = tomllib.load(f)
            for key, value in configuration.items():
                self[key] = value


configuration_settings = ConfigurationSettings()


class Encoding:
    def __init__(self, key: str):
        self._name = key

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name


class Encodings(dict):
    """A catalog of out-of-the-box encodings."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Encodings, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        global configuration_settings
        super().__init__()
        self._latex_math = self.register(key='latex_math')
        self._unicode_extended = self.register(key='unicode_extended')
        self._unicode_limited = self.register(key='unicode_limited')
        default_encoding = configuration_settings['presentation_1']['default_encoding']
        self._default = self[default_encoding]

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, encoding: typing.Union[Encoding, str]):
        if isinstance(encoding, str):
            encoding: Encoding = self[encoding]
        self._default = encoding

    @property
    def latex_math(self):
        return self._latex_math

    def register(self, key: str):
        encoding: Encoding = Encoding(key=key)
        self[key] = encoding
        return encoding

    @property
    def unicode_extended(self):
        return self._unicode_extended

    @property
    def unicode_limited(self):
        return self._unicode_limited


encodings = Encodings()


class TypesettingMethod:
    """A renderer is a python object with the capability to represent some objects."""

    def __init__(self):
        pass

    def rep(self, o: Typesettable, encoding: Encoding, **kwargs) -> str:
        pass


class Typesettable:
    """A typesettable is a python object equipped with some renderers that can represent it."""

    def __init__(self, typesetting_method: typing.Optional[TypesettingMethod] = None):
        self._renderer: typing.Optional[TypesettingMethod] = typesetting_method

    @property
    def typesetting_method(self) -> typing.Optional[TypesettingMethod]:
        return self._renderer

    @typesetting_method.setter
    def typesetting_method(self, renderer: typing.Optional[TypesettingMethod]):
        self._renderer: typing.Optional[TypesettingMethod] = renderer

    def rep(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        if self.typesetting_method is None:
            raise Exception('no typesetting-method available, ooops')
        else:
            return self.typesetting_method.rep(o=self, **kwargs)


class Symbol(TypesettingMethod):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math: str = latex_math
        self._unicode_extended: str = unicode_extended
        self._unicode_limited: str = unicode_limited
        super().__init__()

    @property
    def latex_math(self) -> str:
        return self._latex_math

    def rep(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        if encoding is None:
            encoding: Encoding = encodings.default

        if encoding is encodings.unicode_limited:
            return self.unicode_limited
        elif encoding is encodings.unicode_extended:
            return self.unicode_extended
        elif encoding is encodings.latex_math:
            return self.latex_math
        else:
            raise ValueError('ooops')

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


class Symbols(list):
    """A catalog of out-of-the-box symbols."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Symbols, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._asterisk_operator = self.register(latex_math='\\ast', unicode_extended='∗', unicode_limited='*')
        self._close_parenthesis = self.register(latex_math='\\right)', unicode_extended=')', unicode_limited=')')
        self._collection_separator = self.register(latex_math=', ', unicode_extended=', ', unicode_limited=', ')
        self._not_sign = self.register(latex_math='\\lnot', unicode_extended='¬', unicode_limited='not')
        self._open_parenthesis = self.register(latex_math='\\left(', unicode_extended='(', unicode_limited='(')
        self._p_uppercase_serif_italic = self.register(latex_math='\\textit{P}', unicode_extended='𝑃',
                                                       unicode_limited='P')
        self._q_uppercase_serif_italic = self.register(latex_math='\\textit{Q}', unicode_extended='𝑄',
                                                       unicode_limited='Q')
        self._r_uppercase_serif_italic = self.register(latex_math='\\textit{R}', unicode_extended='𝑅',
                                                       unicode_limited='R')
        self._rightwards_arrow = self.register(latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->')
        self._space = self.register(latex_math=' ', unicode_extended=' ', unicode_limited=' ')
        self._tilde = self.register(latex_math='\\sim', unicode_extended='~', unicode_limited='~')

    @property
    def asterisk_operator(self) -> Symbol:
        return self._asterisk_operator

    @property
    def close_parenthesis(self) -> Symbol:
        return self._close_parenthesis

    @property
    def collection_separator(self) -> Symbol:
        return self._collection_separator

    @property
    def not_sign(self) -> Symbol:
        return self._not_sign

    @property
    def open_parenthesis(self) -> Symbol:
        return self._open_parenthesis

    @property
    def p_uppercase_serif_italic(self) -> Symbol:
        return self._p_uppercase_serif_italic

    @property
    def q_uppercase_serif_italic(self) -> Symbol:
        return self._q_uppercase_serif_italic

    def register(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        symbol = Symbol(latex_math=latex_math, unicode_extended=unicode_extended, unicode_limited=unicode_limited)
        self.append(symbol)
        return symbol

    @property
    def r_uppercase_serif_italic(self) -> Symbol:
        return self._r_uppercase_serif_italic

    @property
    def rightwards_arrow(self) -> Symbol:
        return self._rightwards_arrow

    @property
    def space(self) -> Symbol:
        return self._space

    @property
    def tilde(self) -> Symbol:
        return self._tilde


symbols = Symbols()


class IndexedSymbol(TypesettingMethod):
    pass
