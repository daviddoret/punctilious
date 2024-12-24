import punctilious as pu
from test_shared_library import create_atomic_connector


class TestFormula:
    def test_formula(self):
        """Test of representation with multiple string-constant renderers.
        """

        p = create_atomic_connector('P')
        q = create_atomic_connector('Q')
        r = create_atomic_connector('R')
        land = pu.operators_1.conjunction
        lnot = pu.operators_1.negation

        phi1 = pu.Formula(p)
        assert str(phi1) == 'P'

        phi2 = pu.Formula(land, (p, q,))
        assert str(phi2) == 'P ∧ Q'

        phi3 = pu.Formula(lnot, (p,))
        assert str(phi3) == '¬P'

        phi4 = pu.Formula(land, (phi3, phi2))
        assert str(phi4) == '(¬P) ∧ (P ∧ Q)'

        phi5 = pu.Formula(land, (phi2, phi2))
        assert phi5.represent() == '(P ∧ Q) ∧ (P ∧ Q)'

    def test_formula_2(self):
        prefs = pu.OptionsPreferences()
        # tag = pu.Tag('technical_language', 'unicode_extended')
        prefs[pu.tags.technical_language.unicode_extended] = 100000

        x = create_atomic_connector('x')
        element_of = pu.operators_1.element_of
        n = pu.constants_1.n
        phi6 = pu.Formula(element_of, (x, n))
        assert phi6.represent() == 'x ∈ N'
