import pytest

import punctilious.formal_language as fl


class TestStructure:

    def test_structure_01(self):
        s0 = fl.Structure(0)
        assert s0.is_leaf
        assert s0.is_canonical
        s1 = fl.Structure(1)
        assert s1.is_leaf
        assert not s1.is_canonical
        s2 = fl.Structure(2)
        assert s2.is_leaf
        assert not s2.is_canonical
        s3 = fl.Structure(0, (s0,))
        assert not s3.is_leaf
        assert s3.is_canonical
        s4 = fl.Structure(0, (s1,))
        assert not s4.is_leaf
        assert s4.is_canonical
        s5 = fl.Structure(0, (s2,))
        assert not s5.is_leaf
        assert not s5.is_canonical
        s6 = fl.Structure(0, (s2, s5, s1, s0,))
        assert not s6.is_leaf
        assert not s6.is_canonical
        s7 = fl.Structure(0, (s1, s2, s3, s4, s5, s6,))
        assert not s7.is_leaf
        assert s7.is_canonical
        pass


class TestFormula:
    def test_formula(self):
        c1 = fl.Connector()
        c2 = fl.Connector()
        c3 = fl.Connector()
        s1 = fl.Structure(0)
        s2 = fl.Structure(1)
        s3 = fl.Structure(0, (s1,))
        s4 = fl.Structure(1, (s1, s2,))
        s4 = fl.Structure(2, (s3, s1, s2, s3, s4,))
        phi1 = fl.Formula((c1,), s1)
        phi2 = fl.Formula((c2,), s1)
        phi3 = fl.Formula((c1,), s3)
        phi4 = fl.Formula((c2,), s3)
        with pytest.raises(Exception) as e:
            fl.Formula((c2, c2,), s3)
        phi5 = fl.Formula((c2, c3, c1,), s4)
        phi6 = fl.Formula((c3, c2, c1,), s4)
        phi7 = fl.Formula((c1, c2, c3,), s4)
        pass
