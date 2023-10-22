from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestConstructiveDilemma(TestCase):
    def test_constructive_dilemma(self):
        import sample.sample_constructive_dilemma as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        o4: pu.SimpleObjct = test.o4
        theory_axiom: pu.AxiomInclusion = test.theory_axiom
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to(phi=o2 | u.r.lor | o4))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.constructive_dilemma.infer_formula_statement(p_implies_q=o1 | u.r.iff | o2,
                r_implies_s=o3 | u.r.implies | o4, p_or_r=o1 | u.r.lor | o4)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Syntax error 2
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.constructive_dilemma.infer_formula_statement(p_implies_q=o2 | u.r.implies | o1,
                r_implies_s=o3 | u.r.implies | o4, p_or_r=o1 | u.r.lor | o4)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.constructive_dilemma.infer_formula_statement(p_implies_q=o2 | u.r.implies | o1,
                r_implies_s=o3 | u.r.implies | o4, p_or_r=o2 | u.r.lor | o3)
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
