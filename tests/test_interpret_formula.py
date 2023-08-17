from unittest import TestCase
import punctilious as pu
import random_data


class TestInterpretFormula(TestCase):
    def test_interpret_binary_infix_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.infix, symbol='*', auto_index=False)
        t = u.t()
        self.assertEqual('(o1 * o2)', u.f(r1, o1, o2).rep_formula())
        self.assertEqual('(o1 * o2)',
            pu.interpret_formula(u=u, arity=2, argument=(r1, o1, o2)).rep_formula())
        self.assertEqual('(o1 * o2)',
            pu.interpret_formula(u=u, arity=2, argument=o1 | r1 | o2).rep_formula())

    def test_interpret_binary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.function_call, symbol='*',
            auto_index=False)
        t = u.t()
        self.assertEqual('*(o1, o2)', u.f(r1, o1, o2).rep_formula())
        self.assertEqual('*(o1, o2)',
            pu.interpret_formula(u=u, arity=2, argument=(r1, o1, o2)).rep_formula())
        self.assertEqual('*(o1, o2)',
            pu.interpret_formula(u=u, arity=2, argument=o1 | r1 | o2).rep_formula())
