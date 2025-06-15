import uuid

import pytest

import punctilious as pu


class TestConnectorSequence:
    def test_connector_sequence(self):
        x = pu.connector.Connector("x")
        y = pu.connector.Connector("y")
        s1 = pu.cs.ConnectorSequence(pu.connectors.addition, x, y, )
        assert s1.length == 3
        s2 = pu.cs.ConnectorSequence(pu.connectors.addition, y, x, )
        assert s2.length == 3
        assert s1 != s2
        assert s1 is not s2
        s3 = pu.cs.ConnectorSequence(pu.connectors.addition, x, y, )
        assert s3.length == 3
        assert s1 == s3
        assert s1 is s3
        with pytest.raises(pu.util.PunctiliousException):
            pu.cs.ConnectorSequence()
