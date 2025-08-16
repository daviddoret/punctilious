import math
import punctilious as pu


def binom(n, k):
    if k < 0 or n < 0 or k > n:
        return 0
    return math.comb(n, k)


def get_lexicographic_rank_within_adjusted_sum_and_length_class(x):
    r"""

    :param x:
    :param s:
    :param l:
    :return:
    """
    x: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.NaturalNumber0Sequence.from_any(x)
    l: int = x.length
    s: int = x.sum + x.length

    # This function algorithm is designed for 1-based natural numbers,
    # adjust the sequence accordingly:
    adjusted_x: pu.nn0sl.NaturalNumber0Sequence = x.scalar_addition(1)
    rank: int = 0  # 1-based rank
    r: int = s
    for i in range(l - 1):  # positions 0..l-2
        k: int = l - (i + 1)
        rank += binom(r - 1, k) - binom(r - adjusted_x[i], k)
        r -= adjusted_x[i]
    return rank


def get_reverse_lexicographic_rank_within_adjusted_sum_and_length_class(x):
    r"""Returns the rank

    :param x:
    :param s:
    :param l:
    :return:
    """
    x: pu.nn0sl.NaturalNumber0Sequence = pu.nn0sl.NaturalNumber0Sequence.from_any(x)
    l: int = x.length
    s: int = x.sum + x.length

    if x == ():
        return 0
    if x == (1,):
        return 0
    total: int = binom(s - 1, l - 1)
    return total - get_lexicographic_rank_within_adjusted_sum_and_length_class(x) - 1


x = pu.nn0sl.NaturalNumber0Sequence()
for i in range(32):
    # x2 = x.scalar_addition(1)
    # assert adjusted_sum == x2.sum
    r = get_lexicographic_rank_within_adjusted_sum_and_length_class(x)
    r_reversed = get_reverse_lexicographic_rank_within_adjusted_sum_and_length_class(x)
    print(
        f"{i},     s: {x},         {r}, {r_reversed}")
    # class_arity = pu.nn0sl.AdjustedSumFirstLengthSecondLexicographicThirdOrder.get_adjusted_sum_and_length_class_rank_cardinality(
    #    8, l)
    # r2 = class_arity - r
    # print(r)
    x = x.successor
