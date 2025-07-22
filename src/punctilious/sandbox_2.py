def cantor_pair(x, y):
    """
    Cantor pairing function: maps two natural numbers to a unique natural number.
    π(x,y) = (x + y)(x + y + 1)/2 + y
    """
    return ((x + y) * (x + y + 1)) // 2 + y


def cantor_unpair(z):
    """
    Inverse of Cantor pairing function: maps a natural number back to a pair.
    """
    # Find the triangular root
    w = int(((8 * z + 1) ** 0.5 - 1) / 2)
    t = (w * (w + 1)) // 2
    y = z - t
    x = w - y
    return (x, y)


def rank_pair(x, y):
    """
    Ranking function: maps a pair (x,y) to its rank in the canonical order.
    Lower ranks correspond to pairs that come later in the order.
    """
    return cantor_pair(x, y)


def unrank_pair(rank):
    """
    Unranking function: maps a rank back to the corresponding pair.
    """
    return cantor_unpair(rank)


# Alternative comparison function for pairs
def pair_greater_than(pair1, pair2):
    """
    Returns True if pair1 > pair2 in the canonical order.
    """
    return rank_pair(*pair1) > rank_pair(*pair2)


# Test the implementation
if __name__ == "__main__":
    # Test some pairs and their ranks
    test_pairs = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0), (2, 1)]

    print("Pair -> Rank -> Pair (verification)")
    print("-" * 35)
    for pair in test_pairs:
        rank = rank_pair(*pair)
        recovered = unrank_pair(rank)
        print(f"{pair} -> {rank} -> {recovered}")

    print("\nOrder verification (higher rank = greater in order):")
    print("-" * 50)
    sorted_by_rank = sorted(test_pairs, key=lambda p: rank_pair(*p), reverse=True)
    for i, pair in enumerate(sorted_by_rank):
        rank = rank_pair(*pair)
        print(f"{i + 1}. {pair} (rank: {rank})")

    print("\nComparison examples:")
    print("-" * 20)
    print(f"(2,1) > (1,1): {pair_greater_than((2, 1), (1, 1))}")
    print(f"(0,2) > (1,1): {pair_greater_than((0, 2), (1, 1))}")
    print(f"(1,0) > (0,1): {pair_greater_than((1, 0), (0, 1))}")
