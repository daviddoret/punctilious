import pytest
import punctilious as pu


class TestTypesettingConfiguration:
    def test_typesetting_configuration(self):
        tc = pu.pl1.Typesettable()
        tc.typesetting_configuration.typesetting_method = pu.pl1.symbols.p_uppercase_serif_italic
        assert tc.typeset_as_string(encoding=pu.pl1.encodings.latex_math) == '\\textit{P}'
        assert tc.typeset_as_string(encoding=pu.pl1.encodings.unicode_extended) == '𝑃'
        assert tc.typeset_as_string(encoding=pu.pl1.encodings.unicode_limited) == 'P'
