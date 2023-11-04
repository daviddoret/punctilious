from unittest import TestCase
import punctilious as pu


class TestValidateFormulaStatement(TestCase):

    def test_validate_statement_unary_function_call_formula(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        u2 = pu.UniverseOfDiscourse()
        o1 = u.o.declare(symbol='o', index=1)
        o1_in_u2 = u2.o.declare(symbol='o', index=1)
        o2 = u.o.declare()
        r1 = u.r.declare(arity=1, symbol='r', index=1, signal_proposition=True)
        r1_in_u2 = u2.r.declare(arity=1, symbol='r', index=1, signal_proposition=True)
        r2 = u.r.declare(arity=1, signal_proposition=True)
        phi = u.declare_compound_formula(r1, o1)
        t = u.declare_theory()
        a = t.include_axiom(a=u.declare_axiom(natural_language='Dummy axiom for testing purposes'))
        t.i.axiom_interpretation.infer_formula_statement(a=a, p=phi)
        _, phi1_formula, _ = pu.verify_formula_statement(t=t,
            input_value=u.declare_compound_formula(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi1_formula))
        _, phi1_tuple, _ = pu.verify_formula_statement(t=t, input_value=(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_tuple))
        _, phi1_prefix, _ = pu.verify_formula_statement(t=t, input_value=r1 ^ o1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi1_prefix))
        _, phi1_postfix, _ = pu.verify_formula_statement(t=t, input_value=o1 & r1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi1_postfix))
        _, phi_form_ok_1, _ = pu.verify_formula_statement(t=t, input_value=phi, form=phi)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi_form_ok_1))
        # Successful form validations
        with u.with_variable('x') as x:
            _, phi_form_ok_1, _ = pu.verify_formula_statement(t=t, input_value=phi, form=(r1, x),
                mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi_form_ok_1))
        with u.with_variable('x') as x:
            _, phi_form_ok_1, _ = pu.verify_formula_statement(t=t, input_value=phi, form=(x, o1),
                mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi_form_ok_1))
        with u.with_variable('x') as x, u.with_variable('y') as y:
            _, phi_form_ok_1, _ = pu.verify_formula_statement(t=t, input_value=phi, form=(x, y),
                mask=[x, y])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi=phi_form_ok_1))
        # Failed form validations
        with self.assertRaises(pu.PunctiliousException):
            with u.with_variable('x') as x:
                pu.verify_formula_statement(t=t, input_value=phi, form=(r2, x), mask=[x])
        with self.assertRaises(pu.PunctiliousException):
            with u.with_variable('x') as x:
                pu.verify_formula_statement(t=t, input_value=phi, form=(x, o2), mask=[x])
        # Inconsistent connective universe
        with self.assertRaises(pu.PunctiliousException):
            pu.verify_formula_statement(t=t, input_value=(r1_in_u2, o1))
        # Inconsistent parameter universe
        with self.assertRaises(pu.PunctiliousException):
            pu.verify_formula_statement(t=t, input_value=(r1, o1_in_u2))
        # Well-formed formula but not valid formula-statement
        with self.assertRaises(pu.PunctiliousException):
            pu.verify_formula_statement(t=t, input_value=(r1, o2))
