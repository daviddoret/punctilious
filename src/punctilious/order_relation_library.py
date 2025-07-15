from __future__ import annotations
import abc
import util


class OrderRelation(abc.ABC):
    r"""An abstract class of order-relation.

    Bibliography
    -------------
    - http://www.mathmatique.com/naive-set-theory/relations/order-relations
    - https://encyclopediaofmath.org/wiki/Order_(on_a_set)

    """

    def __init__(self, *, python_type_constraint: type | None,
                 is_antisymmetric: bool | None = None,
                 is_asymmetric: bool | None = None,
                 is_connected: bool | None = None,
                 is_irreflexive: bool | None = None,
                 is_reflexive: bool | None = None,
                 is_strongly_connected: bool | None = None,
                 is_transitive: bool | None = None, **kwargs):

        self._python_type_constraint = python_type_constraint

        self._is_antisymmetric: bool | None = is_antisymmetric
        self._is_asymmetric: bool | None = is_asymmetric
        self._is_connected: bool | None = is_connected
        self._is_irreflexive: bool | None = is_irreflexive
        self._is_reflexive: bool | None = is_reflexive
        self._is_strongly_connected: bool | None = is_strongly_connected
        self._is_transitive: bool | None = is_transitive

    def get_python_type_constraint(self) -> type:
        r"""Returns the Python type on which this order-relation can be applied. `None` if there is no Python type constraint.

        :return: A Python type.
        """
        return self._python_type_constraint

    @abc.abstractmethod
    def is_less_than(self, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`x \prec y`, `False` otherwise.

        :param y:
        :param x:
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    def is_equal_to(self, x: object, y: object) -> bool:
        r"""

        :param x: An element of the underlying set of this order-relation.
        :param y: An element of the underlying set of this order-relation.
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    @property
    def is_a_non_strict_total_order(self) -> bool:
        r"""Returns `True` if this order-relation is a non-strict-total-order,
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
    def is_a_partial_order(self) -> bool:
        r"""Returns `True` if this order-relation is a partial-order,
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
        r"""Returns `True` if this order-relation is a strict-total-order,
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

    @property
    def is_antisymmetric(self) -> bool:
        r"""Returns `True` if this order-relation is antisymmetric,
        `False` if not,
        and `None` if this property is not configured.

        Mathematical definition - antisymmetric
        -------------------------------------------------

        A binary relation :math:`(S, R)` is antisymmetric if and only if, :math:`\forall x \in S`:

        - :math:`xRy \land yRx \implies x=y` (antisymmetric)

        :return: `True`, `False`, or `None`.

        Bibliography
        ---------------

        -https://en.wikipedia.org/wiki/Antisymmetric_relation

        """
        return self._is_antisymmetric

    @property
    def is_asymmetric(self) -> bool:
        r"""Returns `True` if this order-relation is asymmetric,
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
        return self._is_asymmetric

    @property
    def is_connected(self) -> bool:
        r"""Returns `True` if this order-relation is connected,
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
        return self._is_connected

    @property
    def is_irreflexive(self) -> bool:
        r"""Returns `True` if this order-relation is irreflexive,
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
        return self._is_irreflexive

    @property
    def is_reflexive(self) -> bool:
        r"""Returns `True` if this order-relation is reflexive,
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
        return self._is_reflexive

    @property
    def is_strongly_connected(self) -> bool:
        r"""Returns `True` if this order-relation is strongly-connected,
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
        return self._is_strongly_connected

    @property
    def is_transitive(self) -> bool:
        r"""Returns `True` if this order-relation is transitive,
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
        return self._is_transitive


def is_less_than(x: object, y: object, o: OrderRelation | None) -> bool:
    r"""Returns `True` if :math:`x \prec y` under `o`, `False` otherwise.

    :param x: An element of the underlying set of order-relation `o`.
    :param y: An element of the underlying set of order-relation `o`.
    :param o: An order-relation.
    :return: `True` if :math:`x \prec y`, `False` otherwise.
    """
    return o.is_less_than(x=x, y=y)


class Orderable(abc.ABC):
    r"""An abstract Python class that supports relation-orders.

    """
    _default_order_relation: OrderRelation | None = None

    def __lt__(self, x):
        return self.is_less_than(x)

    @classmethod
    def get_default_order_relation(cls) -> OrderRelation | None:
        return cls._default_order_relation

    @classmethod
    def set_default_order_relation(cls, o: OrderRelation | None):
        if o is not None and not isinstance(o, OrderRelation):
            raise util.PunctiliousException("Invalid parameter `o`.", o=o)
        o_cls = o.__class__  # type(o)
        if o is not None and o_cls.get_python_type_constraint() != cls:
            raise util.PunctiliousException(
                "Python-type `t1`'s default order-relation cannot be set to `o`, because `o` requires python-type `t2`.",
                t1=cls,
                o=o,
                t2=o_cls.get_python_type_constraint())
        cls._default_order_relation: OrderRelation | None = o

    def is_less_than(self, x):
        cls = self.__class__
        if cls.get_default_order_relation() is None:
            util.PunctiliousException("No default order-relation is defined.")
        return is_less_than(x=self, y=x, o=cls.get_default_order_relation())
