from unittest import TestCase
import punctilious as pu


class TestUniverseOfDiscourse(TestCase):
    def test_universe_of_discourse(self):
        u1 = pu.create_universe_of_discourse()
        u1_plaintext = u1.nameset.rep_symbol(encoding=pu.encodings.plaintext)
        u1_unicode = u1.nameset.rep_symbol(encoding=pu.encodings.unicode_extended)
        self.assertEqual(f'Let "{u1_plaintext}" be a universe-of-discourse.',
                         u1.rep_creation(encoding=pu.encodings.plaintext))
        self.assertEqual(f'𝖫𝖾𝗍 ⌜{u1_unicode}⌝ 𝖻𝖾 𝖺 𝑢𝑛𝑖𝑣𝑒𝑟𝑠𝑒-𝑜𝑓-𝑑𝑖𝑠𝑐𝑜𝑢𝑟𝑠𝑒.',
                         u1.rep_creation(encoding=pu.encodings.unicode_extended))
        u2 = pu.create_universe_of_discourse()
        u2_plaintext = u2.nameset.rep_symbol(encoding=pu.encodings.plaintext)
        u2_unicode = u2.nameset.rep_symbol(encoding=pu.encodings.unicode_extended)
        self.assertEqual(f'Let "{u2_plaintext}" be a universe-of-discourse.',
                         u2.rep_creation(encoding=pu.encodings.plaintext))
        self.assertEqual(f'𝖫𝖾𝗍 ⌜{u2_unicode}⌝ 𝖻𝖾 𝖺 𝑢𝑛𝑖𝑣𝑒𝑟𝑠𝑒-𝑜𝑓-𝑑𝑖𝑠𝑐𝑜𝑢𝑟𝑠𝑒.',
                         u2.rep_creation(encoding=pu.encodings.unicode_extended))
