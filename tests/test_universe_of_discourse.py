from unittest import TestCase
import punctilious as pu
import random_data


class TestUniverseOfDiscourse(TestCase):
    def test_universe_of_discourse(self):
        u1 = pu.declare_universe_of_discourse()
        self.assertEqual('U1', u1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒰₁', u1.rep(encoding=pu.encodings.unicode))
        self.assertEqual('Let U1 be a universe-of-discourse.',
                         u1.rep_declaration(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual('𝖫𝖾𝗍 𝒰₁ 𝖻𝖾 𝖺 𝑢𝑛𝑖𝑣𝑒𝑟𝑠𝑒-𝑜𝑓-𝑑𝑖𝑠𝑐𝑜𝑢𝑟𝑠𝑒.',
                         u1.rep_declaration(encoding=pu.encodings.unicode, cap=True))
        u2 = pu.declare_universe_of_discourse()
        self.assertEqual('U2', u2.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒰₂', u2.rep(encoding=pu.encodings.unicode))
        self.assertEqual('Let U2 be a universe-of-discourse.',
                         u2.rep_declaration(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual('𝖫𝖾𝗍 𝒰₂ 𝖻𝖾 𝖺 𝑢𝑛𝑖𝑣𝑒𝑟𝑠𝑒-𝑜𝑓-𝑑𝑖𝑠𝑐𝑜𝑢𝑟𝑠𝑒.',
                         u2.rep_declaration(encoding=pu.encodings.unicode, cap=True))
