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


@pytest.fixture
def reps():
    d: dict = pu.util.get_yaml_from_package(path='data.representations', resource='operators_representation_1.yaml')
    raw = d.get('representations', [])
    return pu.presentation.ensure_representations(o=raw)


@pytest.fixture
def conjunction_connector(reps):
    return reps[0]


class TestRepresentation:
    def test_representation(self, en, fr, word, symbol, prefs):
        """Test of representation with multiple string-constant renderers.
        """
        x = pu.presentation.RendererForStringConstant(string_constant='and', tags=(en, word,))
        y = pu.presentation.RendererForStringConstant(string_constant='et', tags=(fr, word,))
        z = pu.presentation.RendererForStringConstant(string_constant='∧', tags=(symbol,))
        rep = pu.presentation.Representation(renderers=(x, y, z,))

        assert (rep.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (rep.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (rep.rep(prefs=prefs) == 'and')

    def test_from_yaml(self, en, fr, word, symbol, conjunction_connector, prefs):
        """Test of representation coming from aa yaml file with multiple string-constant renderers.
        """

        assert (conjunction_connector.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (conjunction_connector.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (conjunction_connector.rep(prefs=prefs) == 'and')
