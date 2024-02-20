import pytest

import punctilious as pu


class TestTypesettingClass:
    def test_typesetting_class(self):
        class H1(pu.ts.TypesettingClass):
            FORMAL_OBJECT = pu.ts.TC(None)
            FORMULA = pu.ts.TC(FORMAL_OBJECT)
            BINARY_FORMULA = pu.ts.TC(FORMULA)

        pu.ts.TypesettingClass.load_elements(H1)

        class H2(pu.ts.TypesettingClass):
            FORMAL_OBJECT = pu.ts.TC(None)
            FORMULA = pu.ts.TC(FORMAL_OBJECT)
            BINARY_FORMULA = pu.ts.TC(FORMULA)

        pu.ts.TypesettingClass.load_elements(H2)

        assert H1.FORMAL_OBJECT.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.FORMULA.is_subclass_of(H1.FORMULA)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.FORMAL_OBJECT)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.FORMULA)
        assert H1.BINARY_FORMULA.is_subclass_of(H1.BINARY_FORMULA)
        assert not H1.FORMULA.is_subclass_of(H2.FORMULA)
        assert not H1.FORMAL_OBJECT.is_subclass_of(H1.BINARY_FORMULA)
        assert not H1.FORMULA.is_subclass_of(H1.BINARY_FORMULA)


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
        c = pu.ts.TC()
        d = pu.ts.TC(c)
        e = pu.ts.TC(d)
        f = pu.ts.TC(c)
        g = pu.ts.TC(f)
        assert c.is_subclass_of(tc=c)
        assert d.is_subclass_of(tc=c)
        assert e.is_subclass_of(tc=c)
        assert f.is_subclass_of(tc=c)
        assert g.is_subclass_of(tc=c)
        assert not c.is_subclass_of(tc=d)
        assert not c.is_subclass_of(tc=e)
        assert not c.is_subclass_of(tc=f)
        assert not c.is_subclass_of(tc=g)
        assert not f.is_subclass_of(tc=d)
        assert not d.is_subclass_of(tc=f)
        assert not e.is_subclass_of(tc=g)
        assert not g.is_subclass_of(tc=e)


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
