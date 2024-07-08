from __future__ import annotations

import abc
import typing
import tomllib
import pathlib

import state_1 as st1

# Pseudo-constants
FORMULA_TS = 'formula_ts'
REF_TS = 'ref_ts'
DECLARATION_TS = 'declaration_ts'


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
        # return ''.join(self.typeset_from_generator(**kwargs))
        return ''.join([str(x) for x in self.typeset_from_generator(**kwargs)])

    @abc.abstractmethod
    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        raise NotImplementedError('This is an abstract method.')

    def __str__(self):
        return f'ts:{self.typeset_as_string()}'

    def __repr__(self):
        return f'ts:{self.typeset_as_string()}'


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


class NaturalIndexedSymbolTypesetter(Typesetter):
    def __init__(self, body_ts: Typesetter, index: int):
        super().__init__()
        self._body_ts: Typesetter = body_ts
        self._index: int = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def body_ts(self) -> Typesetter:
        return self._body_ts

    def typeset_from_generator(self, encoding: typing.Optional[encodings] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        if encoding is None:
            encoding = encodings.default
        yield from self.body_ts.typeset_from_generator(encoding=encoding, **kwargs)
        if encoding is encodings.latex_math:
            yield f'_{{{self.index}}}'
        elif encoding is encodings.unicode_extended:
            yield unicode_subscriptify(s=str(self.index))
        elif encoding is encodings.unicode_limited:
            yield str(self.index)
        else:
            raise ValueError('Unsupported encoding')


class ArbitraryIndexedSymbolTypesetter(Typesetter):
    """"""

    def __init__(self, body_ts: Typesetter, subscript_ts: Typesetter):
        super().__init__()
        body_ts: Typesetter = coerce_typesetter(ts=body_ts)
        subscript_ts: Typesetter = coerce_typesetter(ts=subscript_ts)
        self._body_ts: FlexibleTypesetter = body_ts
        self._subscript_ts: FlexibleTypesetter = subscript_ts

    @property
    def subscript_ts(self) -> Typesetter:
        return self._subscript_ts

    @property
    def body_ts(self) -> Typesetter:
        return self._body_ts

    def typeset_from_generator(self, encoding: typing.Optional[encodings] = None, **kwargs) -> (
            typing.Generator)[str, None, None]:
        if encoding is None:
            encoding = encodings.default
        yield from self.body_ts.typeset_from_generator(encoding=encoding, **kwargs)
        if encoding is encodings.latex_math:
            yield f'_{{'
            yield from self.subscript_ts.typeset_from_generator(encoding=encoding, **kwargs)
            yield f'}}'
        elif encoding is encodings.unicode_extended:
            subscript: str = self.subscript_ts.typeset_as_string(encoding=encoding, **kwargs)
            yield unicode_subscriptify(s=subscript)
        elif encoding is encodings.unicode_limited:
            subscript: str = self.subscript_ts.typeset_as_string(encoding=encoding, **kwargs)
            yield '_'
            yield subscript
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


digit_names = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
               '8': 'eight', '9': 'nine'}


class Monospace(Typesetter):
    """A multi-format best-effort string in monospace style.

    """

    def __init__(self, text: str):
        super().__init__()
        self._text: str = str(text)

    @property
    def text(self) -> str:
        return self._text

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        for c in self.text:
            c: str
            if c in '0123456789':
                digit_name: str = digit_names.get(c)
                key: str = f'{digit_name}_monospace'
                symbol: Symbol = symbols.get(key, c)
                yield from symbol.typeset_from_generator(**kwargs)
            elif c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key: str = f'{c.lower()}_uppercase_monospace'
                symbol: Symbol = symbols.get(key, c)
                yield from symbol.typeset_from_generator(**kwargs)
            elif c in 'abcdefghijklmnopqrstuvwxyz':
                key: str = f'{c}_lowercase_monospace'
                symbol: Symbol = symbols.get(key, c)
                yield from symbol.typeset_from_generator(**kwargs)
            else:
                yield c


class Script(Typesetter):
    """A multi-format best-effort string in script style.



    """

    def __init__(self, text: str):
        super().__init__()
        self._text: str = str(text)

    @property
    def text(self) -> str:
        return self._text

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        for c in self.text:
            c: str
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key: str = f'{c.lower()}_uppercase_script'
                symbol: Symbol = symbols.get(key, c)
                yield from symbol.typeset_from_generator(**kwargs)
            elif c in 'abcdefghijklmnopqrstuvwxyz':
                key: str = f'{c}_lowercase_script'
                symbol: Symbol = symbols.get(key, c)
                yield from symbol.typeset_from_generator(**kwargs)
            else:
                yield c


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

    def indexed_symbol(self, symbol: Symbol, index: int) -> NaturalIndexedSymbolTypesetter:
        return NaturalIndexedSymbolTypesetter(body_ts=symbol, index=index)


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
    """A catalog of out-of-the-box symbols.

    References:
        - https://mirror.init7.net/ctan/macros/unicodetex/latex/unicode-math/unimath-symbols.pdf
        - https://gist.github.com/taliesinb/4c2700c543c6e06a47a8a3cc85bb9772

    """
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
        self._close_square_bracket = self._register(
            Symbol(key='close_square_bracket', latex_math='\\right]', unicode_extended=']', unicode_limited=']'))
        self._comma = self._register(
            Symbol(key='collection_separator', latex_math=',', unicode_extended=',', unicode_limited=','))
        self._conjunction = self._register(
            Symbol(key='conjunction', latex_math='\\wedge', unicode_extended='∧', unicode_limited='and'))
        self._disjunction = self._register(
            Symbol(key='disjunction', latex_math='\\vee', unicode_extended='∨', unicode_limited='or'))
        self._implication = self._register(
            Symbol(key='implication', latex_math='\\implies', unicode_extended='⇒', unicode_limited='==>'))
        self._maps_to = self._register(
            Symbol(key='maps_to', latex_math='\\mapsto', unicode_extended='↦', unicode_limited='|-->'))
        self._negation = self._register(
            Symbol(key='negation', latex_math='\\lnot', unicode_extended='¬', unicode_limited='not'))
        self._open_curly_brace = self._register(
            Symbol(key='open_curly_brace', latex_math='\\left\\{', unicode_extended='{', unicode_limited='{'))
        self._open_parenthesis = self._register(
            Symbol(key='open_parenthesis', latex_math='\\left(', unicode_extended='(', unicode_limited='('))
        self._open_square_bracket = self._register(
            Symbol(key='open_square_bracket', latex_math='\\left[', unicode_extended='[', unicode_limited='['))
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
        # Monospace digits
        self._zero_monospace = self._register(
            Symbol(key='zero_monospace', latex_math='\\texttt{𝟶}', unicode_extended='0',
                   unicode_limited='𝟶'))

        self._one_monospace = self._register(
            Symbol(key='one_monospace', latex_math='\\texttt{𝟷}', unicode_extended='1',
                   unicode_limited='𝟷'))

        self._two_monospace = self._register(
            Symbol(key='two_monospace', latex_math='\\texttt{𝟸}', unicode_extended='2',
                   unicode_limited='𝟸'))

        self._three_monospace = self._register(
            Symbol(key='three_monospace', latex_math='\\texttt{𝟹}', unicode_extended='3',
                   unicode_limited='𝟹'))

        self._four_monospace = self._register(
            Symbol(key='four_monospace', latex_math='\\texttt{𝟺}', unicode_extended='4',
                   unicode_limited='𝟺'))

        self._five_monospace = self._register(
            Symbol(key='five_monospace', latex_math='\\texttt{𝟻}', unicode_extended='5',
                   unicode_limited='𝟻'))

        self._six_monospace = self._register(
            Symbol(key='six_monospace', latex_math='\\texttt{𝟼}', unicode_extended='6',
                   unicode_limited='𝟼'))

        self._seven_monospace = self._register(
            Symbol(key='seven_monospace', latex_math='\\texttt{𝟽}', unicode_extended='7',
                   unicode_limited='𝟽'))

        self._eight_monospace = self._register(
            Symbol(key='eight_monospace', latex_math='\\texttt{𝟾}', unicode_extended='8',
                   unicode_limited='𝟾'))

        self._nine_monospace = self._register(
            Symbol(key='nine_monospace', latex_math='\\texttt{𝟿}', unicode_extended='9',
                   unicode_limited='𝟿'))

        # Uppercase monospace
        self._a_uppercase_monospace = self._register(
            Symbol(key='a_uppercase_monospace', latex_math='\\texttt{A}', unicode_extended='𝙰',
                   unicode_limited='A'))
        self._b_uppercase_monospace = self._register(
            Symbol(key='b_uppercase_monospace', latex_math='\\texttt{B}', unicode_extended='𝙱',
                   unicode_limited='B'))
        self._c_uppercase_monospace = self._register(
            Symbol(key='c_uppercase_monospace', latex_math='\\texttt{C}', unicode_extended='𝙲',
                   unicode_limited='C'))
        self._d_uppercase_monospace = self._register(
            Symbol(key='d_uppercase_monospace', latex_math='\\texttt{D}', unicode_extended='𝙳',
                   unicode_limited='D'))
        self._e_uppercase_monospace = self._register(
            Symbol(key='e_uppercase_monospace', latex_math='\\texttt{E}', unicode_extended='𝙴',
                   unicode_limited='E'))
        self._f_uppercase_monospace = self._register(
            Symbol(key='f_uppercase_monospace', latex_math='\\texttt{F}', unicode_extended='𝙵',
                   unicode_limited='F'))
        self._g_uppercase_monospace = self._register(
            Symbol(key='g_uppercase_monospace', latex_math='\\texttt{G}', unicode_extended='𝙶',
                   unicode_limited='G'))
        self._h_uppercase_monospace = self._register(
            Symbol(key='h_uppercase_monospace', latex_math='\\texttt{H}', unicode_extended='𝙷',
                   unicode_limited='H'))
        self._i_uppercase_monospace = self._register(
            Symbol(key='i_uppercase_monospace', latex_math='\\texttt{I}', unicode_extended='𝙸',
                   unicode_limited='I'))
        self._j_uppercase_monospace = self._register(
            Symbol(key='j_uppercase_monospace', latex_math='\\texttt{J}', unicode_extended='𝙹',
                   unicode_limited='J'))
        self._k_uppercase_monospace = self._register(
            Symbol(key='k_uppercase_monospace', latex_math='\\texttt{K}', unicode_extended='𝙺',
                   unicode_limited='K'))
        self._l_uppercase_monospace = self._register(
            Symbol(key='l_uppercase_monospace', latex_math='\\texttt{L}', unicode_extended='𝙻',
                   unicode_limited='L'))
        self._m_uppercase_monospace = self._register(
            Symbol(key='m_uppercase_monospace', latex_math='\\texttt{M}', unicode_extended='𝙼',
                   unicode_limited='M'))
        self._n_uppercase_monospace = self._register(
            Symbol(key='n_uppercase_monospace', latex_math='\\texttt{N}', unicode_extended='𝙽',
                   unicode_limited='N'))
        self._o_uppercase_monospace = self._register(
            Symbol(key='o_uppercase_monospace', latex_math='\\texttt{O}', unicode_extended='𝙾',
                   unicode_limited='O'))
        self._p_uppercase_monospace = self._register(
            Symbol(key='p_uppercase_monospace', latex_math='\\texttt{P}', unicode_extended='𝙿',
                   unicode_limited='P'))
        self._q_uppercase_monospace = self._register(
            Symbol(key='q_uppercase_monospace', latex_math='\\texttt{Q}', unicode_extended='𝚀',
                   unicode_limited='Q'))
        self._r_uppercase_monospace = self._register(
            Symbol(key='r_uppercase_monospace', latex_math='\\texttt{R}', unicode_extended='𝚁',
                   unicode_limited='R'))
        self._s_uppercase_monospace = self._register(
            Symbol(key='s_uppercase_monospace', latex_math='\\texttt{S}', unicode_extended='𝚂',
                   unicode_limited='S'))
        self._t_uppercase_monospace = self._register(
            Symbol(key='t_uppercase_monospace', latex_math='\\texttt{T}', unicode_extended='𝚃',
                   unicode_limited='T'))
        self._u_uppercase_monospace = self._register(
            Symbol(key='u_uppercase_monospace', latex_math='\\texttt{U}', unicode_extended='𝚄',
                   unicode_limited='U'))
        self._v_uppercase_monospace = self._register(
            Symbol(key='v_uppercase_monospace', latex_math='\\texttt{V}', unicode_extended='𝚅',
                   unicode_limited='V'))
        self._w_uppercase_monospace = self._register(
            Symbol(key='w_uppercase_monospace', latex_math='\\texttt{W}', unicode_extended='𝚆',
                   unicode_limited='W'))
        self._x_uppercase_monospace = self._register(
            Symbol(key='x_uppercase_monospace', latex_math='\\texttt{X}', unicode_extended='𝚇',
                   unicode_limited='X'))
        self._y_uppercase_monospace = self._register(
            Symbol(key='y_uppercase_monospace', latex_math='\\texttt{Y}', unicode_extended='𝚈',
                   unicode_limited='Y'))
        self._z_uppercase_monospace = self._register(
            Symbol(key='z_uppercase_monospace', latex_math='\\texttt{Z}', unicode_extended='𝚉',
                   unicode_limited='Z'))

        # Lowercase monospace
        self._a_lowercase_monospace = self._register(
            Symbol(key='a_lowercase_monospace', latex_math='\\texttt{a}', unicode_extended='𝚊',
                   unicode_limited='a'))
        self._b_lowercase_monospace = self._register(
            Symbol(key='b_lowercase_monospace', latex_math='\\texttt{b}', unicode_extended='𝚋',
                   unicode_limited='b'))
        self._c_lowercase_monospace = self._register(
            Symbol(key='c_lowercase_monospace', latex_math='\\texttt{c}', unicode_extended='𝚌',
                   unicode_limited='c'))
        self._d_lowercase_monospace = self._register(
            Symbol(key='d_lowercase_monospace', latex_math='\\texttt{d}', unicode_extended='𝚍',
                   unicode_limited='d'))
        self._e_lowercase_monospace = self._register(
            Symbol(key='e_lowercase_monospace', latex_math='\\texttt{e}', unicode_extended='𝚎',
                   unicode_limited='e'))
        self._f_lowercase_monospace = self._register(
            Symbol(key='f_lowercase_monospace', latex_math='\\texttt{f}', unicode_extended='𝚏',
                   unicode_limited='f'))
        self._g_lowercase_monospace = self._register(
            Symbol(key='g_lowercase_monospace', latex_math='\\texttt{g}', unicode_extended='𝚐',
                   unicode_limited='g'))
        self._h_lowercase_monospace = self._register(
            Symbol(key='h_lowercase_monospace', latex_math='\\texttt{h}', unicode_extended='𝚑',
                   unicode_limited='h'))
        self._i_lowercase_monospace = self._register(
            Symbol(key='i_lowercase_monospace', latex_math='\\texttt{i}', unicode_extended='𝚒',
                   unicode_limited='i'))
        self._j_lowercase_monospace = self._register(
            Symbol(key='j_lowercase_monospace', latex_math='\\texttt{j}', unicode_extended='𝚓',
                   unicode_limited='j'))
        self._k_lowercase_monospace = self._register(
            Symbol(key='k_lowercase_monospace', latex_math='\\texttt{k}', unicode_extended='𝚔',
                   unicode_limited='k'))
        self._l_lowercase_monospace = self._register(
            Symbol(key='l_lowercase_monospace', latex_math='\\texttt{l}', unicode_extended='𝚕',
                   unicode_limited='l'))
        self._m_lowercase_monospace = self._register(
            Symbol(key='m_lowercase_monospace', latex_math='\\texttt{m}', unicode_extended='𝚖',
                   unicode_limited='m'))
        self._n_lowercase_monospace = self._register(
            Symbol(key='n_lowercase_monospace', latex_math='\\texttt{n}', unicode_extended='𝚗',
                   unicode_limited='n'))
        self._o_lowercase_monospace = self._register(
            Symbol(key='o_lowercase_monospace', latex_math='\\texttt{o}', unicode_extended='𝚘',
                   unicode_limited='o'))
        self._p_lowercase_monospace = self._register(
            Symbol(key='p_lowercase_monospace', latex_math='\\texttt{p}', unicode_extended='𝚙',
                   unicode_limited='p'))
        self._q_lowercase_monospace = self._register(
            Symbol(key='q_lowercase_monospace', latex_math='\\texttt{q}', unicode_extended='𝚚',
                   unicode_limited='q'))
        self._r_lowercase_monospace = self._register(
            Symbol(key='r_lowercase_monospace', latex_math='\\texttt{r}', unicode_extended='𝚛',
                   unicode_limited='r'))
        self._s_lowercase_monospace = self._register(
            Symbol(key='s_lowercase_monospace', latex_math='\\texttt{s}', unicode_extended='𝚜',
                   unicode_limited='s'))
        self._t_lowercase_monospace = self._register(
            Symbol(key='t_lowercase_monospace', latex_math='\\texttt{t}', unicode_extended='𝚝',
                   unicode_limited='t'))
        self._u_lowercase_monospace = self._register(
            Symbol(key='u_lowercase_monospace', latex_math='\\texttt{u}', unicode_extended='𝚞',
                   unicode_limited='u'))
        self._v_lowercase_monospace = self._register(
            Symbol(key='v_lowercase_monospace', latex_math='\\texttt{v}', unicode_extended='𝚟',
                   unicode_limited='v'))
        self._w_lowercase_monospace = self._register(
            Symbol(key='w_lowercase_monospace', latex_math='\\texttt{w}', unicode_extended='𝚠',
                   unicode_limited='w'))
        self._x_lowercase_monospace = self._register(
            Symbol(key='x_lowercase_monospace', latex_math='\\texttt{x}', unicode_extended='𝚡',
                   unicode_limited='x'))
        self._y_lowercase_monospace = self._register(
            Symbol(key='y_lowercase_monospace', latex_math='\\texttt{y}', unicode_extended='𝚢',
                   unicode_limited='y'))
        self._z_lowercase_monospace = self._register(
            Symbol(key='z_lowercase_monospace', latex_math='\\texttt{z}', unicode_extended='𝚣',
                   unicode_limited='z'))

        # Script Uppercase

        self._a_uppercase_script = self._register(
            Symbol(key='a_uppercase_script', latex_math='\\texttt{A}', unicode_extended='𝒜',
                   unicode_limited='A'))

        self._b_uppercase_script = self._register(
            Symbol(key='b_uppercase_script', latex_math='\\texttt{B}', unicode_extended='ℬ',
                   unicode_limited='B'))

        self._c_uppercase_script = self._register(
            Symbol(key='c_uppercase_script', latex_math='\\texttt{C}', unicode_extended='𝒞',
                   unicode_limited='C'))

        self._d_uppercase_script = self._register(
            Symbol(key='d_uppercase_script', latex_math='\\texttt{D}', unicode_extended='𝒟',
                   unicode_limited='D'))

        self._e_uppercase_script = self._register(
            Symbol(key='e_uppercase_script', latex_math='\\texttt{E}', unicode_extended='ℰ',
                   unicode_limited='E'))

        self._f_uppercase_script = self._register(
            Symbol(key='f_uppercase_script', latex_math='\\texttt{F}', unicode_extended='ℱ',
                   unicode_limited='F'))

        self._g_uppercase_script = self._register(
            Symbol(key='g_uppercase_script', latex_math='\\texttt{G}', unicode_extended='𝒢',
                   unicode_limited='G'))

        self._h_uppercase_script = self._register(
            Symbol(key='h_uppercase_script', latex_math='\\texttt{H}', unicode_extended='ℋ',
                   unicode_limited='H'))

        self._i_uppercase_script = self._register(
            Symbol(key='i_uppercase_script', latex_math='\\texttt{I}', unicode_extended='ℐ',
                   unicode_limited='I'))

        self._j_uppercase_script = self._register(
            Symbol(key='j_uppercase_script', latex_math='\\texttt{J}', unicode_extended='𝒥',
                   unicode_limited='J'))

        self._k_uppercase_script = self._register(
            Symbol(key='k_uppercase_script', latex_math='\\texttt{K}', unicode_extended='𝒦',
                   unicode_limited='K'))

        self._l_uppercase_script = self._register(
            Symbol(key='l_uppercase_script', latex_math='\\texttt{L}', unicode_extended='ℒ',
                   unicode_limited='L'))

        self._m_uppercase_script = self._register(
            Symbol(key='m_uppercase_script', latex_math='\\texttt{M}', unicode_extended='ℳ',
                   unicode_limited='M'))

        self._n_uppercase_script = self._register(
            Symbol(key='n_uppercase_script', latex_math='\\texttt{N}', unicode_extended='𝒩',
                   unicode_limited='N'))

        self._o_uppercase_script = self._register(
            Symbol(key='o_uppercase_script', latex_math='\\texttt{O}', unicode_extended='𝒪',
                   unicode_limited='O'))

        self._p_uppercase_script = self._register(
            Symbol(key='p_uppercase_script', latex_math='\\texttt{P}', unicode_extended='𝒫',
                   unicode_limited='P'))

        self._q_uppercase_script = self._register(
            Symbol(key='q_uppercase_script', latex_math='\\texttt{Q}', unicode_extended='𝒬',
                   unicode_limited='Q'))

        self._r_uppercase_script = self._register(
            Symbol(key='r_uppercase_script', latex_math='\\texttt{R}', unicode_extended='ℛ',
                   unicode_limited='R'))

        self._s_uppercase_script = self._register(
            Symbol(key='s_uppercase_script', latex_math='\\texttt{S}', unicode_extended='𝒮',
                   unicode_limited='S'))

        self._t_uppercase_script = self._register(
            Symbol(key='t_uppercase_script', latex_math='\\texttt{T}', unicode_extended='𝒯',
                   unicode_limited='T'))

        self._u_uppercase_script = self._register(
            Symbol(key='u_uppercase_script', latex_math='\\texttt{U}', unicode_extended='𝒰',
                   unicode_limited='U'))

        self._v_uppercase_script = self._register(
            Symbol(key='v_uppercase_script', latex_math='\\texttt{V}', unicode_extended='𝒱',
                   unicode_limited='V'))

        self._w_uppercase_script = self._register(
            Symbol(key='w_uppercase_script', latex_math='\\texttt{W}', unicode_extended='𝒲',
                   unicode_limited='W'))

        self._x_uppercase_script = self._register(
            Symbol(key='x_uppercase_script', latex_math='\\texttt{X}', unicode_extended='𝒳',
                   unicode_limited='X'))

        self._y_uppercase_script = self._register(
            Symbol(key='y_uppercase_script', latex_math='\\texttt{Y}', unicode_extended='𝒴',
                   unicode_limited='Y'))

        self._z_uppercase_script = self._register(
            Symbol(key='z_uppercase_script', latex_math='\\texttt{Z}', unicode_extended='𝒵',
                   unicode_limited='Z'))

        # Script lowercase

        self._a_lowercase_script = self._register(
            Symbol(key='a_lowercase_script', latex_math='\\texttt{a}', unicode_extended='𝒶',
                   unicode_limited='a'))

        self._b_lowercase_script = self._register(
            Symbol(key='b_lowercase_script', latex_math='\\texttt{b}', unicode_extended='𝒷',
                   unicode_limited='b'))

        self._c_lowercase_script = self._register(
            Symbol(key='c_lowercase_script', latex_math='\\texttt{c}', unicode_extended='𝒸',
                   unicode_limited='c'))

        self._d_lowercase_script = self._register(
            Symbol(key='d_lowercase_script', latex_math='\\texttt{d}', unicode_extended='𝒹',
                   unicode_limited='d'))

        self._e_lowercase_script = self._register(
            Symbol(key='e_lowercase_script', latex_math='\\texttt{e}', unicode_extended='ℯ',
                   unicode_limited='e'))

        self._f_lowercase_script = self._register(
            Symbol(key='f_lowercase_script', latex_math='\\texttt{f}', unicode_extended='𝒻',
                   unicode_limited='f'))

        self._g_lowercase_script = self._register(
            Symbol(key='g_lowercase_script', latex_math='\\texttt{g}', unicode_extended='ℊ',
                   unicode_limited='g'))

        self._h_lowercase_script = self._register(
            Symbol(key='h_lowercase_script', latex_math='\\texttt{h}', unicode_extended='𝒽',
                   unicode_limited='h'))

        self._i_lowercase_script = self._register(
            Symbol(key='i_lowercase_script', latex_math='\\texttt{i}', unicode_extended='𝒾',
                   unicode_limited='i'))

        self._j_lowercase_script = self._register(
            Symbol(key='j_lowercase_script', latex_math='\\texttt{j}', unicode_extended='𝒿',
                   unicode_limited='j'))

        self._k_lowercase_script = self._register(
            Symbol(key='k_lowercase_script', latex_math='\\texttt{k}', unicode_extended='𝓀',
                   unicode_limited='k'))

        self._l_lowercase_script = self._register(
            Symbol(key='l_lowercase_script', latex_math='\\texttt{l}', unicode_extended='𝓁',
                   unicode_limited='l'))

        self._m_lowercase_script = self._register(
            Symbol(key='m_lowercase_script', latex_math='\\texttt{m}', unicode_extended='𝓂',
                   unicode_limited='m'))

        self._n_lowercase_script = self._register(
            Symbol(key='n_lowercase_script', latex_math='\\texttt{n}', unicode_extended='𝓃',
                   unicode_limited='n'))

        self._o_lowercase_script = self._register(
            Symbol(key='o_lowercase_script', latex_math='\\texttt{o}', unicode_extended='ℴ',
                   unicode_limited='o'))

        self._p_lowercase_script = self._register(
            Symbol(key='p_lowercase_script', latex_math='\\texttt{p}', unicode_extended='𝓅',
                   unicode_limited='p'))

        self._q_lowercase_script = self._register(
            Symbol(key='q_lowercase_script', latex_math='\\texttt{q}', unicode_extended='𝓆',
                   unicode_limited='q'))

        self._r_lowercase_script = self._register(
            Symbol(key='r_lowercase_script', latex_math='\\texttt{r}', unicode_extended='𝓇',
                   unicode_limited='r'))

        self._s_lowercase_script = self._register(
            Symbol(key='s_lowercase_script', latex_math='\\texttt{s}', unicode_extended='𝓈',
                   unicode_limited='s'))

        self._t_lowercase_script = self._register(
            Symbol(key='t_lowercase_script', latex_math='\\texttt{t}', unicode_extended='𝓉',
                   unicode_limited='t'))

        self._u_lowercase_script = self._register(
            Symbol(key='u_lowercase_script', latex_math='\\texttt{u}', unicode_extended='𝓊',
                   unicode_limited='u'))

        self._v_lowercase_script = self._register(
            Symbol(key='v_lowercase_script', latex_math='\\texttt{v}', unicode_extended='𝓋',
                   unicode_limited='v'))

        self._w_lowercase_script = self._register(
            Symbol(key='w_lowercase_script', latex_math='\\texttt{w}', unicode_extended='𝓌',
                   unicode_limited='w'))

        self._x_lowercase_script = self._register(
            Symbol(key='x_lowercase_script', latex_math='\\texttt{x}', unicode_extended='𝓍',
                   unicode_limited='x'))

        self._y_lowercase_script = self._register(
            Symbol(key='y_lowercase_script', latex_math='\\texttt{y}', unicode_extended='𝓎',
                   unicode_limited='y'))

        self._z_lowercase_script = self._register(
            Symbol(key='z_lowercase_script', latex_math='\\texttt{z}', unicode_extended='𝓏',
                   unicode_limited='z'))

    def _register(self, symbol: Symbol):
        self[symbol.key] = symbol
        return symbol

    def is_sans_serif_letter(self, letter: str) -> bool:
        if letter is None or not len(letter) == 1 or not letter.isalpha():
            return False
        else:
            return True

    def is_monospace_letter(self, letter: str) -> bool:
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

    def get_monospace_letter(self, letter: str) -> Symbol:
        if not self.is_monospace_letter(letter=letter):
            raise ValueError(f'ooooops')
        case: str
        if letter.islower():
            case = 'lowercase'
        else:
            case = 'uppercase'
        key: str = f'{letter.lower()}_{case}_monospace'
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
    def close_square_bracket(self) -> Symbol:
        return self._close_square_bracket

    @property
    def comma(self) -> Symbol:
        return self._comma

    @property
    def conjunction(self) -> Symbol:
        return self._conjunction

    @property
    def disjunction(self) -> Symbol:
        return self._disjunction

    @property
    def implication(self) -> Symbol:
        return self._implication

    @property
    def maps_to(self) -> Symbol:
        return self._maps_to

    @property
    def negation(self) -> Symbol:
        return self._negation

    @property
    def open_curly_brace(self) -> Symbol:
        return self._open_curly_brace

    @property
    def open_parenthesis(self) -> Symbol:
        return self._open_parenthesis

    @property
    def open_square_bracket(self) -> Symbol:
        return self._open_square_bracket

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

    # Monospace digits

    @property
    def zero_monospace(self) -> Symbol:
        return self._zero_monospace

    @property
    def one_monospace(self) -> Symbol:
        return self._one_monospace

    @property
    def two_monospace(self) -> Symbol:
        return self._two_monospace

    @property
    def three_monospace(self) -> Symbol:
        return self._three_monospace

    @property
    def four_monospace(self) -> Symbol:
        return self._four_monospace

    @property
    def five_monospace(self) -> Symbol:
        return self._five_monospace

    @property
    def six_monospace(self) -> Symbol:
        return self._six_monospace

    @property
    def seven_monospace(self) -> Symbol:
        return self._seven_monospace

    @property
    def eight_monospace(self) -> Symbol:
        return self._eight_monospace

    @property
    def nine_monospace(self) -> Symbol:
        return self._nine_monospace

    # Monospace uppercase letters

    @property
    def a_uppercase_monospace(self) -> Symbol:
        return self._a_uppercase_monospace

    @property
    def b_uppercase_monospace(self) -> Symbol:
        return self._b_uppercase_monospace

    @property
    def c_uppercase_monospace(self) -> Symbol:
        return self._c_uppercase_monospace

    @property
    def d_uppercase_monospace(self) -> Symbol:
        return self._d_uppercase_monospace

    @property
    def e_uppercase_monospace(self) -> Symbol:
        return self._e_uppercase_monospace

    @property
    def f_uppercase_monospace(self) -> Symbol:
        return self._f_uppercase_monospace

    @property
    def g_uppercase_monospace(self) -> Symbol:
        return self._g_uppercase_monospace

    @property
    def h_uppercase_monospace(self) -> Symbol:
        return self._h_uppercase_monospace

    @property
    def i_uppercase_monospace(self) -> Symbol:
        return self._i_uppercase_monospace

    @property
    def j_uppercase_monospace(self) -> Symbol:
        return self._j_uppercase_monospace

    @property
    def k_uppercase_monospace(self) -> Symbol:
        return self._k_uppercase_monospace

    @property
    def l_uppercase_monospace(self) -> Symbol:
        return self._l_uppercase_monospace

    @property
    def m_uppercase_monospace(self) -> Symbol:
        return self._m_uppercase_monospace

    @property
    def n_uppercase_monospace(self) -> Symbol:
        return self._n_uppercase_monospace

    @property
    def o_uppercase_monospace(self) -> Symbol:
        return self._o_uppercase_monospace

    @property
    def p_uppercase_monospace(self) -> Symbol:
        return self._p_uppercase_monospace

    @property
    def q_uppercase_monospace(self) -> Symbol:
        return self._q_uppercase_monospace

    @property
    def r_uppercase_monospace(self) -> Symbol:
        return self._r_uppercase_monospace

    @property
    def s_uppercase_monospace(self) -> Symbol:
        return self._s_uppercase_monospace

    @property
    def t_uppercase_monospace(self) -> Symbol:
        return self._t_uppercase_monospace

    @property
    def u_uppercase_monospace(self) -> Symbol:
        return self._u_uppercase_monospace

    @property
    def v_uppercase_monospace(self) -> Symbol:
        return self._v_uppercase_monospace

    @property
    def w_uppercase_monospace(self) -> Symbol:
        return self._w_uppercase_monospace

    @property
    def x_uppercase_monospace(self) -> Symbol:
        return self._x_uppercase_monospace

    @property
    def y_uppercase_monospace(self) -> Symbol:
        return self._y_uppercase_monospace

    @property
    def z_uppercase_monospace(self) -> Symbol:
        return self._z_uppercase_monospace

    # Uppercase script

    @property
    def a_uppercase_script(self) -> Symbol:
        return self._a_uppercase_script

    @property
    def b_uppercase_script(self) -> Symbol:
        return self._b_uppercase_script

    @property
    def c_uppercase_script(self) -> Symbol:
        return self._c_uppercase_script

    @property
    def d_uppercase_script(self) -> Symbol:
        return self._d_uppercase_script

    @property
    def e_uppercase_script(self) -> Symbol:
        return self._e_uppercase_script

    @property
    def f_uppercase_script(self) -> Symbol:
        return self._f_uppercase_script

    @property
    def g_uppercase_script(self) -> Symbol:
        return self._g_uppercase_script

    @property
    def h_uppercase_script(self) -> Symbol:
        return self._h_uppercase_script

    @property
    def i_uppercase_script(self) -> Symbol:
        return self._i_uppercase_script

    @property
    def j_uppercase_script(self) -> Symbol:
        return self._j_uppercase_script

    @property
    def k_uppercase_script(self) -> Symbol:
        return self._k_uppercase_script

    @property
    def l_uppercase_script(self) -> Symbol:
        return self._l_uppercase_script

    @property
    def m_uppercase_script(self) -> Symbol:
        return self._m_uppercase_script

    @property
    def n_uppercase_script(self) -> Symbol:
        return self._n_uppercase_script

    @property
    def o_uppercase_script(self) -> Symbol:
        return self._o_uppercase_script

    @property
    def p_uppercase_script(self) -> Symbol:
        return self._p_uppercase_script

    @property
    def q_uppercase_script(self) -> Symbol:
        return self._q_uppercase_script

    @property
    def r_uppercase_script(self) -> Symbol:
        return self._r_uppercase_script

    @property
    def s_uppercase_script(self) -> Symbol:
        return self._s_uppercase_script

    @property
    def t_uppercase_script(self) -> Symbol:
        return self._t_uppercase_script

    @property
    def u_uppercase_script(self) -> Symbol:
        return self._u_uppercase_script

    @property
    def v_uppercase_script(self) -> Symbol:
        return self._v_uppercase_script

    @property
    def w_uppercase_script(self) -> Symbol:
        return self._w_uppercase_script

    @property
    def x_uppercase_script(self) -> Symbol:
        return self._x_uppercase_script

    @property
    def y_uppercase_script(self) -> Symbol:
        return self._y_uppercase_script

    @property
    def z_uppercase_script(self) -> Symbol:
        return self._z_uppercase_script

    # Lowercase script

    @property
    def a_lowercase_script(self) -> Symbol:
        return self._a_lowercase_script

    @property
    def b_lowercase_script(self) -> Symbol:
        return self._b_lowercase_script

    @property
    def c_lowercase_script(self) -> Symbol:
        return self._c_lowercase_script

    @property
    def d_lowercase_script(self) -> Symbol:
        return self._d_lowercase_script

    @property
    def e_lowercase_script(self) -> Symbol:
        return self._e_lowercase_script

    @property
    def f_lowercase_script(self) -> Symbol:
        return self._f_lowercase_script

    @property
    def g_lowercase_script(self) -> Symbol:
        return self._g_lowercase_script

    @property
    def h_lowercase_script(self) -> Symbol:
        return self._h_lowercase_script

    @property
    def i_lowercase_script(self) -> Symbol:
        return self._i_lowercase_script

    @property
    def j_lowercase_script(self) -> Symbol:
        return self._j_lowercase_script

    @property
    def k_lowercase_script(self) -> Symbol:
        return self._k_lowercase_script

    @property
    def l_lowercase_script(self) -> Symbol:
        return self._l_lowercase_script

    @property
    def m_lowercase_script(self) -> Symbol:
        return self._m_lowercase_script

    @property
    def n_lowercase_script(self) -> Symbol:
        return self._n_lowercase_script

    @property
    def o_lowercase_script(self) -> Symbol:
        return self._o_lowercase_script

    @property
    def p_lowercase_script(self) -> Symbol:
        return self._p_lowercase_script

    @property
    def q_lowercase_script(self) -> Symbol:
        return self._q_lowercase_script

    @property
    def r_lowercase_script(self) -> Symbol:
        return self._r_lowercase_script

    @property
    def s_lowercase_script(self) -> Symbol:
        return self._s_lowercase_script

    @property
    def t_lowercase_script(self) -> Symbol:
        return self._t_lowercase_script

    @property
    def u_lowercase_script(self) -> Symbol:
        return self._u_lowercase_script

    @property
    def v_lowercase_script(self) -> Symbol:
        return self._v_lowercase_script

    @property
    def w_lowercase_script(self) -> Symbol:
        return self._w_lowercase_script

    @property
    def x_lowercase_script(self) -> Symbol:
        return self._x_lowercase_script

    @property
    def y_lowercase_script(self) -> Symbol:
        return self._y_lowercase_script

    @property
    def z_lowercase_script(self) -> Symbol:
        return self._z_lowercase_script


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
        ts: Typesetter = typesetters.failsafe()
        return ts
    elif isinstance(ts, str):
        # temporary fix
        if len(ts) == 1 and symbols.is_sans_serif_letter(letter=ts):
            # TODO: Temporary fix for variable names.
            ts: Typesetter = symbols.get_sans_serif_letter(letter=ts)
            return ts
        else:
            ts: Typesetter = typesetters.text(text=ts)
            return ts
    elif isinstance(ts, Typesetter):
        return ts
    else:
        raise Exception('unsupported value')


def extract_typesetters(t: dict[str, typing.Any]) -> dict[str, Typesetter]:
    """Returns a python-dict of (string, typesetter)pairs from a dict of anything.
    Used to process *kwargs in __init__ methods."""
    return {key: value for key, value in t.items() if isinstance(value, Typesetter)}
