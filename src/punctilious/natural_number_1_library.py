from __future__ import annotations
import typing
import punctilious.util as util
import punctilious.binary_relation_library as brl


# Relation classes


class StrictLessThan(brl.BinaryRelation):
    r"""The natural order of natural numbers starting at 0.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}^{+}, < )`.

    """

    # mathematical properties
    _is_antisymmetric: bool | None = None
    _is_asymmetric: bool | None = True
    _is_connected: bool | None = None
    _is_irreflexive: bool | None = True
    _is_reflexive: bool | None = None
    _is_strongly_connected: bool | None = None
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        y: NaturalNumber1 = NaturalNumber1.from_any(y)
        return int(x) < int(y)


class StrictGreaterThan(brl.BinaryRelation):
    r"""The natural order inverse of natural numbers starting at 0.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}^{+}, > )`.

    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = None
    _is_connected: bool | None = None
    _is_irreflexive: bool | None = True
    _is_reflexive: bool | None = None
    _is_strongly_connected: bool | None = None
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber1 = NaturalNumber1.from_any(x)
        y: NaturalNumber1 = NaturalNumber1.from_any(y)
        return int(x) > int(y)


# Relation orders


strictly_less_than = StrictLessThan()
strictly_greater_than = StrictGreaterThan()


# Main class

class NaturalNumber1(brl.RelationalElement, int):
    r"""A natural number starting at 1.

    Mathematical definition
    -------------------------

    :math:`\mathbb{N}^{+}`.


    """

    # Configuration of class properties (cf. Relatable).
    _canonical_order: brl.BinaryRelation = strictly_less_than
    _strictly_less_than: brl.BinaryRelation = strictly_less_than

    def __new__(cls, x):
        x = int(x)
        if x < 1:
            raise util.PunctiliousException("`x` is less than 1.", x=x)
        return super().__new__(cls, x)

    def __str__(self):
        return str(int(self))

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber1:
        r"""Declares a natural-number-1 from a Python object that can be interpreted as a natural-number-sequence.

        :param o: A Python object that can be interpreted as a natural-number-sequence.
        :return: A natural-number-sequence.
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
