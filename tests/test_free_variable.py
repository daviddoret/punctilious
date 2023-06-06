from unittest import TestCase
import punctilious as p
import random_data


class TestFreeVariable(TestCase):
    def test_with_statement(self):
        p.configuration.echo_variable = True
        with p.u.v('x', echo=True) as x, p.u.v('y', echo=True) as y:
            r = p.u.r(arity=2)
            phi = p.u.f(r, x, y)
            self.assertIs(x, phi.parameters[0])
            self.assertIs(y, phi.parameters[1])
            self.assertIsNot(y, phi.parameters[0])
            self.assertIsNot(x, phi.parameters[1])
        with self.assertRaises(p.FailedVerificationException):
            # Outside the with statement, scope is locked.
            # Trying to extend the scope raises an exception.
            psi = p.u.f(r, y, x)
