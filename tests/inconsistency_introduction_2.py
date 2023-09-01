from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction2(TestCase):
    def test_inconsistency_introduction_2(self):
        import sample.code.inconsistency_introduction_2 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        inc_proof: pu.InferredStatement = test.inc_proof
        self.assertIs(pu.consistency_values.proved_inconsistent, t1.consistency)
        self.assertTrue(inc_proof.is_formula_syntactically_equivalent_to(u.r.inc(t1)))
        self.assertEqual('𝐼𝑛𝑐(𝒯₁)', inc_proof.rep_formula(encoding=pu.encodings.unicode))