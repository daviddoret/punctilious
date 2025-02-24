import pytest
import uuid

import punctilious.formal_language as fl


class TestStructure:

    def test_structure_01(self):
        s0 = fl.Structure(0)
        assert s0.is_leaf
        assert s0.is_canonical
        s0b = fl.Structure(0)
        assert s0 == s0b
        assert id(s0) == id(s0b)
        assert s0 is s0b
        s1 = fl.Structure(1)
        assert s1.is_leaf
        assert not s1.is_canonical
        assert s1 is not s0
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
        s7b = fl.Structure(0, (s1, s2, s3, s4, s5, s6,))
        assert s7 == s7b
        assert id(s7) == id(s7b)
        assert s7 is s7b
        assert s7 is not s5
        pass


class TestConnector:
    def test_connector(self):
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        c1 = fl.Connector(uid=uid1)
        c2 = fl.Connector(uid=uid2)
        assert c1 != c2
        assert c1 == c1
        assert c2 == c2
        c1_reuse = fl.Connector(uid=uid1)
        assert c1 == c1_reuse
        assert c1 is c1_reuse
        assert id(c1) == id(c1_reuse)
        assert c1_reuse != c2


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
        assert phi1 != phi2
        phi1b = fl.Formula((c1,), s1)
        assert phi1 == phi1b
        phi3 = fl.Formula((c1,), s3)
        phi4 = fl.Formula((c2,), s3)
        with pytest.raises(Exception) as e:
            fl.Formula((c2, c2,), s3)
        phi5 = fl.Formula((c2, c3, c1,), s4)
        phi6 = fl.Formula((c3, c2, c1,), s4)
        phi7 = fl.Formula((c1, c2, c3,), s4)
        pass
