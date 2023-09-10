from unittest import TestCase
import punctilious as pu


class TestText(TestCase):

    def test_1(self):
        pangram = 'The quick brown fox jumps over the lazy dog 0123456789!'
        compo = pu.ComposableText(plaintext=pangram)
        self.assertEqual(pangram, compo.rep(encoding=pu.encodings.plaintext))
        self.assertEqual(pangram, compo.rep(encoding=pu.encodings.unicode))

    def test_styled_text(self):
        pangram = 'The quick brown fox jumps over the lazy dog 0123456789!'
        x = pu.SansSerifBold(pangram)
        x_plaintext = x.rep(encoding=pu.encodings.plaintext)
        self.assertEqual('The quick brown fox jumps over the lazy dog 0123456789!', x_plaintext)
        x_unicode = x.rep(encoding=pu.encodings.unicode)
        self.assertEqual(
            '𝗧𝗵𝗲 𝗾𝘂𝗶𝗰𝗸 𝗯𝗿𝗼𝘄𝗻 𝗳𝗼𝘅 𝗷𝘂𝗺𝗽𝘀 𝗼𝘃𝗲𝗿 𝘁𝗵𝗲 𝗹𝗮𝘇𝘆 𝗱𝗼𝗴 𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵!', x_unicode)
        x_latex = x.rep(encoding=pu.encodings.latex)
        self.assertEqual(
            '\\boldsymbol\\mathsf{The quick brown fox jumps over the lazy dog 0123456789!}}',
            x_latex)
        x = pu.ComposableText(pangram)
        self.assertEqual('The quick brown fox jumps over the lazy dog 0123456789!',
            x.rep(pu.encodings.plaintext))
        self.assertEqual('The quick brown fox jumps over the lazy dog 0123456789!', x.rep(
            pu.encodings.unicode))  # self.assertEqual('\\mathnormal{The quick brown fox jumps over the lazy dog 0123456789!}',  #    x.rep(pu.encodings.latex))  # x = pu.ComposableText(pangram, pu.text_styles.double_struck)  # self.assertEqual('The quick brown fox jumps over the lazy dog 0123456789!',  #    x.rep(pu.encodings.plaintext))  # self.assertEqual(  #    '𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡!', x.rep(  #        pu.encodings.unicode))  # self.assertEqual('\\mathbb{The quick brown fox jumps over the lazy dog 0123456789!}',  #    x.rep(pu.encodings.latex))

    def test_equality(self):
        t1 = pu.ComposableText(plaintext='foo')
        t2 = pu.ComposableText(plaintext='foo', unicode='bar')
        self.assertNotEqual(t1, t2)
        self.assertEqual(t2, t2)
        t3 = pu.ComposableText(unicode='bar')
        self.assertNotEqual(t1, t3)
        self.assertNotEqual(t2, t3)
        self.assertEqual(t3,
            t3)  # t4 = pu.ComposableText(unicode='bar', text_style=pu.text_styles.double_struck)  # self.assertNotEqual(t1, t4)  # self.assertNotEqual(t2, t4)  # self.assertNotEqual(t3, t4)  # self.assertEqual(t4, t4)
