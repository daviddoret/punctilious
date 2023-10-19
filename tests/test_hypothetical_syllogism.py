from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestHypotheticalSyllogism(TestCase):

    def test_hypothetical_syllogism(self):
        import sample.sample_hypothetical_syllogism as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=r1(o1, o2) | u.r.implies | r1(o3, o1)))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.hypothetical_syllogism.infer_formula_statement(p_implies_q=o3 | u.r.implies | o2,
                q_implies_r=o1 | u.r.implies | o2)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.hypothetical_syllogism.infer_formula_statement(p_implies_q=o3 | u.r.implies | o2,
                q_implies_r=o2 | u.r.implies | o1)
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
