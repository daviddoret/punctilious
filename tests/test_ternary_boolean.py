import pytest
import punctilious as pu


class TestTernaryBoolean:
    def test_ternary_boolean(self):
        t = pu.tbl.TernaryBoolean.TRUE
        f = pu.tbl.TernaryBoolean.FALSE
        na = pu.tbl.TernaryBoolean.NOT_AVAILABLE

        assert t and t
        assert not (t and f)
        assert not (f and t)
        assert not (f and f)
        assert t and na == na
        assert not (f and na)  # if one operand is false, the conjunction is necessarily false
        with pytest.raises(Exception):
            assert na and t == na  # raise exception due to implicit bool conversion
        with pytest.raises(Exception):
            assert not (na and f)  # raise exception due to implicit bool conversion
        with pytest.raises(Exception):
            assert na and na == na  # raise exception due to implicit bool conversion

        assert t.land(t)
        assert not t.land(f)
        assert not f.land(t)
        assert not f.land(f)
        assert not f.land(na)
        assert not na.land(f)
        assert na.land(t) == na
        assert t.land(na) == na
        assert na.land(na) == na

        assert t.lor(t)
        assert t.lor(f)
        assert f.lor(t)
        assert not f.lor(f)
        assert f.lor(na) == na
        assert na.lor(f) == na
        assert na.lor(t)
        assert t.lor(na)
        assert na.lor(na) == na

        assert not t.lnot()
        assert f.lnot()
        assert na.lnot() == na
