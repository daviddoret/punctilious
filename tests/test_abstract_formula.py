import pytest

import punctilious as pu


class TestAbstractFormula:
    def test_construction_success(self):
        phi1 = pu.af.AbstractFormula(t=(((),), (),), s=(1, 2, 3, 4,))
        phi2 = pu.af.AbstractFormula(t=(((),), (),), s=(1, 2, 1, 1,))
        pass

    def test_construction_failure(self):
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(1, 3, 2, 1,))  # invalid
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(1, 2, 1,))
        with pytest.raises(pu.util.PunctiliousException):
            pu.af.AbstractFormula(t=(((),), (),), s=(1, 2, 1, 2, 1,))
