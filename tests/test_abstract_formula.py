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

    def test_iterate_children(self, af1, af2a, af2b, af4, af6a):
        l = tuple(af for af in af1.iterate_sub_formulas_direct_children())
        assert len(l) == 0
        l = tuple(af for af in af2a.iterate_sub_formulas_direct_children())
        assert l[0] == af1
        l = tuple(af for af in af2b.iterate_sub_formulas_direct_children())
        assert l[0] == af1
        l = tuple(af for af in af4.iterate_sub_formulas_direct_children())
        assert l[0] == af1
        assert l[1] == af2b
        assert l[2] == af6a
        assert l[3] == af2b
