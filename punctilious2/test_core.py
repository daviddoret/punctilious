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


class TestAxiom(TestCase):

    def test_init(self):
        t1 = core.Theory()
        a1 = core.Axiom(theory=t1, text='If something is red, then it is neither green, nor blue.')
        a2 = core.Axiom(theory=t1, text='If something is green, then it is neither red, nor blue.')
        a3 = core.Axiom(theory=t1, text='If something is blue, then it is neither red, nor green.')

        self.assertIs(t1, a1.theory)
        self.assertIs(t1, a2.theory)
        self.assertIs(t1, a3.theory)


class TestStatement(TestCase):

    def test_init(self):
        t1 = core.Theory()
        a1 = core.Axiom(theory=t1, text='If something is red, then it is neither green, nor blue.')
        s1 = core.Statement(theory=t1, truth_object=a1)

        self.assertIs(t1, s1.theory)
        print(s1)


class TestFormula(TestCase):

    def test_init(self):
        t1 = core.Theory()
        o11 = core.SimpleObjct(theory=t1)
        o12 = core.SimpleObjct(theory=t1)

        r_unary = core.Relation(theory=t1, arity=1)
        phi_unary = core.Formula(theory=t1, relation=r_unary, parameters=tuple([o11]))
        self.assertEqual('◆₁(ℴ₁)', phi_unary.repr(rep=core.Formula.frmts.prefix_operator))
        self.assertEqual('(ℴ₁)◆₁', phi_unary.repr(rep=core.Formula.frmts.suffix_operator))
        self.assertEqual('◆₁(ℴ₁)', phi_unary.repr(rep=core.Formula.frmts.function_call))
        self.assertEqual('𝜑₁', phi_unary.repr(rep=core.Formula.frmts.symbol))

        r_binary = core.Relation(theory=t1, arity=2)
        phi_binary = core.Formula(theory=t1, relation=r_binary, parameters=tuple([o11, o12]))
        self.assertEqual('◆₂(ℴ₁, ℴ₂)', phi_binary.repr(rep=core.Formula.frmts.function_call))
        self.assertEqual('(ℴ₁ ◆₂ ℴ₂)', phi_binary.repr(rep=core.Formula.frmts.infix_operator))
        self.assertEqual('𝜑₂', phi_binary.repr(rep=core.Formula.frmts.symbol))

    def test_str(self):
        self.fail()


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


class TestRelation(TestCase):
    def test_init(self):
        t1 = core.Theory()
        r11 = core.Relation(theory=t1, arity=1)
        self.assertIs(t1, r11.theory)
        self.assertEqual(1, r11.arity)
        r12 = core.Relation(theory=t1, arity=2)
        self.assertIs(t1, r12.theory)
        self.assertEqual(2, r12.arity)
        r13 = core.Relation(theory=t1, arity=2)
        self.assertIs(t1, r13.theory)
        self.assertEqual(2, r13.arity)
        t2 = core.Theory()
        r21 = core.Relation(theory=t2, arity=2)
        self.assertIs(t2, r21.theory)
        self.assertEqual(2, r21.arity)
        r22 = core.Relation(theory=t2, arity=1)
        self.assertIs(t2, r22.theory)
        self.assertEqual(1, r22.arity)
        r23 = core.Relation(theory=t2, arity=1)
        self.assertIs(t2, r23.theory)
        self.assertEqual(1, r23.arity)
        pass


class TestSimpleObjct(TestCase):
    def test_init(self):
        t1 = core.Theory()
        o11 = core.SimpleObjct(theory=t1)
        o12 = core.SimpleObjct(theory=t1)
        o13 = core.SimpleObjct(theory=t1)
        t2 = core.Theory()
        o21 = core.SimpleObjct(theory=t2)
        o22 = core.SimpleObjct(theory=t2)
        o23 = core.SimpleObjct(theory=t2)
        pass


class TestTheory(TestCase):
    def test___init__(self):
        t1 = core.Theory(dashed='test-theory-1')
        a1 = core.Axiom(theory=t1, text='If a filooboo is wala, then it is sholo.')
        s1 = core.Statement(theory=t1, truth_object=a1)
        t1.print()

