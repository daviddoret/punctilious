import punctilious as pu


class TestGreekAlphabetLowercaseSerifItalic:
    def test_greek_alphabet_lowercase_serif_italic(self):
        """Test of representation with multiple string-constant renderers.
        """
        prefs = pu.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == 'Phi')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == '𝛷')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == '\\Phi')
        prefs[pu.options.technical_language.latex_math] = pu._representation.get_forbidden()
        assert (pu.greek_alphabet_uppercase_serif_italic.phi.rep(prefs=prefs) == '𝛷')
