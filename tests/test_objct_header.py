from unittest import TestCase
import punctilious as pu
import random_data


class TestHeader(TestCase):
    def test_header_1(self):
        header_reference = random_data.random_word()
        header = pu.TitleOBSOLETE(header_reference, cat=pu.paragraph_headers.axiom_declaration)
        self.assertEqual(f'axiom {header_reference}', str(header))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep(encoding=pu.encodings.plaintext))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep_title(encoding=pu.encodings.plaintext))
        self.assertEqual(f'axiom {header_reference}',
                         header.rep_ref(encoding=pu.encodings.plaintext))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep_title(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual(f'Axiom {header_reference}',
                         header.rep_ref(encoding=pu.encodings.plaintext, cap=True))

    def test_header_2(self):
        header_reference = random_data.random_word()
        header_title = random_data.random_sentence()
        header = pu.TitleOBSOLETE(header_reference,
                                  cat=pu.paragraph_headers._hypothesis_statement_in_child_theory,
                                  subtitle=header_title)
        self.assertEqual(f'prop. {header_reference}', str(header))
        self.assertEqual(f'prop. {header_reference}',
                         header.rep(encoding=pu.encodings.plaintext))
        self.assertEqual(f'proposition {header_reference} - {header_title}',
                         header.rep_title(encoding=pu.encodings.plaintext))
        self.assertEqual(f'prop. {header_reference}',
                         header.rep_ref(encoding=pu.encodings.plaintext))
        self.assertEqual(f'Prop. {header_reference}',
                         header.rep(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual(f'Proposition {header_reference} - {header_title}',
                         header.rep_title(encoding=pu.encodings.plaintext, cap=True))
        self.assertEqual(f'Prop. {header_reference}',
                         header.rep_ref(encoding=pu.encodings.plaintext, cap=True))
