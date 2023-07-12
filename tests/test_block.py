from unittest import TestCase
import punctilious as pu
import random_data


class TestBlock(TestCase):
    def test_block(self):
        # TODO: Extend testing to latex math
        b1 = pu.Block(start_tag=pu.Text(plaintext='<plaintext>', unicode='<unicode>'),
                      end_tag=pu.Text(plaintext='</plaintext>', unicode='</unicode>'))
        self.assertEqual('<plaintext></plaintext>',
                         b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('<unicode></unicode>',
                         b1.rep(encoding=pu.encodings.unicode))
        b1.append(pu.Text(plaintext='plaintext content', unicode='unicode content'))
        self.assertEqual('<plaintext>plaintext content</plaintext>',
                         b1.rep(encoding=pu.encodings.plaintext))
        self.assertEqual('<unicode>unicode content</unicode>',
                         b1.rep(encoding=pu.encodings.unicode))
