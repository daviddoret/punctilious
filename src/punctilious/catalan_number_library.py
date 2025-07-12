import math
import punctilious.util as util


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
    return int(math.factorial(2 * n) / (math.factorial(n) * math.factorial(n + 1)))


c = get_catalan_number  # Shortcut for get_catalan_number
