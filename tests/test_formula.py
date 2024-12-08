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
