import pytest

import punctilious as pu


class TestDyckWord:

    def test_dyck_word_trivial(self):
        with pytest.raises(pu.util.PunctiliousException):
            d = pu.dwl.DyckWord("")

    def test_dyck_word(self):
        d2 = None
        for n in range(0, 100):
            d = pu.dwl.lexicographic_order.unrank(n)
            n2 = pu.dwl.lexicographic_order.rank(d)
            assert n2 == n
            if d2 is None:
                d2 = pu.dwl.lexicographic_order.least_element
            else:
                d2 = pu.dwl.lexicographic_order.successor(d2)
            assert d == d2
            # print(f"{n}=={n2}: {d}=={d2}")

    def test_least_element(self):
        assert pu.dwl.LexicographicOrder.least_element == pu.dwl.DW("()")
        assert pu.dwl.DyckWord.least_element == pu.dwl.DW("()")


pass
