from unittest import TestCase
import punctilious as pu


class TestConnectiveDict(TestCase):
    def test_connective_dict(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        self.assertEqual('implies', u.c1.implication.rep(pu.encodings.plaintext))
        self.assertEqual('⊃', u.c1.implication.rep(pu.encodings.unicode_extended))
        self.assertEqual('and', u.c1.conjunction.rep(pu.encodings.plaintext))
        self.assertEqual('∧', u.c1.conjunction.rep(pu.encodings.unicode_extended))
        self.assertEqual('not', u.c1.negation.rep(pu.encodings.plaintext))
        self.assertEqual('¬', u.c1.negation.rep(pu.encodings.unicode_extended))
