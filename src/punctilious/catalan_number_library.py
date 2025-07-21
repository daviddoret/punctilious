import math
import functools
import punctilious.util as util


@functools.lru_cache(maxsize=None)
def get_catalan_number(n: int) -> int:
    """Returns the `n`-th Catalan number with `n` index starting at 0.

    Catalan numbers
    1, 1, 2, 5, 14, 42, 132, 429, 1430,
    https://oeis.org/A000108
    https://en.wikipedia.org/wiki/Catalan_number


    :param n:
    :return:
    """
    #  (2n)!/(n!(n+1)!)
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` must be greater or equal to 0.")
    # return int(math.factorial(2 * n) / (math.factorial(n) * math.factorial(n + 1)))
    return math.comb(2 * n, n) // (n + 1)


def get_catalan_triangle_number(n: int, k: int):
    r"""Compute the Catalan triangle value C(n, k).

    Bibliography
    --------------

    - https://en.wikipedia.org/wiki/Catalan%27s_triangle

    """
    if k > n or k < 0:
        return 0
    if k == 0 or k == n:
        return 1
    return get_catalan_triangle_number(n - 1, k) + get_catalan_triangle_number(n, k - 1)


c = get_catalan_number  # Shortcut for get_catalan_number

ct = get_catalan_triangle_number  # Shortcut for get_catalan_triangle_number
