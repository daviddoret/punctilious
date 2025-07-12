import math
import punctilious.util as util

_bell_numbers: tuple[int, ...] = ()  # A private database of bell numbers to cache recursions.


def get_bell_number(n: int) -> int:
    """Returns the `n`-th Bell number with `n` index starting at 0.

    List of first elements
    ________________________
    1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570, 4213597, 27644437, 190899322, 1382958545, 10480142147, 82864869804, 682076806159, 5832742205057, 51724158235372, 474869816156751, 4506715738447323, 44152005855084346, 445958869294805289, 4638590332229999353, 49631246523618756274

    References
    ____________
    - https://en.wikipedia.org/wiki/Bell_number
    - https://oeis.org/A000110

    :param n: A 0-based natural number
    :return:
    """
    global _bell_numbers
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` must be greater or equal to 0.")
    else:
        while len(_bell_numbers) < n + 1:
            # Generate cache.
            m: int = len(_bell_numbers)
            if m == 0:
                b: int = 1
                _bell_numbers = (b,)
            else:
                # b: int = sum(math.comb(m - 1, k) * get_bell_number(k) for k in range(0, m - 1))
                b: int = 0
                k: int
                for k in range(0, m):
                    b += math.comb(m - 1, k) * get_bell_number(k)
                _bell_numbers = _bell_numbers + (b,)
    return _bell_numbers[n]


c = get_bell_number  # Shortcut for get_bell_number
