from __future__ import annotations
import abc
import util


class OrderRelation(abc.ABC):
    """An abstract class of order-relation.

    Bibliography
    -------------
    - http://www.mathmatique.com/naive-set-theory/relations/order-relations
    - https://encyclopediaofmath.org/wiki/Order_(on_a_set)

    """
    _python_type_constraint: type | None = None

    def __init_subclass__(cls, *, t, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._python_type_constraint = t  # Store at class level

    @classmethod
    def get_python_type_constraint(cls) -> type:
        """Returns the Python type on which this order-relation can be applied. `None` if there is no Python type constraint.

        :return: A Python type.
        """
        return cls._python_type_constraint

    @abc.abstractmethod
    def is_less_than(self, x: object, y: object) -> bool:
        """Returns `True` if :math:`x \prec y`, `False` otherwise.

        :param y:
        :param x:
        :param o:
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    def is_equal_to(self, x: object, y: object) -> bool:
        """

        :param x: An element of the underlying set of this order-relation.
        :param y: An element of the underlying set of this order-relation.
        :return:
        """
        raise util.PunctiliousException("Abstract method.")

    @property
    def is_a_non_strict_total_order(self) -> bool:
        r"""Returns `True` if this order-relation is a non-strict-total-order, `False` otherwise.

        Mathematical definition - non-strict-total-order
        -------------------------------------------------

        A binary relation :math:`(S, R)` is a non-strict total order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`xRx` (reflexivity)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`xRy \land yRx \implies x = y` (anti-symmetry)

        - :math:`xRy \lor yRx` (strongly connected)

        :return: `True` if this order-relation is a non-strict-total-order, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Total_order

        """
        raise util.PunctiliousException("Abstract method.")

    @property
    def is_a_partial_order(self) -> bool:
        r"""Returns `True` if this order-relation is a partial-order, `False` otherwise.

        Mathematical definition - partial-order
        ----------------------------------------------

        A binary relation :math:`(S, R)` is a partial order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`xRx` (reflexivity)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`xRy \land yRx \implies x=y` (anti-symmetry)

        :return: `True` if this order-relation is a partial-order, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set

        """
        return self.is_reflexive and self.is_transitive and self.is_anti_symmetric

    @property
    def is_a_strict_total_order(self) -> bool:
        r"""Returns `True` if this order-relation is a strict-total-order, `False` otherwise.

        Mathematical definition - strict-total-order
        -------------------------------------------------

        A binary relation :math:`(S, R)` is a strict total order if and only if, :math:`\forall x, y, z \in S`:

        - :math:`\neg( xRx )` (irreflexivity)

        - :math:`xRy \implies \neg( yRy )` (asymmetry)

        - :math:`xRy \land yRz \implies xRz` (transitivity)

        - :math:`( x \neq y ) \implies ( xRy \lor yRx )` (connected)

        :return: `True` if this order-relation is a strict-total-order, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Total_order

        """
        return self.is_irreflexive and self.is_asymmetric and self.is_transitive and self.is_connected

    @abc.abstractmethod
    @property
    def is_asymmetric(self) -> bool:
        r"""Returns `True` if this order-relation is asymmetric, `False` otherwise.

        Mathematical definition - asymmetric
        -------------------------------------------------

        A binary relation :math:`(S, R)` is asymmetric if and only if, :math:`\forall x \in S`:

        - :math:`xRy \implies \neg( yRy )` (asymmetry)

        :return: `True` if this order-relation is asymmetric, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Asymmetric_relation

        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    @property
    def is_connected(self) -> bool:
        r"""Returns `True` if this order-relation is connected, `False` otherwise.

        Mathematical definition - connected
        -------------------------------------------------

        A binary relation :math:`(S, R)` is connected if and only if, :math:`\forall x, y \in S`:

        - :math:`( x \neq y ) \implies ( xRy \lor yRx )` (connected)

        :return: `True` if this order-relation is connected, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Connected_relation

        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    @property
    def is_irreflexive(self) -> bool:
        r"""Returns `True` if this order-relation is irreflexive, `False` otherwise.

        Mathematical definition - irreflexive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is irreflexive if and only if, :math:`\forall x \in S`:

        - :math:`\neg( xRx )` (irreflexivity)

        :return: `True` if this order-relation is irreflexive, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Reflexive_relation#Irreflexive_relation

        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    @property
    def is_reflexive(self) -> bool:
        r"""Returns `True` if this order-relation is reflexive, `False` otherwise.

        Mathematical definition - reflexive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is reflexive if and only if, :math:`\forall x \in S`:

        - :math:`xRx` (reflexivity)

        :return: `True` if this order-relation is reflexive, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set
        - https://en.wikipedia.org/wiki/Reflexive_relation

        """
        raise util.PunctiliousException("Abstract method.")

    @abc.abstractmethod
    @property
    def is_transitive(self) -> bool:
        r"""Returns `True` if this order-relation is transitive, `False` otherwise.

        Mathematical definition - transitive
        -------------------------------------------------

        A binary relation :math:`(S, R)` is transitive if and only if, :math:`\forall x, y, z \in S`:

        - :math:`( xRy \land yRz ) \implies xRz` (transitivity)

        :return: `True` if this order-relation is transitive, `False` otherwise.

        Bibliography
        ---------------

        - https://en.wikipedia.org/wiki/Partially_ordered_set
        - https://en.wikipedia.org/wiki/Transitive_relation

        """
        raise util.PunctiliousException("Abstract method.")


def is_less_than(x: object, y: object, o: OrderRelation | None) -> bool:
    """Returns `True` if :math:`x \prec y` under `o`, `False` otherwise.

    :param x: An element of the underlying set of order-relation `o`.
    :param y: An element of the underlying set of order-relation `o`.
    :param o: An order-relation.
    :return: `True` if :math:`x \prec y`, `False` otherwise.
    """
    return o.is_less_than(x=x, y=y)


class Orderable(abc.ABC):
    """An abstract Python class that supports relation-orders.

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
