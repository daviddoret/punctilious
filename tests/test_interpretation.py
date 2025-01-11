import pytest
import punctilious as pu
from test_shared_library import create_atomic_connector


@pytest.fixture
def prefs():
    prefs = pu.rpr.Preferences()
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
        prefs = pu.representation.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 1
        prefs[pu.options.technical_language.unicode_extended] = 2
        prefs[pu.options.technical_language.latex_math] = pu.representation.get_forbidden()

        p = create_atomic_connector('P')
        q = create_atomic_connector('Q')
        r = create_atomic_connector('R')
        # weird = create_atomic_connector('weird')
        lnot = pu.operators_1.negation
        land = pu.operators_1.conjunction
        f = pu.declare_function('f')
        g = pu.declare_function('g')
        atomic_connectors = {'P': p, 'Q': q, 'R': r}
        prefix_connectors = {}
        infix_connectors = {'and': land}
        function_connectors = {'not': lnot, 'f': f, 'g': g}
        postfix_connectors = {}

        uid = pu.ids.UniqueIdentifier(slug='test', uuid='f75433aa-3d3c-43ae-8387-421c25772ba1')

        # Output the parsed structure
        interpreter = pu.interpretation.Interpret(
            uid=uid,
            atomic_connectors=atomic_connectors,
            prefix_connectors=prefix_connectors,
            infix_connectors=infix_connectors,
            function_connectors=function_connectors,
            postfix_connectors=postfix_connectors)

        input_string = "P"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == 'P'
        input_string = "not(P)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬P'
        input_string = "f(P)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '𝑓(P)'
        input_string = "P and Q"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == 'P ∧ Q'
        input_string = "(P and Q)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == 'P ∧ Q'
        input_string = "(P and Q) and (Q and P)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '(P ∧ Q) ∧ (Q ∧ P)'
        input_string = "not(not(P))"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬(¬P)'
        input_string = "not(not(f(P) and Q) and (Q and P))"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬((¬(𝑓(P) ∧ Q)) ∧ (Q ∧ P))'

    def test_interpretation_2(self):
        prefs = pu.representation.Preferences()
        prefs[pu.options.technical_language.unicode_basic] = 1
        prefs[pu.options.technical_language.unicode_extended] = 2
        prefs[pu.options.technical_language.latex_math] = pu.representation.get_forbidden()

        interpreter = pu.default_interpreter.default_interpreter

        pass
        input_string = "𝑃"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '𝑃'
        input_string = "¬𝑃"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬𝑃'
        input_string = "¬(𝑃)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬𝑃'
        input_string = "𝑃 ∧ 𝑄"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '𝑃 ∧ 𝑄'
        input_string = "(𝑃 ∧ 𝑄)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '𝑃 ∧ 𝑄'
        input_string = "(𝑃 ∧ 𝑄) ∧ (𝑄 ∧ 𝑃)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '(𝑃 ∧ 𝑄) ∧ (𝑄 ∧ 𝑃)'
        input_string = "¬(¬ 𝑃)"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬(¬𝑃)'
        input_string = "¬(¬((𝑃 ∧ 𝑄) ∧ (𝑄 ∧ 𝑃)))"
        assert interpreter.interpret_formula(input_string).represent(prefs=prefs) == '¬(¬((𝑃 ∧ 𝑄) ∧ (𝑄 ∧ 𝑃)))'
