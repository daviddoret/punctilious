import punctilious.formula as formula


class TestFormula:
    def test_pointer(self):
        p0 = formula.Pointer(0)
        assert p0 == 0
        p1 = formula.Pointer(1)
        assert p1 > p0
        p2 = formula.Pointer(2)
        assert p2 == p1 + p1

    def test_structure(self):
        p0 = formula.Pointer(0)
        p1 = formula.Pointer(1)
        p2 = formula.Pointer(2)
        s0 = formula.Structure(p0)
        assert s0.is_leaf
        assert s0.is_canonical
        s1 = formula.Structure(p1)
        assert s1.is_leaf
        assert not s1.is_canonical
        s2 = formula.Structure(p2)
        assert s2.is_leaf
        assert not s2.is_canonical
        s3 = formula.Structure(p0, (s0,))
        assert not s3.is_leaf
        assert s3.is_canonical
        s4 = formula.Structure(p0, (s1,))
        assert not s4.is_leaf
        assert s4.is_canonical
        s5 = formula.Structure(p0, (s2,))
        assert not s5.is_leaf
        assert not s5.is_canonical
