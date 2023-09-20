from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


# TODO: Proof by refutation: design test
class TestProofByRefutation1(TestCase):
    def test_proof_by_refutation_1(self):
        import sample.sample_proof_by_refutation_1 as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        f: pu.Relation = test.f
        h: pu.Relation = test.h
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(
            proposition_of_interest.is_formula_syntactically_equivalent_to(o2=u.r.lnot(f(o1, o3))))
        self.assertEqual('not(f1(o1, o3))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('¬(𝑓₁(𝑜₁, 𝑜₃))', proposition_of_interest.rep_formula(pu.encodings.unicode))
