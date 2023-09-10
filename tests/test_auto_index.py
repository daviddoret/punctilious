from unittest import TestCase
import punctilious as pu


class TestAutoIndex(TestCase):
    def test_auto_index(self):
        u1 = pu.create_universe_of_discourse()
        a1 = u1.declare_symbolic_objct(symbol='a', auto_index=True)
        self.assertEqual(1, a1.nameset.index_as_int)
        b1 = u1.declare_symbolic_objct(symbol='b', auto_index=True)
        self.assertEqual(1, b1.nameset.index_as_int)
        b2 = u1.declare_symbolic_objct(symbol='b', auto_index=True)
        self.assertEqual(2, b2.nameset.index_as_int)
        a2 = u1.declare_symbolic_objct(symbol='a', auto_index=True)
        self.assertEqual(2, a2.nameset.index_as_int)
        a3 = u1.declare_symbolic_objct(symbol='a', auto_index=True)
        self.assertEqual(3, a3.nameset.index_as_int)
        b3 = u1.declare_symbolic_objct(symbol='b', auto_index=True)
        self.assertEqual(3, b3.nameset.index_as_int)
        big_a1 = u1.declare_symbolic_objct(symbol='A', auto_index=True)
        self.assertEqual(1, big_a1.nameset.index_as_int)
