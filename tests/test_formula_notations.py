import pytest
import punctilious as pu


class TestFormulaNotations:
    def test_infix_notation(self):
        assert pu.formula_notations.infix_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)}) == 'x f y'

    def test_formula_notation(self):
        prefs = pu.TagsPreferences()

        tag = pu.Tag('technical_language', 'unicode_basic')
        prefs[tag] = 100

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ()}) == 'f()'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)}) == 'f(x)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)}) == 'f(x, y)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y', 'z',)}) == 'f(x, y, z)'

        tag = pu.Tag('technical_language', 'latex_math')
        prefs[tag] = 200

        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)},
            config=prefs) == 'f\\left(x\\right)'

    def test_prefix_notation(self):
        assert pu.formula_notations.prefix_formula.rep(
            variables={'connector': '++', 'argument': ('x',)}) == '++x'
        pass
