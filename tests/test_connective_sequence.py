# import pytest

import punctilious as pu


class TestConnectiveSequence:
    def test_connective_sequence(self):
        x = pu.cl.Connective("x")
        y = pu.cl.Connective("y")
        s1 = pu.csl.ConnectiveSequence(pu.cc.addition, x, y, )
        assert s1.length == 3
        s2 = pu.csl.ConnectiveSequence(pu.cc.addition, y, x, )
        assert s2.length == 3
        assert s1 != s2
        assert s1 is not s2
        s3 = pu.csl.ConnectiveSequence(pu.cc.addition, x, y, )
        assert s3.length == 3
        assert s1 == s3
        assert s1 is s3

    def test_combined_fixed_length_integers_with_sentinel_order(self):
        s = pu.csl.ConnectiveSequence.least_element
        for n in range(0, 128):
            r = s.rank
            s2 = pu.csl.combined_fixed_length_integers_with_sentinel_order.unrank(r)
            assert s == s2
            s_successor = s.successor
            assert s < s_successor
