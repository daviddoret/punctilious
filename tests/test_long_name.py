from unittest import TestCase
import punctilious as p
import random_data


class TestLongName(TestCase):
    def test_long_name_1(self):
        n1_reference = random_data.random_word()
        n1 = p.LongName(n1_reference, category=p.statement_categories.axiom)
        self.assertEqual(f'axiom {n1_reference}', str(n1))
        self.assertEqual(f'axiom {n1_reference}', n1.repr())
        self.assertEqual(f'axiom {n1_reference}', n1.repr_as_long_name())
        self.assertEqual(f'axiom {n1_reference}', n1.repr_as_reference())
        self.assertEqual(f'Axiom {n1_reference}', n1.repr(cap=True))
        self.assertEqual(f'Axiom {n1_reference}', n1.repr_as_long_name(cap=True))
        self.assertEqual(f'Axiom {n1_reference}', n1.repr_as_reference(cap=True))

    def test_long_name_2(self):
        n1_reference = random_data.random_word()
        n1_title = random_data.random_sentence()
        n1 = p.LongName(n1_reference, category=p.statement_categories.axiom, title=n1_title)
        self.assertEqual(f'axiom {n1_reference}', str(n1))
        self.assertEqual(f'axiom {n1_reference}', n1.repr())
        self.assertEqual(f'axiom {n1_reference} - {n1_title}', n1.repr_as_long_name())
        self.assertEqual(f'axiom {n1_reference}', n1.repr_as_reference())
        self.assertEqual(f'Axiom {n1_reference}', n1.repr(cap=True))
        self.assertEqual(f'Axiom {n1_reference} - {n1_title}', n1.repr_as_long_name(cap=True))
        self.assertEqual(f'Axiom {n1_reference}', n1.repr_as_reference(cap=True))
