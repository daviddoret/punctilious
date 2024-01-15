from unittest import TestCase
import punctilious as pu


class TestBiconditionalElimination1(TestCase):
    def test_be1(self):
        import sample.sample_biconditional_elimination_1 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to((r1(o1, o2) | u.c1.implies | r2(o3))))
        self.assertEqual('(r1(o1, o2) implies r2(o3))', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ⊃ 𝑟₂(𝑜₃))', proposition_of_interest.rep_formula(pu.encodings.unicode_extended))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.biconditional_elimination_1.infer_formula_statement(p_iff_q=r1(o1, o3))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error, error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.biconditional_elimination_1.infer_formula_statement(p_iff_q=o2 | u.c1.iff | o3)
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error, error.exception.error_code)
