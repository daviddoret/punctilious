from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestFormulaIsAlphaEquivalentTo(TestCase):
    def test_formula_is_alpha_equivalent_to(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(signal_proposition=True)
        r2 = u.r.declare(signal_proposition=True)
        r3 = u.r.declare()

        phi1: pu.Formula = o1 | r2 | o2
        # A formula is always alpha-equivalent to itself
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi1, psi=phi1))
        psi1: pu.Formula = o1 | r2 | o2
        # If two distinct python objects represent the same formula "content",
        # they are alpha-equivalent
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi1, psi=psi1))

        with u.with_variable(symbol='x', auto_index=False) as x:
            phi2: pu.Formula = o1 | r2 | x
        with u.with_variable(symbol='y', auto_index=False) as y:
            psi2: pu.Formula = o1 | r2 | y
        # Two formula that are the same except for variable names
        # are still alpha-equivalent
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi2, psi=psi2))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi2, psi=psi1))

        # Multi variables case
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
                auto_index=False) as y:
            phi3: pu.Formula = r2(o1, x, x, o2, y, x, x, x, y)
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
                auto_index=False) as y:
            psi3: pu.Formula = r2(o1, y, y, o2, x, y, y, y, x)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi3))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi1))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi2))

        # A small difference in the variable sequence
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
                auto_index=False) as y:
            psi4: pu.Formula = r2(o1, y, y, o2, x, y, y, x, x)
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi4))

        # With 1 constant
        phi5: pu.Formula = o1 | r2 | o2
        psi5: pu.ConstantDeclaration = u.c.declare(symbol='A', value=o1 | r2 | o2)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi5, psi=psi5))

        # With embedded constants
        phi6: pu.Formula = o1 | r2 | (o1 | r2 | (o1 | r2 | o2))
        psi6a: pu.ConstantDeclaration = u.c.declare(symbol='A', value=o1 | r2 | o2)
        psi6b: pu.ConstantDeclaration = u.c.declare(symbol='B', value=o1 | r2 | psi6a)
        psi6c: pu.ConstantDeclaration = u.c.declare(symbol='C', value=o1 | r2 | psi6b)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi6, psi=psi6c))

        # TODO: Manage the case where we have variables inside constants. This require a little analysis.
