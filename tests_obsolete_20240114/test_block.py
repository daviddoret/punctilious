from unittest import TestCase
import punctilious as pu


class TestBlock(TestCase):
    def test_block(self):
        # TODO: Extend testing to latex math
        b1 = pu.ComposableBlockSequence(
            start_tag=pu.ComposableText(plaintext='<plaintext>', unicode='<unicode>'),
            end_tag=pu.ComposableText(plaintext='</plaintext>', unicode='</unicode>'))
        self.assertEqual('<plaintext></plaintext>', b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('<unicode></unicode>', b1.rep(encoding=pu.encodings.unicode_extended))
        b1.append(pu.ComposableText(plaintext='plaintext content', unicode='unicode content'))
        self.assertEqual('<plaintext>plaintext content</plaintext>',
                         b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('<unicode>unicode content</unicode>',
                         b1.rep(encoding=pu.encodings.unicode_extended))
