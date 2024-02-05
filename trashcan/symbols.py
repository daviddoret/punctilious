import typing
import typesetting as ts


class Symbol(ts.Typesettable):
    """An atomic symbol."""

    def __init__(self, latex_math: str, unicode_extended: str, unicode_limited: str):
        self._latex_math = latex_math
        self._unicode_extended = unicode_extended
        self._unicode_limited = unicode_limited
        super().__init__()
        self.declare_clazz_element(clazz=ts.clazzes.symbol)

    @property
    def latex_math(self) -> str:
        return self._latex_math

    @property
    def unicode_extended(self) -> str:
        return self._unicode_extended

    @property
    def unicode_limited(self) -> str:
        return self._unicode_limited


class Symbols:
    """A catalog of out-of-the-box symbols."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Symbols, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._asterisk_operator = Symbol(latex_math='\\ast', unicode_extended='∗', unicode_limited='*')
        self._close_parenthesis = Symbol(latex_math='\\right)', unicode_extended=')', unicode_limited=')')
        self._collection_separator = Symbol(latex_math=', ', unicode_extended=', ', unicode_limited=', ')
        self._not_sign = Symbol(latex_math='\\lnot', unicode_extended='¬', unicode_limited='lnot')
        self._open_parenthesis = Symbol(latex_math='\\left(', unicode_extended='(', unicode_limited='(')
        self._p_uppercase_serif_italic = Symbol(latex_math='\\textit{P}', unicode_extended='𝑃', unicode_limited='P')
        self._q_uppercase_serif_italic = Symbol(latex_math='\\textit{Q}', unicode_extended='𝑄', unicode_limited='Q')
        self._r_uppercase_serif_italic = Symbol(latex_math='\\textit{R}', unicode_extended='𝑅', unicode_limited='R')
        self._rightwards_arrow = Symbol(latex_math='\\rightarrow', unicode_extended='→', unicode_limited='-->')
        self._space = Symbol(latex_math=' ', unicode_extended=' ', unicode_limited=' ')
        self._tilde = Symbol(latex_math='\\sim', unicode_extended='~', unicode_limited='~')

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


class IndexedSymbol(ts.Typesettable):

    def __init__(self, symbol: Symbol, index: int):
        self._symbol: Symbol = symbol
        self._index: int = index
        super().__init__()
        self.declare_clazz_element(clazz=ts.clazzes.indexed_symbol)

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.symbol, self.index,))

    @property
    def index(self) -> int:
        return self._index

    @property
    def symbol(self) -> Symbol:
        return self._symbol


def register_symbol(clazz: ts.Clazz, symbol: Symbol, **kwargs1) -> typing.Callable:
    """Register a typesetting-method that outputs an atomic symbol."""

    # dynamically generate the desired typesetting-method.
    def typesetting_method(o: ts.Typesettable, **kwargs2) -> typing.Generator[str, None, None]:
        merged_kwargs = {**kwargs1, **kwargs2}  # overwrite kwargs1 with kwargs2
        return typeset_symbol(o=symbol, **merged_kwargs)

    # register that typesetting-method.
    python_function: typing.Callable = ts.register_typesetting_method(python_function=typesetting_method, clazz=clazz,
        **kwargs1)

    return python_function
