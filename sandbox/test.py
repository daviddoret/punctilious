from typing import List


def combine_nbit_ints_with_sentinel(values: List[int], n: int = 128) -> int:
    """
    Combine multiple n-bit integers with a sentinel bit to preserve length.

    Format: [actual_data_bits][1 sentinel bit]
    The structure preserves exactly len(values) * n data bits.

    Args:
        values: List of integers, each in range [0, 2^n)
        n: Number of bits per integer (default: 128)

    Returns:
        Combined integer with sentinel bit
    """
    if not values:
        raise ValueError("values list cannot be empty")
    if n <= 0:
        raise ValueError("n must be positive")

    max_value = 2 ** n
    for i, value in enumerate(values):
        if not (0 <= value < max_value):
            raise ValueError(f"values[{i}] must be in range [0, 2^{n}). Got: {value}")

    # Calculate the position where sentinel bit should go
    total_data_bits = len(values) * n

    # Combine values into their designated bit positions
    result = 0
    num_values = len(values)
    for i, value in enumerate(values):
        shift_amount = (num_values - 1 - i) * n
        result |= (value << shift_amount)

    # The sentinel bit goes at position total_data_bits (0-indexed from right)
    # This means we set bit at position total_data_bits
    sentinel_position = total_data_bits
    final_result = result | (1 << sentinel_position)

    return final_result


def split_nbit_ints_with_sentinel(combined: int, n: int = 128) -> List[int]:
    """
    Split a combined integer back to original values using sentinel bit.

    Args:
        combined: Combined integer with sentinel bit
        n: Number of bits per integer (default: 128)

    Returns:
        List of original integers with preserved leading zeros
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if combined <= 0:
        raise ValueError("combined must be positive")

    # Find the sentinel bit (highest bit set)
    total_bits = combined.bit_length()
    sentinel_position = total_bits - 1  # 0-indexed from right

    # Verify sentinel bit is set
    if not (combined & (1 << sentinel_position)):
        raise ValueError("Sentinel bit not found at expected position")

    # Remove sentinel bit
    values_combined = combined & ((1 << sentinel_position) - 1)

    # Calculate number of values
    total_data_bits = sentinel_position
    if total_data_bits % n != 0:
        raise ValueError(f"Invalid bit structure: {total_data_bits} data bits, need multiple of {n}")

    num_values = total_data_bits // n
    if num_values < 1:
        raise ValueError("Invalid structure: no values detected")

    # Split the values
    result = []
    mask = (1 << n) - 1

    for i in range(num_values):
        shift_amount = (num_values - 1 - i) * n
        value = (values_combined >> shift_amount) & mask
        result.append(value)

    return result


def test_problematic_case():
    """Test the specific failing case."""
    values = [0, 1, 2, 3, 0]
    n = 32

    print(f"Testing problematic case: {values} with n={n}")
    print("=" * 60)

    try:
        # Combine
        combined = combine_nbit_ints_with_sentinel(values, n)
        print(f"Combined: {combined}")
        print(f"Combined binary: {bin(combined)}")
        print(f"Bit length: {combined.bit_length()}")

        # Expected structure
        expected_data_bits = len(values) * n
        expected_total_bits = expected_data_bits + 1
        actual_total_bits = combined.bit_length()

        print(f"Expected total bits: {expected_total_bits}")
        print(f"Actual total bits: {actual_total_bits}")
        print(f"Sentinel at position: {expected_data_bits}")

        # Split
        recovered = split_nbit_ints_with_sentinel(combined, n)
        print(f"Recovered: {recovered}")

        success = values == recovered
        print(f"Success: {'✓' if success else '✗'}")

        if not success:
            print(f"ERROR: Expected {values}, got {recovered}")

    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()


def test_comprehensive_fixed():
    """Test various cases with the fixed implementation."""

    test_cases = [
        ([0], 4, "Single zero"),
        ([1], 4, "Single non-zero"),
        ([0, 1], 4, "Leading zero"),
        ([1, 0], 4, "Trailing zero"),
        ([0, 0, 1], 4, "Two leading zeros"),
        ([0, 0, 0], 4, "All zeros"),
        ([15, 14, 13], 4, "All non-zero"),
        ([0, 1, 2, 3, 0], 32, "Problematic case"),
        ([0, 0, 0, 0, 1], 8, "Many leading zeros"),
    ]

    print("\nComprehensive test with fixed implementation")
    print("=" * 60)

    all_passed = True
    for values, n_bits, description in test_cases:
        try:
            combined = combine_nbit_ints_with_sentinel(values, n_bits)
            recovered = split_nbit_ints_with_sentinel(combined, n_bits)

            success = values == recovered
            status = '✓' if success else '✗'
            print(f"{status} {description:20} | {values} -> {recovered}")

            if not success:
                all_passed = False
                print(f"    ERROR: Expected {values}, got {recovered}")

        except Exception as e:
            all_passed = False
            print(f"✗ {description:20} | Exception: {e}")

    print(f"\nOverall result: {'All tests passed! ✓' if all_passed else 'Some tests failed ✗'}")


if __name__ == "__main__":
    test_problematic_case()
    test_comprehensive_fixed()


def test_comprehensive():
    """Comprehensive test with detailed debugging."""

    test_cases = [
        ([0], 4, "Single zero"),
        ([0, 1, 2, 3, 0], 32, "Special"),
        ([1], 4, "Single non-zero"),
        ([0, 1], 4, "Leading zero"),
        ([1, 0], 4, "Trailing zero"),
        ([0, 0, 1], 4, "Two leading zeros"),
        ([0, 0, 0], 4, "All zeros"),
        ([15, 14, 13], 4, "All max values"),
        ([0, 0, 0, 0, 1], 4, "Many leading zeros"),
        ([5, 0, 3, 0, 7], 4, "Mixed with internal zeros"),
    ]

    print("Comprehensive Test with Debugging")
    print("=" * 60)

    for values, n_bits, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Original: {values} (n={n_bits})")

        try:
            # Combine
            combined = combine_nbit_ints_with_sentinel(values, n_bits)

            # Show bit structure
            expected_total_bits = len(values) * n_bits + 1
            actual_total_bits = combined.bit_length()

            print(f"Combined: {combined}")
            print(f"Binary: {bin(combined)}")
            print(f"Expected total bits: {expected_total_bits}, actual: {actual_total_bits}")

            # Split
            recovered = split_nbit_ints_with_sentinel(combined, n_bits)

            success = values == recovered
            print(f"Recovered: {recovered}")
            print(f"Success: {'✓' if success else '✗'}")

            if not success:
                print(f"MISMATCH - Expected: {values}, Got: {recovered}")

        except Exception as e:
            print(f"ERROR: {e}")
            # Debug info
            if 'combined' in locals():
                print(f"Debug - Combined: {combined}, Binary: {bin(combined)}")


def demonstrate_step_by_step():
    """Show the exact bit manipulations step by step."""

    values = [0, 0, 5]  # This was problematic
    n = 4

    print(f"\nStep-by-step: {values} with {n}-bit integers")
    print("=" * 50)

    # Step 1: Show original values
    for i, val in enumerate(values):
        print(f"values[{i}] = {val:2d} = {val:0{n}b}")

    # Step 2: Combine without sentinel
    result = 0
    num_values = len(values)
    for i, value in enumerate(values):
        shift_amount = (num_values - 1 - i) * n
        result |= (value << shift_amount)
        print(f"After adding values[{i}]: {result:0{num_values * n}b} (shift by {shift_amount})")

    print(f"Combined data: {result:0{num_values * n}b} = {result}")

    # Step 3: Add sentinel
    final = (result << 1) | 1
    print(f"After sentinel: {final:0{num_values * n + 1}b} = {final}")
    print(f"Total bits: {final.bit_length()}")

    # Step 4: Split back
    print(f"\nSplitting back:")
    print(f"Remove sentinel: {final >> 1:0{num_values * n}b}")
    print(f"Data bit capacity: {final.bit_length() - 1}")
    print(f"Number of values: {(final.bit_length() - 1) // n}")


if __name__ == "__main__":
    demonstrate_step_by_step()
    test_comprehensive()
