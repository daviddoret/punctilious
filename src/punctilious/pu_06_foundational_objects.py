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


class ExtensionTuple(_formal_language.Formula):
    """A Tuple1 is a model of a mathematical tuple with the following constraints:
         - it is finite,
         - it is computable,
         - it is defined by extension.

    It is implemented as a formula with a well-known `tuple_1` connector,
    whose arguments are denoted as the elements of the tuple.
    """

    def __init__(self, *a):
        super().__init__(c=_foundational_connectors.tuple_1, a=a)

    def __new__(cls, *a):
        return super().__new__(cls, c=_foundational_connectors.tuple_1, a=a)

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

    def is_tuple_equivalent_to(self, other: ExtensionTuple) -> bool:
        """Returns `True` if this tuple is equal to the `other` tuple.

        This is equivalent to formula-equivalence."""
        return self.is_formula_equivalent(other=other)

    def to_python_list(self) -> list[_formal_language.Formula]:
        return list(self.elements)

    def to_python_tuple(self) -> tuple[_formal_language.Formula, ...]:
        return tuple(self.elements)

    def to_unique_tuple(self, duplicate_processing: _formal_language.DuplicateProcessing =
    _formal_language.DuplicateProcessing.RAISE_ERROR) -> UniqueExtensionTuple:
        return UniqueExtensionTuple(self.elements, duplicate_processing=duplicate_processing)


class UniqueExtensionTuple(_formal_language.Formula):
    """A UniqueTuple is a model of a pseudo-set from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension,
     - its elements are unique,
     - its elements are ordered but unique-tuple-equivalence makes it possible to compare
       UniqueTuples without taking order in consideration.

    It is implemented as a formula with a well-known `unique_tuple` connector,
    whose arguments are denoted as the elements of the set,
    and for which no two arguments are formula-equivalent to each other.

    UniqueTuple supports the is_set_equivalent method that,
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
        super().__init__(c=_foundational_connectors.unique_tuple, a=elements)

    def __new__(cls, *elements,
                duplicate_processing: _formal_language.DuplicateProcessing =
                _formal_language.DuplicateProcessing.RAISE_ERROR):
        elements = _formal_language.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        return super().__new__(cls, c=_foundational_connectors.unique_tuple, a=elements)

    @property
    def arity(self) -> int:
        return _formal_language.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        return (element for element in self.arguments)

    def has_element(self, element: _formal_language.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple."""
        return self.has_direct_argument(argument=element)

    def is_set_equivalent_to(self, other: UniqueExtensionTuple) -> bool:
        """Returns `True` if this set is equal to the `other` set."""
        # TODO: UniqueTuple.is_set_equivalent_to: validate other.

        # Check condition for all elements in self.
        for x in self.elements:
            if not other.has_element(element=x):
                return False

        # Check condition for all elements in `other`
        for x in other.elements:
            if not self.has_element(element=x):
                return False

        return True

    def to_python_list(self) -> list[_formal_language.Formula]:
        return list(self.elements)

    def to_python_tuple(self) -> tuple[_formal_language.Formula, ...]:
        return tuple(self.elements)

    def to_python_set(self) -> set[_formal_language.Formula]:
        return set(self.elements)

    def to_tuple_1(self) -> ExtensionTuple:
        return ExtensionTuple(self.elements)


def ensure_unique_tuple(o: object,
                        duplicate_processing: _formal_language.DuplicateProcessing = _formal_language.DuplicateProcessing.RAISE_ERROR):
    """Ensures that the input is a UniqueTuple.

    Args:
        :param o:
        :param duplicate_processing:

    Returns:
        UniqueTuple: the input as an ExtensionSet

    Raises:
        ValueError: if the input is not a UniqueTuple.
    """
    if isinstance(o, UniqueExtensionTuple):
        return o
    if isinstance(o, _formal_language.Formula):
        if o.connector == _foundational_connectors.unique_tuple:
            pass
            return UniqueExtensionTuple(*o.arguments, duplicate_processing=duplicate_processing)
    raise ValueError(f'Expected UniqueTuple. o={o}. type={type(o).__name__}')


import itertools


def union_unique_tuples(*sets: UniqueExtensionTuple):
    """Returns the union of UniqueTuple provided. Strip any duplicate in the process."""
    sets = tuple(
        ensure_unique_tuple(o=s, duplicate_processing=_formal_language.DuplicateProcessing.RAISE_ERROR) for s in sets)
    flattened_set = tuple(element for sub_tuple in sets for element in sub_tuple.elements)
    output = UniqueExtensionTuple(*flattened_set, duplicate_processing=_formal_language.DuplicateProcessing.STRIP)
    return output


class ExtensionMap(_formal_language.Formula):
    """A Map1 is a model of a mathematical map with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.
     
    It is implemented as a formula with the well-known `map_1` root connector,
    whose arguments of the form:
        (D, C)
    where:
     - D is UniqueTuple denoted as the domain,
     - C is Tuple1 denoted as the codomain,
     - the arity of D and C are equal.

    Map1 supports the get_image method that,
    given an element of D, returns the corresponding element of C at the same position.
    This leverages the fact that UniqueTuple is both a model of a set,
    for which elements order is not taken into account,
    and also a Formula, whose arguments are effectively ordered.
    """

    def __init__(self, d: UniqueExtensionTuple, c: ExtensionTuple):
        if d.arity != c.arity:
            raise ValueError(f'`d` and `c` do not have equal arity. `d`: {d}. `c`: {c}.')
        super().__init__(c=_foundational_connectors.map_1, a=(d, c,))

    def __new__(cls, d: UniqueExtensionTuple, c: ExtensionTuple):
        return super().__new__(cls, c=_foundational_connectors.map_1, a=(d, c,))

    @property
    def codomain(self) -> ExtensionTuple:
        return self.arguments[1]

    @property
    def domain(self) -> UniqueExtensionTuple:
        return self.arguments[0]

    def get_image(self, x: _formal_language.Formula) -> _formal_language.Formula:
        if not self.domain.has_element(element=x):
            raise ValueError(f'`x` is not an element of the map domain. `x`: {x}.')
        i: int = self.domain.get_argument_first_index(argument=x)
        return self.codomain.arguments[i]

    def is_map_equivalent(self, other: ExtensionMap):
        """Two maps m1 and m2 are map-equivalent if and only if:
        for every element x in the union of m1 and m2 domains,
        x is defined in both domains and returns the same image."""
        # the two domains must be formula-equivalent,
        # i.e. preserving element order.
        union_of_domains = union_unique_tuples(self.domain, other.domain)
        for element in union_of_domains.elements:
            if not self.domain.has_element(element=element):
                return False
            if not other.domain.has_element(element=element):
                return False
            if not self.get_image(x=element).is_formula_equivalent(other.get_image(x=element)):
                return False
        return True

    def to_python_dict(self) -> dict[_formal_language.Formula, _formal_language.Formula]:
        return dict(zip(self.domain.elements, self.codomain.elements))


def substitute_formulas(phi: _formal_language.Formula, m: ExtensionMap,
                        include_root: bool = True) -> _formal_language.Formula:
    """Construct a new formula by substituting formulas in the formula tree of `phi` by applying map `m`.

    Implementation:
    `phi` is parsed recursively.
    If `phi` is formula-equivalent to an element of the domain of `m`, its image is returned.
    Otherwise, the same process is applied recursively to all arguments of `phi`.

    :param phi:
    :param m:
    :param include_root:
    :return:
    """
    if include_root and m.domain.has_element(phi):
        return m.get_image(x=phi)
    substituted_arguments = tuple(substitute_formulas(phi=x, m=m, include_root=True) for x in phi.arguments)
    return _formal_language.Formula(c=phi.connector, a=substituted_arguments)


def is_formula_equivalent_with_variables(phi: _formal_language.Formula, psi: _formal_language.Formula,
                                         v: UniqueExtensionTuple) -> [bool, UniqueExtensionTuple]:
    phi = _formal_language.ensure_formula(o=phi)
    psi = _formal_language.ensure_formula(o=psi)
    m: dict[_formal_language.Formula, _formal_language.Formula] = dict.fromkeys(v.elements, None)

    def _is_formula_equivalent_with_variables(phi: _formal_language.Formula, psi: _formal_language.Formula,
                                              m: dict[_formal_language.Formula, _formal_language.Formula]) -> bool:
        """

        :param phi: A formula.
        :param psi: A formula possibly with variables in it.
        :param m:
        :return:
        """
        if phi.is_formula_equivalent(psi):
            return True
        else:
            if psi in m.keys():
                # psi is a variable.
                if m[psi] is None:
                    m[psi] = phi
                    # the variable slot was not assigned yet, assign it now.
                    return True
                elif psi.is_formula_equivalent(m[phi]):
                    # matching variable value.
                    return True
                else:
                    # the variable values do not match,
                    # it follows that the two formulas are not formula-equivalent-with-variables.
                    return False
            else:
                # psi is not a variable.
                if not phi.is_root_connector_equivalent(psi):
                    # if root connectors are not equivalent,
                    # it follows that the two formulas are not formula-equivalent-with-variables.
                    return False
                else:
                    for phi_argument, psi_argument in zip(phi.arguments, psi.arguments):
                        if not _is_formula_equivalent_with_variables(phi=phi_argument, psi=psi_argument, m=m):
                            # if one sub-argument is not formula-equivalent-with-variables,
                            # it follows that the two formulas are not formula-equivalent-with-variables.
                            return False
                    # if all sub-arguments are formula-equivalent-with-variables,
                    # it follows that the two formulas are formula-equivalent-with-variables.
                    return True


class InferenceRule1(_formal_language.Formula):

    def __init__(self, v: UniqueExtensionTuple, p: UniqueExtensionTuple, c: _formal_language.Formula):
        """
        :param v: the variables.
        :param p: the premises.
        :param c: the conclusion.
        """
        super().__init__(c=_foundational_connectors.inference_rule_1, a=(v, p, c,))

    def __new__(cls, v: UniqueExtensionTuple, p: UniqueExtensionTuple, c: _formal_language.Formula):
        return super().__new__(cls, c=_foundational_connectors.inference_rule_1, a=(v, p, c,))

    @property
    def conclusion(self) -> _formal_language.Formula:
        return self.arguments[2]

    @property
    def premises(self) -> UniqueExtensionTuple:
        return self.arguments[1]

    @property
    def variables(self) -> UniqueExtensionTuple:
        return self.arguments[0]

    def apply_rule(self, arguments: ExtensionTuple) -> _formal_language.Formula:
        if arguments.arity != self.premises.arity:
            raise ValueError('arities dont match')

        # infer the variable values
        for v in self.variables.elements:
            # retrieve the position of the variable in the premises
            variable_value = None
            for p in iterate_formulas_positions(v, self.premises):
                # retrieve variable value
                new_value = retrieve_position_value(p, arguments)
                if variable_value is None:
                    variable_value = new_value
                else:
                    # check the variable value is unique
                    if variable_value.is_not_formula_equivalent(new_value):
                        raise ValueError('variable mapping inconsistency')
            # store the variable value in a map for later usage
            variable_values_map = None

        # substitute variable with values in arguments

        # check consistency with premises

        # substitute variable with values in conclusion
