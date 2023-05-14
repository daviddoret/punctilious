from unittest import TestCase
import core
from types import SimpleNamespace


def generate_test_data_1():
    o1 = core.SymbolicObjct(python='o1', dashed='object-1', symbol='o₁')
    o2 = core.SymbolicObjct(python='o2', dashed='object-2', symbol='o₂')
    o3 = core.SymbolicObjct(python='o3', dashed='object-3', symbol='o₃')
    return SimpleNamespace(o1=o1, o2=o2, o3=o3)


def generate_test_data_2():
    t1 = core.Theory(python='T1', dashed='theory-1', symbol='𝒯₁')
    return t1


class TestFormula(TestCase):

    def test_init(self):
        t1 = core.Theory(python='T1', dashed='theory-1', symbol='𝒯₁')
        self.assertEqual('T1', t1.python)
        self.assertEqual('theory-1', t1.dashed)
        self.assertEqual('𝒯₁', t1.symbol)


class TestSymbolicObjct(TestCase):
    def test_python(self):
        test_data = generate_test_data_1()
        self.assertEqual('o1', test_data.o1.python)
        self.assertEqual('o2', test_data.o2.python)
        self.assertEqual('o3', test_data.o3.python)

    def test_dashed(self):
        test_data = generate_test_data_1()
        self.assertEqual('object-1', test_data.o1.dashed)
        self.assertEqual('object-2', test_data.o2.dashed)
        self.assertEqual('object-3', test_data.o3.dashed)

    def test_symbol(self):
        test_data = generate_test_data_1()
        self.assertEqual('o₁', test_data.o1.symbol)
        self.assertEqual('o₂', test_data.o2.symbol)
        self.assertEqual('o₃', test_data.o3.symbol)


class TestNote(TestCase):
    pass


class TestRelationDeclarationFormula(TestCase):
    def test_init(self):
        t1 = core.Theory(dashed='test-theory-1')
        r1 = core.Relation(arity=2, dashed='test-relation-1')
        rdf1 = core.RelationDeclarationFormula(theory=t1, relation=r1)
        self.assertIs(core.theoretical_relations.relation_declaration, rdf1.component)
        self.assertIs(t1, rdf1.subformulae[0])
        self.assertIs(r1, rdf1.subformulae[1])


class TestSimpleObjctComponent(TestCase):
    def test_init(self):
        t1 = core.Theory(dashed='test-theory-1')
        o1 = core.SimpleObjct(dashed='test-object-1')


class TestTheory(TestCase):
    def test__get_next_position(self):
        t1 = core.Theory(dashed='test-theory-1')
        pass

    def test_append_statement(self):
        pass

    def test_append_theoretical_statement(self):
        pass

    def test_declare_relation(self):
        pass
