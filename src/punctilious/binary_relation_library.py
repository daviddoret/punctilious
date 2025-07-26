from __future__ import annotations
import abc
import docstring_inheritance
import typing

import punctilious.util as util
import punctilious.special_values_library as spl
import punctilious.ternary_boolean_library as tbl
import punctilious.special_values_library as svl


class BinaryRelation(metaclass=docstring_inheritance.NumpyDocstringInheritanceMeta):
    r"""A (pseudo-)abstract class for binary-relations.

    Bibliography
    -------------

    - http://www.mathmatique.com/naive-set-theory/relations/order-relations
    - https://encyclopediaofmath.org/wiki/Order_(on_a_set)

    """

    @util.readonly_class_property
    def is_a_non_strict_total_order(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is a non-strict-total-order,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - non-strict-total-order
        -------------------------------------------------

        A binary relation :math:`(S, R)` is a non-strict total order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`xRx` (reflexivity)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`xRy \land yRx \implies x = y` (antisymmetry)

        - :math:`xRy \lor yRx` (strongly connected)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Total_order

        """
        return cls.is_reflexive.land(cls.is_transitive.land(cls.is_antisymmetric.land(cls.is_strongly_connected)))

    @util.readonly_class_property
    def is_a_partial_order(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is a partial-order,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - partial-order
        ----------------------------------------------

        A binary relation :math:`(S, R)` is a partial order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`xRx` (reflexivity)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`xRy \land yRx \implies x=y` (antisymmetry)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set

        """
        return cls.is_reflexive.land(cls.is_transitive.land(cls.is_antisymmetric))

    @util.readonly_class_property
    def is_a_strict_total_order(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is a strict-total-order,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - strict-total-order
        -------------------------------------------------

        A binary relation :math:`(S, R)` is a strict total order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`\neg( xRx )` (irreflexivity)

        - :math:`xRy \implies \neg( yRy )` (asymmetry)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`( x \neq y ) \implies ( xRy \lor yRx )` (connected)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Total_order

        """
        return cls.is_irreflexive.land(cls.is_asymmetric.land(cls.is_transitive.land(cls.is_connected)))

    @util.readonly_class_property
    def is_antisymmetric(cls) -> tbl.TernaryBoolean:
        r"""Returns `:attr:`tbl.TernaryBoolean.TRUE` if this binary-relation is antisymmetric,
        `:attr:`tbl.TernaryBoolean.FALSE` if it is not antisymmetric,
        and `:attr:`tbl.TernaryBoolean.NOT_AVAILABLE` if this property is not available.

        Mathematical definition - antisymmetric
        -------------------------------------------------

        A binary relation :math:`(S, R)` is antisymmetric if and only if, :math:`\forall x \in S`:

        - :math:`xRy \land yRx \implies x=y` (antisymmetric)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        -https://en.wikipedia.org/wiki/Antisymmetric_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_asymmetric(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is asymmetric,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - asymmetric
        -------------------------------------------------

        A binary relation :math:`(S, R)` is asymmetric if and only if, :math:`\forall x \in S`:

        - :math:`xRy \implies \neg( yRy )` (asymmetry)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Asymmetric_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_connected(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is connected,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - connected
        -------------------------------------------------

        A binary relation :math:`(S, R)` is connected if and only if, :math:`\forall x, y \in S`:

        - :math:`( x \neq y ) \implies ( xRy \lor yRx )` (connected)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Connected_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_irreflexive(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is irreflexive,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - irreflexive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is irreflexive if and only if, :math:`\forall x \in S`:

        - :math:`\neg( xRx )` (irreflexivity)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Reflexive_relation#Irreflexive_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""Returns `:attr:`tbl.TernaryBoolean.TRUE` if this binary-relation is order isomorphic to :math:`( \mathbb{N}, < )`,
        `:attr:`tbl.TernaryBoolean.FALSE` if it is not,
        and `:attr:`tbl.TernaryBoolean.NOT_AVAILABLE` if this property is not available.

        Mathematical definition - order isomorphism with :math:`( \mathbb{N}, < )`
        ----------------------------------------------------------------------------

        The binary relation :math:`(S, R)` and :math:`( \mathbb{N}, < )` are order isomorphic
        if there is a bijective function :math:`f` from :math:`S \to \mathbb{N}` such that,
        for every :math:`x` and :math:`y` in :math:`S`,
        :math:`xRy` if and only if :math:`f(x) < f(y)`.
        (Reference: Ciesielski 1997, p. 38-39)

        :return: `:attr:`tbl.TernaryBoolean.TRUE`, `:attr:`tbl.TernaryBoolean.FALSE`, or `:attr:`tbl.TernaryBoolean.NOT_AVAILABLE`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Isomorphism
        - https://en.wikipedia.org/wiki/Order_isomorphism
        - Ciesielski, Krzysztof. Set Theory for the Working Mathematician. London Mathematical Society Student Texts 39. 1997.

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_reflexive(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is reflexive,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - reflexive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is reflexive if and only if, :math:`\forall x \in S`:

        - :math:`xRx` (reflexivity)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set
        - https://en.wikipedia.org/wiki/Reflexive_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_strongly_connected(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is strongly-connected,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - strongly-connected
        -------------------------------------------------

        A binary relation :math:`(S, R)` is strongly-connected if and only if, :math:`\forall x, y \in S`:

        - :math:`xRy \lor yRx` (strongly-connected)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Connected_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def is_transitive(cls) -> tbl.TernaryBoolean:
        r"""Returns `True` if this binary-relation is transitive,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - transitive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is transitive if and only if, :math:`\forall x, y, z \in S`:

        - :math:`( xRy \land yRz ) \implies xRz` (transitivity)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set
        - https://en.wikipedia.org/wiki/Transitive_relation

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def least_element(cls) -> object | typing.Literal[spl.SpecialValues.NOT_AVAILABLE]:
        r"""Returns the least element if 1) this is a relation order, 2) it has a least element,
        and 3) it is configured. Returns :py:attr:`spl.SpecialValues.NOT_AVAILABLE` otherwise.

        :return: the least element.
        """
        return spl.SpecialValues.NOT_AVAILABLE

    @classmethod
    def rank(cls, x: object) -> int | typing.Literal[spl.SpecialValues.NOT_AVAILABLE]:
        r"""Returns the rank of `x`.
        Returns :py:attr:`spl.SpecialValues.NOT_AVAILABLE` if rank is undefined or if a ranking algorithm is not configured.

        :param x: an element of the relation set.
        :return: the rank of `x`.
        """
        return spl.SpecialValues.NOT_AVAILABLE

    @classmethod
    def relates(cls, x: object, y: object) -> tbl.TernaryBoolean:
        r"""Returns `True` if :math:`xRy` and `False` if :math:`\neg(xRy)`.
        Returns :py:attr:`spl.SpecialValues.NOT_AVAILABLE` if a relates algorithm is not configured.

        :param x: an element of the relation set.
        :param y: an element of the relation set.
        :return:
        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @classmethod
    def successor(cls, x: object) -> object | typing.Literal[spl.SpecialValues.NOT_AVAILABLE]:
        r"""Returns the successor of `x`.
        Returns :py:attr:`spl.SpecialValues.NOT_AVAILABLE` if successor is not defined,
        or if a successor algorithm is not configured.

        :param x:
        :return:
        """
        return spl.SpecialValues.NOT_AVAILABLE

    @classmethod
    def unrank(cls, n: int) -> object:
        r"""Returns the element of the relation set such that :math:`\mathrm{rank}(x) = n`.
        Returns :py:attr:`spl.SpecialValues.NOT_AVAILABLE` if unrank is undefined or if an unranking algorithm is not configured.

        :param n: a rank.
        :return: an element of the relation set.
        """
        return spl.SpecialValues.NOT_AVAILABLE


def rank(x: object, o: BinaryRelation | None) -> int:
    r"""If the binary-relation `o` is an order-relation that is homomorphic to the natural numbers,
    and if a ranking algorithm is configured,
    returns the rank of object `x`.

    :math:`\mathrm{rank}(x) = n`.

    :param x:
    :return:
    """

    return o.rank(x)


def relates(x: object, y: object, o: BinaryRelation | None) -> bool:
    r"""Returns `True` if :math:`xRy` under `o`, `False` otherwise.

    :param x: An element of the underlying set of `o`.
    :param y: An element of the underlying set of `o`.
    :param o: A binary-relation.
    :return: `True` if :math:`x \prec y`, `False` otherwise.
    """
    return o.relates(x=x, y=y)


def unrank(n: int, o: BinaryRelation | None) -> object:
    r"""If the binary-relation is an order-relation that is homomorphic to the natural numbers,
    and if an unranking algorithm is configured,
    returns the object :math:`x` such that :math:`\mathrm{rank}(x) = n`.

    :param o:
    :return:
    """
    return o.unrank(n)


class RelationalElement(abc.ABC):
    r"""An abstract Python class for elements (objects) supporting relations.

    """

    def __eq__(self, x):
        return self.is_equal_to(x)

    def __gt__(self, x):
        return self.is_strictly_greater_than(x)

    def __lt__(self, x):
        return self.is_strictly_less_than(x)

    # Class properties expected to be configured by child classes
    _is_equal_to: BinaryRelation | None = None
    _is_strictly_greater_than: BinaryRelation | None = None
    _is_strictly_less_than: BinaryRelation | None = None

    @util.readonly_class_property
    def canonical_order(cls) -> BinaryRelation | typing.Literal[svl.SpecialValues.NOT_AVAILABLE]:
        r"""Returns the canonical (default) order for this Python class.
        Returns :py:attr:`svl.SpecialValues.NOT_AVAILABLE` if a canonical order is not defined.

        :return: the canonical order.
        """
        return svl.SpecialValues.NOT_AVAILABLE

    def is_equal_to(self, x: object) -> bool | None:
        """Returns `True` if this element is equal to `x`
        under the canonical equality relation for elements of this Python class,
        `False` otherwise.

        :return: `True` or `False`.
        """
        if self.__class__._is_equal_to is None:
            raise util.PunctiliousException("The is-equal-to relation is not configured on this Python class.",
                                            self_type=str(type(self)),
                                            self_class=self.__class__.__name__,
                                            self=self)
        else:
            return self.__class__._is_equal_to.relates(x=self, y=x)

    def is_strictly_greater_than(self, x: object) -> bool | None:
        """Returns `True` if this element is strictly greater than `x`
        under the canonical is-strictly-greater-than relation for elements of this Python class,
        `False` otherwise.

        :return: `True` or `False`.
        """
        if hasattr(self.__class__, "_is_strictly_greater_than") and hasattr(
                self.__class__._is_strictly_greater_than, "relates"):
            return self.__class__._is_strictly_greater_than.relates(x=self, y=x)
        else:
            return self.__class__._is_strictly_less_than.relates(x=y, y=self)

    def is_strictly_less_than(self, x: object) -> bool | None:
        """Returns `True` if this element is strictly less than `x`
        under the canonical is-strictly-less-than relation for elements of this Python class,
        `False` otherwise.

        :return: `True` or `False`.
        """
        return self.__class__._is_strictly_less_than.relates(x=self, y=x)

    def rank(self) -> int | typing.Literal[svl.SpecialValues.NOT_AVAILABLE]:
        """Returns the rank of this element in its canonical order.
        Returns :p<:attr:`svl.SpecialValues.NOT_AVAILABLE`
        if a canonical order is not configured,
        or if rank is not available on the canonical order.

        :return: The rank of this element.
        """
        if self.__class__.canonical_order is svl.SpecialValues.NOT_AVAILABLE:
            return svl.SpecialValues.NOT_AVAILABLE
        else:
            return self.__class__.canonical_order.rank(self)

    @classmethod
    def from_rank(cls, n: int) -> object:
        if cls.canonical_order is svl.SpecialValues.NOT_AVAILABLE:
            raise util.PunctiliousException("A canonical order is not defined, from_rank cannot be called.")
        else:
            return cls.canonical_order.unrank(n)
