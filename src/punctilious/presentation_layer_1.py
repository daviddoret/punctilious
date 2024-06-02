from __future__ import annotations

import abc
import typing
import tomllib
import pathlib

import state_1 as st1


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
        configuration_file_path: pathlib.Path = module_folder.joinpath('presentation_layer_1.toml')
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

    def __new__(cls):
        if st1.presentation_layer_1_encodings is None:
            st1.presentation_layer_1_encodings = super(Encodings, cls).__new__(cls)
        return st1.presentation_layer_1_encodings

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


class Typesetter(abc.ABC):
    """An abstract class that represent a typesetting-method with the capability to typeset objects. It exposes
    two key methods:
     - typeset_as_string(...)
     - typeset_from_generator(...)
     """

    def typeset_as_string(self, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        return ''.join(self.typeset_from_generator(**kwargs))

    @abc.abstractmethod
    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        raise NotImplementedError('This is an abstract method.')


class FailsafeTypesetter(Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, encoding: typing.Optional[Encoding] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield f'python-object-{id(self)}'


class SymbolTypesetter(Typesetter):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self._symbol: Symbol = symbol

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield from self.symbol.typeset_from_generator(**kwargs)


class IndexedSymbolTypesetter(Typesetter):
    def __init__(self, symbol: Symbol, index: int):
        super().__init__()
        self._symbol: Symbol = symbol
        self._index: int = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    def typeset_from_generator(self, encoding: typing.Optional[encodings], **kwargs) -> (
            typing.Generator)[str, None, None]:
        if encoding is None:
            encoding = encodings.default
        yield from self.symbol.typeset_from_generator(encoding=encoding, **kwargs)
        if encoding is encodings.latex_math:
            yield f'_{{{self.index}}}'
        elif encoding is encodings.unicode_extended:
            yield unicode_subscriptify(s=str(self.index))
        elif encoding is encodings.unicode_limited:
            yield str(self.index)
        else:
            raise ValueError('Unsupported encoding')


class TextTypesetter(Typesetter):
    """TODO: implement support for multiple font variants.

    """

    def __init__(self, text: str):
        super().__init__()
        self._text: str = str(text)

    @property
    def text(self) -> str:
        return self._text

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield self.text


class Typesetters:
    """A factory of out-of-the-box encodings."""

    def __new__(cls):
        if st1.presentation_layer_1_typesetters is None:
            st1.presentation_layer_1_typesetters = super(Typesetters, cls).__new__(cls)
        return st1.presentation_layer_1_typesetters

    def failsafe(self) -> FailsafeTypesetter:
        return FailsafeTypesetter()

    def symbol(self, symbol: Symbol) -> SymbolTypesetter:
        return SymbolTypesetter(symbol=symbol)

    def text(self, text: str) -> TextTypesetter:
        return TextTypesetter(text=text)

    def indexed_symbol(self, symbol: Symbol, index: int) -> IndexedSymbolTypesetter:
        return IndexedSymbolTypesetter(symbol=symbol, index=index)


typesetters = Typesetters()


class Symbol(Typesetter):
    """An atomic symbol."""

    def __init__(self, key: str, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._key = key
        self._latex_math: str = latex_math
        self._unicode_extended: str = unicode_extended
        self._unicode_limited: str = unicode_limited
        super().__init__()

    @property
    def key(self) -> str:
        return self._key

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
        # Symbols and punctuation
        self._asterisk_operator = self._register(
            Symbol(key='asterisk_operator', latex_math='\\ast', unicode_extended='∗', unicode_limited='*'))
        self._close_curly_brace = self._register(
            Symbol(key='close_curly_brace', latex_math='\\right\\}', unicode_extended='}', unicode_limited='}'))
        self._close_parenthesis = self._register(
            Symbol(key='close_parenthesis', latex_math='\\right)', unicode_extended=')', unicode_limited=')'))
        self._collection_separator = self._register(
            Symbol(key='collection_separator', latex_math=', ', unicode_extended=', ', unicode_limited=', '))
        self._not_sign = self._register(
            Symbol(key='not_sign', latex_math='\\lnot', unicode_extended='¬', unicode_limited='not'))
        self._open_curly_brace = self._register(
            Symbol(key='open_curly_brace', latex_math='\\left\\{', unicode_extended='{', unicode_limited='{'))
        self._open_parenthesis = self._register(
            Symbol(key='open_parenthesis', latex_math='\\left(', unicode_extended='(', unicode_limited='('))
        self._rightwards_arrow = self._register(
            Symbol(key='rightwards_arrow', latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->'))
        self._space = self._register(Symbol(key='space', latex_math=' ', unicode_extended=' ', unicode_limited=' '))
        self._tilde = self._register(Symbol(key='tilde', latex_math='\\sim', unicode_extended='~', unicode_limited='~'))
        # Lowercase serif italic
        self._a_lowercase_serif_italic = self._register(
            Symbol(key='a_lowercase_serif_italic', latex_math='\\textit{a}', unicode_extended='𝑎',
                   unicode_limited='a'))
        self._b_lowercase_serif_italic = self._register(
            Symbol(key='b_lowercase_serif_italic', latex_math='\\textit{b}', unicode_extended='𝑏',
                   unicode_limited='b'))
        self._c_lowercase_serif_italic = self._register(
            Symbol(key='c_lowercase_serif_italic', latex_math='\\textit{c}', unicode_extended='𝑐',
                   unicode_limited='c'))
        self._d_lowercase_serif_italic = self._register(
            Symbol(key='d_lowercase_serif_italic', latex_math='\\textit{d}', unicode_extended='𝑑',
                   unicode_limited='d'))
        self._e_lowercase_serif_italic = self._register(
            Symbol(key='e_lowercase_serif_italic', latex_math='\\textit{e}', unicode_extended='𝑒',
                   unicode_limited='e'))
        self._f_lowercase_serif_italic = self._register(
            Symbol(key='f_lowercase_serif_italic', latex_math='\\textit{f}', unicode_extended='𝑓',
                   unicode_limited='f'))
        self._g_lowercase_serif_italic = self._register(
            Symbol(key='g_lowercase_serif_italic', latex_math='\\textit{g}', unicode_extended='𝑔',
                   unicode_limited='g'))
        self._h_lowercase_serif_italic = self._register(
            Symbol(key='h_lowercase_serif_italic', latex_math='\\textit{h}', unicode_extended='ℎ',
                   unicode_limited='h'))
        self._p_lowercase_serif_italic = self._register(
            Symbol(key='p_lowercase_serif_italic', latex_math='\\textit{p}', unicode_extended='𝑝',
                   unicode_limited='p'))
        self._q_lowercase_serif_italic = self._register(
            Symbol(key='q_lowercase_serif_italic', latex_math='\\textit{q}', unicode_extended='𝑞',
                   unicode_limited='q'))
        self._r_lowercase_serif_italic = self._register(
            Symbol(key='r_lowercase_serif_italic', latex_math='\\textit{r}', unicode_extended='𝑟',
                   unicode_limited='r'))
        self._x_lowercase_serif_italic = self._register(
            Symbol(key='x_lowercase_serif_italic', latex_math='\\textit{x}', unicode_extended='𝑥',
                   unicode_limited='x'))
        self._y_lowercase_serif_italic = self._register(
            Symbol(key='y_lowercase_serif_italic', latex_math='\\textit{y}', unicode_extended='𝑦',
                   unicode_limited='y'))
        self._z_lowercase_serif_italic = self._register(
            Symbol(key='z_lowercase_serif_italic', latex_math='\\textit{z}', unicode_extended='𝑧',
                   unicode_limited='z'))
        # Uppercase serif italic
        self._a_uppercase_serif_italic = self._register(
            Symbol(key='a_uppercase_serif_italic', latex_math='\\textit{A}', unicode_extended='𝐴',
                   unicode_limited='A'))
        self._b_uppercase_serif_italic = self._register(
            Symbol(key='b_uppercase_serif_italic', latex_math='\\textit{B}', unicode_extended='𝐵',
                   unicode_limited='B'))
        self._c_uppercase_serif_italic = self._register(
            Symbol(key='c_uppercase_serif_italic', latex_math='\\textit{C}', unicode_extended='𝐶',
                   unicode_limited='C'))
        self._d_uppercase_serif_italic = self._register(
            Symbol(key='d_uppercase_serif_italic', latex_math='\\textit{D}', unicode_extended='𝐷',
                   unicode_limited='D'))
        self._e_uppercase_serif_italic = self._register(
            Symbol(key='e_uppercase_serif_italic', latex_math='\\textit{E}', unicode_extended='𝐸',
                   unicode_limited='E'))
        self._f_uppercase_serif_italic = self._register(
            Symbol(key='f_uppercase_serif_italic', latex_math='\\textit{F}', unicode_extended='𝐹',
                   unicode_limited='F'))
        self._g_uppercase_serif_italic = self._register(
            Symbol(key='g_uppercase_serif_italic', latex_math='\\textit{G}', unicode_extended='𝐺',
                   unicode_limited='G'))
        self._h_uppercase_serif_italic = self._register(
            Symbol(key='h_uppercase_serif_italic', latex_math='\\textit{H}', unicode_extended='𝐻',
                   unicode_limited='H'))
        self._p_uppercase_serif_italic = self._register(
            Symbol(key='p_uppercase_serif_italic', latex_math='\\textit{P}', unicode_extended='𝑃',
                   unicode_limited='P'))
        self._q_uppercase_serif_italic = self._register(
            Symbol(key='q_uppercase_serif_italic', latex_math='\\textit{Q}', unicode_extended='𝑄',
                   unicode_limited='Q'))
        self._r_uppercase_serif_italic = self._register(
            Symbol(key='r_uppercase_serif_italic', latex_math='\\textit{R}', unicode_extended='𝑅',
                   unicode_limited='R'))
        self._x_uppercase_serif_italic = self._register(
            Symbol(key='x_uppercase_serif_italic', latex_math='\\textit{X}', unicode_extended='𝑋',
                   unicode_limited='X'))
        self._y_uppercase_serif_italic = self._register(
            Symbol(key='y_uppercase_serif_italic', latex_math='\\textit{Y}', unicode_extended='𝑌',
                   unicode_limited='Y'))
        self._z_uppercase_serif_italic = self._register(
            Symbol(key='z_uppercase_serif_italic', latex_math='\\textit{Z}', unicode_extended='𝑍',
                   unicode_limited='Z'))

    def _register(self, symbol: Symbol):
        self[symbol.key] = symbol
        return symbol

    def is_sans_serif_letter(self, letter: str) -> bool:
        if letter is None or not len(letter) == 1 or not letter.isalpha():
            return False
        else:
            return True

    def get_sans_serif_letter(self, letter: str) -> Symbol:
        if not self.is_sans_serif_letter(letter=letter):
            raise ValueError(f'ooooops')
        case: str
        if letter.islower():
            case = 'lowercase'
        else:
            case = 'uppercase'
        key: str = f'{letter.lower()}_{case}_serif_italic'
        return self[key]

    # Symbols and punctuation

    @property
    def asterisk_operator(self) -> Symbol:
        return self._asterisk_operator

    @property
    def close_curly_brace(self) -> Symbol:
        return self._close_curly_brace

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
    def open_curly_brace(self) -> Symbol:
        return self._open_curly_brace

    @property
    def open_parenthesis(self) -> Symbol:
        return self._open_parenthesis

    @property
    def rightwards_arrow(self) -> Symbol:
        return self._rightwards_arrow

    @property
    def space(self) -> Symbol:
        return self._space

    @property
    def tilde(self) -> Symbol:
        return self._tilde

    # Lowercase serif italic

    @property
    def a_lowercase_serif_italic(self) -> Symbol:
        return self._a_lowercase_serif_italic

    @property
    def b_lowercase_serif_italic(self) -> Symbol:
        return self._b_lowercase_serif_italic

    @property
    def c_lowercase_serif_italic(self) -> Symbol:
        return self._c_lowercase_serif_italic

    @property
    def d_lowercase_serif_italic(self) -> Symbol:
        return self._d_lowercase_serif_italic

    @property
    def e_lowercase_serif_italic(self) -> Symbol:
        return self._e_lowercase_serif_italic

    @property
    def f_lowercase_serif_italic(self) -> Symbol:
        return self._f_lowercase_serif_italic

    @property
    def g_lowercase_serif_italic(self) -> Symbol:
        return self._g_lowercase_serif_italic

    @property
    def h_lowercase_serif_italic(self) -> Symbol:
        return self._h_lowercase_serif_italic

    @property
    def p_lowercase_serif_italic(self) -> Symbol:
        return self._p_lowercase_serif_italic

    @property
    def q_lowercase_serif_italic(self) -> Symbol:
        return self._q_lowercase_serif_italic

    @property
    def r_lowercase_serif_italic(self) -> Symbol:
        return self._r_lowercase_serif_italic

    @property
    def x_lowercase_serif_italic(self) -> Symbol:
        return self._x_lowercase_serif_italic

    @property
    def y_lowercase_serif_italic(self) -> Symbol:
        return self._y_lowercase_serif_italic

    @property
    def z_lowercase_serif_italic(self) -> Symbol:
        return self._z_lowercase_serif_italic

    # Uppercase serif italic

    @property
    def a_uppercase_serif_italic(self) -> Symbol:
        return self._a_uppercase_serif_italic

    @property
    def b_uppercase_serif_italic(self) -> Symbol:
        return self._b_uppercase_serif_italic

    @property
    def c_uppercase_serif_italic(self) -> Symbol:
        return self._c_uppercase_serif_italic

    @property
    def d_uppercase_serif_italic(self) -> Symbol:
        return self._d_uppercase_serif_italic

    @property
    def f_uppercase_serif_italic(self) -> Symbol:
        return self._f_uppercase_serif_italic

    @property
    def g_uppercase_serif_italic(self) -> Symbol:
        return self._g_uppercase_serif_italic

    @property
    def h_uppercase_serif_italic(self) -> Symbol:
        return self._h_uppercase_serif_italic

    @property
    def e_uppercase_serif_italic(self) -> Symbol:
        return self._e_uppercase_serif_italic

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
    def x_uppercase_serif_italic(self) -> Symbol:
        return self._x_uppercase_serif_italic

    @property
    def y_uppercase_serif_italic(self) -> Symbol:
        return self._y_uppercase_serif_italic

    @property
    def z_uppercase_serif_italic(self) -> Symbol:
        return self._z_uppercase_serif_italic


symbols = Symbols()

unicode_subscript_dictionary = {'0': u'₀', '1': u'₁', '2': u'₂', '3': u'₃', '4': u'₄', '5': u'₅',
                                '6': u'₆', '7': u'₇', '8': u'₈', '9': u'₉', 'a': u'ₐ', 'e': u'ₑ',
                                'o': u'ₒ', 'x': u'ₓ',  # '???': u'ₔ',
                                'h': u'ₕ', 'k': u'ₖ', 'l': u'ₗ', 'm': u'ₘ', 'n': u'ₙ', 'p': u'ₚ',
                                's': u'ₛ', 't': u'ₜ', '+': u'₊', '-': u'₋', '=': u'₌', '(': u'₍',
                                ')': u'₎', 'j': u'ⱼ', 'i': u'ᵢ',
                                # Alternative from the Unicode Phonetic Extensions block: ᵢ
                                'r': u'ᵣ',  # Source: Unicode Phonetic Extensions block.
                                'u': u'ᵤ',  # Source: Unicode Phonetic Extensions block.
                                'v': u'ᵥ',  # Source: Unicode Phonetic Extensions block.
                                'β': u'ᵦ',  # Source: Unicode Phonetic Extensions block.
                                'γ': u'ᵧ',  # Source: Unicode Phonetic Extensions block.
                                # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
                                'φ': u'ᵩ',  # Source: Unicode Phonetic Extensions block.
                                'χ': u'ᵪ'  # Source: Unicode Phonetic Extensions block.
                                }


def unicode_subscriptify(s: str = ''):
    """Converts to unicode-subscript the string s.

    This is done in best-effort mode, knowing that Unicode only contains a small subset of subscript characters.
    In particular, this function can be called safely to to convert digits to subscripts.

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
        * https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    """
    global unicode_subscript_dictionary
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([unicode_subscript_dictionary.get(c, c) for c in s])


FlexibleTypesetter = typing.Union[Typesetter, str]


def coerce_typesetter(ts: FlexibleTypesetter) -> Typesetter:
    global typesetters
    if ts is None:
        ts = typesetters.failsafe()
    elif isinstance(ts, str):
        # temporary fix
        if len(ts) == 1 and symbols.is_sans_serif_letter(letter=ts):
            # TODO: Temporary fix for variable names.
            ts = symbols.get_sans_serif_letter(letter=ts)
        else:
            ts = typesetters.text(text=ts)

        return typesetters.text(text=ts)
    elif isinstance(ts, Typesetter):
        return ts
    else:
        raise Exception('unsupported value')
