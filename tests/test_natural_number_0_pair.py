import punctilious as pu


class TestNaturalNumbersPair:

    def test_max_value(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert pu.nn0pl.NaturalNumber0Pair(0, 0).max_value == 0
        assert pu.nn0pl.NaturalNumber0Pair(0, 2).max_value == 2
        assert pu.nn0pl.NaturalNumber0Pair(4, 2).max_value == 4

    def test_is_restricted_growth_function_sequence(self):
        assert pu.nn0pl.NaturalNumber0Pair(0, 1, ).is_restricted_growth_function_sequence
        assert pu.nn0pl.NaturalNumber0Pair(0, 0, ).is_restricted_growth_function_sequence
        assert not pu.nn0pl.NaturalNumber0Pair(0, 2, ).is_restricted_growth_function_sequence

    def test_canonical_natural_number_sequence(self):
        assert pu.nn0pl.NaturalNumber0Pair(0, 1, ).is_natural_number_0_pair_equivalent_to(
            pu.nn0pl.NaturalNumber0Pair(0, 1, ))
        assert pu.nn0pl.NaturalNumber0Pair(0, 0, ).is_natural_number_0_pair_equivalent_to(
            pu.nn0pl.NaturalNumber0Pair(0, 0, ))
        assert not pu.nn0pl.NaturalNumber0Pair(0, 2, ).is_natural_number_0_pair_equivalent_to(
            pu.nn0pl.NaturalNumber0Pair(0, 1, ))

    def test_image(self):
        s = pu.nn0pl.NaturalNumber0Pair(1, 1)
        assert s.image == (1,)
        s = pu.nn0pl.NaturalNumber0Pair(1, 2)
        assert s.image == (1, 2)
        s = pu.nn0pl.NaturalNumber0Pair(3, 2)
        assert s.image == (2, 3)

    def test_image_cardinality(self):
        s = pu.nn0pl.NaturalNumber0Pair(1, 1)
        assert s.image_cardinality == 1
        s = pu.nn0pl.NaturalNumber0Pair(1, 2)
        assert s.image_cardinality == 2
        s = pu.nn0pl.NaturalNumber0Pair(3, 2)
        assert s.image_cardinality == 2

    def test_is_increasing(self):
        s = pu.nn0pl.NaturalNumber0Pair(1, 2)
        assert s.is_increasing
        s = pu.nn0pl.NaturalNumber0Pair(17, 17)
        assert s.is_increasing
        s = pu.nn0pl.NaturalNumber0Pair(1, 0)
        assert not s.is_increasing
        s = pu.nn0pl.NaturalNumber0Pair(5001, 5000)
        assert not s.is_increasing

    def test_is_strictly_increasing(self):
        s = pu.nn0pl.NaturalNumber0Pair(1, 2)
        assert s.is_strictly_increasing
        s = pu.nn0pl.NaturalNumber0Pair(17, 19)
        assert s.is_strictly_increasing
        s = pu.nn0pl.NaturalNumber0Pair(1, 1)
        assert not s.is_strictly_increasing
        s = pu.nn0pl.NaturalNumber0Pair(5001, 5001)
        assert not s.is_strictly_increasing

    def test_order(self):
        t = ()
        for i in range(0, 100):
            n1: pu.nn0pl.NaturalNumber0Pair = pu.nn0pl.cantor_pairing_order.unrank(i)
            i2 = pu.nn0pl.cantor_pairing_order.rank(n1)
            assert i2 == i
            for j in range(0, 100):
                n2: pu.nn0pl.NaturalNumber0Pair = pu.nn0pl.cantor_pairing_order.unrank(j)
                if i < j:
                    assert n1.is_strictly_less_than(n2)
                    assert n1 < n2
                if j < i:
                    assert n2.is_strictly_less_than(n1)
                    assert n2 < n1
                if i == j:
                    assert n1.is_equal_to(n2)
                    assert n1 == n2
