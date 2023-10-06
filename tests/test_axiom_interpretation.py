from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestAxiomInterpretation(TestCase):

    def test_axiom_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.unicode
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        # Prepare the universe-of-discourse
        a1 = u.declare_axiom(natural_language=random_data.random_sentence())
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, signal_proposition=True)
        r2 = u.r.declare(arity=1)
        phi1 = u.f(r1, o1, o2)
        # Elaborate the theory
        t = u.t()
        a2 = t.include_axiom(a1)
        p1 = t.i.axiom_interpretation.infer_formula_statement(a2, phi1)
        self.assertTrue(
            p1.valid_proposition.is_formula_syntactically_equivalent_to(u.f(r1, o1, o2)))
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t.i.axiom_interpretation.infer_formula_statement(a2, r2(o1))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
