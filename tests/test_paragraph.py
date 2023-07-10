from unittest import TestCase
import punctilious as pu
import random_data


class TestParagraph(TestCase):
    def test_paragraph(self):
        p = pu.Paragraph()
        p.append(item=random_data.random_sentence())
        p.append(item=random_data.random_sentence())
        p.append(item=random_data.random_sentence())
        s = p.rep(text_format=pu.text_formats.plaintext)
        print(s)
