from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestSansSerifBold(TestCase):
    def test_sans_serif_bold(self):
        compo = pu.SansSerifBold(plaintext=random_data.pangram1)

        self.assertEqual('the quick brown fox jumps over the lazy dog. 0123456789!',
                         compo.rep(encoding=pu.encodings.plaintext))
        self.assertEqual(
            '𝘁𝗵𝗲 𝗾𝘂𝗶𝗰𝗸 𝗯𝗿𝗼𝘄𝗻 𝗳𝗼𝘅 𝗷𝘂𝗺𝗽𝘀 𝗼𝘃𝗲𝗿 𝘁𝗵𝗲 𝗹𝗮𝘇𝘆 𝗱𝗼𝗴. 𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵!',
            compo.rep(encoding=pu.encodings.unicode_extended))
        self.assertEqual(
            '\\boldsymbol\\mathsf{the quick brown fox jumps over the lazy dog. 0123456789!}}',
            compo.rep(encoding=pu.encodings.latex))
