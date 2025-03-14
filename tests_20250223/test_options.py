import punctilious_20250223 as pu


class TestOptions:

    def test_abstract_options(self):
        option_a = pu.rpr.Option('option_a', 'description of option_a')
        option_b = pu.rpr.Option('option_b', 'description of option_b')
        option_c = pu.rpr.Option('option_c', 'description of option_c')

        prefs = pu.rpr.Preferences()
        prefs[option_a] = 1
        prefs[option_b] = pu.representation.get_forbidden()
        prefs[option_c] = 5

        assert prefs.score_options(tuple()) == (0, 0,)
        assert prefs.score_options((option_a,)) == (1, 0,)
        assert prefs.score_options((option_b,)) == (0, 1,)
        assert prefs.score_options((option_a, option_b,)) == (1, 1,)
        assert prefs.score_options((option_a, option_b, option_c,)) == (6, 1,)
        assert prefs.score_options((option_a, option_c,)) == (6, 0,)

    def test_technical_language_1(self):
        """Test various values of the technical_language option.
        """
        pass
        prefs = pu.rpr.Preferences()
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
        prefs = pu.rpr.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.operators.element_of.rep_connector(prefs=prefs) == 'in')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.operators.element_of.rep_connector(prefs=prefs) == '∈')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.operators.element_of.rep_connector(prefs=prefs) == '\\in')
        prefs[pu.options.technical_language.latex_math] = pu.representation.get_forbidden()
        assert (pu.operators.element_of.rep_connector(prefs=prefs) == '∈')
        pass
