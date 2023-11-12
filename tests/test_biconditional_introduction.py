from unittest import TestCase
import punctilious as pu


class TestBiconditionalIntroduction(TestCase):

    def test_biconditional_introduction(self):
        import sample.sample_biconditional_introduction as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        biconditional_inference: pu.InferredStatement = test.biconditional_inference
        phi = (r1(o1, o2) | u.c1.biconditional | r2(o3))
        self.assertTrue(biconditional_inference.is_formula_syntactically_equivalent_to(phi))
        self.assertEqual('(r1(o1, o2) <==> r2(o3))',
            biconditional_inference.rep_formula(encoding=pu.encodings.plaintext))
