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
        lnot = create_function('not')
        land = create_function('and')
        is_a_proposition = create_function('is-a-proposition')

        phi1 = pu.Formula(p)
        assert str(phi1) == 'P()'

        phi2 = pu.Formula(land, (p, q,))
        assert str(phi2) == 'and(P(), Q())'

        phi3 = pu.Formula(lnot, (p,))
        assert str(phi3) == 'not(P())'

        phi4 = pu.Formula(land, (phi3, phi2))
        assert str(phi4) == 'and(not(P()), and(P(), Q()))'
