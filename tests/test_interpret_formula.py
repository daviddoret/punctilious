from unittest import TestCase
import punctilious as pu


class TestInterpretFormula(TestCase):

    def test_interpret_unary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        r1 = u.r.declare(arity=1, formula_rep=pu.Formula.function_call, symbol='*',
                         auto_index=False)
        self.assertEqual('*(o1)', u.f(r1, o1).rep_formula())
        self.assertEqual('*(o1)',
                         pu.interpret_formula(u=u, arity=1, flexible_formula=(r1, o1)).rep_formula())
        self.assertEqual('*(o1)',
                         pu.interpret_formula(u=u, arity=None, flexible_formula=(r1, o1)).rep_formula())
        self.assertEqual('*(o1)',
                         pu.interpret_formula(u=u, arity=None, flexible_formula=r1 ^ o1).rep_formula())
        self.assertEqual('*(o1)',
                         pu.interpret_formula(u=u, arity=None, flexible_formula=o1 & r1).rep_formula())

    def test_interpret_binary_infix_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.infix, symbol='*', auto_index=False)
        self.assertEqual('(o1 * o2)', u.f(r1, o1, o2).rep_formula())
        self.assertEqual('(o1 * o2)',
                         pu.interpret_formula(u=u, arity=2, flexible_formula=(r1, o1, o2)).rep_formula())
        self.assertEqual('(o1 * o2)',
                         pu.interpret_formula(u=u, arity=2, flexible_formula=o1 | r1 | o2).rep_formula())

    def test_interpret_binary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.function_call, symbol='*',
                         auto_index=False)
        self.assertEqual('*(o1, o2)', u.f(r1, o1, o2).rep_formula())
        self.assertEqual('*(o1, o2)',
                         pu.interpret_formula(u=u, arity=2, flexible_formula=(r1, o1, o2)).rep_formula())
        self.assertEqual('*(o1, o2)',
                         pu.interpret_formula(u=u, arity=2, flexible_formula=o1 | r1 | o2).rep_formula())
