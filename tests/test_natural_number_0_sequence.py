# import math
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

    def test_reverse(self):
        assert pu.nn0sl.NaturalNumber0Sequence().reverse == pu.nn0sl.NaturalNumber0Sequence()
        assert pu.nn0sl.NaturalNumber0Sequence(0).reverse == pu.nn0sl.NaturalNumber0Sequence(0)
        assert pu.nn0sl.NaturalNumber0Sequence(0, 1, 2, 3).reverse == pu.nn0sl.NaturalNumber0Sequence(3, 2, 1, 0)
        assert pu.nn0sl.NaturalNumber0Sequence(3, 2, 1, 0).reverse == pu.nn0sl.NaturalNumber0Sequence(0, 1, 2, 3)

    def test_concatenate_single(self, nns0, nns00, nns01, nns012345, nns0123456789_10_11):
        assert nns0.concatenate_with(nns00) == pu.nn0sl.NaturalNumber0Sequence(*nns0, *nns00)
        assert pu.nn0sl.concatenate_natural_number_0_sequences(nns0123456789_10_11,
                                                               nns00) == pu.nn0sl.NaturalNumber0Sequence(
            *nns0123456789_10_11, *nns00)

    def test_scalare_addition(self):

        s = pu.nn0sl.NaturalNumber0Sequence()
        s = s + 1
        assert s == pu.nn0sl.NaturalNumber0Sequence()

        s = pu.nn0sl.NaturalNumber0Sequence(0, 0, 0)
        s = s + 1
        assert s == pu.nn0sl.NaturalNumber0Sequence(1, 1, 1)

        s = pu.nn0sl.NaturalNumber0Sequence(0, 1, 2)
        s = s + 1
        assert s == pu.nn0sl.NaturalNumber0Sequence(1, 2, 3)

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
                    assert pu.nn0sl.refined_godel_number_order.relates(n1, n2)
                if j < i:
                    assert not pu.nn0sl.refined_godel_number_order.relates(n1, n2)
                if i == j:
                    assert not pu.nn0sl.refined_godel_number_order.relates(n1, n2)

    def test_combined_integer_with_sentinel_order(self):

        x = pu.nn0sl.NaturalNumber0Sequence()
        n = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.rank(x)
        assert n == 0
        x2 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.unrank(n)
        assert x == x2

        x = pu.nn0sl.NaturalNumber0Sequence(0)
        n = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.rank(x)
        assert n == 4294967296
        x2 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.unrank(n)
        assert x == x2

        for i in range(0, 128):
            sequence_length: int = random.randint(1, 256)
            fixed_length: int = random.randint(1, 16)
            l1: tuple[int, ...] = tuple(random.randint(0, 2 ** (fixed_length - 1)) for x in range(0, sequence_length))
            s1 = pu.nn0sl.NaturalNumber0Sequence(*l1)
            n1 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.rank(s1)
            s2 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.unrank(n1)
            assert s1 == s2

        s = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.least_element
        previous_s = None
        for i in range(0, 128):
            previous_s = s
            s = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.successor(s)
            n1 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.rank(s)
            s2 = pu.nn0sl.combined_fixed_length_integers_with_sentinel_order.unrank(n1)
            assert s == s2
            assert previous_s < s

    def test_asflslto_adjusted_sum(self):

        for r in range(4):
            adjusted_sum_from_rank = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.get_adjusted_sum_from_rank(
                r)
            s = pu.nn0sl.NaturalNumber0Sequence.from_rank(r)
            adjusted_sum_from_sequence = pu.nn0sl.get_adjusted_sum(
                s)
            assert adjusted_sum_from_rank == adjusted_sum_from_sequence
            pass

    def test_order(self):

        s = pu.nn0sl.NaturalNumber0Sequence(1, 0)
        r = s.rank
        t = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        assert s == t

        # OK
        s = pu.nn0sl.NaturalNumber0Sequence(1, 2, 3)
        r = s.rank
        t = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        assert s == t

        # ??
        s = pu.nn0sl.NaturalNumber0Sequence(3, 2, 1)
        r = s.rank
        t = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        assert s == t

        s = pu.nn0sl.NaturalNumber0Sequence(0, )
        r = s.rank
        t = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        assert s == t

        s = pu.nn0sl.NaturalNumber0Sequence()
        r = s.rank
        t = pu.nn0sl.NaturalNumber0Sequence.unrank(r)
        assert s == t

        pass

        for i in range(8):
            # generate a random sequence
            n = random.randint(1, 3)
            m = tuple(random.randint(0, 3) for x in range(n))
            s1: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.NaturalNumber0Sequence(*m)
            r1 = s1.rank
            s2 = pu.nn0sl.NaturalNumber0Sequence.unrank(r1)
            r2 = s2.rank
            assert s1 == s2
            assert r1 == r2
        pass

    def test_order_2(self):
        s = pu.nn0sl.NaturalNumber0Sequence(2, 7, 4, 8, )
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
        for i in range(64):
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

    def test_cantor_tupling_with_sentinel_value_order(self):
        for i in range(32):
            l = random.randint(0, 8)
            s = tuple(random.randint(0, 8) for x in range(l))
            s = pu.nn0sl.NaturalNumber0Sequence(*s)
            n = pu.nn0sl.CantorTuplingWithSentinelValue.rank(s)
            s2 = pu.nn0sl.CantorTuplingWithSentinelValue.unrank(n)
            assert s == s2


class TestAS1L2RL3O:

    def test_as1l2rl3o_class_consistency(self):
        r"""The consistency between the size of the "adjusted sum" classes
        and the sum of the sizes of the "adjusted sum and length" classes for the same sum.
        """

        MAX_SIZE = 32

        for s in range(MAX_SIZE):
            sum_class_size = pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
                s)
            cumulative_sum_length_class_size = 0
            for j in range(s + 1):
                cumulative_sum_length_class_size += pu.nn0sl.AS1L2RL3O.get_adjusted_sum_and_length_class_rank_cardinality(
                    s, j)
            assert sum_class_size == cumulative_sum_length_class_size

    def test_as1l2rl3o_class_and_rank(self):

        s = pu.nn0sl.NaturalNumber0Sequence()
        previous_r = 0
        previous_r2 = 0
        for i in range(0, 32):
            r = pu.nn0sl.get_lexicographic_rank_within_adjusted_sum_and_length_class(
                s)
            assert r >= previous_r or r == previous_r - 1  # remember the canonical order is reverse lexicographic
            previous_r = r
            r2 = pu.nn0sl.get_reverse_lexicographic_rank_within_adjusted_sum_and_length_class(
                s)
            assert r2 == 0 or r2 == previous_r2 + 1
            previous_r2 = r2
            s = s.successor

    def test_as1l2rl3o_order_long_random_sequences(self):

        MAX_TESTS = 32
        MAX_SEQUENCE_LENGTH = 128
        MAX_ELEMENT_VALUE = 32

        for i in range(MAX_TESTS):
            l = random.randint(0, MAX_SEQUENCE_LENGTH)
            s = tuple(random.randint(0, MAX_ELEMENT_VALUE) for x in range(l))
            s = pu.nn0sl.NaturalNumber0Sequence(*s)
            n = pu.nn0sl.AS1L2RL3O.rank(s)
            s2 = pu.nn0sl.AS1L2RL3O.unrank(n)
            assert s == s2

    def test_as1l2rl3o_class_cardinalities(self):

        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            0) == 1
        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            1) == 1
        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            2) == 2
        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            3) == 4
        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            4) == 8
        assert pu.nn0sl.AS1L2RL3O.get_adjusted_sum_class_rank_cardinality(
            5) == 16
        pass

    def test_as1l2rl3o_order(self):

        RANK_MAX = 256

        # fill in a list of RANK_MAX sequences using the successor function
        l = []
        s = pu.nn0sl.NaturalNumber0Sequence()
        l.append(s)
        for rank in range(RANK_MAX):
            s = pu.nn0sl.AS1L2RL3O.successor(s)
            l.append(s)

        for i, s in enumerate(l):
            rank_of_s: int = pu.nn0sl.AS1L2RL3O.rank(s)
            unrank_s = pu.nn0sl.AS1L2RL3O.unrank(rank_of_s)
            assert s == unrank_s
            for j, t in enumerate(l):
                rank_of_t: int = pu.nn0sl.AS1L2RL3O.rank(t)
                if i < j:
                    assert pu.nn0sl.AS1L2RL3O.relates(s, t)
                    assert s < t
                    assert rank_of_s < rank_of_t
                if i == j:
                    assert not pu.nn0sl.AS1L2RL3O.relates(s, t)
                    assert not s < t
                    assert not rank_of_s < rank_of_t
                if i > j:
                    assert not pu.nn0sl.AS1L2RL3O.relates(s, t)
                    assert not s < t
                    assert not rank_of_s < rank_of_t
