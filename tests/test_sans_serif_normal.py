from unittest import TestCase
import punctilious as pu
import random_data


class TestSansSerifNormal(TestCase):
    def test_sans_serif_normal(self):
        compo = pu.SansSerifNormal(plaintext=random_data.pangram1)

        self.assertEqual('the quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext))
        self.assertEqual(
            '𝗍𝗁𝖾 𝗊𝗎𝗂𝖼𝗄 𝖻𝗋𝗈𝗐𝗇 𝖿𝗈𝗑 𝗃𝗎𝗆𝗉𝗌 𝗈𝗏𝖾𝗋 𝗍𝗁𝖾 𝗅𝖺𝗓𝗒 𝖽𝗈𝗀. 𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫!',
            compo.rep(encoding=pu.encodings.unicode))
        self.assertEqual('\\mathsf{the quick brown fox jumps over the lazy dog. 0123456789!}',
                         compo.rep(encoding=pu.encodings.latex))
