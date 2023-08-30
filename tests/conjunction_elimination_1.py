from unittest import TestCase
import punctilious as pu
import random_data


class TestConjunctionElimination1(TestCase):
    def test_ce1(self):
        import sample.code.conjunction_elimination_1 as test
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        r1: pu.Relation = test.r1
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(r1(o1, o2)))
        self.assertEqual('r1(o1, o2)', proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₂)', proposition_of_interest.rep_formula(pu.encodings.unicode))
