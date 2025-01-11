import punctilious as pu


class TestLatinAlphabetLowercaseSerifItalic:
    def test_latin_alphabet_lowercase_serif_italic(self):
        """Test of representation with multiple string-constant renderers.
        """
        prefs = pu.rpr.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 2
        assert (pu.latin_alphabet_uppercase_serif_italic.p.rep(prefs=prefs) == 'P')
        prefs[pu.options.technical_language.unicode_extended] = 3
        assert (pu.latin_alphabet_uppercase_serif_italic.p.rep(prefs=prefs) == '𝑃')
        prefs[pu.options.technical_language.latex_math] = 4
        assert (pu.latin_alphabet_uppercase_serif_italic.p.rep(prefs=prefs) == '\\textit{P}')
        prefs[pu.options.technical_language.latex_math] = pu.representation.get_forbidden()
        assert (pu.latin_alphabet_uppercase_serif_italic.p.rep(prefs=prefs) == '𝑃')
