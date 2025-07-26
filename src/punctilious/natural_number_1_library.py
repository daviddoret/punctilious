r"""A library for (1-based) natural numbers.

"""
from __future__ import annotations
import typing
import punctilious.util as util
import punctilious.binary_relation_library as brl


# Relation classes


class IsEqualTo(brl.BinaryRelation):
    r"""The (1-based) natural numbers equipped with the standard equality order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_1, = )`.

    """

    # mathematical properties
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = False
    _is_irreflexive: bool | None = False
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = False
    _is_reflexive: bool | None = True
    _is_strongly_connected: bool | None = False
    _is_symmetric: bool | None = True
    _is_transitive: bool | None = True

    def is_antisymmetric(cls) -> util.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return util.TernaryBoolean.TRUE

    def relates(self, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object.
        :param y: A Python object.
        :return: `True` or `False`.
        """
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        y: NaturalNumber1 = NaturalNumber1.from_any(y)
        return int(x) == int(y)


class IsStrictlyGreaterThan(brl.BinaryRelation):
    r"""The (1-based) natural numbers equipped with the standard strictly greater-than order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_1, > )`.

    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = True
    _is_connected: bool | None = True
    _is_irreflexive: bool | None = True
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = False
    _is_reflexive: bool | None = False
    _is_strongly_connected: bool | None = False
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object.
        :param y: A Python object.
        :return: `True` or `False`.
        """
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        y: NaturalNumber1 = NaturalNumber1.from_any(y)
        return int(x) > int(y)


class IsStrictlyLessThan(brl.BinaryRelation):
    r"""The (1-based) natural numbers equipped with the standard strictly less-than order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_1, < )`.

    """

    # mathematical properties
    _is_antisymmetric: bool | None = None
    _is_asymmetric: bool | None = True
    _is_connected: bool | None = None
    _is_irreflexive: bool | None = True
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = None
    _is_reflexive: bool | None = None
    _is_strongly_connected: bool | None = None
    _is_transitive: bool | None = True

    def rank(self, x: object) -> int:
        r"""Returns the rank of `x` in :math:`( \mathbb{N}_1, < )`.

        :param x: A Python object interpretable as a (1-based) natural number.
        :return: An integer.
        """
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        return int(x)

    def relates(self, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object interpretable as a (1-based) natural number.
        :param y: A Python object interpretable as a (1-based) natural number.
        :return: `True` or `False`.
        """
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        y: NaturalNumber1 = NaturalNumber1.from_any(y)
        return int(x) < int(y)

    def successor(self, x: object) -> object:
        r"""Returns the successor of `x` in :math:`( \mathbb{N}_1, < )`.

        :param x: A Python object interpretable as a (1-based) natural number.
        :return: The successor of `x`.
        """
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        return NaturalNumber1(x + 1)

    def unrank(self, n: int) -> object:
        r"""Returns the (1-based) natural number of `x` such that its rank in :math:`( \mathbb{N}_1, < ) = n`.

        :param n: A positive integer.
        :return: A (1-based) natural number.
        """
        n = int(n)
        if n < 1:
            raise util.PunctiliousException("`n` must be a positive integer.", n=n)
        x: NaturalNumber1 = NaturalNumber1(n)
        return x


# Relations

is_equal_to: IsEqualTo = IsEqualTo  # The canonical equality relation for natural-number-1 elements.
is_strictly_greater_than: IsStrictlyGreaterThan = IsStrictlyGreaterThan  # The canonical is-strictly-greater-than relation for natural-number-1 elements.
is_strictly_less_than: IsStrictlyLessThan = IsStrictlyLessThan  # The canonical is-strictly-less-than relation for natural-number-1 elements.


# Main class

class NaturalNumber1(brl.RelationalElement, int):
    r"""A (1-based) natural number.

    Mathematical definition
    -------------------------

    :math:`\mathbb{N}_1`.


    """

    _HASH_SEED: int = 11751098203082057729  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    # Configuration of class properties (cf. Relatable).
    _is_equal_to: brl.BinaryRelation = is_equal_to
    _is_strictly_greater_than: brl.BinaryRelation = is_strictly_greater_than
    _is_strictly_less_than: brl.BinaryRelation = is_strictly_less_than

    def __hash__(self):
        return hash((NaturalNumber1, NaturalNumber1._HASH_SEED, int(self),))

    def __new__(cls, x):
        x = int(x)
        if x < 1:
            raise util.PunctiliousException("`x` is less than 1.", x=x)
        return super().__new__(cls, x)

    def __str__(self):
        return str(int(self))

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber1:
        r"""Declares a (1-based) natural number from a Python object, using implicit conversion if necessary.

        :param o: A Python object interpretable as a (1-based) natural number).
        :return: A (1-based) natural number.
        """
        if isinstance(o, NaturalNumber1):
            return o
        if isinstance(o, int):
            return NaturalNumber1(o)
        raise util.PunctiliousException('Failure to interpret `o` as a natural-number-1.', o_type=type(o), o=o)


# Flexible types to facilitate data validation

FlexibleNaturalNumber1 = typing.Union[
    NaturalNumber1, int]

# Aliases

NN1 = NaturalNumber1  # An alias for NaturalNumber1
