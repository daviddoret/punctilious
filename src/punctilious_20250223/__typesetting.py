import typing
import abc
import enum

import punctilious_20250223.pu_01_utilities as _util


class Representable(abc.ABC):
    pass


class Typeface:
    pass


class DiacriticalMark:
    """A diacritical mark or accent."""

    def __init__(self, diacritical_mark_name: str):
        self._diacritical_mark_name = diacritical_mark_name

    @property
    def diacritical_mark_name(self) -> str:
        return self._diacritical_mark_name


diacritical_marks = {
    'circumflex': DiacriticalMark('circumflex'),
    'dot': DiacriticalMark('dot'),
    'overline': DiacriticalMark('overline'),
    'tilde': DiacriticalMark('tilde'),
}


class Symbol(Representable, abc.ABC):
    pass


class AbstractSymbol(Symbol, abc.ABC):
    """An base symbol without typeface, nor diacritical_mark."""

    def __init__(self, symbol_name: str):
        self._symbol_name = symbol_name

    @property
    def symbol_name(self) -> str:
        return self._symbol_name


abstract_symbols = {
    'a': AbstractSymbol('a'),
    'b': AbstractSymbol('b'),
    'c': AbstractSymbol('c'),
    'A': AbstractSymbol('A'),
    'B': AbstractSymbol('B'),
    'C': AbstractSymbol('C')
}


class AtomicSymbol(AbstractSymbol):
    """An atomic symbol with typeface, and possibly diacritical mark."""

    def __init__(self, symbol_name, diacritical_mark: DiacriticalMark | None = None, typeface: Typeface | None = None):
        self._symbol_name = symbol_name
        self._diacritical_mark: DiacriticalMark | None = diacritical_mark
        self._typeface = typeface
        super().__init__(symbol_name)

    @property
    def symbol_name(self) -> str:
        return self._symbol_name

    @property
    def diacritical_mark(self) -> DiacriticalMark | None:
        return self._diacritical_mark

    @property
    def typeface(self) -> Typeface:
        return self._typeface


class ComposedSymbol(Symbol):
    """A composed symbol with a certain typeface."""

    def __init__(self, symbol_names: typing.Iterable, diacritical_mark: DiacriticalMark | None = None,
                 typeface: Typeface | None = None):
        self.symbol_names = tuple(symbol_names)
        self._diacritical_mark: DiacriticalMark | None = diacritical_mark
        self._typeface = typeface


class DecoratedSymbol(Representable):
    def __init__(self, symbol: Type, subscript: Type | None = None, superscript: Type | None = None,
                 overlay: Type | None = None,
                 underlay: Type | None = None):
        self._symbol = symbol
        self._subscript: Type | None = subscript
        self._superscript: Type | None = superscript
        self._overlay: Type | None = overlay
        self._underlay: Type | None = underlay


class FontRun(Representable):
    """A sequence of symbols sharing the same typeface."""

    def __init__(self, symbol_names: typing.Iterable, typeface: Typeface | None = None):
        self._symbol_names = tuple(symbol_names)
        self._typeface: Typeface = typeface


class TextRun(Representable):
    """A sequence of symbols possibly in different typefaces."""

    def __init__(self, elements: typing.Iterable[Representable]):
        self._elements: typing.Iterable[Representable] = elements

    @property
    def elements(self) -> typing.Iterable[Representable]:
        return self._elements


class Radical(Representable):
    pass


class Fraction(Representable):
    def __init__(self, numerator, denominator):
        pass


class Matrix(Representable):
    pass


class OutputAmbiguityOptions(enum.Enum):
    """Options when some typesetting may be ambiguous, and an arbitrage is necessary
    between ambiguity, and readability.

     Attributes:
        AMBIGUOUS_BUT_MORE_READABLE:
        UNAMBIGUOUS_BUT_LESS_READABLE:
    """
    AMBIGUOUS_BUT_MORE_READABLE = 'AMBIGUOUS_BUT_MORE_READABLE'
    UNAMBIGUOUS_BUT_LESS_READABLE = 'UNAMBIGUOUS_BUT_LESS_READABLE'


class Renderer:

    def to_string(self, representable: Representable) -> str:
        output = ''
        for x in yield from

    def yield_any(self, representable: Representable):
        if isinstance(representable, AtomicSymbol):
            atomic_symbol: AtomicSymbol = typing.cast(AtomicSymbol, representable)
            yield from self.yield_atomic_symbol(atomic_symbol)
        elif isinstance(representable, ComposedSymbol):
            composed_symbol: ComposedSymbol = typing.cast(ComposedSymbol, representable)
            yield from self.yield_composed_symbol(composed_symbol)
        # etc.

    def yield_atomic_symbol(self, atomic_symbol):
        pass

    def yield_composed_symbol(self, composed_symbol: ComposedSymbol):
        pass

    def yield_decorated_symbol(self, decorated_symbol: DecoratedSymbol):
        pass

    def yield_font_run(self, font_run: FontRun):
        pass

    def yield_text_run(self, text_run: TextRun):
        for element in text_run.elements:
            yield element
        pass


class ExtendedUnicodeRenderer(Renderer):
    """Typeset the output using extended Unicode characters, without consideration for ambiguities
    when representation is not properly supported (e.g. typeface, fractions, etc.)."""

    def __init__(self):
        pass

    def yield_atomic_symbol(self, atomic_symbol: AtomicSymbol):
        if atomic_symbol in basic_unicode_symbols:
            yield basic_unicode_symbols[atomic_symbol]
        else:
            raise _util.PunctiliousError(
                title='Unknown symbol',
                details='`symbol` is not present in `basic_unicode_symbols`',
                atomic_symbol=atomic_symbol,
                basic_unicode_symbols=basic_unicode_symbols
            )
