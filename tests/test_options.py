import pytest
import punctilious as pu


class TestOptions:
    def test_technical_language(self):
        """Test various values of the technical_language option.
        """
        pass
        prefs = pu.OptionsPreferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == 'lambda')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == '𝜆')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.greek_alphabet_lowercase_serif_italic.lambda2.rep(config=prefs) == '\\lambda')
        pass
