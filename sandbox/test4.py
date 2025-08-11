from typing import List
from math import comb


def rank(sequence: List[int]) -> int:
    """
    Rank a finite sequence of non-negative integers to a unique non-negative integer.

    The ranking uses sum-first, then lexicographic ordering, where the sum is computed
    after incrementing each element by 1 to avoid infinite sequences of the same sum.

    Args:
        sequence: A list of non-negative integers to rank

    Returns:
        A non-negative integer rank, with empty sequence mapped to 0

    Examples:
        rank([]) -> 0
        rank([0]) -> 1  # sum=1, first sequence of sum 1
        rank([1]) -> 2  # sum=2, first sequence of sum 2
        rank([0,0]) -> 3  # sum=2, second sequence of sum 2
    """
    if not sequence:
        return 0

    # Validate input
    if not all(isinstance(x, int) and x >= 0 for x in sequence):
        raise ValueError("All elements must be non-negative integers")

    # Convert to 1-based sum to avoid infinite sequences
    adjusted_sum = sum(sequence) + len(sequence)

    # Count all sequences with smaller adjusted sums
    rank_value = 0
    for s in range(1, adjusted_sum):
        rank_value += _count_sequences_with_adjusted_sum(s)

    # Count sequences with same adjusted sum but lexicographically smaller
    rank_value += _rank_within_sum_class(sequence)

    # Add 1 because we want 1-based ranking within each sum class
    return rank_value + 1


def unrank(rank_value: int) -> List[int]:
    """
    Convert a rank back to its corresponding sequence.

    Args:
        rank_value: A non-negative integer rank to convert back to sequence

    Returns:
        The sequence corresponding to the given rank

    Examples:
        unrank(0) -> []
        unrank(1) -> [0]
        unrank(2) -> [1]
        unrank(3) -> [0, 0]
    """
    if not isinstance(rank_value, int) or rank_value < 0:
        raise ValueError("Rank must be a non-negative integer")

    if rank_value == 0:
        return []

    # Find which sum class this rank belongs to
    current_rank = rank_value
    adjusted_sum = 1

    while True:
        count_for_sum = _count_sequences_with_adjusted_sum(adjusted_sum)
        if current_rank <= count_for_sum:
            break
        current_rank -= count_for_sum
        adjusted_sum += 1

    # Find the sequence within this sum class (convert to 0-based within class)
    return _unrank_within_sum_class(current_rank - 1, adjusted_sum)


def _count_sequences_with_adjusted_sum(adjusted_sum: int) -> int:
    """
    Count the number of sequences with a given adjusted sum.

    For adjusted sum s, we need sequences where sum(seq) + len(seq) = s.
    This is equivalent to the number of compositions of s into positive parts,
    which is 2^(s-1) for s >= 1.
    """
    if adjusted_sum < 1:
        return 0
    return 2 ** (adjusted_sum - 1)


def _rank_within_sum_class(sequence: List[int]) -> int:
    """
    Rank a sequence among all sequences with the same adjusted sum.
    Returns 0-based rank within the sum class.
    """
    if not sequence:
        return 0

    adjusted_sum = sum(sequence) + len(sequence)
    rank_value = 0

    # Try all possible shorter lengths first
    for length in range(1, len(sequence)):
        rank_value += _count_sequences_with_sum_and_length(adjusted_sum, length)

    # Now rank within sequences of the same length
    rank_value += _rank_within_length_class(sequence, adjusted_sum, len(sequence))

    return rank_value


def _unrank_within_sum_class(rank_within_class: int, adjusted_sum: int) -> List[int]:
    """
    Find the sequence with given 0-based rank within sequences of the same adjusted sum.
    """
    current_rank = rank_within_class

    # Try each possible length in order
    for length in range(1, adjusted_sum + 1):
        count_for_length = _count_sequences_with_sum_and_length(adjusted_sum, length)
        if current_rank < count_for_length:
            return _unrank_within_length_class(current_rank, adjusted_sum, length)
        current_rank -= count_for_length

    raise ValueError("Invalid rank for given sum")


def _count_sequences_with_sum_and_length(adjusted_sum: int, length: int) -> int:
    """
    Count sequences with specific adjusted sum and length.
    Using stars and bars: we need to place (adjusted_sum - length) extra units
    among length positions, which is C(adjusted_sum - 1, length - 1).
    """
    if length <= 0 or adjusted_sum < length:
        return 0
    return comb(adjusted_sum - 1, length - 1)


def _rank_within_length_class(sequence: List[int], adjusted_sum: int, length: int) -> int:
    """
    Rank a sequence among sequences of the same adjusted sum and length.
    Uses lexicographic ordering.
    """
    if length == 1:
        return 0  # Only one sequence of length 1 for given sum

    rank_value = 0
    remaining_sum = adjusted_sum
    remaining_length = length

    for i, element in enumerate(sequence):
        # Count sequences that have smaller values at position i
        min_value = 0  # Minimum original value

        for smaller_value in range(min_value, element):
            # Calculate remaining sum after placing smaller_value at position i
            new_remaining_sum = remaining_sum - (smaller_value + 1)
            new_remaining_length = remaining_length - 1

            # Count valid completions
            if new_remaining_length == 0:
                if new_remaining_sum == 0:
                    rank_value += 1
            else:
                # Must have at least 1 (adjusted) for each remaining position
                if new_remaining_sum >= new_remaining_length:
                    rank_value += _count_sequences_with_sum_and_length(
                        new_remaining_sum, new_remaining_length
                    )

        # Update for next iteration
        remaining_sum -= (element + 1)
        remaining_length -= 1

    return rank_value


def _unrank_within_length_class(rank_value: int, adjusted_sum: int, length: int) -> List[int]:
    """
    Find the sequence with given rank among sequences of specific adjusted sum and length.
    """
    if length == 1:
        return [adjusted_sum - 1]  # Convert back to 0-based

    result = []
    current_rank = rank_value
    remaining_sum = adjusted_sum
    remaining_length = length

    for position in range(length):
        if remaining_length == 1:
            # Last element must use all remaining sum
            result.append(remaining_sum - 1)  # Convert back to 0-based
            break

        # Try each possible value for current position (0-based)
        element_value = 0
        while True:
            # Count sequences that start with element_value at this position
            new_remaining_sum = remaining_sum - (element_value + 1)
            new_remaining_length = remaining_length - 1

            if new_remaining_length == 0:
                count = 1 if new_remaining_sum == 0 else 0
            else:
                if new_remaining_sum < new_remaining_length:
                    count = 0
                else:
                    count = _count_sequences_with_sum_and_length(
                        new_remaining_sum, new_remaining_length
                    )

            if current_rank < count:
                # This is the right value for this position
                result.append(element_value)
                remaining_sum = new_remaining_sum
                remaining_length = new_remaining_length
                break

            current_rank -= count
            element_value += 1

            # Safety check to avoid infinite loop
            if element_value > remaining_sum:
                raise ValueError("Invalid rank calculation")

    return result


def _test_bijection():
    """Test that rank and unrank are proper inverses."""
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
        [0, 2],
        [1, 0, 0],
        [1, 1],
        [2, 0],
        [3]
    ]

    print("Testing rank/unrank bijection:")
    for seq in test_sequences:
        r = rank(seq)
        recovered_seq = unrank(r)
        print(f"sequence: {seq} -> rank: {r} -> unrank: {recovered_seq}")
        assert seq == recovered_seq, f"Bijection failed for {seq}"

    print("\nTesting unrank/rank bijection:")
    for r in range(15):
        seq = unrank(r)
        recovered_rank = rank(seq)
        print(f"rank: {r} -> sequence: {seq} -> rank: {recovered_rank}")
        assert r == recovered_rank, f"Bijection failed for rank {r}"

    print("\nAll tests passed!")


if __name__ == "__main__":
    _test_bijection()
