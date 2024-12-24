import pytest
import punctilious as pu
from test_shared_library import create_atomic_connector


@pytest.fixture
def en():
    return pu.Tag('language', 'en')


@pytest.fixture
def fr():
    return pu.Tag('language', 'fr')


@pytest.fixture
def symbol():
    return pu.Tag('connector_representation', 'symbol')


@pytest.fixture
def word():
    return pu.Tag('connector_representation', 'word')


@pytest.fixture
def traditional_formula():
    return pu.Tag('layout', 'traditional_formula')


@pytest.fixture
def infix_formula():
    return pu.Tag('layout', 'infix_formula')


@pytest.fixture
def unicode_basic():
    return pu.Tag('technical_language', 'unicode_basic')


@pytest.fixture
def unicode_extended():
    return pu.Tag('technical_language', 'unicode_extended')


@pytest.fixture
def latex_math():
    return pu.Tag('technical_language', 'latex_math')


@pytest.fixture
def prefs(en, fr, symbol, word):
    prefs = pu.TagsPreferences()
    prefs[en] = 6
    prefs[fr] = 9
    prefs[symbol] = 100
    prefs[word] = 1
    return prefs


@pytest.fixture
def reps():
    d: dict = pu.get_yaml_from_package(path='punctilious.data.representations', resource='operators_1.yaml')
    raw = d.get('representations', [])
    return pu.ensure_abstract_representations(o=raw)


@pytest.fixture
def conjunction_connector(reps):
    return reps[0]


class TestRepresentation:
    def test_representation(self, en, fr, word, symbol, prefs, unicode_basic, unicode_extended, latex_math):
        """Test of representation with multiple string-constant renderers.
        """

        p = create_atomic_connector('P')
        q = create_atomic_connector('Q')
        r = create_atomic_connector('R')
        # weird = create_atomic_connector('weird')
        lnot = pu.operators_1.negation
        land = pu.operators_1.conjunction
        f = pu.declare_function('f')
        g = pu.declare_function('g')
        atomic_connectors = {'P': p, 'Q': q, 'R': r}
        prefix_connectors = {'not': lnot}
        infix_connectors = {'and': land}
        function_connectors = {'not': lnot, 'f': f, 'g': g}

        # Output the parsed structure
        interpreter = pu.Interpreter(atomic_connectors=atomic_connectors,
                                     prefix_connectors=prefix_connectors,
                                     infix_connectors=infix_connectors,
                                     function_connectors=function_connectors)
        input_string = "P"
        assert str(interpreter.interpret(input_string)) == 'P'
        input_string = "not P"
        assert str(interpreter.interpret(input_string)) == '¬P'
        input_string = "f(P)"
        assert str(interpreter.interpret(input_string)) == 'f(P)'
        input_string = "P and Q"
        assert str(interpreter.interpret(input_string)) == 'P ∧ Q'
        input_string = "(P and Q)"
        assert str(interpreter.interpret(input_string)) == 'P ∧ Q'
        input_string = "(P and Q) and (Q and P)"
        assert str(interpreter.interpret(input_string)) == '(P ∧ Q) ∧ (Q ∧ P)'
        input_string = "not(not P)"
        assert str(interpreter.interpret(input_string)) == '¬(¬P)'
        input_string = "not(not (f(P) and Q) and (Q and P))"
        assert str(
            interpreter.interpret(input_string)) == '¬((¬(f(P) ∧ Q)) ∧ (Q ∧ P))'
