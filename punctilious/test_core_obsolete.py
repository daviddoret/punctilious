from unittest import TestCase
import core
import test_env_1


class TestObjct(TestCase):
    def test_is_antivariable_equal_to(self):
        o = core.ObjctObsolete('o')
        p = core.ObjctObsolete('p')
        x = core.Var('x')
        self.assertTrue(o.is_antivariable_equal_to(o))
        self.assertFalse(o.is_antivariable_equal_to(p))
        self.assertFalse(o.is_antivariable_equal_to(x))

    def test_is_variable_equal_to(self):
        o = core.ObjctObsolete('o')
        p = core.ObjctObsolete('p')
        x = core.Var('x')
        self.assertTrue(o.is_variable_equal_to(o))
        self.assertFalse(o.is_variable_equal_to(p))
        self.assertTrue(o.is_variable_equal_to(x))


class TestVariable(TestCase):
    def test_is_antivariable_equal_to(self):
        x = core.Var('x')
        self.assertFalse(x.is_antivariable_equal_to(x))
        y = core.Var('y')
        self.assertFalse(x.is_antivariable_equal_to(y))
        o = core.ObjctObsolete('o')
        self.assertFalse(x.is_antivariable_equal_to(o))

    def test_is_variable_equal_to(self):
        x = core.Var('x')
        self.assertTrue(x.is_variable_equal_to(x))
        y = core.Var('y')
        self.assertTrue(x.is_variable_equal_to(y))
        o = core.ObjctObsolete('o')
        self.assertTrue(x.is_variable_equal_to(o))


class TestFormula(TestCase):
    def test_is_antivariable_equal_to(self):
        f = core.ObjctObsolete('𝑓')
        o1 = core.ObjctObsolete('o₁')
        o2 = core.ObjctObsolete('o₂')
        x = core.Var('x')
        y = core.Var('y')
        phi1 = core.FormulaStatement((f, o1, o2))
        self.assertTrue(phi1.is_antivariable_equal_to(phi1))
        phi2 = core.FormulaStatement((f, o1, o2))
        self.assertTrue(phi1.is_antivariable_equal_to(phi2))
        phi3 = core.FormulaStatement((f, o1, o1))
        self.assertFalse(phi1.is_antivariable_equal_to(phi3))
        phi4 = core.FormulaStatement((f, o1, x))
        self.assertFalse(phi1.is_antivariable_equal_to(phi4))
        phi5 = core.FormulaStatement((f, x, x))
        self.assertFalse(phi1.is_antivariable_equal_to(phi5))
        phi6 = core.FormulaStatement((f, x, y))
        self.assertFalse(phi1.is_antivariable_equal_to(phi6))

    def test_is_variable_equal_to(self):
        f = core.ObjctObsolete('𝑓')
        o1 = core.ObjctObsolete('o₁')
        o2 = core.ObjctObsolete('o₂')
        x = core.Var('x')
        y = core.Var('y')
        phi1 = core.FormulaStatement((f, o1, o2))
        self.assertTrue(phi1.is_variable_equal_to(phi1))
        phi2 = core.FormulaStatement((f, o1, o2))
        self.assertTrue(phi1.is_variable_equal_to(phi2))
        phi3 = core.FormulaStatement((f, o1, o1))
        self.assertFalse(phi1.is_variable_equal_to(phi3))
        phi4 = core.FormulaStatement((f, o1, x))
        self.assertTrue(phi1.is_variable_equal_to(phi4))
        phi5 = core.FormulaStatement((f, x, x))
        self.assertTrue(phi1.is_variable_equal_to(phi5))
        phi6 = core.FormulaStatement((f, x, y))
        self.assertTrue(phi1.is_variable_equal_to(phi6))
        phi7 = core.FormulaStatement((f, o1, y))
        self.assertTrue(phi1.is_variable_equal_to(phi7))


class TestTheory(TestCase):

    def test__init(self):
        theory_1 = core.Theory(dashed_name='some-theory')

    def test_append_note(self):
        theory = core.Theory(dashed_name='test-note-theory')
        note_1_text = 'This is a note.'
        note_2_text = 'This is another note.'
        note_1 = theory.append_note(text=note_1_text)
        self.assertTrue(note_1.text == note_1_text)
        self.assertTrue(note_1.cat == core.cats.note)
        note_2 = theory.append_note(text=note_2_text)
        self.assertTrue(note_2.text == note_2_text)
        self.assertTrue(note_2.cat == core.cats.note)

    def test_append_axiom(self):
        theory = core.Theory(dashed_name='test-axiom-theory')
        axiom_1_text = 'This is a text describing an axiomatic truth.'
        axiom_1_citation = 'Some reference'
        axiom_2_text = 'This is another text describing another axiomatic truth.'
        axiom_2_citation = None
        axiom_1 = theory.append_axiom(text=axiom_1_text, citation=axiom_1_citation)
        self.assertTrue(axiom_1.text == axiom_1_text)
        self.assertTrue(axiom_1.cat == core.cats.axiom)
        axiom_2 = theory.append_axiom(text=axiom_2_text, citation=axiom_2_citation)
        self.assertTrue(axiom_2.text == axiom_2_text)
        self.assertTrue(axiom_2.cat == core.cats.axiom)

    def test_append_objct(self):

    def test_append_relation(self):


    def test_append_variable(self):


    def test_assure_free_formula(self):



class TestFreeFormula(TestCase):

    def test__init(self):
        pass

    def test_first_level_cardinality(self):
        pass

    def test_is_antivariable_equal_to(self):
        pass

    def test_is_variable_equal_to(self):
        pass

    def test_str(self):


