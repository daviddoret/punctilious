import pytest

import punctilious as pu


class TestConnective:
    def test_typesetting(self):
        c = pu.fl1.Connective()
        assert (c.to_string(protocol=pu.ts.protocols.unicode_limited) == "*")


class TestFormalObject:
    def test_formal_object(self):
        o = pu.fl1.FormalObject()
        output_1 = o.to_string(protocol=pu.ts.protocols.unicode_limited)
        pu.log.debug(output_1)
        assert len(output_1) > 0
