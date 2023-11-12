from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestModusTollens(TestCase):

    def test_modus_tollens_without_variable(self):
        import sample.sample_modus_tollens as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(phi=u.c1.lnot(r1(o1, o2))))
        self.assertEqual('not(r1(o1, o2))', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.modus_tollens.infer_formula_statement(p_implies_q=o3 | u.c1.implies | o2, not_q=o2)
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.modus_tollens.infer_formula_statement(p_implies_q=o3 | u.c1.implies | o2, not_q=u.c1.lnot(o2))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)
