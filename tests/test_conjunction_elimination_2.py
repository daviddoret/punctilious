from unittest import TestCase
import punctilious as pu


class TestConjunctionElimination2(TestCase):
    def test_ce2(self):
        import sample.sample_conjunction_elimination_2 as test
        o3: pu.SimpleObjct = test.o3
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(o2=r2(o3)))
        self.assertEqual('r2(o3)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₂(𝑜₃)', proposition_of_interest.rep_formula(pu.encodings.unicode))
