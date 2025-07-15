from __future__ import annotations
import typing
import order_relation_library as orl
import util


class NaturalNumber0(orl.Orderable, int):
    """A natural number starting at 0.

    Mathematical definition
    -------------------------

    :math:`\mathbb{N}^{+}`.


    """

    def __new__(cls, x):
        x = int(x)
        if x < 0:
            raise util.PunctiliousException("`x` is less than 0.", x=x)
        return super().__new__(cls, x)

    def __str__(self):
        return str(int(self))

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber0:
        r"""Declares a natural-number-0 from a Python object that can be interpreted as a natural-number-sequence.

        :param o: A Python object that can be interpreted as a natural-number-sequence.
        :return: A natural-number-sequence.
        """
        if isinstance(o, NaturalNumber0):
            return o
        if isinstance(o, int):
            return NaturalNumber0(o)
        raise util.PunctiliousException('Failure to interpret `o` as a natural-number-0.', o_type=type(o), o=o)


class O1(orl.OrderRelation, t=NaturalNumber0):
    """The natural order of natural numbers starting at 0.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}^{+}, < )`.

    """

    @classmethod
    def python_type(cls) -> type:
        return NaturalNumber0

    def is_less_than(self, x: object, y: object) -> bool:
        x: NaturalNumber0 = NaturalNumber0.from_any(x)
        y: NaturalNumber0 = NaturalNumber0.from_any(y)
        return int(x) < int(y)

    def is_equal_to(self, x: object, y: object) -> bool:
        raise util.PunctiliousException("Not implemented.")


class O2(orl.OrderRelation, t=NaturalNumber0):
    """The natural order inverse of natural numbers starting at 0.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}^{+}, > )`.

    """

    @classmethod
    def python_type(cls) -> type:
        return NaturalNumber0

    def is_less_than(self, x: object, y: object) -> bool:
        x: NaturalNumber0 = NaturalNumber0.from_any(x)
        y: NaturalNumber0 = NaturalNumber0.from_any(y)
        return int(x) > int(y)

    def is_equal_to(self, x: object, y: object) -> bool:
        raise util.PunctiliousException("Not implemented.")


# Flexible types to facilitate data validation

FlexibleNaturalNumber0 = typing.Union[
    NaturalNumber0, int]

# Aliases

NN0 = NaturalNumber0  # An alias for NaturalNumber0

# Relation orders

o1 = O1()
o2 = O2()
