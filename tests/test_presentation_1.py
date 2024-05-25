import pytest
import punctilious as pu


class TestSymbols:
    def test_symbols(self):
        o = pu.p1.Typesettable()
        o.typesetting_method = pu.p1.symbols.p_uppercase_serif_italic
        assert o.rep(encoding=pu.p1.encodings.latex_math) == '\\textit{P}'
        assert o.rep(encoding=pu.p1.encodings.unicode_extended) == '𝑃'
        assert o.rep(encoding=pu.p1.encodings.unicode_limited) == 'P'
