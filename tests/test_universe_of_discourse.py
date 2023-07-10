from unittest import TestCase
import punctilious as pu
import random_data


class TestUniverseOfDiscourse(TestCase):
    def test_universe_of_discourse(self):
        u1 = pu.UniverseOfDiscourse()
        self.assertEqual('U1', u1.rep(text_format=pu.text_formats.plaintext))
        self.assertEqual('𝒰₁', u1.rep(text_format=pu.text_formats.unicode))
        self.assertEqual('Let U1 be a universe-of-discourse.\n\n',
                         u1.rep_declaration(text_format=pu.text_formats.plaintext))
        self.assertEqual('Let 𝒰₁ be a universe-of-discourse.\n\n',
                         u1.rep_declaration(text_format=pu.text_formats.unicode))
        u2 = pu.UniverseOfDiscourse()
