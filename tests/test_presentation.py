import pytest
import punctilious as pu


@pytest.fixture
def en():
    return pu.Option('language', 'en')


@pytest.fixture
def fr():
    return pu.Option('language', 'fr')


@pytest.fixture
def symbol():
    return pu.Option('connector_representation', 'symbol')


@pytest.fixture
def word():
    return pu.Option('connector_representation', 'word')


@pytest.fixture
def traditional_formula():
    return pu.Option('layout', 'traditional_formula')


@pytest.fixture
def infix_formula():
    return pu.Option('layout', 'infix_formula')


@pytest.fixture
def unicode_basic():
    return pu.Option('technical_language', 'unicode_basic')


@pytest.fixture
def unicode_extended():
    return pu.Option('technical_language', 'unicode_extended')


@pytest.fixture
def latex_math():
    return pu.Option('technical_language', 'latex_math')


@pytest.fixture
def prefs(en, fr, symbol, word):
    prefs = pu.Preferences()
    prefs[en] = 6
    prefs[fr] = 9
    prefs[symbol] = 100
    prefs[word] = 1
    return prefs


@pytest.fixture
def reps():
    d: dict = pu.get_yaml_from_package(path='punctilious.data.representations', resource='operators_1.yaml')
    raw = d.get('representations', [])
    return pu.load_abstract_representations(o=raw)


@pytest.fixture
def conjunction_connector(reps):
    return reps[0]


class TestRepresentation:
    def test_representation(self, en, fr, word, symbol, prefs, unicode_basic, unicode_extended, latex_math):
        """Test of representation with multiple string-constant renderers.
        """
        x = pu.RendererForStringConstant(string_constant='and', options=(en, word,))
        y = pu.RendererForStringConstant(string_constant='et', options=(fr, word,))
        z = pu.RendererForStringConstant(string_constant='∧', options=(symbol,))
        rep = pu.AbstractRepresentation(pu.create_uid('rep'), renderers=(x, y, z,))

        prefs[word] = 10
        prefs[symbol] = 20
        prefs[latex_math] = 0
        prefs[unicode_basic] = 10
        prefs[unicode_extended] = 20
        assert (rep.rep(prefs=prefs) == '∧')

        prefs[word] = 1
        prefs[symbol] = 20
        prefs[latex_math] = 0
        prefs[unicode_basic] = 20
        prefs[unicode_extended] = 10
        assert (rep.rep(prefs=prefs) == '∧')

        prefs[word] = 20
        prefs[symbol] = 1
        prefs[en] = 1
        prefs[fr] = 20
        assert (rep.rep(prefs=prefs) == 'et')

        prefs[en] = 20
        prefs[fr] = 1
        assert (rep.rep(prefs=prefs) == 'and')

    def test_from_yaml(self, en, fr, word, symbol, conjunction_connector, prefs):
        """Test of representation coming from aa yaml file with multiple string-constant renderers.
        """

        assert (conjunction_connector.rep(prefs=prefs) == '∧')

        prefs[word] = 100
        assert (conjunction_connector.rep(prefs=prefs) == 'et')

        prefs[en] = 500
        assert (conjunction_connector.rep(prefs=prefs) == 'and')

    def test_template(self, traditional_formula, infix_formula, prefs):
        infix = pu.RendererForStringTemplate(
            string_template='{{ arguments[0] }} {{ connector }} {{ arguments[1] }}',
            options=(infix_formula,))
        traditional = pu.RendererForStringTemplate(
            string_template='{{ connector }}({% for argument in arguments %}{{ argument }}{% if not loop.last %}, {% endif %}{% endfor %})',
            options=(traditional_formula,))
        rep = pu.AbstractRepresentation(uid=pu.create_uid('rep'), renderers=(infix, traditional,))

        prefs[traditional_formula] = 10
        prefs[infix_formula] = 20

        assert (rep.rep(prefs=prefs, variables={'connector': 'and', 'arguments': ('a', 'b',)}) == 'a and b')

        prefs[traditional_formula] = 20
        prefs[infix_formula] = 10

        assert (rep.rep(prefs=prefs,
                        variables={'connector': 'f', 'arguments': ('a', 'b', 'c', 'd',)}) == 'f(a, b, c, d)')
