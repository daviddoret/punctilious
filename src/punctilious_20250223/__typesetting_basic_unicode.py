import punctilious_20250223.pu_01_utilities as _util
import punctilious_20250223.__typesetting as _typesetting

diacritical_mark_map = {
    _typesetting.diacritical_marks['circumflex']: '\u0302',
    _typesetting.diacritical_marks['dot']: '\u0307',
    _typesetting.diacritical_marks['overline']: '\u0304',
    _typesetting.diacritical_marks['tilde']: '\u0303'
}

symbol_map = {
    _typesetting.abstract_symbols['a']: 'a',
    _typesetting.abstract_symbols['b']: 'b',
    _typesetting.abstract_symbols['c']: 'c'
}


class BasicUnicodeRenderer(_typesetting.Renderer):
    """Typeset the output using basic Unicode characters, without consideration for ambiguities
    when representation is not properly supported (e.g. typeface, fractions, etc.)."""

    def __init__(self):
        pass

    def yield_atomic_symbol(self, atomic_symbol: _typesetting.AtomicSymbol):
        global diacritical_mark_map
        global symbol_map
        if atomic_symbol in symbol_map:
            yield symbol_map[atomic_symbol]
            if atomic_symbol.diacritical_mark is not None:
                if atomic_symbol.diacritical_mark in diacritical_mark_map:
                    yield diacritical_mark_map[atomic_symbol.diacritical_mark]
                else:
                    raise _util.PunctiliousError(
                        title='Unknown diacritical mark',
                        details='`diacritical_map` is not present in `diacritical_mark_map`',
                        diacritical_mark=atomic_symbol.diacritical_mark,
                        diacritical_mark_map=diacritical_mark_map
                    )
        else:
            raise _util.PunctiliousError(
                title='Unknown symbol',
                details='`symbol` is not present in `symbol_map`',
                atomic_symbol=atomic_symbol,
                symbol_map=symbol_map
            )


x = _typesetting.AtomicSymbol('a', diacritical_mark=_typesetting.diacritical_marks['dot'])
