from unittest import TestCase
import punctilious as pu


class TestTheoryElaborationSequence(TestCase):
    def test_theory_derivation(self):
        u1 = pu.UniverseOfDiscourse()
        u_plaintext = u1.nameset.rep_symbol(encoding=pu.encodings.plaintext)
        u_unicode = u1.nameset.rep_symbol(encoding=pu.encodings.unicode_extended)
        t1 = u1.t.declare()
        self.assertEqual('T1', t1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝒯₁', t1.rep(encoding=pu.encodings.unicode_extended))
        self.assertEqual(f'Let "T1" be a theory-derivation in {u_plaintext}.',
                         t1.rep_report(encoding=pu.encodings.plaintext))
        self.assertEqual(f'𝖫𝖾𝗍 ⌜𝒯₁⌝ 𝖻𝖾 𝖺 𝑡ℎ𝑒𝑜𝑟𝑦-𝑑𝑒𝑟𝑖𝑣𝑎𝑡𝑖𝑜𝑛 𝗂𝗇 {u_unicode}.',
                         t1.rep_report(encoding=pu.encodings.unicode_extended))
