from unittest import TestCase
import punctilious as p
import random_data


class TestFreeVariable(TestCase):
    def test_with_statement(self):
        p.configuration.echo_variable = True
        u = p.UniverseOfDiscourse('test_with_statement')
        with u.v('x', echo=True) as x, u.v('y', echo=True) as y:
            r = u.r.declare(arity=2)
            phi = u.f(r, x, y)
            self.assertIs(x, phi.parameters[0])
            self.assertIs(y, phi.parameters[1])
            self.assertIsNot(y, phi.parameters[0])
            self.assertIsNot(x, phi.parameters[1])
        with self.assertRaises(p.FailedVerificationException):
            # Outside the with statement, scope is locked.
            # Trying to extend the scope raises an exception.
            psi = u.f(r, y, x)
