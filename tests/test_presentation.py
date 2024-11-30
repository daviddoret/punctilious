import pytest
import punctilious as pu


class TestRepresentation:
    def test_representation(self):
        en = pu.presentation.Tag('language', 'en')
        fr = pu.presentation.Tag('language', 'fr')
        symbol = pu.presentation.Tag('connector_representation', 'symbol')
        word = pu.presentation.Tag('connector_representation', 'word')

        x = pu.presentation.RendererForStringConstant(string_constant='and', tags=(en, word,))
        y = pu.presentation.RendererForStringConstant(string_constant='et', tags=(fr, word,))
        z = pu.presentation.RendererForStringConstant(string_constant='∧', tags=(symbol,))
        rep = pu.presentation.Representation(renderers=(x, y, z,))

        prefs = pu.presentation.TagsPreferences()
        prefs[en] = 6
        prefs[fr] = 9
        prefs[symbol] = 100
        prefs[word] = 1
        assert (rep.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (rep.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (rep.rep(prefs=prefs) == 'and')
