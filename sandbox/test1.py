from math import comb
import punctilious as pu


def unrank_weak_composition_lex(r: int, l: int, s: int):
    """
    Return the 0-based lexicographic r-th sequence T of length l consisting of natural numbers
    such that sum(T) + l = s, i.e., sum(T) = n = s - l.

    Assumptions:
      - r is 0-based (i.e., the first sequence has r = 0).
      - Lexicographic order compares tuples left-to-right, with smaller numbers first.

    Raises:
      - ValueError if inputs are invalid or r is out of range.

    Complexity:
      - Time: O(l log n), Space: O(1) besides the output, using math.comb for exact big integers.
    """
    if l <= 0:
        raise ValueError("l must be a positive integer")
    if s < l:
        raise ValueError("s must be at least l (since entries are nonnegative)")

    n = s - l  # total sum to distribute among l slots
    total = comb(n + l - 1, l - 1)
    if r < 0 or r >= total:
        raise ValueError(f"rank r out of range: 0 <= r < {total}")

    T = [0] * l
    m = n  # remaining sum

    for i in range(l):
        # k is the number of remaining slots AFTER this position
        k = l - i - 1

        if k == 0:
            # Last slot is forced
            T[i] = m
            # r should now be 0
            # (Optional) assert r == 0
            break

        # We need to find smallest x in [0, m] with S(x+1) > r,
        # where S(x) = C(m + k, k) - C(m - x + k, k).
        # Equivalently, find the largest x with C(m - x + k, k) >= C(m + k, k) - r.
        target = comb(m + k, k) - r

        lo, hi = 0, m  # search over x
        # We want the largest x such that comb(m - x + k, k) >= target
        while lo <= hi:
            mid = (lo + hi) // 2
            val = comb(m - mid + k, k)
            if val >= target:
                lo = mid + 1
            else:
                hi = mid - 1
        x = hi  # largest x meeting the inequality

        # Update r: subtract the number of sequences with first entry < x
        # S(x) = C(m + k, k) - C(m - x + k, k)
        r -= comb(m + k, k) - comb(m - x + k, k)

        T[i] = x
        m -= x

    return T


# Example usage:
# l = 3, s = 7 -> n = 4. All length-3 sequences summing to 4 in lex order.
# r = 0 -> [0,0,4]
# r = 1 -> [0,1,3]
# r = 2 -> [0,2,2]
# r = 3 -> [0,3,1]
# r = 4 -> [0,4,0]
# r = 5 -> [1,0,3]
# ...
for i in range(32):
    adjusted_sum = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.get_adjusted_sum_from_rank(i)
    l = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.get_length_from_rank(i)
    if l == 0:
        s = ()
        print(s)
    else:
        # take the last element in the set
        last = (0,) * (l - 1) + (adjusted_sum - l,)
        r = pu.nn0sl.AdjustedSumFirstLengthSecondReverseLexicographicThirdOrder.rank(last)
        # get the rank of the sequence in its adjusted sum and length class
        j = r - i  # trick: this is reverse lexicographic order
        z = unrank_weak_composition_lex(j, l, adjusted_sum)
        print(z)
