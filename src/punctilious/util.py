from __future__ import annotations

import typing
import uuid
import math


class ReadOnlyClassPropertyDescriptor:
    """Descriptor for creating class-level properties."""

    def __init__(self, f):
        self.func = f
        self.__doc__ = f.__doc__

    def __get__(self, f, cls):
        return self.func(cls)

    def __set__(self, f, x):
        raise PunctiliousException("This class property is read-only.", f=f, x=x)


def readonly_class_property(p):
    """Decorator to create read-only class properties."""
    return ReadOnlyClassPropertyDescriptor(p)


def decrement_last_element(s):
    """Receives a sequence of natural numbers (s0, s1, ..., si) and returns (s0, s1, ..., si - 1).

    :param s:
    :return:
    """
    return s[0:-1] + (s[-1] - 1,)


def deduplicate_integer_sequence(t: tuple[int, ...]) -> tuple[int, ...]:
    """Given a sequence S of integers, return a sequence T such that:
     - the order and values of elements are preserved with the exception that
     - only the first occurrence of every distinct value is copied to T.

    Samples:
    (1,5,0,3,5,1,1,2) --> (1,5,0,3,2)

    :param t:
    :return:
    """
    observed = set()
    result = []
    for item in t:
        if item not in observed:
            observed.add(item)
            result.append(item)
    return tuple(result)


def data_validate_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
    """Given some `elements`, returns a tuple of unique elements.

    :param elements:
    :param raise_error_on_duplicate:
    :return:
    """
    unique_elements = []
    for element in elements:
        if element not in unique_elements:
            unique_elements.append(element)
        elif raise_error_on_duplicate:
            raise ValueError('Duplicate elements.')
    return tuple(unique_elements)


def increment_last_element(s):
    """Receives a sequence of natural numbers (s0, s1, ..., si) and returns (s0, s1, ..., si + 1).

    :param s:
    :return:
    """
    return s[0:-1] + (s[-1] + 1,)


class PunctiliousException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message: str = message
        self.variables: dict = kwargs
        super().__init__(message)

    def __str__(self):
        variables: str = ' | '.join(f'`{k}` {"is" if v is None else "="} `{v!r}`' for k, v in self.variables.items())
        return f'{self.message} | {variables}'


def data_validate_uid(o: uuid.UUID) -> uuid.UUID:
    """Ensures `o` is of type `uuid.UUID`, using implicit conversion if necessary.

    :param o:
    :return:
    """
    if isinstance(o, uuid.UUID):
        return o
    elif isinstance(o, str):
        try:
            return uuid.UUID(o)
        except ValueError:
            raise PunctiliousException('`uuid.UUID` ensurance failure. `o` is not a string in valid UUID format.',
                                       o=o)
    else:
        raise PunctiliousException('`uuid.UUID` ensurance failure. `o` is not of a supported type.', o=o)


def int_to_bits(n: int, bit_positional_significance: str = "msb", fixed_length: None | int = None):
    """Converts integer `n`to tuple of bits using bit operations.

    :param n: An integer.
    :param bit_positional_significance: "msb" (most significant bit first) or "lsb" (least significant bit first).
    :param fixed_length: Fixed length for the bit tuple (pads with zeros if needed).
    :return: A tuple of bits.
    """
    if n < 0:
        raise PunctiliousException("Negative numbers not supported")

    if bit_positional_significance not in ["msb", "lsb"]:
        raise PunctiliousException("bit_positional_significance must be 'msb' or 'lsb'")

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
            raise PunctiliousException(f"Number requires {len(bits)} bits, but fixed_length is {fixed_length}")
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


def combine_fixed_length_ints_with_sentinel(ints: tuple[int, ...], fixed_length: int = 32) -> int:
    """Combine a tuple of n-bit integers into a single integer,
    with a sentinel bit to preserve leading zeroes.

    Note
    -----

    Least significant bit (lsb) is used.

    :param ints: A tuple of integers.
    :param fixed_length: The number of bits per integer (default: 32).
    :return: An integer.
    """
    if not ints:
        raise PunctiliousException("`ints` cannot be empty")
    if fixed_length <= 0:
        raise PunctiliousException("`fixed_length` must be positive")

    bits: tuple[int, ...] = ()
    for n in ints:
        bits = bits + int_to_bits(n=n, bit_positional_significance="lsb", fixed_length=fixed_length)

    # append the sentinel value
    bits = bits + (1,)

    # convert bits to int
    n: int = bits_to_int(bits=bits, bit_positional_significance="lsb")

    return n


def split_fixed_length_ints_with_sentinel(n: int, fixed_length: int = 32) -> tuple[int, ...]:
    """Split a combined integer back to original values using sentinel bit.

    Note
    -----

    Least significant bit (lsb) is used.


    :param n: A combined integer with sentinel bit.
    :param fixed_length: Number of bits per integer (default: 32).
    :return: A tuple of integers.
    """
    if n <= 0:
        raise PunctiliousException("n must be positive")
    if n <= 0:
        raise PunctiliousException("combined must be positive")
    if fixed_length <= 0:
        raise PunctiliousException("`fixed_length` must be positive")

    bits: tuple[int, ...] = int_to_bits(n=n, bit_positional_significance="lsb", fixed_length=None)

    # Extract and check the sentinel value
    sentinel_bits: tuple[int, ...] = bits[-1:]
    sentinel_value: int = bits_to_int(bits=sentinel_bits, bit_positional_significance="lsb")
    if sentinel_value != 1:
        raise PunctiliousException("The sentinel value is not equal to 1.", sentinel_bits=sentinel_bits,
                                   sentinel_value=sentinel_value, n=n, bits=bits, fixed_length=fixed_length)

    # Remove the sentinel bit to retrieve the meaningful value
    bits: tuple[int, ...] = bits[:-1]

    ints: tuple[int, ...] = ()
    # Convert the fixed-length bits to integers
    for i in range(len(bits) // fixed_length):
        start_index: int = fixed_length * i
        end_index: int = fixed_length * (i + 1)
        int_bits: tuple[int, ...] = bits[start_index: end_index]
        m: int = bits_to_int(bits=int_bits, bit_positional_significance="lsb")
        ints = ints + (m,)

    return ints


def binomial_coefficient(k: int, n: int):
    r"""Returns the binomial coefficient :math:`C(n, k)`, aka ":math:`n` choose :math:`k`".

    Note
    -----

    Python's math.comb function should be safe for very large integers,
    i.e. it should not yield float errors.

    TODO: CLEAN THIS UP. Redundant with combination()


    :param k: A (0-based) natural number.
    :param n: A (0-based) natural number.
    :return: The binomial coefficient.
    """
    k: int = int(k)
    n: int = int(n)

    if k < 0 or n < 0 or k > n:
        return 0
    return math.comb(n, k)


def combination(n: int, r: int):
    r"""Calculate nCr (combinations) using integer arithmetic.

    TODO: CLEAN THIS UP. Redundant with binomial_coefficient()
    """
    n: int = int(n)
    r: int = int(r)
    if r > n or r < 0:
        return 0
    if r == 0 or r == n:
        return 1

    # Use the property C(n,r) = C(n, n-r) and choose smaller r
    r = min(r, n - r)

    result: int = 1
    i: int
    for i in range(r):
        result = result * (n - i) // (i + 1)

    return result
