import punctilious_20250223 as pu
from test_shared_library import create_atomic_connector


class TestFormula:
    def test_formula(self):
        """Test of representation with multiple string-constant renderers.
        """
        prefs = pu.rpr.Preferences()
        prefs[pu.options.technical_language.unicode_extended] = 3
        prefs[pu.options.technical_language.unicode_extended] = 4
        prefs[pu.options.technical_language.latex_math] = 0

        p = create_atomic_connector('P')
        q = create_atomic_connector('Q')
        r = create_atomic_connector('R')
        land = pu.operators.conjunction
        lnot = pu.operators.negation

        phi1 = pu.fml.Formula(p)
        assert phi1.represent(prefs=prefs) == 'P'

        phi2 = pu.fml.Formula(land, (p, q,))
        assert phi2.represent(prefs=prefs) == 'P ∧ Q'

        phi3 = pu.fml.Formula(lnot, (p,))
        assert phi3.represent(prefs=prefs) == '¬P'

        phi4 = pu.fml.Formula(land, (phi3, phi2))
        assert phi4.represent(prefs=prefs) == '(¬P) ∧ (P ∧ Q)'

        phi5 = pu.fml.Formula(land, (phi2, phi2))
        assert phi5.represent(prefs=prefs) == '(P ∧ Q) ∧ (P ∧ Q)'

    def test_formula_2(self):
        prefs = pu.rpr.Preferences()
        prefs[pu.options.technical_language.unicode_extended] = 3
        prefs[pu.options.technical_language.unicode_extended] = 4
        prefs[pu.options.technical_language.latex_math] = 0

        x = create_atomic_connector('x')
        element_of = pu.operators.element_of
        n = pu.constants_1.n
        phi6 = pu.fml.Formula(element_of, (x, n))
        assert phi6.represent(prefs=prefs) == 'x ∈ ℕ'


class TestFormulaRootConnectorEquivalence:
    def test_1(self):
        a = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='a'))
        b = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='b'))
        c = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='c'))
        d = pu.fml.Connector(uid=pu.identifiers.create_uid(slug='d'))
        phi = a(b(a(), c(), d(b())))
        psi = a(b(a(), c(), d(b())))
        assert pu.fml.is_formula_equivalent(phi=phi, psi=psi)
        psi = a(b(a(), c(), d(c())))
        assert not pu.fml.is_formula_equivalent(phi=phi, psi=psi)
