import punctilious as pu


class TestDyckWord:

    def test_dyck_word_trivial(self):
        d = pu.dwl.DyckWord("")
        assert d == ""
        assert pu.dwl.lexicographic_order.rank(d) == 0

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


pass
