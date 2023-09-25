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
        phi = u.f(r1, o1)
        t = u.declare_theory()
        a = t.include_axiom(a=u.declare_axiom(natural_language='Dummy axiom for testing purposes'))
        t.i.axiom_interpretation.infer_formula_statement(axiom=a, formula=phi)
        phi1_formula = pu.validate_formula_statement(t=t, input_value=u.f(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_formula))
        phi1_tuple = pu.validate_formula_statement(t=t, input_value=(r1, o1))
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_tuple))
        phi1_prefix = pu.validate_formula_statement(t=t, input_value=r1 ^ o1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_prefix))
        phi1_postfix = pu.validate_formula_statement(t=t, input_value=o1 & r1)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi1_postfix))
        phi_form_ok_1 = pu.validate_formula_statement(t=t, input_value=phi, form=phi)
        self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        # Successful form validations
        with u.v('x') as x:
            phi_form_ok_1 = pu.validate_formula_statement(t=t, input_value=phi, form=(r1, x),
                mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        with u.v('x') as x:
            phi_form_ok_1 = pu.validate_formula_statement(t=t, input_value=phi, form=(x, o1),
                mask=[x])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        with u.v('x') as x, u.v('y') as y:
            phi_form_ok_1 = pu.validate_formula_statement(t=t, input_value=phi, form=(x, y),
                mask=[x, y])
            self.assertTrue(phi.is_formula_syntactically_equivalent_to(phi_form_ok_1))
        # Failed form validations
        with self.assertRaises(pu.PunctiliousException):
            with u.v('x') as x:
                pu.validate_formula_statement(t=t, input_value=phi, form=(r2, x), mask=[x])
        with self.assertRaises(pu.PunctiliousException):
            with u.v('x') as x:
                pu.validate_formula_statement(t=t, input_value=phi, form=(x, o2), mask=[x])
        # Inconsistent relation universe
        with self.assertRaises(pu.PunctiliousException):
            pu.validate_formula_statement(t=t, input_value=(r1_in_u2, o1))
        # Inconsistent parameter universe
        with self.assertRaises(pu.PunctiliousException):
            pu.validate_formula_statement(t=t, input_value=(r1, o1_in_u2))
        # Well-formed formula but not valid formula-statement
        with self.assertRaises(pu.PunctiliousException):
            pu.validate_formula_statement(t=t, input_value=(r1, o2))
