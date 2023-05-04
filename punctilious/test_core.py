from unittest import TestCase
import core


class TestObjct(TestCase):
    def test_is_antivariable_equal_to(self):
        o = core.Objct('o')
        p = core.Objct('p')
        x = core.Variable('x')
        self.assertTrue(o.is_antivariable_equal_to(o))
        self.assertFalse(o.is_antivariable_equal_to(p))
        self.assertFalse(o.is_antivariable_equal_to(x))

    def test_is_variable_equal_to(self):
        o = core.Objct('o')
        p = core.Objct('p')
        x = core.Variable('x')
        self.assertTrue(o.is_variable_equal_to(o))
        self.assertFalse(o.is_variable_equal_to(p))
        self.assertTrue(o.is_variable_equal_to(x))


class TestVariable(TestCase):
    def test_is_antivariable_equal_to(self):
        x = core.Variable('x')
        self.assertFalse(x.is_antivariable_equal_to(x))
        y = core.Variable('y')
        self.assertFalse(x.is_antivariable_equal_to(y))
        o = core.Objct('o')
        self.assertFalse(x.is_antivariable_equal_to(o))

    def test_is_variable_equal_to(self):
        x = core.Variable('x')
        self.assertTrue(x.is_variable_equal_to(x))
        y = core.Variable('y')
        self.assertTrue(x.is_variable_equal_to(y))
        o = core.Objct('o')
        self.assertTrue(x.is_variable_equal_to(o))


class TestFormula(TestCase):
    def test_is_antivariable_equal_to(self):
        f = core.Objct('𝑓')
        o1 = core.Objct('o₁')
        o2 = core.Objct('o₂')
        x = core.Variable('x')
        y = core.Variable('y')
        phi1 = core.Formula((f, o1, o2))
        self.assertTrue(phi1.is_antivariable_equal_to(phi1))
        phi2 = core.Formula((f, o1, o2))
        self.assertTrue(phi1.is_antivariable_equal_to(phi2))
        phi3 = core.Formula((f, o1, o1))
        self.assertFalse(phi1.is_antivariable_equal_to(phi3))
        phi4 = core.Formula((f, o1, x))
        self.assertFalse(phi1.is_antivariable_equal_to(phi4))
        phi5 = core.Formula((f, x, x))
        self.assertFalse(phi1.is_antivariable_equal_to(phi5))
        phi6 = core.Formula((f, x, y))
        self.assertFalse(phi1.is_antivariable_equal_to(phi6))

    def test_is_variable_equal_to(self):
        f = core.Objct('𝑓')
        o1 = core.Objct('o₁')
        o2 = core.Objct('o₂')
        x = core.Variable('x')
        y = core.Variable('y')
        phi1 = core.Formula((f, o1, o2))
        self.assertTrue(phi1.is_variable_equal_to(phi1))
        phi2 = core.Formula((f, o1, o2))
        self.assertTrue(phi1.is_variable_equal_to(phi2))
        phi3 = core.Formula((f, o1, o1))
        self.assertFalse(phi1.is_variable_equal_to(phi3))
        phi4 = core.Formula((f, o1, x))
        self.assertTrue(phi1.is_variable_equal_to(phi4))
        phi5 = core.Formula((f, x, x))
        self.assertTrue(phi1.is_variable_equal_to(phi5))
        phi6 = core.Formula((f, x, y))
        self.assertTrue(phi1.is_variable_equal_to(phi6))
        phi7 = core.Formula((f, o1, y))
        self.assertTrue(phi1.is_variable_equal_to(phi7))