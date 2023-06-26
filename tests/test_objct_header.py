from unittest import TestCase
import punctilious as p
import random_data


class TestHeader(TestCase):
    def test_header_1(self):
        header_reference = random_data.random_word()
        header = p.Title(header_reference, category=p.title_categories.declare_axiom)
        self.assertEqual(f'axiom {header_reference}', str(header))
        self.assertEqual(f'axiom {header_reference}', header.repr())
        self.assertEqual(f'axiom {header_reference}', header.repr_as_title())
        self.assertEqual(f'axiom {header_reference}', header.repr_as_ref())
        self.assertEqual(f'Axiom {header_reference}', header.repr(cap=True))
        self.assertEqual(f'Axiom {header_reference}', header.repr_as_title(cap=True))
        self.assertEqual(f'Axiom {header_reference}', header.repr_as_ref(cap=True))

    def test_header_2(self):
        header_reference = random_data.random_word()
        header_title = random_data.random_sentence()
        header = p.Title(header_reference, category=p.title_categories.proposition,
                         complement=header_title)
        self.assertEqual(f'proposition {header_reference}', str(header))
        self.assertEqual(f'proposition {header_reference}', header.repr())
        self.assertEqual(f'proposition {header_reference} - {header_title}', header.repr_as_title())
        self.assertEqual(f'proposition {header_reference}', header.repr_as_ref())
        self.assertEqual(f'Proposition {header_reference}', header.repr(cap=True))
        self.assertEqual(f'Proposition {header_reference} - {header_title}', header.repr_as_title(cap=True))
        self.assertEqual(f'Proposition {header_reference}', header.repr_as_ref(cap=True))
