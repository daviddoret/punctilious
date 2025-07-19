def sieve_of_eratosthenes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []

    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False

    return [i for i in range(2, limit + 1) if sieve[i]]


def get_prime(n):
    """Get the nth prime number (0-indexed)."""
    if n == 0:
        return 2

    # Estimate upper bound for nth prime using prime number theorem
    if n < 6:
        limit = 15
    else:
        import math
        limit = int(n * (math.log(n) + math.log(math.log(n))))

    primes = sieve_of_eratosthenes(limit)

    # If we don't have enough primes, expand the search
    while len(primes) <= n:
        limit *= 2
        primes = sieve_of_eratosthenes(limit)

    return primes[n]


def prime_factorization(n):
    """Return prime factorization as list of (prime, exponent) pairs."""
    if n <= 1:
        return []

    factors = []
    d = 2

    while d * d <= n:
        exp = 0
        while n % d == 0:
            n //= d
            exp += 1
        if exp > 0:
            factors.append((d, exp))
        d += 1

    if n > 1:
        factors.append((n, 1))

    return factors


def unrank_godel(godel_number):
    """
    Unrank a Gödel number back to a sequence of 0-based natural numbers.

    Uses the standard Gödel numbering: g = 2^(a0+1) * 3^(a1+1) * 5^(a2+1) * ...
    where the sequence is [a0, a1, a2, ...]

    Args:
        godel_number (int): The Gödel number to unrank

    Returns:
        list: The original sequence of 0-based natural numbers
    """
    if godel_number <= 0:
        raise ValueError("Gödel number must be positive")

    if godel_number == 1:
        return []  # Empty sequence

    # Get prime factorization
    factors = prime_factorization(godel_number)

    # Convert to dictionary for easier lookup
    factor_dict = {prime: exp for prime, exp in factors}

    # Find the highest prime in the factorization to determine sequence length
    if not factors:
        return []

    max_prime = max(prime for prime, _ in factors)

    # Generate enough primes to find the index of max_prime
    primes = sieve_of_eratosthenes(max_prime + 1)
    prime_to_index = {prime: i for i, prime in enumerate(primes)}

    if max_prime not in prime_to_index:
        raise ValueError(f"Error in prime generation for {max_prime}")

    max_index = prime_to_index[max_prime]

    # Reconstruct the sequence
    sequence = []
    for i in range(max_index + 1):
        prime = primes[i]
        exponent = factor_dict.get(prime, 0)
        if exponent > 0:
            sequence.append(exponent - 1)  # Convert back to 0-based
        else:
            # This shouldn't happen with valid Gödel numbers
            # but we include it for robustness
            sequence.append(0)

    # Remove trailing zeros (they represent the end of meaningful sequence)
    while sequence and sequence[-1] == 0:
        sequence.pop()

    return sequence


def rank_godel(sequence):
    """
    Rank a sequence of 0-based natural numbers to its Gödel number.
    Useful for testing the unrank function.

    Args:
        sequence (list): Sequence of 0-based natural numbers

    Returns:
        int: The corresponding Gödel number
    """
    if not sequence:
        return 1

    result = 1
    for i, value in enumerate(sequence):
        prime = get_prime(i)
        result *= prime ** (value + 1)

    return result


for n in range(1, 100):
    print(f"{n}: {unrank_godel(n)}")
