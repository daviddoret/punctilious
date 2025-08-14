from math import log2


def a(n: int) -> int:
    """
    Length of the nth finite sequence of nonnegative integers
    ordered by (sum+length), then length, then lexicographic order.
    0-based n. Returns a(n).
    """
    if n == 0:
        return 0

    # Determine weight t: indices [2^(t-1), 2^t - 1] are weight t
    t = n.bit_length()  # since 2^(t-1) <= n < 2^t for n>=1
    m = t - 1
    r = n - (1 << (t - 1))  # offset within the weight-t block

    # Find smallest L in {1,...,t} with cumulative > r,
    # where cumulative(j) = sum_{k=0}^{j-1} C(m, k) for j>=1.
    # We iterate binomial coefficients C(m,k) incrementally.
    cum = 0
    c = 1  # C(m,0)
    for j in range(1, t + 1):  # j plays the role of L
        cum += c
        if r < cum:
            return j
        # update c = C(m, j) from C(m, j-1)
        # safe integer arithmetic: c *= (m - (j-1)); c //= j
        c = c * (m - (j - 1)) // j

    # Should never reach here
    raise RuntimeError("Unexpected state")


# Quick test: print first few terms
if __name__ == "__main__":
    seq = [a(i) for i in range(128)]
    print(seq)
