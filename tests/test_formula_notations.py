import pytest
import punctilious as pu


class TestFormulaNotations:
    def test_infix_notation(self):
        assert pu.formula_notations.infix_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)}) == 'x f y'

    def test_formula_notation(self):
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ()}) == 'f()'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)}) == 'f(x)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y',)}) == 'f(x, y)'
        assert pu.formula_notations.function_formula.rep(
            variables={'connector': 'f', 'argument': ('x', 'y', 'z',)}) == 'f(x, y, z)'

    def test_prefix_notation(self):
        assert pu.formula_notations.prefix_formula.rep(
            variables={'connector': 'f', 'argument': ('x',)}) == 'f x'
        pass
