from unittest import TestCase
import punctilious as pu
import random_data


class TestRelationDict(TestCase):
    def test_relation_dict(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        self.assertEqual('==>', u.r.implication.rep(pu.encodings.plaintext))
        self.assertEqual('⟹', u.r.implication.rep(pu.encodings.unicode))
        self.assertEqual('and', u.r.conjunction.rep(pu.encodings.plaintext))
        self.assertEqual('∧', u.r.conjunction.rep(pu.encodings.unicode))
        self.assertEqual('not', u.r.negation.rep(pu.encodings.plaintext))
        self.assertEqual('¬', u.r.negation.rep(pu.encodings.unicode))
