import pytest
import punctilious as pu


@pytest.fixture
def en():
    return pu.presentation.Tag('language', 'en')


@pytest.fixture
def fr():
    return pu.presentation.Tag('language', 'fr')


@pytest.fixture
def symbol():
    return pu.presentation.Tag('connector_representation', 'symbol')


@pytest.fixture
def word():
    return pu.presentation.Tag('connector_representation', 'word')


@pytest.fixture
def prefs(en, fr, symbol, word):
    prefs = pu.presentation.TagsPreferences()
    prefs[en] = 6
    prefs[fr] = 9
    prefs[symbol] = 100
    prefs[word] = 1
    return prefs


class TestRepresentation:
    def test_representation(self, en, fr, word, symbol, prefs):
        x = pu.presentation.RendererForStringConstant(string_constant='and', tags=(en, word,))
        y = pu.presentation.RendererForStringConstant(string_constant='et', tags=(fr, word,))
        z = pu.presentation.RendererForStringConstant(string_constant='∧', tags=(symbol,))
        rep = pu.presentation.Representation(renderers=(x, y, z,))

        assert (rep.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (rep.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (rep.rep(prefs=prefs) == 'and')

    def test_from_yaml(self, en, fr, word, symbol, prefs):
        d: dict = pu.util.get_yaml_from_package(path='data.representations', resource='operators_representation_1.yaml')
        assert d is not None
        raw = d.get('representations', [])
        reps = pu.presentation.ensure_representations(o=raw)

        conjunction_connector: pu.presentation.Representation = reps[0]
        print(conjunction_connector.rep(prefs=prefs))

        assert (conjunction_connector.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (conjunction_connector.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (conjunction_connector.rep(prefs=prefs) == 'and')
