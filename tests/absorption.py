from unittest import TestCase
import punctilious as pu


class TestAbsorption(TestCase):
    def test_absorption_1(self):
        import sample.code.absorption as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            (r1(o1, o2) | u.r.implies | (r1(o1, o2) | u.r.land | r2(o3)))))
        self.assertEqual('(r1(o1, o2) ==> (r1(o1, o2) and r2(o3)))',
                         proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ⟹ (𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃)))',
                         proposition_of_interest.rep_formula(pu.encodings.unicode))
