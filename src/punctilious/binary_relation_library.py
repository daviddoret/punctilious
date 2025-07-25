from __future__ import annotations
import abc
import docstring_inheritance

import punctilious.util as util


class BinaryRelation(metaclass=docstring_inheritance.NumpyDocstringInheritanceMeta):
    r"""A (pseudo-)abstract class for binary-relations.

    Bibliography
    -------------

    - http://www.mathmatique.com/naive-set-theory/relations/order-relations
    - https://encyclopediaofmath.org/wiki/Order_(on_a_set)

    """

    # mathematical properties
    _is_asymmetric: bool | None = None
    _is_connected: bool | None = None
    _is_irreflexive: bool | None = None
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = None
    _is_reflexive: bool | None = None
    _is_strongly_connected: bool | None = None
    _is_transitive: bool | None = None

    @property
    def is_a_non_strict_total_order(self) -> bool | None:
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
        if self.is_reflexive is None or self.is_transitive is None or self.is_antisymmetric is None or self.is_strongly_connected is None:
            return None
        else:
            return self.is_reflexive and self.is_transitive and self.is_antisymmetric and self.is_strongly_connected

    @property
    def is_a_partial_order(self) -> bool | None:
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
        if self.is_reflexive is None or self.is_transitive is None or self.is_antisymmetric is None:
            return None
        else:
            return self.is_reflexive and self.is_transitive and self.is_antisymmetric

    @property
    def is_a_strict_total_order(self) -> bool | None:
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
        if self.is_irreflexive is None or self.is_asymmetric is None or self.is_transitive is None or self.is_connected:
            return None
        else:
            return self.is_irreflexive and self.is_asymmetric and self.is_transitive and self.is_connected

    @util.class_property
    def is_antisymmetric(cls) -> util.TernaryBoolean:
        r"""Returns `:attr:`util.TernaryBoolean.TRUE` if this binary-relation is antisymmetric,
        `:attr:`util.TernaryBoolean.FALSE` if not,
        and `:attr:`util.TernaryBoolean.NOT_AVAILABLE` if this property is not available.

        Mathematical definition - antisymmetric
        -------------------------------------------------

        A binary relation :math:`(S, R)` is antisymmetric if and only if, :math:`\forall x \in S`:

        - :math:`xRy \land yRx \implies x=y` (antisymmetric)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        -https://en.wikipedia.org/wiki/Antisymmetric_relation

        """
        return None

    @property
    def is_asymmetric(self) -> bool:
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
        return self.__class__._is_asymmetric

    @property
    def is_connected(self) -> bool:
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
        return self.__class__._is_connected

    @property
    def is_irreflexive(self) -> bool:
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
        return self.__class__._is_irreflexive

    @property
    def is_reflexive(self) -> bool:
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
        return self.__class__._is_reflexive

    @property
    def is_strongly_connected(self) -> bool:
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
        return self.__class__._is_strongly_connected

    @property
    def is_transitive(self) -> bool:
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
        return self.__class__._is_transitive

    @property
    def least_element(self) -> object:
        r"""If this is a relation order, and if it has a unique least element, returns that element.

        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    def rank(self, x: object) -> int:
        r"""If the binary-relation is an order-relation that is homomorphic to the natural numbers,
        and if a ranking algorithm is configured,
        returns the rank of object `x`.

        :math:`\mathrm{rank}(x) = n`.

        :param x:
        :return:
        """

        raise util.PunctiliousException("Abstract method.")

    def relates(self, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param y:
        :param x:
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    def successor(self, x: object) -> object:
        r"""Returns the successor of `x`.

        :param x:
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    def unrank(self, n: int) -> object:
        r"""If the binary-relation is an order-relation that is homomorphic to the natural numbers,
        and if an unranking algorithm is configured,
        returns the object :math:`x` such that :math:`\mathrm{rank}(x) = n`.

        :param n:
        :return:
        """
        raise util.PunctiliousException("Abstract method.")


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

    @property
    def canonical_order(self) -> BinaryRelation:
        return self.__class__._is_strictly_less_than

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

    def rank(self) -> int:
        return self.__class__._is_strictly_less_than.rank(x=self)

    @classmethod
    def from_rank(cls, n: int) -> object:
        return cls._is_strictly_less_than.unrank(n)
