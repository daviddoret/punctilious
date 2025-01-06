# special features
from __future__ import annotations

# external modules
import abc
import collections.abc
from logging import setLogRecordFactory

# internal modules
import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_foundational_connectors as _foundational_connectors
from punctilious.pu_04_formal_language import DuplicateProcessing


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

    def __init__(self, *elements,
                 duplicate_processing: _formal_language.DuplicateProcessing =
                 _formal_language.DuplicateProcessing.RAISE_ERROR):
        """

        :param elements:
        :param duplicate_processing: 'raise_error' (default), or 'strip'.
        """
        elements = _formal_language.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        super().__init__(c=_foundational_connectors.set_1, a=elements)

    def __new__(cls, *elements,
                duplicate_processing: _formal_language.DuplicateProcessing =
                _formal_language.DuplicateProcessing.RAISE_ERROR):
        elements = _formal_language.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        return super().__new__(cls, c=_foundational_connectors.set_1, a=elements)

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


def ensure_set_1(o: object,
                 duplicate_processing: _formal_language.DuplicateProcessing = _formal_language.DuplicateProcessing.RAISE_ERROR):
    """Ensures that the input is a Set1.

    Args:
        :param o:
        :param duplicate_processing:

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
            return Set1(*o.arguments, duplicate_processing=duplicate_processing)
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
        XXX
        return self.is_formula_equivalent(other=other)


def substitute_formulas(phi: _formal_language.Formula, m: Map1, include_root: bool = True) -> _formal_language.Formula:
    """Construct a new formula by substituting formulas in the formula tree of `phi` by applying map `m`.

    :param phi:
    :param m:
    :param include_root:
    :return:
    """
    if include_root and m.domain.has_element(phi):
        return m.get_image(x=phi)
    substituted_arguments = tuple(substitute_formulas(phi=x, m=m, include_root=True) for x in phi.arguments)
    return _formal_language.Formula(c=phi.connector, a=substituted_arguments)
