import uuid

import pytest

import punctilious as pu


class TestRestrictedGrowthFunctionSequence:
    def test_connective(self):
        c1 = pu.connective.Connective("*1")
        c2 = pu.connective.Connective("*2")
        assert c1 != c2
        uid1 = uuid.uuid4()
        c3 = pu.connective.Connective("*3", uid=uid1)
        c4 = pu.connective.Connective("*4", uid=uid1)
        assert c3 != c1
        assert c3 is not c1
        assert c3 == c4
        assert c3 is c4
