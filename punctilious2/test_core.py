from unittest import TestCase
import core
from types import SimpleNamespace


def generate_test_data():
    o1 = core.SymbolicObjct(python='o1', dashed='object-1', symbol='o₁')
    o2 = core.SymbolicObjct(python='o2', dashed='object-2', symbol='o₂')
    o3 = core.SymbolicObjct(python='o3', dashed='object-3', symbol='o₃')
    return SimpleNamespace(o1=o1, o2=o2, o3=o3)


class TestFormula(TestCase):
    pass


class TestSymbolicObjct(TestCase):
    def test_python(self):
        test_data = generate_test_data()
        self.assertEqual('o1', test_data.o1.python)
        self.assertEqual('o2', test_data.o2.python)
        self.assertEqual('o3', test_data.o3.python)

    def test_dashed(self):
        test_data = generate_test_data()
        self.assertEqual('object-1', test_data.o1.dashed)
        self.assertEqual('object-2', test_data.o2.dashed)
        self.assertEqual('object-3', test_data.o3.dashed)

    def test_symbol(self):
        test_data = generate_test_data()
        self.assertEqual('o₁', test_data.o1.symbol)
        self.assertEqual('o₂', test_data.o2.symbol)
        self.assertEqual('o₃', test_data.o3.symbol)
