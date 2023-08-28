from unittest import TestCase
import punctilious as pu
import random_data


class TestBiconditionalIntroduction(TestCase):

    def test_biconditional_introduction(self):
        import sample.code.biconditional_introduction as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        biconditional_inference: pu.InferredStatement = test.biconditional_inference
        phi = (r1(o1, o2) | u.r.biconditional | r2(o3))
        self.assertTrue(biconditional_inference.is_formula_syntactically_equivalent_to(phi))
        self.assertEqual('(r1(o1, o2) <==> r2(o3))',
            biconditional_inference.rep_formula(encoding=pu.encodings.plaintext))
