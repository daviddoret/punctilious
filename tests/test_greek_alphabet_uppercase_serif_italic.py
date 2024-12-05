import pytest
import punctilious as pu


class TestGreekAlphabetLowercaseSerifItalic:
    def test_greek_alphabet_lowercase_serif_italic(self):
        """Test of representation with multiple string-constant renderers.
        """
        pass
        prefs = pu.presentation.TagsPreferences()
        prefs[pu.presentation.unicode_basic] = 2
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == 'Phi')
        prefs[pu.presentation.unicode_extended] = 3
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == '𝛷')
        prefs[pu.presentation.latex_math] = 4
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == f'\\Phi')
        pass
