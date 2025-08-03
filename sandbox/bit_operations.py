def int_to_bits(n: int, bit_positional_significance: str = "msb", fixed_length: None | int = None):
    """Converts integer `n`to tuple of bits using bit operations.

    :param n: An integer.
    :param bit_positional_significance: "msb" (most significant bit first) or "lsb" (least significant bit first).
    :param fixed_length: Fixed length for the bit tuple (pads with zeros if needed).
    :return: A tuple of bits.
    """
    if n < 0:
        raise ValueError("Negative numbers not supported")

    if bit_positional_significance not in ["msb", "lsb"]:
        raise ValueError("bit_positional_significance must be 'msb' or 'lsb'")

    if n == 0:
        bits = [0]
    else:
        bits = []
        temp_n = n
        while temp_n > 0:
            bits.append(temp_n & 1)  # Get least significant bit
            temp_n >>= 1  # Right shift by 1
        # bits now contains LSB first

    # Handle fixed_length
    if fixed_length:
        if len(bits) > fixed_length:
            raise ValueError(f"Number requires {len(bits)} bits, but fixed_length is {fixed_length}")
        bits.extend([0] * (fixed_length - len(bits)))  # Pad with zeros

    # Adjust order based on bit_positional_significance
    if bit_positional_significance == "msb":
        bits.reverse()  # Most significant bit first
    # If "lsb", bits are already in LSB first order

    return tuple(bits)


def bits_to_int(bits: tuple[int, ...], bit_positional_significance: str = "msb"):
    """Convert tuple of bits back to integer using bit operations

    :param bits: A tuple of bits.
    :param bit_positional_significance: "msb" (most significant bit first) or "lsb" (least significant bit first).
    :return: An integer.
    """

    result = 0

    if bit_positional_significance == "msb":
        # Process from left to right (MSB first)
        for bit in bits:
            result = (result << 1) | bit
    else:  # "lsb"
        # Process from right to left (LSB first)
        for i, bit in enumerate(bits):
            result |= bit << i

    return result


n = 255
print(int_to_bits(n))
print(int_to_bits(n, bit_positional_significance="lsb"))
print(int_to_bits(n, bit_positional_significance="msb"))
print(int_to_bits(n, fixed_length=32))
print(int_to_bits(n, fixed_length=32, bit_positional_significance="lsb"))
print(int_to_bits(n, fixed_length=32, bit_positional_significance="msb"))
