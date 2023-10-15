from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


# TODO: Proof by refutation: design test
class TestProofByRefutation2(TestCase):
    def test_proof_by_refutation_2(self):
        import sample.sample_proof_by_refutation_2 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        h: pu.Hypothesis = test.h
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        pass
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to(o2=o1 | u.r.neq | o2))
        self.assertEqual('(o1 neq o2)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑜₁ ≠ 𝑜₂)', proposition_of_interest.rep_formula(pu.encodings.unicode))
