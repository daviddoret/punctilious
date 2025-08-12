from typing import Tuple


def increment_lexicographic_rank(s: Tuple[int, ...]) -> Tuple[int, ...]:
    """
    Return the next tuple in reverse-lexicographic order within the class of
    nonnegative integer tuples of the same length and the same adjusted sum
    (adjusted sum = sum(s) + len(s)). The first tuple in this order is
    (N, 0, 0, ..., 0) and the last is (0, 0, ..., 0, N), where N = sum(s).

    Raises ValueError if s is already the last tuple in this class.
    """
    if not isinstance(s, tuple) or not s:
        raise ValueError("Input must be a non-empty tuple of nonnegative integers.")
    if any((not isinstance(x, int)) or x < 0 for x in s):
        raise ValueError("All elements must be integers >= 0.")

    n = len(s)
    # Find the rightmost index i (but not the last position) with s[i] > 0.
    # If none exists, we are at the last tuple (..., 0, 0, N).
    for i in range(n - 2, -1, -1):
        if s[i] > 0:
            # Move one unit from position i to position i+1,
            # and pack the entire tail sum to i+1 to keep the result as large
            # as possible under the new prefix (i.e., immediate next in reverse-lex order).
            tail_sum = 1 + sum(s[i + 1:])  # the 1 we moved plus existing tail
            out = list(s)
            out[i] -= 1
            out[i + 1] = tail_sum
            for j in range(i + 2, n):
                out[j] = 0
            return tuple(out)

    # If we didn’t find such an i, we’re at the end of the class.
    raise ValueError("End of class reached.")


s = (3, 0, 0, 0,)
for i in range(32):
    print(s)
    s = increment_lexicographic_rank(s)
