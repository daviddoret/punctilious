import uuid

import pytest

import punctilious as pu


class TestConnectiveSequence:
    def test_connective_sequence(self):
        x = pu.connective.Connective("x")
        y = pu.connective.Connective("y")
        s1 = pu.cs.ConnectiveSequence(pu.connective_library.addition, x, y, )
        assert s1.length == 3
        s2 = pu.cs.ConnectiveSequence(pu.connective_library.addition, y, x, )
        assert s2.length == 3
        assert s1 != s2
        assert s1 is not s2
        s3 = pu.cs.ConnectiveSequence(pu.connective_library.addition, x, y, )
        assert s3.length == 3
        assert s1 == s3
        assert s1 is s3
        with pytest.raises(pu.util.PunctiliousException):
            pu.cs.ConnectiveSequence()
