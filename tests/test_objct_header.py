from unittest import TestCase
import punctilious as p
import random_data


class TestHeader(TestCase):
    def test_header_1(self):
        header_reference = random_data.random_word()
        header = p.ObjctHeader(header_reference, category=p.statement_categories.declare_axiom)
        self.assertEqual(f'axiom {header_reference}', str(header))
        self.assertEqual(f'axiom {header_reference}', header.repr())
        self.assertEqual(f'axiom {header_reference}', header.repr_header())
        self.assertEqual(f'axiom {header_reference}', header.repr_reference())
        self.assertEqual(f'Axiom {header_reference}', header.repr(cap=True))
        self.assertEqual(f'Axiom {header_reference}', header.repr_header(cap=True))
        self.assertEqual(f'Axiom {header_reference}', header.repr_reference(cap=True))

    def test_header_2(self):
        header_reference = random_data.random_word()
        header_title = random_data.random_sentence()
        header = p.ObjctHeader(header_reference, category=p.statement_categories.declare_axiom, title=header_title)
        self.assertEqual(f'axiom {header_reference}', str(header))
        self.assertEqual(f'axiom {header_reference}', header.repr())
        self.assertEqual(f'axiom {header_reference} - {header_title}', header.repr_header())
        self.assertEqual(f'axiom {header_reference}', header.repr_reference())
        self.assertEqual(f'Axiom {header_reference}', header.repr(cap=True))
        self.assertEqual(f'Axiom {header_reference} - {header_title}', header.repr_header(cap=True))
        self.assertEqual(f'Axiom {header_reference}', header.repr_reference(cap=True))
