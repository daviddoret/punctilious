import pytest
import punctilious as pu
from test_shared_library import create_atomic_connector
import punctilious.interpreters as interpreters


@pytest.fixture
def prefs():
    prefs = pu.Preferences()
    prefs[pu.options.language.en] = 6
    prefs[pu.options.language.fr] = 9
    prefs[pu.options.connector_representation.symbol] = 100
    prefs[pu.options.connector_representation.word] = 1
    return prefs


@pytest.fixture
def reps():
    d: dict = pu.get_yaml_from_package(path='punctilious.data.representations', resource='operators_1.yaml')
    raw = d.get('representations', [])
    return pu.ensure_abstract_representations(o=raw)


@pytest.fixture
def conjunction_connector(reps):
    return reps[0]


class TestInterpretation:
    def test_interpretation_1(self):
        """test with a manually designed interpreter.
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
        interpreter = pu.Interpreter(
            variable_connectors={},
            atomic_connectors=atomic_connectors,
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

    def test_interpretation_2(self):
        interpreter = interpreters.generate_interpreter()
        pass
        input_string = "P"
        assert str(interpreter.interpret(input_string)) == 'P'
        input_string = "¬P"
        assert str(interpreter.interpret(input_string)) == '¬P'
        input_string = "¬(P)"
        assert str(interpreter.interpret(input_string)) == '¬P'
        input_string = "P ∧ Q"
        assert str(interpreter.interpret(input_string)) == 'P ∧ Q'
        input_string = "(P ∧ Q)"
        assert str(interpreter.interpret(input_string)) == 'P ∧ Q'
        input_string = "(P ∧ Q) ∧ (Q ∧ P)"
        assert str(interpreter.interpret(input_string)) == '(P ∧ Q) ∧ (Q ∧ P)'
        input_string = "¬(¬ P)"
        assert str(interpreter.interpret(input_string)) == '¬(¬P)'
        input_string = "¬(¬((P ∧ Q) ∧ (Q ∧ P)))"
        assert str(
            interpreter.interpret(input_string)) == '¬(¬((P ∧ Q) ∧ (Q ∧ P)))'
