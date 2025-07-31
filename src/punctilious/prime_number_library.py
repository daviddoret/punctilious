# https://oeis.org/A000040
from functools import lru_cache
import punctilious.util as util


@lru_cache(maxsize=None, typed=False)  # Unlimited cache size
def factorize(n: int) -> tuple[int, ...]:
    r"""Returns the prime factors :math:`(p_0, p_1, p_2, \ldots, p_m)` of n, such that :math:`2^{p_0} \cdot 3^{p_1} \cdot 5^{p_2} \cdot \ldots = n`.

    Note
    -----
    This is a naive algorithm. It can take a very long period of time for large numbers.

    :param n: A (0-based) natural number.
    :return: A tuple of prime factors.
    """
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` is not a (0-based) natural number.", n=n)
    l: tuple[int, ...] = ()
    p: int = 1
    while True:
        p: int = get_next_prime(p)
        factor: int = 0
        while n % p == 0:
            factor: int = factor + 1
            n = n // p  # Floor division is safe, because we know that p is a factor of n.
        l: tuple[int, ...] = l + (factor,)
        if n == 1:
            return l


@lru_cache(maxsize=None, typed=False)  # Unlimited cache size
def is_prime(n: int):
    r"""Returns `True` if `n` is prime, `False` otherwise.

    :param n: A (0-based) natural number.
    :return: `True` or `False`.
    """
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` is not a (0-based) natural number.", n=n)
    if n < 2:
        return False
    elif n == 2:
        return True  # 2 is the first prime number.
    elif n % 2 == 0:
        return False  # Even numbers are not prime. This is a minor optimization.
    else:
        # Check odd divisors up to sqrt(n)
        i: int = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2  # Pick the next odd number.
        return True


@lru_cache(maxsize=None, typed=False)  # Unlimited cache size
def get_next_prime(n: int) -> int:
    r"""Returns the first prime number p such that p > n.

    :param n: A (0-based) natural number.
    :return: A prime number.
    """
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` is not a (0-based) natural number.", n=n)
    if n < 2:
        # The first prime number.
        return 2

    # Start checking for the next prime starting from n + 1.
    m: int = n + 1

    # If the first candidate prime number is even (and > 2), make it odd.
    # This is a basic optimization that allows to only check the primality of odd numbers.
    if m % 2 == 0:
        m += 1

    # Check odd numbers until we find a prime number.
    while not is_prime(m):
        m += 2

    return m


def get_first_n_primes(n: int) -> tuple[int, ...]:
    r"""Returns a tuple whose elements are the first `n` prime numbers.

    :param n: A (0-based) natural number.
    :return: A tuple of prime numbers.
    """
    n: int = int(n)
    if n < 0:
        raise util.PunctiliousException("`n` is not a (0-based) natural number.", n=n)
    p: int = 1
    l: tuple[int, ...] = ()
    m: int
    for m in range(n):
        p: int = get_next_prime(p)
        l: tuple[int, ...] = l + (p,)
    return l
