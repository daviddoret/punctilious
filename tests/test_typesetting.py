import pytest

import punctilious as pu


class TestSymbols:
    def test_to_string(self):
        assert pu.ts.symbols.p_uppercase_serif_italic.to_string(protocol=pu.ts.protocols.latex) == '\\textit{P}'
        assert pu.ts.symbols.p_uppercase_serif_italic.to_string(protocol=pu.ts.protocols.unicode_extended) == "𝑃"
        assert pu.ts.symbols.p_uppercase_serif_italic.to_string(protocol=pu.ts.protocols.unicode_limited) == "P"

    def test_to_string_2(self):
        assert pu.ts.symbols.space.to_string(protocol=pu.ts.protocols.unicode_extended) == ' '
        assert pu.ts.symbols.space.to_string(protocol=pu.ts.protocols.unicode_limited) == ' '
        assert pu.ts.symbols.space.to_string(protocol=pu.ts.protocols.latex) == ' '
        assert ''.join(pu.ts.typeset_symbol(o=pu.ts.symbols.space, protocol=pu.ts.protocols.unicode_extended)) == ' '
        assert ''.join(pu.ts.typeset_symbol(o=pu.ts.symbols.space, protocol=pu.ts.protocols.unicode_limited)) == ' '
        assert ''.join(pu.ts.typeset_symbol(o=pu.ts.symbols.space, protocol=pu.ts.protocols.latex)) == ' '
        assert ''.join(pu.ts.typeset(o=pu.ts.symbols.space, protocol=pu.ts.protocols.unicode_extended)) == ' '
        assert ''.join(pu.ts.typeset(o=pu.ts.symbols.space, protocol=pu.ts.protocols.unicode_limited)) == ' '
        assert ''.join(pu.ts.typeset(o=pu.ts.symbols.space, protocol=pu.ts.protocols.latex)) == ' '


class TestIndexSymbol:
    def test_to_string(self):
        assert pu.ts.IndexedSymbol(symbol=pu.ts.symbols.p_uppercase_serif_italic, index=6).to_string(
            protocol=pu.ts.protocols.latex) == "\\textit{P}_{6}"
        assert pu.ts.IndexedSymbol(symbol=pu.ts.symbols.p_uppercase_serif_italic, index=6).to_string(
            protocol=pu.ts.protocols.unicode_extended) == "𝑃₆"
        assert pu.ts.IndexedSymbol(symbol=pu.ts.symbols.p_uppercase_serif_italic, index=6).to_string(
            protocol=pu.ts.protocols.unicode_limited) == "P6"
