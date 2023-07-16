from unittest import TestCase
import punctilious as pu
import random_data


class TestUniverseOfDiscourse(TestCase):
    def test_universe_of_discourse(self):
        u1 = pu.declare_universe_of_discourse()
        self.assertEqual('U1', u1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒰₁', u1.rep(encoding=pu.encodings.unicode))
        self.assertEqual('Let U1 be a universe-of-discourse.\n\n',
                         u1.rep_declaration(encoding=pu.encodings.plaintext))
        self.assertEqual('Let 𝒰₁ be a universe-of-discourse.\n\n',
                         u1.rep_declaration(encoding=pu.encodings.unicode))
        u2 = pu.declare_universe_of_discourse(name='my universe')
        self.assertEqual('U2', u2.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒰₂', u2.rep(encoding=pu.encodings.unicode))
        self.assertEqual('Let U2 be a universe-of-discourse.\n\n',
                         u2.rep_declaration(encoding=pu.encodings.plaintext))
        self.assertEqual('Let 𝒰₂ be a universe-of-discourse.\n\n',
                         u2.rep_declaration(encoding=pu.encodings.unicode))
