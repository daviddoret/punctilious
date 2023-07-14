from unittest import TestCase
import punctilious as pu
import random_data


class TestSansSerifNormal(TestCase):
    def test_sans_serif_normal(self):
        # TODO: Extend testing to latex math
        compo = pu.ComposableSansSerifNormal(plaintext='hello world')

        self.assertEqual('hello world', compo.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('𝗁𝖾𝗅𝗅𝗈 𝗐𝗈𝗋𝗅𝖽', compo.rep(encoding=pu.encodings.unicode))
        self.assertEqual('\\mathsf{hello world}', compo.rep(encoding=pu.encodings.latex_math))
