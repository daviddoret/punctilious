import pytest

import punctilious as pu
import conftest


class TestAbstractStructures:
    def test_abstract_map(self, t1_a, t3_a_aa_ab):
        phi1 = pu.afl.AbstractFormula(t=((), (),), s=(0, 1, 2,))
        phi2 = pu.afl.AbstractFormula(t=((), (),), s=(0, 3, 4,))
        m: pu.afl.AbstractFormula = pu.afl.AbstractFormula.from_immediate_sub_formulas(0, (phi1, phi2,))
        # m: pu.asl.AbstractMap = pu.asl.AbstractMap.from_abstract_formula(m)
        i1 = pu.afl.AbstractFormula(t1_a, (1,))
        i2 = pu.afl.AbstractFormula(t1_a, (2,))
        i3 = pu.afl.AbstractFormula(t1_a, (3,))
        i4 = pu.afl.AbstractFormula(t1_a, (4,))
        assert m.get_abstract_map_value(i1) == i3
        assert m.get_abstract_map_value(i2) == i4
        with pytest.raises(pu.util.PunctiliousException):
            m.get_abstract_map_value(i3)
        with pytest.raises(pu.util.PunctiliousException):
            m.get_abstract_map_value(i4)
        pass
