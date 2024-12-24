import punctilious as pu


class TestGreekAlphabetLowercaseSerifItalic:
    def test_greek_alphabet_lowercase_serif_italic(self):
        """Test of representation with multiple string-constant renderers.
        """
        pass
        prefs = pu.OptionsPreferences()
        prefs[pu.unicode_basic] = 2
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == 'lambda')
        prefs[pu.unicode_extended] = 3
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == '𝜆')
        prefs[pu.latex_math] = 4
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == '\\lambda')
        pass
