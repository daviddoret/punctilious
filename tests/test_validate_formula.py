from unittest import TestCase
import punctilious as pu


class TestValidateFormula(TestCase):

    def test_validate_unary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        u2 = pu.UniverseOfDiscourse()
        o1 = u.o.declare(symbol='o', index=1)
        o1_in_u2 = u2.o.declare(symbol='o', index=1)
        o2 = u.o.declare()
        r1 = u.r.declare(arity=1, symbol='r', index=1)
        r1_in_u2 = u2.r.declare(arity=1, symbol='r', index=1)
        r2 = u.r.declare(arity=1)
        phi = u.f(r1, o1)
        _, phi1_formula, _ = pu.verify_formula(u=u, input_value=u.f(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_formula))
        _, phi1_tuple, _ = pu.verify_formula(u=u, input_value=(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_tuple))
        _, phi1_prefix, _ = pu.verify_formula(u=u, input_value=r1 ^ o1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_prefix))
        _, phi1_postfix, _ = pu.verify_formula(u=u, input_value=o1 & r1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_postfix))
        _, phi_form_ok_1, _ = pu.verify_formula(u=u, input_value=phi, form=phi)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        # Successful form validations
        with u.v('x') as x:
            _, phi_form_ok_1, _ = pu.verify_formula(u=u, input_value=phi, form=(r1, x), mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        with u.v('x') as x:
            _, phi_form_ok_1, _ = pu.verify_formula(u=u, input_value=phi, form=(x, o1), mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        with u.v('x') as x, u.v('y') as y:
            _, phi_form_ok_1, _ = pu.verify_formula(u=u, input_value=phi, form=(x, y), mask=[x, y])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        # Failed form validations
        with self.assertRaises(pu.PunctiliousException):
            with u.v('x') as x:
                pu.verify_formula(u=u, input_value=phi, form=(r2, x), mask=[x])
        with self.assertRaises(pu.PunctiliousException):
            with u.v('x') as x:
                pu.verify_formula(u=u, input_value=phi, form=(x, o2), mask=[x])
        # Inconsistent relation universe
        with self.assertRaises(pu.PunctiliousException):
            pu.verify_formula(u=u, input_value=(r1_in_u2, o1))
        # Inconsistent parameter universe
        with self.assertRaises(pu.PunctiliousException):
            pu.verify_formula(u=u, input_value=(r1, o1_in_u2))

    def test_validate_binary_infix_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.infix, symbol='*', auto_index=False)
        self.assertEqual('(o1 * o2)', u.f(r1, o1, o2).rep_formula())
        phi1: pu.Formula
        _, phi1, _ = pu.verify_formula(u=u, input_value=(r1, o1, o2))
        self.assertEqual('(o1 * o2)', phi1.rep_formula())
        phi2: pu.Formula
        _, phi2, _ = pu.verify_formula(u=u, input_value=o1 | r1 | o2)
        self.assertEqual('(o1 * o2)', phi2.rep_formula())

    def test_validate_binary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, formula_rep=pu.Formula.function_call, symbol='*',
            auto_index=False)
        self.assertEqual('*(o1, o2)', u.f(r1, o1, o2).rep_formula())
        phi1: pu.Formula
        _, phi1, _ = pu.verify_formula(u=u, input_value=(r1, o1, o2))
        self.assertEqual('*(o1, o2)', phi1.rep_formula(encoding=pu.encodings.plaintext))
        phi2: pu.Formula
        _, phi2, _ = pu.verify_formula(u=u, input_value=o1 | r1 | o2)
        self.assertEqual('*(o1, o2)', phi2.rep_formula(encoding=pu.encodings.plaintext))
