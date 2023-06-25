from unittest import TestCase
import text


class TestStyledText(TestCase):
    def test_styled_text(self):
        pangram = 'The quick brown fox jumps over the lazy dog 0123456789!'
        x = text.StyledText(pangram, text.text_styles.serif_bold)
        self.assertEqual(
            r'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(text.text_formats.plaintext))
        self.assertEqual(
            r'𝐓𝐡𝐞 𝐪𝐮𝐢𝐜𝐤 𝐛𝐫𝐨𝐰𝐧 𝐟𝐨𝐱 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠 𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗!',
            x.repr(text.text_formats.unicode))
        self.assertEqual(
            r'\mathbf{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.repr(text.text_formats.latex_math))
        x = text.StyledText(pangram, text.text_styles.serif_normal)
        self.assertEqual(
            r'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(text.text_formats.plaintext))
        self.assertEqual(
            r'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(text.text_formats.unicode))
        self.assertEqual(
            r'\mathnormal{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.repr(text.text_formats.latex_math))
        x = text.StyledText(pangram, text.text_styles.double_struck)
        self.assertEqual(
            r'The quick brown fox jumps over the lazy dog 0123456789!',
            x.repr(text.text_formats.plaintext))
        self.assertEqual(
            r'𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡!',
            x.repr(text.text_formats.unicode))
        self.assertEqual(
            r'\mathbb{The quick brown fox jumps over the lazy dog 0123456789!}',
            x.repr(text.text_formats.latex_math))
