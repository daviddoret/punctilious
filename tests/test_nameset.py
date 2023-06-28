from unittest import TestCase
import punctilious as pu
import random_data


class TestNameSet(TestCase):
    def test_nameset_1(self):
        n = pu.NameSet(symbol='x', index=1, acronym='xy', name='something', explicit_name='something precise')
        self.assertEqual('x', n.repr_compact())
        self.assertEqual('something precise', n.repr_accurate())
        self.assertEqual('something', n.repr_conventional())

    def test_nameset_2(self):
        n = pu.NameSet(symbol='⩒', index=1, name='dot big vee')
        self.assertEqual('⩒', n.repr_compact())
        self.assertEqual('dot big vee', n.repr_accurate())
        self.assertEqual('dot big vee', n.repr_conventional())
        self.assertEqual('dot big vee', n.repr_compact(text_format=pu.text_formats.plaintext))
        self.assertEqual('⩒', n.repr_compact(text_format=pu.text_formats.unicode))
