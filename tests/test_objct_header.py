from unittest import TestCase
import punctilious as pu
import random_data


class TestHeader(TestCase):
    def test_header_1(self):
        header_reference = random_data.random_word()
        header = pu.Title(header_reference, cat=pu.title_categories.axiom_declaration)
        self.assertEqual(f'axiom {header_reference}', str(header))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep_title(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep_ref(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep(text_format=pu.text_formats.plaintext, cap=True))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep_title(text_format=pu.text_formats.plaintext, cap=True))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep_ref(text_format=pu.text_formats.plaintext, cap=True))

    def test_header_2(self):
        header_reference = random_data.random_word()
        header_title = random_data.random_sentence()
        header = pu.Title(header_reference, cat=pu.title_categories.proposition,
                          subtitle=header_title)
        self.assertEqual(f'prop. {header_reference}', str(header))
        self.assertEqual(f'prop. {header_reference}',
                         header.rep(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'proposition {header_reference} - {header_title}',
                         header.rep_title(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'prop. {header_reference}',
                         header.rep_ref(text_format=pu.text_formats.plaintext))
        self.assertEqual(f'Prop. {header_reference}',
                         header.rep(text_format=pu.text_formats.plaintext, cap=True))
        self.assertEqual(f'Proposition {header_reference} - {header_title}',
                         header.rep_title(text_format=pu.text_formats.plaintext, cap=True))
        self.assertEqual(f'Prop. {header_reference}',
                         header.rep_ref(text_format=pu.text_formats.plaintext, cap=True))
