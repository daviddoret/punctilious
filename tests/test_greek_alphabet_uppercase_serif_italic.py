import pytest
import punctilious as pu


class TestGreekAlphabetLowercaseSerifItalic:
    def test_greek_alphabet_lowercase_serif_italic(self):
        """Test of representation with multiple string-constant renderers.
        """
        pass
        prefs = pu.TagsPreferences()
        prefs[pu.unicode_basic] = 2
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(config=prefs) == 'Phi')
        prefs[pu.unicode_extended] = 3
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(config=prefs) == '𝛷')
        prefs[pu.latex_math] = 4
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(config=prefs) == '\\Phi')
        pass
