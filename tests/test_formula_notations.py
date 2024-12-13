import pytest
import punctilious as pu


class TestFormulaNotations:
    def test_formula_notations(self):
        connector = 'f'
        argument = ('x', 'y',)
        variables = {'connector': connector, 'argument': argument}
        assert pu.formula_notations.infix_formula.rep(variables=variables) == 'x f y'
        assert pu.formula_notations.function_formula.rep(variables=variables) == 'f(x, y)'
        assert pu.formula_notations.prefix_formula.rep(variables=variables) == 'f x'
        pass
