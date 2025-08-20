import punctilious.util as util


def _find_largest_n_such_that_phi_smaller_than_n(n: int) -> int:
    r"""

    Find the largest integer w such that w*(w + 1)/2 <= n
    Using the quadratic formula: w = floor((sqrt(8*n + 1) - 1)/2)
    But we need to compute it with integer arithmetic to avoid floating-point errors

    :param n:
    :return:
    """

    # Initialize bounds for binary search
    low: int = 0
    high: int = 1
    while high * (high + 1) // 2 <= n:
        high *= 2

    # Binary search to find w
    while low < high:
        mid: int = (low + high + 1) // 2
        t: int = mid * (mid + 1) // 2
        if t <= n:
            low = mid
        else:
            high = mid - 1

    w: int = low
    return w


def cantor_pairing_inverse(n: int) -> tuple[int, int]:
    r"""Returns the output of the inverse Cantor pairing function on :math:`n`.

    Note
    -----
    The Cantor pairing function maps two (0-based) natural numbers to a unique (0-based) natural number.
    Its inverse functions maps the unique (0-based) natural number back to the original pair.

    Definition
    ------------
    :math:`π(x,y) = (x + y)(x + y + 1)/2 + y`

    Bibliography
    ---------------
    - https://en.wikipedia.org/wiki/Pairing_function

    :param n: A (0-based) natural number.
    :return: A pair of (0-based) natural numbers.
    """
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` must be greater or equal to 0.", n=n)

    # w: int = int(((8 * n + 1) ** 0.5 - 1) / 2)  # floating-point version, yield incorrect results when n gets large.
    w: int = _find_largest_n_such_that_phi_smaller_than_n(n)

    t: int = (w * (w + 1)) // 2
    y: int = n - t
    x: int = w - y
    return x, y


def cantor_pairing(x: int, y: int) -> int:
    r"""Returns the output of the Cantor pairing function on :math:`x` and :math:`y`.

    Note
    -----
    The Cantor pairing function maps two (0-based) natural numbers to a unique (0-based) natural number.

    Definition
    ------------
    :math:`π(x,y) = (x + y)(x + y + 1)/2 + y`

    Or equivalently:

    :math:`π(x,y) = \dfrac{x^2 + x + 2xy + 3y + y^2}{2}`

    Bibliography
    ---------------
    - https://en.wikipedia.org/wiki/Pairing_function

    :param x: A (0-based) natural number.
    :param y: A (0-based) natural number.
    :return: A (0-based) natural number.
    """
    x: int = int(x)
    y: int = int(y)
    if x < 0:
        raise util.PunctiliousException("`x` must be greater or equal to 0.", x=x)
    if y < 0:
        raise util.PunctiliousException("`y` must be greater or equal to 0.", y=y)
    return ((x + y) * (x + y + 1)) // 2 + y


def cantor_tupling_with_sentinel_value(*s: int) -> int:
    r"""Returns the Cantor tuple function output of `s`, with a sentinel value to enable the inverse function.

    :param s: A (0-based) natural number sequence.
    :return: A (0-based) natural number.
    """
    s: tuple[int, ...] = tuple(int(n) for n in s)
    if any(n < 0 for n in s):
        raise util.PunctiliousException("All elements of `s` must be greater or equal to 0.", s=s)
    l: int = len(s)
    if l == 0:
        # case #1: empty sequence.
        return 0
    elif l == 1:
        # case #2: sequences containing 1 element.
        return cantor_pairing(s[0], l)
    elif l == 2:
        # case #3: sequences containing 2 elements.
        # the pair
        c: int = cantor_pairing(s[0], s[1])
        # the sentinel value
        c = cantor_pairing(c, l)
        return c
    else:
        # case #3: sequences containing more than 2 elements.
        # first pair
        s0: int = s[0]
        s1: int = s[1]
        c: int = cantor_pairing(s0, s1)
        for i in range(2, l):
            # subsequent pairs
            si: int = s[i]
            c = cantor_pairing(c, si, )
        # sentinel value
        c = cantor_pairing(c, l)
        return c


def cantor_tupling_with_sentinel_value_inverse(n: int) -> tuple[int, ...]:
    n: int = int(n)
    # retrieve the sentinel value
    l: int
    n, l = cantor_pairing_inverse(n)
    if l == 0:
        # case #1: the empty sequence
        # note that `n` is simply dropped
        # it follows that there is an infinity of natural numbers mapped to ()
        return ()
    elif l == 1:
        # case #2: sequence with 1 element
        # note that the element was already retrieved during the first cantor pairing inverse function.
        s0: int = n
        return s0,
    elif l == 2:
        # case #2: sequence with 2 elements
        s0: int
        s1: int
        s0, s1 = cantor_pairing_inverse(n)
        return s0, s1,
    else:
        # case #3: sequence with more than 2 elements.
        # apply `l` times the Cantor pairing function inverse to retrieve the original sequence
        s: tuple[int, ...] = ()
        i: int
        x: int
        y: int
        for i in range(l - 1):
            x, y = cantor_pairing_inverse(n)
            n: int = x
            s_i: int = y
            s = (s_i,) + s
            if i == l - 2:
                # first element
                s0: int = x
                s = (s0,) + s
        return s
