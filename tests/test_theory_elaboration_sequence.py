from unittest import TestCase
import punctilious as pu
import random_data


class TestTheoryElaborationSequence(TestCase):
    def test_theory_elaboration_sequence(self):
        u1 = pu.UniverseOfDiscourse()
        t1 = u1.declare_theory()
        self.assertEqual('T1', t1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒯₁', t1.rep(encoding=pu.encodings.unicode))
        self.assertEqual('Let T1 be a theory-elaboration-sequence in U1.',
            t1.rep_report(encoding=pu.encodings.plaintext))
        self.assertEqual('Let 𝒯₁ be a theory-elaboration-sequence in 𝒰₁.',
            t1.rep_report(encoding=pu.encodings.unicode))
