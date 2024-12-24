import punctilious as pu


class TestOptions:
    def test_technical_language_1(self):
        """Test various values of the technical_language option.
        """
        pass
        prefs = pu.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(prefs=prefs) == 'lambda')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(prefs=prefs) == '𝜆')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(prefs=prefs) == '\\lambda')
        pass

    def test_technical_language_2(self):
        """Test various values of the technical_language option.
        """
        pass
        prefs = pu.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.operators_1.element_of.rep_connector(prefs=prefs) == 'in')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.operators_1.element_of.rep_connector(prefs=prefs) == '∈')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.operators_1.element_of.rep_connector(prefs=prefs) == '\\in')
        pass