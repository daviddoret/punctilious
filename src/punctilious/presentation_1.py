from __future__ import annotations

import abc
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
        """TODO: Provide support for reloading configuration, and loading configuration from a particular path.
        """
        module_path: str = __file__
        module_folder: pathlib.Path = pathlib.Path(module_path).parent
        configuration_file_path: pathlib.Path = module_folder.joinpath('presentation_1.toml')
        with open(file=configuration_file_path, mode='rb') as f:
            configuration: dict[str, typing.Any] = tomllib.load(f)
            for key, value in configuration.items():
                self[key] = value


configuration_settings = ConfigurationSettings()


class Encoding:
    """An encoding is a protocol for the rendering of text.

    """

    def __init__(self, key: str):
        self._key = key

    def __repr__(self):
        return self._key

    def __str__(self):
        return self._key

    @property
    def key(self) -> str:
        return self._key


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
        self._latex_math = self._register(Encoding(key='latex_math'))
        self._unicode_extended = self._register(Encoding(key='unicode_extended'))
        self._unicode_limited = self._register(Encoding(key='unicode_limited'))
        default_encoding = configuration_settings['presentation_1']['default_encoding']
        self._default = self[default_encoding]

    def __repr__(self):
        return 'encodings'

    def __str__(self):
        return 'encodings'

    def _register(self, encoding: Encoding):
        self[encoding.key] = encoding
        return encoding

    @property
    def default(self):
        """The default encoding. This is a user-preference. The default-encoding is used by typesetting-methods
        whenever encoding is not provided as an explicit argument.

        :return:
        """
        return self._default

    @default.setter
    def default(self, encoding: typing.Union[Encoding, str]):
        if isinstance(encoding, str):
            encoding: Encoding = self[encoding]
        self._default = encoding

    @property
    def latex_math(self):
        return self._latex_math

    @property
    def unicode_extended(self):
        """A rich subset of unicode symbols that may not be supported in some environments.

        :return:
        """
        return self._unicode_extended

    @property
    def unicode_limited(self):
        """A well-supported subset of unicode symbols.

        :return:
        """
        return self._unicode_limited


encodings = Encodings()


class TypesettingMethod(abc.ABC):
    """An abstract class that represent a typesetting-method with the capability to typeset objects. It exposes
    two key methods:
     - typeset_as_string(...)
     - typeset_from_generator(...)
     """

    def __init__(self, key: str):
        self._key = key

    def __repr__(self) -> str:
        return self.typeset_as_string(encoding=None)

    def __str__(self) -> str:
        return self.typeset_as_string(encoding=None)

    @property
    def key(self):
        return self._key

    def typeset_as_string(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        raise NotImplementedError('This is an abstract method.')

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        raise NotImplementedError('This is an abstract method.')


class FailsafeTypesettingMethod(TypesettingMethod):
    def __init__(self):
        super().__init__(key='failsafe-typesetting-method')

    def typeset_as_string(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        return f'python-object-{id(self)}'

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield from self.typeset_as_string(encoding=encoding, **kwargs)


class TypesettingMethods(dict):
    """A catalog of out-of-the-box encodings."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(TypesettingMethods, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        global configuration_settings
        super().__init__()
        self._failsafe = self._register(typesetting_method=FailsafeTypesettingMethod())

    def _register(self, typesetting_method: TypesettingMethod) -> TypesettingMethod:
        self[typesetting_method.key] = typesetting_method
        return typesetting_method

    @property
    def failsafe(self):
        return self._failsafe


typesetting_methods = TypesettingMethods()


class Typesettable:
    """A typesettable is a python object equipped with a reusable typesetting-configuration.

    By inheriting from Typesettable, typesetting capabilities are added to the original class."""

    def __init__(self, typesetting_configuration: typing.Optional[TypesettingConfiguration] = None):
        if typesetting_configuration is None:
            typesetting_configuration: TypesettingConfiguration = TypesettingConfiguration(typesetting_method=None)
        self._typesetting_configuration: TypesettingConfiguration = typesetting_configuration

    def __repr__(self) -> str:
        return self.typeset_as_string(encoding=None)

    def __str__(self) -> str:
        return self.typeset_as_string(encoding=None)

    @property
    def typesetting_configuration(self) -> TypesettingConfiguration:
        return self._typesetting_configuration

    @typesetting_configuration.setter
    def typesetting_configuration(self, typesetting_configuration: TypesettingConfiguration):
        self._typesetting_configuration = typesetting_configuration

    def typeset_as_string(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        if encoding is None:
            encoding = encodings.default
        return self.typesetting_configuration.typeset_as_string(encoding=encoding, **kwargs)

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        if encoding is None:
            encoding = encodings.default
        yield from self.typesetting_configuration.typeset_from_generator(encoding=encoding, **kwargs)


class TypesettingConfiguration:
    """A typesetting-configuration equips an object to provide re-configurable typesetting capabilities:
     - typesetting as a string via the typeset_as_string(...) method,
     - typesetting from a generator via the typeset_from_generator(...) method,
     - the capability to reuse the typesetting-configuration across objects, e.g.:
      PropositionVariableTypesettingConfiguration, etc.
     - the capability to modify the typesetting-configuration typesetting-method to change the way some objects
      are typeset.
    """

    def __init__(self, typesetting_method: typing.Optional[TypesettingMethod] = None):
        self._typesetting_method: typing.Optional[TypesettingMethod] = typesetting_method

    def __repr__(self) -> str:
        return self.typeset_as_string(encoding=None)

    def __str__(self) -> str:
        return self.typeset_as_string(encoding=None)

    def typeset_as_string(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        global typesetting_methods
        if self.typesetting_method is not None:
            return self.typesetting_method.typeset_as_string(encoding=encoding, **kwargs)
        else:
            return typesetting_methods.failsafe.typeset_as_string(encoding=encoding, **kwargs)

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        if self.typesetting_method is not None:
            yield from self.typesetting_method.typeset_as_string(encoding=encoding, **kwargs)
        else:
            yield from typesetting_methods.failsafe.typeset_as_string(encoding=encoding, **kwargs)

    @property
    def typesetting_method(self) -> typing.Optional[TypesettingMethod]:
        return self._typesetting_method

    @typesetting_method.setter
    def typesetting_method(self, typesetting_method: typing.Optional[TypesettingMethod]):
        self._typesetting_method: typing.Optional[TypesettingMethod] = typesetting_method


class Symbol(TypesettingMethod):
    """An atomic symbol."""

    def __init__(self, key: str, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math: str = latex_math
        self._unicode_extended: str = unicode_extended
        self._unicode_limited: str = unicode_limited
        super().__init__(key=key)

    @property
    def latex_math(self) -> str:
        return self._latex_math

    def typeset_as_string(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> str:
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

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        yield self.typeset_as_string(encoding=encoding, **kwargs)

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


class Symbols(dict):
    """A catalog of out-of-the-box symbols."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Symbols, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._asterisk_operator = self._register(
            Symbol(key='asterisk_operator', latex_math='\\ast', unicode_extended='∗', unicode_limited='*'))
        self._close_parenthesis = self._register(
            Symbol(key='close_parenthesis', latex_math='\\right)', unicode_extended=')', unicode_limited=')'))
        self._collection_separator = self._register(
            Symbol(key='collection_separator', latex_math=', ', unicode_extended=', ', unicode_limited=', '))
        self._not_sign = self._register(
            Symbol(key='not_sign', latex_math='\\lnot', unicode_extended='¬', unicode_limited='not'))
        self._open_parenthesis = self._register(
            Symbol(key='open_parenthesis', latex_math='\\left(', unicode_extended='(', unicode_limited='('))
        self._p_uppercase_serif_italic = self._register(
            Symbol(key='p_uppercase_serif_italic', latex_math='\\textit{P}', unicode_extended='𝑃',
                   unicode_limited='P'))
        self._q_uppercase_serif_italic = self._register(
            Symbol(key='q_uppercase_serif_italic', latex_math='\\textit{Q}', unicode_extended='𝑄',
                   unicode_limited='Q'))
        self._r_uppercase_serif_italic = self._register(
            Symbol(key='r_uppercase_serif_italic', latex_math='\\textit{R}', unicode_extended='𝑅',
                   unicode_limited='R'))
        self._rightwards_arrow = self._register(
            Symbol(key='rightwards_arrow', latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->'))
        self._space = self._register(Symbol(key='space', latex_math=' ', unicode_extended=' ', unicode_limited=' '))
        self._tilde = self._register(Symbol(key='tilde', latex_math='\\sim', unicode_extended='~', unicode_limited='~'))

    def _register(self, symbol: Symbol):
        self[symbol.key] = symbol
        return symbol

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


class InfixBinaryFormulaTypesettingMethod(TypesettingMethod):
    def __init__(self, connective_symbol: Symbol):
        super().__init__()
        self._connective_symbol = connective_symbol

    @property
    def connective_symbol(self) -> Symbol:
        return self._connective_symbol

    def typeset_as_string(self, phi: BinaryFormula, **kwargs) -> str:
        return f'{phi.term_0.rep(**kwargs)}{symbols.space}{symbols.space}{symbols.space}{phi.term_1.rep(**kwargs)}'


class IndexedSymbol(TypesettingMethod):
    pass
