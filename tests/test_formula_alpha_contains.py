from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestFormulaAlphaContains(TestCase):
    def test_formula_alpha_contains(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(signal_proposition=True)
        r2 = u.r.declare(signal_proposition=True)

        phi1: pu.CompoundFormula = o1 | r2 | o2
        # A formula is always alpha-equivalent to itself
        self.assertTrue(pu.formula_alpha_contains(u=u, phi=phi1, psi=phi1))
        psi1: pu.CompoundFormula = o1 | r2 | o2
        # If two distinct python objects represent the same formula "content",
        # they are alpha-equivalent
        self.assertTrue(pu.formula_alpha_contains(u=u, phi=phi1, psi=psi1))

        with u.with_variable(symbol='x', auto_index=False) as x:
            phi2: pu.CompoundFormula = o1 | r2 | x
        with u.with_variable(symbol='y', auto_index=False) as y:
            psi2: pu.CompoundFormula = o1 | r2 | y
        # Two formula that are the same except for variable names
        # are still alpha-equivalent
        self.assertTrue(pu.formula_alpha_contains(u=u, phi=phi2, psi=psi2))
        # self.assertFalse(pu.formula_alpha_contains(u=u, phi=phi2, psi=psi1))

        # Embedding
        with u.with_variable(symbol='x', auto_index=False) as x, u.with_variable(symbol='y',
                auto_index=False) as y:
            phi3: pu.CompoundFormula = o1 | r1 | phi1
            self.assertTrue(pu.formula_alpha_contains(u=u, phi=phi3, psi=phi1))

        # TODO: Manage the case where we have variables inside constants. This require a little analysis.
