from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestSerifNormal(TestCase):
    def test_serif_normal(self):
        compo = pu.SerifNormal(plaintext=random_data.pangram1)

        self.assertEqual('the quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext, cap=False))
        self.assertEqual('The quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual('the quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.unicode_extended))
        self.assertEqual('\\mathnormal{the quick brown fox jumps over the lazy dog. 0123456789!}',
                         compo.rep(encoding=pu.encodings.latex))
