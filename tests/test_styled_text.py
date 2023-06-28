from unittest import TestCase
import punctilious as pu


class TestStyledText(TestCase):
    def test_styled_text(self):
        pangram = 'The quick brown fox jumps over the lazy dog 0123456789!'
        x = pu.StyledText(pangram, text_style=pu.text_styles.serif_bold)
        x_plaintext = x.repr(text_format=pu.text_formats.plaintext)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x_plaintext)
        x_unicode = x.repr(text_format=pu.text_formats.unicode)
        self.assertEqual(
            '𝐓𝐡𝐞 𝐪𝐮𝐢𝐜𝐤 𝐛𝐫𝐨𝐰𝐧 𝐟𝐨𝐱 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠 𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗!',
            x_unicode)
        x_latex_math = x.repr(text_format=pu.text_formats.latex_math)
        self.assertEqual(
            '\\mathbf{The quick brown fox jumps over the lazy dog 0123456789!}',
            x_latex_math)
        x = pu.StyledText(pangram, text_style=pu.text_styles.serif_normal)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(pu.text_formats.plaintext))
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(pu.text_formats.unicode))
        self.assertEqual(
            '\\mathnormal{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.repr(pu.text_formats.latex_math))
        x = pu.StyledText(pangram, pu.text_styles.double_struck)
        self.assertEqual(
            'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(pu.text_formats.plaintext))
        self.assertEqual(
            '𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡!',
            x.repr(pu.text_formats.unicode))
        self.assertEqual(
            '\\mathbb{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.repr(pu.text_formats.latex_math))
