# https://en.wikipedia.org/wiki/G%C3%B6del_numbering_for_sequences

primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
          499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
          643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
          797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997,)


def factorize(n):
    l = ()
    for p in primes:
        f = 0
        while n % p == 0:
            f = f + 1
            n = n / p
        l = l + (f,)
        if n == 1:
            return l
    return l


def decrement_last_element(s):
    """Receives a sequence of natural numbers (s0, s1, ..., si) and returns (s0, s1, ..., si - 1).

    :param s:
    :return:
    """
    return s[0:-1] + (s[-1] - 1,)


def unrank(n):
    n += 1  # Makes the ranks 0-based.
    if n == 1:
        return ()
    else:
        f = factorize(n)
        # Decrement the last element by 1.
        # This hack makes leading zeroes meaningful.
        s = decrement_last_element(f)
        return s


def increment_last_element(s):
    """Receives a sequence of natural numbers (s0, s1, ..., si) and returns (s0, s1, ..., si + 1).

    :param s:
    :return:
    """
    return s[0:-1] + (s[-1] + 1,)


def rank(s):
    if s == ():
        return 0
    else:
        n = 1
        for i, f in enumerate(s):
            if i == len(s) - 1:
                # this is the last factor
                # Increment it to undo the encoding hack for leading zeroes.
                f += 1
            n = n * primes[i] ** f
        return n - 1


l = []
for n in range(0, 1000):
    s = unrank(n)
    if s in l:
        print(1 / 0)
    l.append(s)
    n2 = rank(s)
    print(f"{n},{n2}={s}")

pass
