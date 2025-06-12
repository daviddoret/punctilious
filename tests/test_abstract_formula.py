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

    def test_iterate_sub_formulas_direct(self, af1, af2a, af2b, af12a, af6a):
        l = tuple(af for af in af1.iterate_sub_formulas_direct())
        assert len(l) == 0
        l = tuple(af for af in af2a.iterate_sub_formulas_direct())
        assert l[0] == af1
        l = tuple(af for af in af2b.iterate_sub_formulas_direct())
        assert l[0] == af1
        l = tuple(af for af in af12a.iterate_sub_formulas_direct())
        assert l[0] == af1
        assert l[1] == af2b
        assert l[2] == af6a
        assert l[3] == af2b

    def test_iterate_sub_formulas_depth_first_ascending(self, af1, af2a, af2b, af6a, af12a):
        l = tuple(t for t in af1.iterate_sub_formulas_depth_first_ascending())
        assert l[0] == af1
        l = tuple(t for t in af2a.iterate_sub_formulas_depth_first_ascending())
        assert l[0] == af2a
        assert l[1] == af1
        l = tuple(t for t in af2b.iterate_sub_formulas_depth_first_ascending())
        assert l[0] == af2b
        assert l[1] == af1
        l = tuple(t for t in af6a.iterate_sub_formulas_depth_first_ascending())
        assert l[0] == af6a
        assert l[1] == af1
        assert l[2] == af1
        assert l[3] == af1
        assert l[4] == af1
        assert l[5] == af1
        l = tuple(t for t in af12a.iterate_depth_first_ascending())
        assert l[0] == af12a
        assert l[1] == af1
        assert l[2] == af2a
        assert l[3] == af1
        assert l[4] == af6a
        assert l[5] == af1
        assert l[6] == af1
        assert l[7] == af1
        assert l[8] == af1
        assert l[9] == af1
        assert l[10] == af2a
        assert l[11] == af1
