"""Incomplete work. Could introduce a new order over natural-number-sequences.

"""

import util as util
import natural_number_1_sequence_library as nnsl


# n = 10
# t = ()
# for n in range(1, n):
#    t = nnsl.NaturalNumberSequence.get_o1_ordered_set_of_natural_number_sequences_of_sum_n(n)
#    print(len(t))

def composition_from_index(n: int, index: int) -> tuple[int, ...]:
    """Unrank: given n and index (0 ≤ index < 2^(n-1)), return the corresponding composition."""
    bits = bin(index)[2:].zfill(n - 1)
    composition = []
    count = 1
    for bit in bits:
        if bit == '0':
            count += 1
        else:
            composition.append(count)
            count = 1
    composition.append(count)
    return tuple(composition)


def index_from_composition(seq: tuple[int, ...]) -> int:
    """Rank: given a composition of n, return its index among all compositions of n."""
    bits = []
    for part in seq[:-1]:
        bits.extend(['0'] * (part - 1) + ['1'])
    print(bits)
    return int(''.join(bits), 2)


def to_stars_and_bars_tuple(seq: tuple[int, ...], star: str = '★', bar: str = '|', closing_bar: bool = False) -> tuple[
    str, ...]:
    """Rank: given a composition of n, return its index among all compositions of n.

    References
    ----------

    - https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

    """
    star = str(star)
    if len(star) != 1:
        raise util.PunctiliousException('Invalid `star` parameter.', star=star)
    bar = str(bar)
    if len(bar) != 1:
        raise util.PunctiliousException('Invalid `bar` parameter.', bar=bar)
    if star == bar:
        raise util.PunctiliousException('Equal `star` and `bar` parameters.', star=star, bar=bar)
    stars_and_bars_tuple = ()
    for part in seq[:-1]:  # -1 because we don't need a delimiter after the last part.
        stars_and_bars_tuple += (star * (part - 1) + bar,)
    # append final leading stars
    stars_and_bars_tuple += (star * (seq[-1] - 1),)
    if closing_bar:
        # append closing bar
        stars_and_bars_tuple += (bar,)
    return stars_and_bars_tuple


def to_stars_and_bars_string(seq: tuple[int, ...], star: str = '0', bar='1') -> str:
    """Rank: given a composition of n, return its index among all compositions of n."""
    star = str(star)
    if len(star) != 1:
        raise util.PunctiliousException('Invalid `star` parameter.', star=star)
    bar = str(bar)
    if len(bar) != 1:
        raise util.PunctiliousException('Invalid `bar` parameter.', bar=bar)
    if star == bar:
        raise util.PunctiliousException('Equal `star` and `bar` parameters.', star=star, bar=bar)
    return ''.join(to_stars_and_bars_tuple(seq, star=star, bar=bar))


def to_stars_and_bars_int(seq: tuple[int, ...]) -> int:
    """Rank: given a composition of n, return its index among all compositions of n."""
    return int(to_stars_and_bars_string(seq, star='0', bar='1'), 2)


def from_stars_and_bars_tuple(n: int, index: int) -> tuple[int, ...]:
    """Unrank: given n and index (0 ≤ index < 2^(n-1)), return the corresponding composition."""
    bits = bin(index)[2:].zfill(n - 1)
    composition = []
    count = 1
    for bit in bits:
        if bit == '0':
            count += 1
        else:
            composition.append(count)
            count = 1
    composition.append(count)
    return tuple(composition)


# print(sum(s))
# i = index_from_composition(s)
# print(i)
# print
d = {}
s = (1,)
t = to_stars_and_bars_string(s)
d[s] = t
# print(to_stars_and_bars_int(s))
s = (1, 1,)
t = to_stars_and_bars_string(s)
d[s] = t
# print(to_stars_and_bars_int(s))
s = (1, 2,)
t = to_stars_and_bars_string(s)
d[s] = t
s = (1, 3,)
t = to_stars_and_bars_string(s)
d[s] = t
# print(to_stars_and_bars_int(s))
s = (2, 1,)
t = to_stars_and_bars_string(s)
d[s] = t
# print(to_stars_and_bars_int(s))
s = (2, 2,)
t = to_stars_and_bars_string(s)
d[s] = t
# print(to_stars_and_bars_int(s))
pass
