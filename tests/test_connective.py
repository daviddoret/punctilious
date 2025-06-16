import uuid

import punctilious as pu


class TestConnective:
    def test_connective(self):
        c1 = pu.connective.Connective("*1")
        assert c1 == c1
        c2 = pu.connective.Connective("*2")
        assert c1 != c2
        uid1 = uuid.uuid4()
        c3 = pu.connective.Connective("*3", uid=uid1)
        c4 = pu.connective.Connective("*4", uid=uid1)
        assert c3 != c1
        assert c3 is not c1
        assert c3 == c4
        assert c3 is c4

    def test_is_connective_equivalent_to(self):
        c1 = pu.connective.Connective("*1")
        assert c1.is_connective_equivalent_to(c1)
        c2 = pu.connective.Connective("*2")
        assert not c1.is_connective_equivalent_to(c2)
        uid1 = uuid.uuid4()
        c3 = pu.connective.Connective("*3", uid=uid1)
        c4 = pu.connective.Connective("*4", uid=uid1)
        assert not c3.is_connective_equivalent_to(c1)
        assert c3.is_connective_equivalent_to(c4)
