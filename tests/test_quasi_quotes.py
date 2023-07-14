from unittest import TestCase
import punctilious as pu
import random_data


class TestQuasiQuotes(TestCase):
    def test_quasi_quotes(self):
        # TODO: Extend testing to latex math
        b1 = pu.QuasiQuotation()
        self.assertEqual('""',
                         b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('⌜⌝',
                         b1.rep(encoding=pu.encodings.unicode))
        b1.append(pu.ComposableText(plaintext='plaintext content', unicode='unicode content'))
        self.assertEqual('"plaintext content"',
                         b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('⌜unicode content⌝',
                         b1.rep(encoding=pu.encodings.unicode))
