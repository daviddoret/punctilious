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


class TestTypesettingClass:
    def test_is_subclass_of(self):
        c = pu.ts.TypesettingClass("c")
        d = pu.ts.TypesettingClass("d", superclass=c)
        e = pu.ts.TypesettingClass("e", superclass=d)
        f = pu.ts.TypesettingClass("f", superclass=c)
        g = pu.ts.TypesettingClass("g", superclass=f)
        assert c.is_subclass_of(c=c)
        assert d.is_subclass_of(c=c)
        assert e.is_subclass_of(c=c)
        assert f.is_subclass_of(c=c)
        assert g.is_subclass_of(c=c)
        assert not c.is_subclass_of(c=d)
        assert not c.is_subclass_of(c=e)
        assert not c.is_subclass_of(c=f)
        assert not c.is_subclass_of(c=g)
        assert not f.is_subclass_of(c=d)
        assert not d.is_subclass_of(c=f)
        assert not e.is_subclass_of(c=g)
        assert not g.is_subclass_of(c=e)


class TestProtocolPreference:
    def test_protocol(self):
        pu.ts.preferences.protocol.protocol = pu.ts.protocols.unicode_extended
        assert pu.ts.symbols.asterisk_operator.to_string() == '∗'
        pu.ts.preferences.protocol.protocol = pu.ts.protocols.unicode_limited
        assert pu.ts.symbols.asterisk_operator.to_string() == '*'
        pu.ts.preferences.protocol.protocol = pu.ts.protocols.unicode_extended
        assert pu.ts.symbols.asterisk_operator.to_string() == '∗'
        pu.ts.preferences.protocol.reset()  # targeted reset
        assert pu.ts.symbols.asterisk_operator.to_string() == '*'
        pu.ts.preferences.protocol.protocol = pu.ts.protocols.unicode_extended
        assert pu.ts.symbols.asterisk_operator.to_string() == '∗'
        pu.ts.preferences.reset()  # full reset
        assert pu.ts.symbols.asterisk_operator.to_string() == '*'
        pu.ts.preferences.protocol.protocol = pu.ts.protocols.latex
        assert pu.ts.symbols.asterisk_operator.to_string() == '\\ast'
        pu.ts.preferences.protocol.reset()
