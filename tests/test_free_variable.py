from unittest import TestCase
import punctilious as pu


class TestFreeVariable(TestCase):
    def test_1(self):
        pu.configuration.encoding = pu.encodings.unicode
        u = pu.UniverseOfDiscourse()
        with u.with_variable(symbol='x') as x1:
            pass
        x1.echo()

    def test_with_statement(self):
        pu.configuration.echo_variable_declaration = True
        u = pu.UniverseOfDiscourse()
        with u.with_variable('x', echo=True) as x, u.with_variable('y', echo=True) as y:
            r = u.r.declare(arity=2)
            phi = u.f(r, x, y)
            self.assertIs(x, phi.parameters[0])
            self.assertIs(y, phi.parameters[1])
            self.assertIsNot(y, phi.parameters[0])
            self.assertIsNot(x, phi.parameters[1])
        with self.assertRaises(pu.PunctiliousException):
            # Outside the with statement, scope is locked.
            # Trying to extend the scope raises an exception.
            psi = u.f(r, y, x)
