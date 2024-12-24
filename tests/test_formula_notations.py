import pytest
import punctilious as pu


class TestFormulaNotations:
    def test_infix_notation(self):
        prefs = pu.OptionsPreferences()
        tag = pu.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100
        assert pu.formula_notations.infix_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)},
            config=prefs) == 'x f y'

    def test_formula_notation(self):
        prefs = pu.OptionsPreferences()
        tag = pu.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ()},
            config=prefs) == 'f()'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)},
            config=prefs) == 'f(x)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)},
            config=prefs) == 'f(x, y)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y', 'z',)},
            config=prefs) == 'f(x, y, z)'

        tag = pu.Option('technical_language', 'latex_math')
        prefs[tag] = 200

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)},
            config=prefs) == 'f\\left(x\\right)'

    def test_prefix_notation(self):
        prefs = pu.OptionsPreferences()
        tag = pu.Option('technical_language', 'unicode_basic')
        prefs[tag] = 100

        assert pu.formula_notations.prefix_formula.rep(
            variables={'connector': '++', 'argument': ('x',)},
            config=prefs) == '++x'
        pass
