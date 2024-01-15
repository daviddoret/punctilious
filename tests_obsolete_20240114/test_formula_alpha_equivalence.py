from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestFormulaIsAlphaEquivalentTo(TestCase):
    def test_formula_is_alpha_equivalent_to(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(signal_proposition=True)
        r2 = u.c1.declare(signal_proposition=True)
        r3 = u.c1.declare()

        phi1: pu.CompoundFormula = o1 | r2 | o2
        # A formula is always alpha-equivalent to itself
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi1, psi=phi1))
        psi1: pu.CompoundFormula = o1 | r2 | o2
        # If two distinct python objects represent the same formula "content",
        # they are alpha-equivalent
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi1, psi=psi1))

        with u.with_variable(symbol='x', auto_index=False) as x:
            phi2: pu.CompoundFormula = o1 | r2 | x
        with u.with_variable(symbol='y', auto_index=False) as y:
            psi2: pu.CompoundFormula = o1 | r2 | y
        # Two formula that are the same except for variable names
        # are still alpha-equivalent
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi2, psi=psi2))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi2, psi=psi1))

        # Multi variables case
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y', auto_index=False) as y:
            phi3: pu.CompoundFormula = r2(o1, x, x, o2, y, x, x, x, y)
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y', auto_index=False) as y:
            psi3: pu.CompoundFormula = r2(o1, y, y, o2, x, y, y, y, x)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi3))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi1))
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi2))

        # A small difference in the variable sequence
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y', auto_index=False) as y:
            psi4: pu.CompoundFormula = r2(o1, y, y, o2, x, y, y, x, x)
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=phi3, psi=psi4))

        # With 1 constant
        phi5: pu.CompoundFormula = o1 | r2 | o2
        psi5: pu.ConstantDeclaration = u.c3.declare(symbol='A', value=o1 | r2 | o2)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi5, psi=psi5))

        # With embedded constants
        phi6: pu.CompoundFormula = o1 | r2 | (o1 | r2 | (o1 | r2 | o2))
        psi6a: pu.ConstantDeclaration = u.c3.declare(symbol='A', value=o1 | r2 | o2)
        psi6b: pu.ConstantDeclaration = u.c3.declare(symbol='B', value=o1 | r2 | psi6a)
        psi6c: pu.ConstantDeclaration = u.c3.declare(symbol='C', value=o1 | r2 | psi6b)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=phi6, psi=psi6c))

        # A variable is alpha-equivalent with itself.
        with u.with_variable(symbol='x', auto_index=False) as x:
            psi9a: pu.CompoundFormula = x
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=psi9a, psi=psi9a))

        # A variable reference is alpha-equivalent with itself.
        with u.with_variable(symbol='x', auto_index=False) as x:
            psi10a: pu.CompoundFormula = u.c1.object_reference(x)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=psi10a, psi=psi10a))

        # Two formulas using the same variable are alpha-equivalent.
        with u.with_variable(symbol='x', auto_index=False) as x:
            psi7a: pu.CompoundFormula = r1(x)
            psi7b: pu.CompoundFormula = r1(x)
        self.assertTrue(pu.is_alpha_equivalent_to(u=u, phi=psi7a, psi=psi7b))

        # A variable is not alpha-equivalent with its reference
        with u.with_variable(symbol='x', auto_index=False) as x:
            psi8a: pu.CompoundFormula = x
        with u.with_variable(symbol='x', auto_index=False) as x:
            psi8b: pu.CompoundFormula = u.c1.object_reference(x)
        self.assertFalse(pu.is_alpha_equivalent_to(u=u, phi=psi8a, psi=psi8b))

        # TODO: Manage the case where we have variables inside constants. This require a little analysis.
