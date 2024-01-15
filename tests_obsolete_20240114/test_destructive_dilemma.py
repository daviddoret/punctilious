from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDestructiveDilemma(TestCase):
    def test_destructive_dilemma(self):
        import sample.sample_destructive_dilemma as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        o4: pu.SimpleObjct = test.o4
        theory_axiom: pu.AxiomInclusion = test.theory_axiom
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            phi=u.c1.lnot(o1) | u.c1.lor | u.c1.lnot(o3)))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.destructive_dilemma.infer_formula_statement(p_implies_q=o1 | u.c1.implies | o2,
                r_implies_s=o3 | u.c1.implies | o4, not_q_or_not_s=o1 | u.c1.lor | o4)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Syntax error 2
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.destructive_dilemma.infer_formula_statement(p_implies_q=o2 | u.c1.implies | o1,
                r_implies_s=o3 | u.c1.implies | o4, not_q_or_not_s=u.c1.lnot(o1) | u.c1.lor | o4)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.destructive_dilemma.infer_formula_statement(p_implies_q=o2 | u.c1.implies | o1,
                r_implies_s=o3 | u.c1.implies | o4, not_q_or_not_s=u.c1.lnot(o1) | u.c1.lor | u.c1.lnot(o4))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)
