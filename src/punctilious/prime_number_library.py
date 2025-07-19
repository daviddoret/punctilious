# https://oeis.org/A000040

def is_prime(n: int):
    r"""Returns `True` if `n` is prime, `False` otherwise."""

    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True


def get_next_prime(n: int):
    """Returns the first prime number > n."""
    if n < 2:
        return 2

    # Start checking from n1 + 1
    m = n + 1

    # If candidate is even (and > 2), make it odd
    if m > 2 and m % 2 == 0:
        m += 1

    # Check odd numbers until we find a prime
    while not is_prime(m):
        m += 2 if m > 2 else 1

    return m


def get_first_n_primes(n: int):
    p = 1
    l = ()
    for m in range(n):
        p = get_next_prime(p)
        l = l + (p,)
    return l
