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
        x = pu.ComposableText(pangram, text_style=pu.text_styles.serif_bold)
        x_plaintext = x.rep(encoding=pu.encodings.plaintext)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x_plaintext)
        x_unicode = x.rep(encoding=pu.encodings.unicode)
        self.assertEqual(
            '𝐓𝐡𝐞 𝐪𝐮𝐢𝐜𝐤 𝐛𝐫𝐨𝐰𝐧 𝐟𝐨𝐱 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠 𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗!',
            x_unicode)
        x_latex_math = x.rep(encoding=pu.encodings.latex_math)
        self.assertEqual(
            '\\mathbf{The quick brown fox jumps over the lazy dog 0123456789!}',
            x_latex_math)
        x = pu.ComposableText(pangram, text_style=pu.text_styles.serif_normal)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.rep(pu.encodings.plaintext))
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.rep(pu.encodings.unicode))
        self.assertEqual(
            '\\mathnormal{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.rep(pu.encodings.latex_math))
        x = pu.ComposableText(pangram, pu.text_styles.double_struck)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.rep(pu.encodings.plaintext))
        self.assertEqual(
            '𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡!',
            x.rep(pu.encodings.unicode))
        self.assertEqual(
            '\\mathbb{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.rep(pu.encodings.latex_math))

    def test_equality(self):
        t1 = pu.ComposableText(plaintext='foo')
        t2 = pu.ComposableText(plaintext='foo', unicode='bar')
        self.assertEqual(t1, t2)
        self.assertEqual(t2, t2)
        t3 = pu.ComposableText(unicode='bar')
        self.assertNotEqual(t1, t3)
        self.assertEqual(t2, t3)
        self.assertEqual(t3, t3)
        t4 = pu.ComposableText(unicode='bar', text_style=pu.text_styles.double_struck)
        self.assertNotEqual(t1, t4)
        self.assertNotEqual(t2, t4)
        self.assertNotEqual(t3, t4)
        self.assertEqual(t4, t4)
