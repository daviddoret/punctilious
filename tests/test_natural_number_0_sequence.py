import random

import punctilious as pu


class TestNaturalNumbersSequence:
    def test_data_validation(self, raw_2_1, raw_1_2_3, raw_1_3_2, raw_00010203043212, raw_00010203043262):
        assert pu.nn0sl.NaturalNumber0Sequence.data_validate_elements(raw_2_1)[1] == raw_2_1
        assert pu.nn0sl.NaturalNumber0Sequence.data_validate_elements(raw_1_2_3)[1] == raw_1_2_3
        assert pu.nn0sl.NaturalNumber0Sequence.data_validate_elements(raw_00010203043212)[1] == raw_00010203043212
        assert pu.nn0sl.NaturalNumber0Sequence.data_validate_elements(raw_1_3_2)[1] == raw_1_3_2
        assert pu.nn0sl.NaturalNumber0Sequence.data_validate_elements(raw_00010203043262)[1] == raw_00010203043262

    def test_equality(self, raw_1_2_3, raw_1_3_2, raw_00010203043212, raw_00010203043262):
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3) == pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3)
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_00010203043212) == pu.nn0sl.NaturalNumber0Sequence(
            *raw_00010203043212)

    def test_inequality(self, raw_1_2_3, raw_1_3_2, raw_00010203043212, raw_00010203043262):
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3) != pu.nn0sl.NaturalNumber0Sequence(
            *raw_00010203043212)
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_00010203043212) != pu.nn0sl.NaturalNumber0Sequence(
            *raw_1_2_3)

    def test_cache(self, raw_1_2_3, raw_1_3_2, raw_00010203043212, raw_00010203043262):
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3) is pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3)
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_00010203043212) is pu.nn0sl.NaturalNumber0Sequence(
            *raw_00010203043212)
        assert pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3) is not pu.nn0sl.NaturalNumber0Sequence(
            *raw_00010203043212)
        assert pu.nn0sl.NaturalNumber0Sequence(
            *raw_00010203043212) is not pu.nn0sl.NaturalNumber0Sequence(*raw_1_2_3)

    def test_max_value(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.max_value == 1
        assert nns00.max_value == 1
        assert nns01.max_value == 2
        assert nns012345.max_value == 6
        assert nns0123456789_10_11.max_value == 12

    def test_is_natural_numbers_sequence_equivalent_to(self, nns0, nns00, nns01, nns10, nns012345, nns746107,
                                                       nns0123456789_10_11):
        assert nns0.is_natural_number_0_sequence_equivalent_to(nns0)
        assert nns00.is_natural_number_0_sequence_equivalent_to(nns00)
        assert nns01.is_natural_number_0_sequence_equivalent_to(nns01)
        assert nns10.is_natural_number_0_sequence_equivalent_to(nns10)
        assert nns012345.is_natural_number_0_sequence_equivalent_to(nns012345)
        assert nns746107.is_natural_number_0_sequence_equivalent_to(nns746107)
        assert nns0123456789_10_11.is_natural_number_0_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns00)
        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns01)
        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns10)
        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns012345)
        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns746107)
        assert not nns0.is_natural_number_0_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns0)
        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns01)
        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns10)
        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns012345)
        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns746107)
        assert not nns00.is_natural_number_0_sequence_equivalent_to(nns0123456789_10_11)

        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns0)
        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns00)
        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns01)
        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns012345)
        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns746107)
        assert not nns10.is_natural_number_0_sequence_equivalent_to(nns0123456789_10_11)

    def test_concatenate_single(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.concatenate_with(nns00) == pu.nn0sl.NaturalNumber0Sequence(*nns0, *nns00)
        assert pu.nn0sl.concatenate_natural_number_0_sequences(nns0123456789_10_11,
                                                               nns00) == pu.nn0sl.NaturalNumber0Sequence(
            *nns0123456789_10_11, *nns00)

    def test_is_restricted_growth_function_sequence(self):
        s = pu.nn0sl.NaturalNumber0Sequence(0, 0, 0)
        assert s.is_restricted_growth_function_sequence
        s = pu.nn0sl.NaturalNumber0Sequence(0, 1, 0)
        assert s.is_restricted_growth_function_sequence
        s = pu.nn0sl.NaturalNumber0Sequence(0, 1, 2)
        assert s.is_restricted_growth_function_sequence
        s = pu.nn0sl.NaturalNumber0Sequence(4, 3, 2)
        assert not s.is_restricted_growth_function_sequence
        s = pu.nn0sl.NaturalNumber0Sequence(0, 2, 1)
        assert not s.is_restricted_growth_function_sequence

    def test_canonical_natural_number_sequence(self):
        s = pu.nn0sl.NaturalNumber0Sequence(4, 3, 2)
        t = s.restricted_growth_function_sequence
        u = pu.nn0sl.NaturalNumber0Sequence(0, 1, 2)
        assert t == u

        s = pu.nn0sl.NaturalNumber0Sequence(0, 1, 2, 3)
        t = s.restricted_growth_function_sequence
        assert s == t

        s = pu.nn0sl.NaturalNumber0Sequence(1, 7, 9, 14, 14, 14, 12, 1, 3, 2, 7, 9)
        t = s.restricted_growth_function_sequence
        u = pu.nn0sl.NaturalNumber0Sequence(0, 1, 2, 3, 3, 3, 4, 0, 5, 6, 1, 2)
        assert t == u

    def test_image(self):
        s = pu.nn0sl.NaturalNumber0Sequence(1, 1, 1)
        assert s.image == (1,)
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 1)
        assert s.image == (1, 2,)
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 3)
        assert s.image == (1, 2, 3,)
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 2, 8, 3, 2, 3, 1, )
        assert s.image == (1, 2, 3, 8,)

    def test_image_cardinality(self):
        s = pu.nn0sl.NaturalNumber0Sequence(1, 1, 1)
        assert s.image_cardinality == 1
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 1)
        assert s.image_cardinality == 2
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 3)
        assert s.image_cardinality == 3
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 2, 8, 3, 2, 3, 1, )
        assert s.image_cardinality == 4

    def test_concatenation(self):
        s1 = pu.nn0sl.NaturalNumber0Sequence(1, 1, 1)
        s2 = pu.nn0sl.NaturalNumber0Sequence(1, )
        s3 = pu.nn0sl.NaturalNumber0Sequence(9, )
        s4 = pu.nn0sl.NaturalNumber0Sequence(6, 7, 2, )
        assert pu.nn0sl.concatenate_natural_number_0_sequences(s1, s2) == (1, 1, 1, 1,)
        assert pu.nn0sl.concatenate_natural_number_0_sequences(s4, s4, s4) == (6, 7, 2, 6, 7, 2, 6, 7, 2,)
        assert pu.nn0sl.concatenate_natural_number_0_sequences(s4, s3, s2, s1) == (6, 7, 2, 9, 1, 1, 1, 1,)

    def test_is_increasing(self):
        s = pu.nn0sl.NaturalNumber0Sequence(1, )
        assert s.is_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(17, )
        assert s.is_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 3, )
        assert s.is_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 2, 7, 8, 12, 2000, 2000, )
        assert s.is_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 1, )
        assert not s.is_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 2, 8, 9, 8, 2000, 2000, )
        assert not s.is_increasing

    def test_is_strictly_increasing(self):
        s = pu.nn0sl.NaturalNumber0Sequence(1, )
        assert s.is_strictly_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(17, )
        assert s.is_strictly_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 3, )
        assert s.is_strictly_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 2, 7, 8, 12, 2000, 2001, )
        assert not s.is_strictly_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 1, )
        assert not s.is_strictly_increasing
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 6, 7, 8, 100, 2000, 2000, )
        assert not s.is_strictly_increasing

    def test_refined_godel_order(self):
        """Test all combinations of sequence ordering under O1 up to sum(S) = n.

        :return:
        """
        t = ()
        for i in range(0, 100):
            n1: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.refined_godel_number_order.unrank(i)
            i2 = pu.nn0sl.refined_godel_number_order.rank(n1)
            assert i2 == i
            for j in range(0, 100):
                n2: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.refined_godel_number_order.unrank(j)
                if i < j:
                    assert n1.is_strictly_less_than(n2)
                    assert n1 < n2
                if j < i:
                    assert n2.is_strictly_less_than(n1)
                    assert n2 < n1
                if i == j:
                    assert n1.is_equal_to(n2)
                    assert n1 == n2

    def test_refined_godel_order_2(self):
        for i in range(8):
            # generate a random sequence
            n = random.randint(1, 8)
            m = tuple(random.randint(0, 32) for x in range(n))
            s1: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.NaturalNumber0Sequence(*m)
            r1 = s1.rank
            s2 = pu.nn0sl.NaturalNumber0Sequence.unrank(r1)
            r2 = s2.rank
            assert s1 == s2
            assert r1 == r2
        pass

    def test_refined_godel_order_3(self):
        s = pu.nn0sl.NaturalNumber0Sequence(2, 7, 4, 8, 5, 6, 2)
        r = s.rank
        s2 = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        r2 = s2.rank
        assert s == s2
        assert r == r2
        pass

    def test_least_element(self):
        assert pu.nn0sl.RefinedGodelNumberOrder.least_element == pu.nn0sl.NN0S()
        assert pu.nn0sl.NaturalNumber0Sequence.least_element == pu.nn0sl.NN0S()
        assert pu.nn0sl.empty_sequence == pu.nn0sl.NN0S()
        assert pu.nn0sl.trivial_sequence == pu.nn0sl.NN0S()

    def test_successor_unrank_consistency(self):
        for i in range(1024):
            s: pu.nn0sl.NaturalNumber0Sequence
            if i == 0:
                s = pu.nn0sl.NaturalNumber0Sequence.least_element
            else:
                s = s.successor
            s2 = pu.nn0sl.NaturalNumber0Sequence.unrank(i)
            assert s == s2
            assert s.rank == i

    def test_concatenate_with(self):
        assert pu.nn0sl.NaturalNumber0Sequence(0, 1, 2).concatenate_with(
            pu.nn0sl.NaturalNumber0Sequence(3, 4, 5)) == pu.nn0sl.NaturalNumber0Sequence(0, 1, 2, 3, 4, 5)
        assert pu.nn0sl.NaturalNumber0Sequence(7, 8, 15).concatenate_with(
            pu.nn0sl.NaturalNumber0Sequence(5)) == pu.nn0sl.NaturalNumber0Sequence(7, 8, 15, 5)
        assert pu.nn0sl.NaturalNumber0Sequence(7, 8, 15).concatenate_with(
            pu.nn0sl.NaturalNumber0Sequence()) == pu.nn0sl.NaturalNumber0Sequence(7, 8, 15)
        assert pu.nn0sl.NaturalNumber0Sequence().concatenate_with(
            pu.nn0sl.NaturalNumber0Sequence(7, 8, 15)) == pu.nn0sl.NaturalNumber0Sequence(7, 8, 15)
