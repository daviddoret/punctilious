# special features
from __future__ import annotations

# external modules
import abc
import collections.abc

# internal modules
import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_foundational_connectors as _foundational_connectors


class Tuple1(_formal_language.Formula):
    """A Tuple1 is a model of a mathematical tuple with the following constraints:
         - it is finite,
         - it is computable,
         - it is defined by extension.

    It is implemented as a formula with a well-known `tuple_1` connector,
    whose arguments are denoted as the elements of the tuple.
    """

    def __init__(self, *a):
        super().__init__(c=_foundational_connectors.tuple1, a=a)

    def __new__(cls, *a):
        return super().__new__(cls, c=_foundational_connectors.tuple1, a=a)

    @property
    def arity(self) -> int:
        return _formal_language.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        return (element for element in self.arguments)

    def has_element(self, element: _formal_language.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple.

        Note that `element` may be multiple times an element of the tuple."""
        return self.has_direct_argument(argument=element)

    def is_tuple_equivalent_to(self, other: Tuple1) -> bool:
        """Returns `True` if this tuple is equal to the `other` tuple.

        This is equivalent to formula-equivalence."""
        return self.is_formula_equivalent(other=other)


class Set1(_formal_language.Formula):
    """A Set1 is a model of a set from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.

    It is implemented as a formula with a well-known `set_1` connector,
    whose arguments are denoted as the elements of the set,
    and for which no two arguments are formula-equivalent to each other.

    Set1 supports the is_set_equivalent method that,
    contrary to formulas and tuples, does not take into account
    the order of the arguments.
    """

    def __init__(self, *a):
        # check that all arguments are unique.
        n = len(a)
        for i in range(n):
            for j in range(i + 1, n):
                if _formal_language.is_formula_equivalent(phi=a[i], psi=a[j]):
                    raise ValueError(f'Arguments must be unique. a[{i}]={a[i]}, a[{j}]={a[j]}.')
        super().__init__(c=_foundational_connectors.set_1, a=a)

    def __new__(cls, *a):
        return super().__new__(cls, c=_foundational_connectors.set_1, a=a)

    @property
    def arity(self) -> int:
        return _formal_language.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        return (element for element in self.arguments)

    def has_element(self, element: _formal_language.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple."""
        return self.has_direct_argument(argument=element)

    def is_set_equivalent_to(self, other: Set1) -> bool:
        """Returns `True` if this set is equal to the `other` set."""
        # TODO: Set1.is_set_equivalent_to: validate other.

        # Check condition for all elements in self.
        for x in self.elements:
            if not other.has_element(element=x):
                return False

        # Check condition for all elements in `other`
        for x in other.elements:
            if not self.has_element(element=x):
                return False

        return True


def ensure_set_1(o):
    """Ensures that the input is a Set1.

    Args:
        o: an object

    Returns:
        Set1: the input as an ExtensionSet

    Raises:
        ValueError: if the input is not a Set1.
    """
    if isinstance(o, Set1):
        return o
    if isinstance(o, _formal_language.Formula):
        if o.connector == _foundational_connectors.set_1:
            pass
            return Set1(*o.arguments)
    raise ValueError(f'Expected Set1. o={o}. type={type(o).__name__}')


class Map1(_formal_language.Formula):
    """A Map1 is a model of a mathematical map with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.
     
    It is implemented as a formula with the well-known `map_1` root connector,
    whose arguments of the form:
        (D, C)
    where:
     - D is Set1 denoted as the domain,
     - C is Tuple1 denoted as the codomain,
     - the arity of D and C are equal.

    Map1 supports the get_image method that,
    given an element of D, returns the corresponding element of C at the same position.
    This leverages the fact that Set1 is both a model of a set,
    for which elements order is not taken into account,
    and also a Formula, whose arguments are effectively ordered.
    """

    def __init__(self, d: Set1, c: Tuple1):
        if d.arity != c.arity:
            raise ValueError(f'`d` and `c` do not have equal arity. `d`: {d}. `c`: {c}.')
        super().__init__(c=_foundational_connectors.map_1, a=(d, c,))

    def __new__(cls, d: Set1, c: Tuple1):
        return super().__new__(cls, c=_foundational_connectors.map_1, a=(d, c,))

    @property
    def codomain(self) -> Tuple1:
        return self.arguments[1]

    @property
    def domain(self) -> Set1:
        return self.arguments[0]

    def get_image(self, x: _formal_language.Formula) -> _formal_language.Formula:
        if not self.domain.has_element(element=x):
            raise ValueError(f'`x` is not an element of the map domain. `x`: {x}.')
        i: int = self.domain.get_argument_first_index(argument=x)
        return self.codomain.arguments[i]

    def is_map_equivalent(self, other: Map1):
        # the two domains must be formula-equivalent,
        # i.e. preserving element order.
        return self.is_formula_equivalent(other=other)
