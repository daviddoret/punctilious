import punctilious as pu
import random


class TestDeduplicateIntegerSequence:
    def test_deduplicate_integer_sequence(self):
        assert pu.util.deduplicate_integer_sequence(()) == ()
        assert pu.util.deduplicate_integer_sequence((1, 2, 3,)) == (1, 2, 3,)
        assert pu.util.deduplicate_integer_sequence((5, 7, 1, 5, 2, 6, 6, 7, 4, 3, 0,)) == (5, 7, 1, 2, 6, 4, 3, 0)

    def test_decrement_last_element(self):
        assert pu.util.decrement_last_element((0, 0, 0, 1,)) == (0, 0, 0, 0,)
        assert pu.util.decrement_last_element((4, 3, 2,)) == (4, 3, 1,)
        assert pu.util.decrement_last_element((1,)) == (0,)

    def test_increment_last_element(self):
        assert pu.util.increment_last_element((0, 0, 0, 0,)) == (0, 0, 0, 1,)
        assert pu.util.increment_last_element((4, 3, 2,)) == (4, 3, 3,)
        assert pu.util.increment_last_element((0,)) == (1,)
        assert pu.util.increment_last_element((1,)) == (2,)


class TestIntToBitsAndBitsToInt:
    def test_int_to_bits_and_bits_to_int(self):
        for n in range(0, 128):
            b = pu.util.int_to_bits(n=n, bit_positional_significance="msb", fixed_length=12)
            n2 = pu.util.bits_to_int(bits=b, bit_positional_significance="msb")
            assert n == n2
            b = pu.util.int_to_bits(n=n, bit_positional_significance="lsb", fixed_length=12)
            n2 = pu.util.bits_to_int(bits=b, bit_positional_significance="lsb")
            assert n == n2


class TestIntegerCombinationWithSentinel:
    def test_integer_combination_with_sentinel(self):
        for i in range(0, 128):
            sequence_length: int = random.randint(1, 256)
            fixed_length: int = random.randint(1, 16)
            l1: tuple[int, ...] = tuple(random.randint(0, 2 ** (fixed_length - 1)) for x in range(0, sequence_length))
            n1 = pu.util.combine_fixed_length_ints_with_sentinel(l1, fixed_length=fixed_length)
            l2 = pu.util.split_fixed_length_ints_with_sentinel(n1, fixed_length=fixed_length)
            assert l1 == l2
