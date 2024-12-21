import pytest
import punctilious as pu
from test_shared_library import create_atomic_connector, create_function


class TestFormula:
    def test_formula(self):
        """Test of representation with multiple string-constant renderers.
        """

        p = create_atomic_connector('P')
        q = create_atomic_connector('Q')
        r = create_atomic_connector('R')
        land = pu.operators_1_connectors.conjunction
        lnot = pu.operators_1_connectors.negation

        phi1 = pu.Formula(p)
        assert str(phi1) == 'P'

        phi2 = pu.Formula(land, (p, q,))
        assert str(phi2) == 'P ∧ Q'

        phi3 = pu.Formula(lnot, (p,))
        assert str(phi3) == '¬P'

        phi4 = pu.Formula(land, (phi3, phi2))
        # TODO: Manage parenthesisation
        assert str(phi4) == '¬P ∧ P ∧ Q'
