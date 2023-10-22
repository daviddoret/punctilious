from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDisjunctionIntroduction2(TestCase):

    def test_di2(self):
        import sample.sample_disjunction_introduction_2 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryDerivation = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            phi=r1(o1, o2) | u.r.lor | r2(o3)))
        self.assertEqual('(r1(o1, o2) or r2(o3))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∨ 𝑟₂(𝑜₃))',
            proposition_of_interest.rep_formula(pu.encodings.unicode))
        # Syntax error
        # r3: pu.Relation = u.r.declare(signal_proposition=False)
        # with self.assertRaises(pu.PunctiliousException) as error:
        #    t1.i.disjunction_introduction_2.infer_formula_statement(p=r1(o1, o2), q=t1)
        # self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
        #    error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.disjunction_introduction_2.infer_formula_statement(p=r2(o2), q=r2(o1))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
