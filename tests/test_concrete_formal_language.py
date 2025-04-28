import pytest
import uuid

import punctilious.concrete_formal_language as cfl


class TestConnector:
    def test_connector_1(self):
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        c1 = cfl.Connector(uid=uid1)
        c2 = cfl.Connector(uid=uid2)
        assert c1.is_connector_equivalent_to(c1)
        assert not (c1.is_connector_equivalent_to(c2))
        assert c1 != c2
        assert c1 == c1
        assert c2 == c2
        c1_reuse = cfl.Connector(uid=uid1)
        assert c1 == c1_reuse
        assert c1 is c1_reuse
        assert id(c1) == id(c1_reuse)
        assert c1_reuse != c2


class TestFormula:
    def test_formula(self):
        c1 = cfl.Connector()
        c2 = cfl.Connector()
        c3 = cfl.Connector()
        s1 = cfl.afl.AbstractFormula(0)
        s2 = cfl.afl.AbstractFormula(1)
        s3 = cfl.afl.AbstractFormula(0, (s1,))
        s4 = cfl.afl.AbstractFormula(1, (s1, s2,))
        s4 = cfl.afl.AbstractFormula(2, (s3, s1, s2, s3, s4,))
        phi1 = cfl.Formula((c1,), s1)
        phi2 = cfl.Formula((c2,), s1)
        assert phi1 != phi2
        phi1b = cfl.Formula((c1,), s1)
        assert phi1 == phi1b
        phi3 = cfl.Formula((c1,), s3)
        phi4 = cfl.Formula((c2,), s3)
        with pytest.raises(Exception) as e:
            cfl.Formula((c2, c2,), s3)
        phi5 = cfl.Formula((c2, c3, c1,), s4)
        phi6 = cfl.Formula((c3, c2, c1,), s4)
        phi7 = cfl.Formula((c1, c2, c3,), s4)
        pass
