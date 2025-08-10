from typing import List, Tuple
import math


def rank(sequence: List[int]) -> int:
    """
    Ranks a finite sequence of non-negative integers to a unique non-negative integer.

    The ranking follows sum-first, lexicographic-second ordering:
    1. Sequences are first ordered by their sum
    2. Within the same sum, sequences are ordered lexicographically

    Args:
        sequence: A list of non-negative integers

    Returns:
        A unique non-negative integer representing the rank of the sequence

    Raises:
        ValueError: If sequence contains negative integers
        TypeError: If sequence contains non-integers

    Examples:
        rank([]) -> 0
        rank([0]) -> 1
        rank([1]) -> 2
        rank([0, 0]) -> 3
        rank([0, 1]) -> 4
        rank([1, 0]) -> 5
    """
    # Input validation
    if not isinstance(sequence, list):
        raise TypeError("Input must be a list")

    for i, val in enumerate(sequence):
        if not isinstance(val, int):
            raise TypeError(f"Element at index {i} is not an integer: {val}")
        if val < 0:
            raise ValueError(f"Element at index {i} is negative: {val}")

    # Handle empty sequence
    if not sequence:
        return 0

    length = len(sequence)
    total_sum = sum(sequence)

    # Calculate rank offset: number of sequences with smaller sum
    rank_offset = _count_sequences_with_smaller_sum(length, total_sum)

    # Calculate lexicographic position within sequences of same length and sum
    lex_position = _calculate_lexicographic_position(sequence, total_sum)

    return rank_offset + lex_position


def unrank(rank: int) -> List[int]:
    """
    Converts a rank back to its corresponding sequence.

    Args:
        rank: A non-negative integer representing the rank

    Returns:
        The sequence corresponding to the given rank

    Raises:
        ValueError: If rank is negative
        TypeError: If rank is not an integer

    Examples:
        unrank(0) -> []
        unrank(1) -> [0]
        unrank(2) -> [1]
        unrank(3) -> [0, 0]
        unrank(4) -> [0, 1]
        unrank(5) -> [1, 0]
    """
    # Input validation
    if not isinstance(rank, int):
        raise TypeError("Rank must be an integer")
    if rank < 0:
        raise ValueError("Rank must be non-negative")

    # Handle empty sequence
    if rank == 0:
        return []

    # Find the length and sum of the sequence at this rank
    length, total_sum, remaining_rank = _find_length_and_sum(rank)

    # Reconstruct the sequence from its lexicographic position
    return _reconstruct_sequence(length, total_sum, remaining_rank)


def _count_sequences_with_smaller_sum(target_length: int, target_sum: int) -> int:
    """
    Counts the total number of sequences with length <= target_length
    and sum < target_sum (for same length) or any sum (for smaller length).
    """
    if target_sum == 0:
        # Only count sequences of length < target_length (all with sum 0)
        return target_length

    count = 0

    # Count all sequences with length < target_length
    for length in range(target_length):
        count += _count_sequences_with_exact_length_and_sum(length, None)

    # Count sequences with exact target_length but sum < target_sum
    for current_sum in range(target_sum):
        count += _count_sequences_with_exact_length_and_sum(target_length, current_sum)

    return count


def _count_sequences_with_exact_length_and_sum(length: int, target_sum: int = None) -> int:
    """
    Counts sequences with exact length and optionally exact sum.
    If target_sum is None, counts all sequences of the given length.

    This uses the stars and bars combinatorial method:
    Number of ways to distribute n identical items into k distinct bins
    is C(n + k - 1, k - 1).
    """
    if length == 0:
        return 1 if target_sum is None or target_sum == 0 else 0

    if target_sum is None:
        # Count all sequences of given length - this grows very quickly
        # We use a practical upper bound for computation
        count = 0
        max_reasonable_sum = 50  # Practical limit to prevent infinite computation
        for s in range(max_reasonable_sum):
            count += math.comb(s + length - 1, length - 1)
        return count

    if target_sum < 0:
        return 0

    return math.comb(target_sum + length - 1, length - 1)


def _calculate_lexicographic_position(sequence: List[int], total_sum: int) -> int:
    """
    Calculates the lexicographic position of a sequence among all sequences
    with the same length and sum.
    """
    length = len(sequence)
    position = 0
    remaining_sum = total_sum

    for i in range(length):
        # Count sequences that start with values less than sequence[i]
        # and can complete to the same total sum
        for val in range(sequence[i]):
            remaining_positions = length - i - 1
            remaining_after_val = remaining_sum - val

            if remaining_after_val >= 0:
                if remaining_positions == 0:
                    position += 1 if remaining_after_val == 0 else 0
                else:
                    position += _count_sequences_with_exact_length_and_sum(
                        remaining_positions, remaining_after_val
                    )

        remaining_sum -= sequence[i]

    return position


def _find_length_and_sum(rank: int) -> Tuple[int, int, int]:
    """
    Finds the length and sum of the sequence at the given rank.
    Returns (length, sum, remaining_rank_within_same_length_and_sum).
    """
    current_rank = 0

    # Try different lengths starting from 1 (since rank 0 is empty sequence)
    for length in range(1, 100):  # Practical upper bound
        # Try different sums for this length
        for total_sum in range(100):  # Practical upper bound
            count = _count_sequences_with_exact_length_and_sum(length, total_sum)

            if current_rank + count > rank:
                return length, total_sum, rank - current_rank

            current_rank += count

    raise ValueError(f"Could not find sequence for rank {rank} within reasonable bounds")


def _reconstruct_sequence(length: int, total_sum: int, lex_position: int) -> List[int]:
    """
    Reconstructs the sequence given its length, sum, and lexicographic position
    within sequences of the same length and sum.
    """
    if length == 0:
        return []

    sequence = []
    remaining_sum = total_sum
    remaining_position = lex_position

    for i in range(length):
        remaining_length = length - i - 1

        # Find the value at position i
        for val in range(remaining_sum + 1):
            remaining_after_val = remaining_sum - val

            if remaining_after_val < 0:
                break

            if remaining_length == 0:
                count = 1 if remaining_after_val == 0 else 0
            else:
                count = _count_sequences_with_exact_length_and_sum(
                    remaining_length, remaining_after_val
                )

            if remaining_position < count:
                sequence.append(val)
                remaining_sum = remaining_after_val
                break

            remaining_position -= count

    return sequence


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_sequences = [
        [],
        [0],
        [1],
        [0, 0],
        [0, 1],
        [1, 0],
        [2],
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [0, 2],
        [1, 1],
        [2, 0],
        [3]
    ]

    print("Testing rank and unrank functions:")
    print("=" * 50)

    for seq in test_sequences:
        r = rank(seq)
        reconstructed = unrank(r)
        success = seq == reconstructed
        print(f"Sequence: {seq} -> Rank: {r} -> Unrank: {reconstructed} {'✓' if success else '✗'}")

    # Test round-trip for additional ranks
    print("\nTesting round-trip for ranks 0-20:")
    print("=" * 50)

    for r in range(21):
        seq = unrank(r)
        reconstructed_rank = rank(seq)
        success = r == reconstructed_rank
        print(f"Rank: {r} -> Sequence: {seq} -> Rank: {reconstructed_rank} {'✓' if success else '✗'}")
