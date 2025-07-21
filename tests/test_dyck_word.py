import pytest

import punctilious as pu


class TestDyckWord:

    def test_dyck_word_trivial(self):
        d = pu.dwl.DyckWord("")
        assert d == ""
        assert pu.dwl.lexicographic_order.rank(d) == 0

    def test_dyck_word(self):
        for n in range(0, 100):
            d = pu.dwl.lexicographic_order.unrank(n)
            n2 = pu.dwl.lexicographic_order.rank(d)
            assert n2 == n
            # print(f"{n}=={n2}: {d}")


pass
