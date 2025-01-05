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
    """A Tuple1 is a model of a mathematical from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.
     It is implemented as a formula with a well-known `tuple_1` connector,
     whose arguments are denoted as the elements of the tuple.
    """

    def __init__(self, *a):
        super().__init__(c=_foundational_connectors.tuple2, a=a)


class ISet(abc.ABC):
    """ISet is a generic interface for set implementations from set theory.

    This is defined for future usages.
    """
    pass


class IWellBehavingSet(abc.ABC, ISet):
    """IWellBehavingSet is a generic interface for well-behaving computable sets.

    By well-behaving it is meant that:
    - The set is finite,
    - The set is computable,
    - The arity of the set is known,
    - Elements of the set can be iterated,
    - Given any object (Formula), an algorithm is able to determine if the object
      os an element of the set or not.
    """

    @property
    @abc.abstractmethod
    def arity(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        pass

    @abc.abstractmethod
    def has_element(self, element: _formal_language.Formula) -> bool:
        pass

    @abc.abstractmethod
    def is_set_equivalent_to(self, other: IWellBehavingSet) -> bool:
        pass


class Set1(_formal_language.Formula, IWellBehavingSet):
    """A Set1 is a model of a set from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.
     It is implemented as a formula with a well-known `set_1` connector,
     whose arguments are denoted as the elements of the set,
     and for which no two arguments are formula-equivalent to each other.

    Set1 is supported by the is_set_equivalent function that,
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
        if any(_formal_language.is_formula_equivalent(phi=element, psi=x) for x in self.elements):
            return True
        return False

    def is_set_equivalent_to(self, other: IWellBehavingSet) -> bool:
        if self.arity != other.arity:
            return False

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


class VerticalMap(_formal_language.Formula):
    """A vertical map is a tuple of the form:
        (D, C)
    where:
     - D is tuple denoted as the domain,
     - C is tuple denoted as the codomain,
     - the arity of D and C are equal,
     - elements in D are unique.
    """

    def __init__(self, d, c):
        super().__init__(c=_foundational_connectors.tuple2, a=(d, c,))
        self._vertical_map = _utilities.get_empty_dict()
