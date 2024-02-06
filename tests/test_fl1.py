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
        fun = pu.ts.register_styledstring(typesetting_class=o.typesetting_class, text="hello world",
            representation=pu.ts.representations.symbolic_representation, )
        output_2 = ''.join(fun(o=o))
        assert len(output_2) > 0
        assert output_2 != output_1
        output_3 = o.to_string()
        assert len(output_3) > 0
        assert output_1 != output_3
        assert output_2 == output_3
