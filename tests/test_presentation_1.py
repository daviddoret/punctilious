import pytest
import punctilious as pu


class TestTypesettingConfiguration:
    def test_typesetting_configuration(self):
        tc = pu.p1.Typesettable()
        tc.typesetting_method = pu.p1.symbols.p_uppercase_serif_italic
        assert tc.rep(encoding=pu.p1.encodings.latex_math) == '\\textit{P}'
        assert tc.rep(encoding=pu.p1.encodings.unicode_extended) == '𝑃'
        assert tc.rep(encoding=pu.p1.encodings.unicode_limited) == 'P'
