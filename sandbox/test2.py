from typing import List, Tuple, Optional
import math


def rank(sequence: List[int]) -> int:
    """
    Ranks a finite 0-based natural number sequence to a 0-based natural number.
    The ranking follows these rules:
    1. The empty sequence maps to 0
    2. Sequences are ordered first by sum (ascending), then by lexicographic order
    3. All sequences are assumed to be in non-decreasing order (sorted)

    Args:
        sequence: A list of non-negative integers in non-decreasing order

    Returns:
        The rank of the sequence as a non-negative integer

    Raises:
        ValueError: If the sequence contains negative numbers or is not sorted
    """
    # Validate input
    if not all(isinstance(x, int) and x >= 0 for x in sequence):
        raise ValueError("All elements must be non-negative integers")
    if sequence != sorted(sequence):
        raise ValueError("Sequence must be in non-decreasing order")

    # Empty sequence has rank 0
    if not sequence:
        return 0

    # Calculate the sum of the sequence
    current_sum = sum(sequence)

    # Initialize rank with 1 (since empty sequence is 0)
    rank_value = 1

    # Iterate through all possible sums less than current_sum
    for s in range(1, current_sum):
        # For each sum, count all sequences with that sum that are lex < current sequence
        rank_value += count_sequences_with_sum(s)

    # Now count sequences with the same sum that are lexicographically smaller
    rank_value += count_lex_smaller_sequences(sequence)

    return rank_value


def unrank(rank_value: int) -> List[int]:
    """
    Unranks a 0-based natural number to a finite 0-based natural number sequence.
    This is the inverse operation of the rank function.

    Args:
        rank_value: A non-negative integer representing the rank

    Returns:
        The sequence corresponding to the given rank

    Raises:
        ValueError: If rank_value is negative
    """
    if rank_value < 0:
        raise ValueError("Rank value must be non-negative")

    # Handle the empty sequence case
    if rank_value == 0:
        return []

    # Find the sum of the target sequence
    current_sum = 1
    sequences_before = 1  # empty sequence

    # Find the smallest sum where sequences_before + count_sequences_with_sum(s) > rank_value
    while True:
        sequences_in_sum = count_sequences_with_sum(current_sum)
        if sequences_before + sequences_in_sum > rank_value:
            break
        sequences_before += sequences_in_sum
        current_sum += 1

    # Now find the specific sequence within this sum
    remaining_rank = rank_value - sequences_before

    # Generate sequences in order and find the one at remaining_rank
    sequence = []
    current_sequence = [0] * current_sum  # Start with the smallest sequence for this sum

    while True:
        # Check if this is our target sequence
        if remaining_rank == 0:
            return current_sequence.copy()

        # Calculate how many sequences are lexicographically smaller than current_sequence
        # with the same sum, and subtract from remaining_rank
        count = count_lex_smaller_sequences(current_sequence)
        if remaining_rank <= count:
            # Need to find the exact sequence
            return find_sequence_at_rank(current_sum, current_sequence, remaining_rank)
        else:
            remaining_rank -= count + 1  # +1 for current_sequence itself
            # Move to next sequence
            current_sequence = next_sequence(current_sequence)


def count_sequences_with_sum(s: int) -> int:
    """
    Counts the number of non-decreasing sequences of non-negative integers that sum to s.

    This is equivalent to the number of integer partitions of s where order matters
    (also known as compositions with parts in non-decreasing order).

    Args:
        s: The target sum

    Returns:
        The count of sequences
    """
    # This is equivalent to the number of partitions of s into any number of parts
    # which is the partition function p(s)
    # We'll use dynamic programming to compute this
    if s == 0:
        return 1

    # Initialize a table to store the number of partitions
    dp = [0] * (s + 1)
    dp[0] = 1  # Base case: one way to make sum 0

    for i in range(1, s + 1):
        for j in range(i, s + 1):
            dp[j] += dp[j - i]

    return dp[s]


def count_lex_smaller_sequences(sequence: List[int]) -> int:
    """
    Counts how many sequences with the same sum are lexicographically smaller than the given sequence.

    Args:
        sequence: The reference sequence

    Returns:
        The count of lexicographically smaller sequences with the same sum
    """
    if not sequence:
        return 0

    current_sum = sum(sequence)
    count = 0

    # Generate all sequences with the same sum in lex order and count those before our sequence
    current = [0] * current_sum  # Start with the smallest sequence for this sum

    while True:
        if current == sequence:
            break
        count += 1
        current = next_sequence(current)

    return count


def next_sequence(sequence: List[int]) -> List[int]:
    """
    Generates the next sequence in lexicographic order with the same sum.

    Args:
        sequence: The current sequence

    Returns:
        The next sequence in lex order with the same sum
    """
    if not sequence:
        return []

    # Find the rightmost element that can be incremented
    n = len(sequence)
    current_sum = sum(sequence)

    # Start from the end and find the first element that can be incremented
    for i in range(n - 1, -1, -1):
        if sequence[i] + 1 <= current_sum - sum(sequence[:i]):
            # Increment this element and adjust the rest
            new_sequence = sequence.copy()
            new_sequence[i] += 1
            remaining_sum = current_sum - sum(new_sequence[:i + 1])

            # Distribute the remaining sum starting from the next position
            if i + 1 < n:
                # Reset all following elements to the minimum possible
                for j in range(i + 1, n):
                    new_sequence[j] = 0

                # Distribute the remaining sum
                remaining = remaining_sum
                pos = i + 1
                while remaining > 0 and pos < n:
                    max_possible = remaining - (n - pos - 1)
                    if max_possible <= new_sequence[pos - 1]:
                        max_possible = new_sequence[pos - 1]
                    new_sequence[pos] = max_possible
                    remaining -= max_possible
                    pos += 1

            return new_sequence

    # If we get here, we've reached the last sequence, so return the first one
    return [0] * current_sum


def find_sequence_at_rank(s: int, start_sequence: List[int], rank: int) -> List[int]:
    """
    Finds the sequence at a specific rank within all sequences that sum to s.

    Args:
        s: The target sum
        start_sequence: The sequence to start searching from
        rank: The rank within sequences of sum s

    Returns:
        The sequence at the specified rank
    """
    current = start_sequence.copy()
    for _ in range(rank):
        current = next_sequence(current)
    return current


# Example usage
if __name__ == "__main__":
    # Test cases
    test_sequences = [
        [],
        [0],
        [1],
        [2],
        [0, 0],
        [1, 1],
        [0, 1],
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 1],
        [0, 0, 1],
        [2, 2],
        [1, 2],
        [0, 2],
        [0, 1, 1],
        [0, 0, 2],
        [1, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 0, 1]
    ]

    print("Testing rank and unrank functions:")
    for seq in test_sequences:
        try:
            r = rank(seq)
            unranked = unrank(r)
            assert unranked == seq, f"Failed for {seq}: got {unranked}"
            print(f"Sequence: {seq} -> Rank: {r}")
        except ValueError as e:
            print(f"Error processing {seq}: {str(e)}")

    # Test some specific cases
    print("\nSpecific test cases:")
    print(f"Rank of []: {rank([])}")
    print(f"Unrank of 0: {unrank(0)}")
    print(f"Rank of [0]: {rank([0])}")
    print(f"Unrank of 1: {unrank(1)}")
    print(f"Rank of [1,1]: {rank([1, 1])}")
    print(f"Unrank of 3: {unrank(3)}")
