import math
import punctilious.util as util


# Catalan numbers
# 1, 1, 2, 5, 14, 42, 132, 429, 1430,
# https://oeis.org/A000108
# https://en.wikipedia.org/wiki/Catalan_number

def get_catalan_number(n: int):
    """Returns the `n`-th Catalan number with `n` index starting at 0.

    :param n:
    :return:
    """
    #  (2n)!/(n!(n+1)!)
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` must be greater or equal to 1.")
    return int(math.factorial(2 * n) / (math.factorial(n) * math.factorial(n + 1)))
