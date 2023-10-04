from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestConjunctionIntroduction(TestCase):
    def test_ci(self):
        import sample.sample_conjunction_introduction as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        theory_axiom: pu.AxiomInclusion = test.theory_axiom
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=r1(o1, o2) | u.r.land | r2(o3)))
        self.assertEqual('(r1(o1, o2) and r2(o3))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃))',
            proposition_of_interest.rep_formula(pu.encodings.unicode))
        # Syntax error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.conjunction_introduction.infer_formula_statement(p=o2, q=r1(o1, o3))
        self.assertIs(pu.error_codes.error_002_inference_premise_syntax_error,
            error.exception.error_code)
        # Validity error
        with self.assertRaises(pu.PunctiliousException) as error:
            t1.i.conjunction_introduction.infer_formula_statement(p=r1(o1, o2), q=r1(o1, o3))
        self.assertIs(pu.error_codes.error_003_inference_premise_validity_error,
            error.exception.error_code)
