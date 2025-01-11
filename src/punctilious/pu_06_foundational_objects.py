# special features
from __future__ import annotations

# external modules
import abc
import typing
import collections.abc
from logging import setLogRecordFactory

# internal modules
import punctilious.pu_01_utilities as _utilities
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_03_representation as _representation
import punctilious.pu_04_formal_language as _formal_language
import punctilious.pu_05_foundational_connectors as _foundational_connectors
from punctilious.pu_04_formal_language import DuplicateProcessing, Formula


class ExtensionTuple(_formal_language.Formula):
    """A `ExtensionTuple` is a model of a mathematical tuple with the following constraints:
         - it is finite,
         - it is computable,
         - it is defined by extension.

    It is implemented as a formula with a well-known `extension_tuple` connector,
    whose arguments are denoted as the elements of the tuple.
    """

    def __init__(self, *a):
        super().__init__(c=_foundational_connectors.extension_tuple, a=a)

    def __new__(cls, *a):
        return super().__new__(cls, c=_foundational_connectors.extension_tuple, a=a)

    @property
    def arity(self) -> int:
        return _formal_language.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        return (element for element in self.arguments)

    def has_element(self, element: _formal_language.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple, `False` otherwise.

        Note that `element` may be multiple times an element of the tuple."""
        return self.has_direct_argument(argument=element)

    @property
    def has_unique_elements(self) -> bool:
        """Returns `True` if all the elements of this ExtensionTuple are unique, `False` otherwise."""
        return self.has_unique_arguments

    def is_tuple_equivalent_to(self, other: ExtensionTuple) -> bool:
        """Returns `True` if this tuple is equal to the `other` tuple, `False` otherwise.

        This is equivalent to formula-equivalence."""
        return self.is_formula_equivalent(other=other)

    def to_python_list(self) -> list[_formal_language.Formula]:
        return list(self.elements)

    def to_python_tuple(self) -> tuple[_formal_language.Formula, ...]:
        return tuple(self.elements)

    def to_unique_extension_tuple(self, duplicate_processing: _formal_language.DuplicateProcessing =
    _formal_language.DuplicateProcessing.RAISE_ERROR) -> UniqueExtensionTuple:
        if duplicate_processing == _formal_language.DuplicateProcessing.RAISE_ERROR and not self.has_unique_arguments:
            raise ValueError(f'All the elements of this `ExtensionTuple` are not unique: {self}')
        return UniqueExtensionTuple(self.elements, duplicate_processing=duplicate_processing)


FlexibleExtensionTuple = typing.Union[ExtensionTuple, collections.abc.Iterable]


class UniqueExtensionTuple(_formal_language.Formula):
    """A UniqueTuple is a model of a pseudo-set from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension,
     - its elements are unique,
     - its elements are ordered but unique-tuple-equivalence makes it possible to compare
       UniqueTuples without taking order in consideration.

    It is implemented as a formula with a well-known `unique_tuple` connector,
    whose arguments are denoted as the elements of the UniqueExtensionTuple,
    and for which no two arguments are formula-equivalent to each other.

    UniqueTuple supports the is_unique_extension_tuple_equivalent method that,
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
        super().__init__(c=_foundational_connectors.unique_extension_tuple, a=elements)

    def __new__(cls, *elements,
                duplicate_processing: _formal_language.DuplicateProcessing =
                _formal_language.DuplicateProcessing.RAISE_ERROR):
        elements = _formal_language.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        return super().__new__(cls, c=_foundational_connectors.unique_extension_tuple, a=elements)

    @property
    def arity(self) -> int:
        return _formal_language.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_formal_language.Formula]:
        return (element for element in self.arguments)

    def has_element(self, element: _formal_language.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple."""
        return self.has_direct_argument(argument=element)

    def is_unique_extension_tuple_equivalent_to(self, other: FlexibleUniqueExtensionTuple) -> bool:
        """Returns `True` if this set is equal to the `other` set."""
        other = ensure_unique_extension_tuple(other)

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

    def to_extension_tuple(self) -> ExtensionTuple:
        """Returns an ExtensionTuple with the same elements, preserving order."""
        return ExtensionTuple(*self.elements)


FlexibleUniqueExtensionTuple = typing.Union[UniqueExtensionTuple, collections.abc.Iterable]


def ensure_unique_extension_tuple(o: FlexibleUniqueExtensionTuple,
                                  duplicate_processing: _formal_language.DuplicateProcessing = _formal_language.DuplicateProcessing.RAISE_ERROR):
    """Ensures that the input is a UniqueTuple.

    Args:
        :param o:
        :param duplicate_processing:

    Returns:
        UniqueTuple: the input as an UniqueExtensionTuple

    Raises:
        ValueError: if the input is not a UniqueTuple.
    """
    if isinstance(o, UniqueExtensionTuple):
        return o
    if isinstance(o, _formal_language.Formula):
        if o.connector == _foundational_connectors.unique_extension_tuple:
            pass
            return UniqueExtensionTuple(*o.arguments, duplicate_processing=duplicate_processing)
    raise ValueError(f'Expected UniqueTuple. o={o}. type={type(o).__name__}')


import itertools


def union_unique_tuples(*args: UniqueExtensionTuple):
    """Returns the union of UniqueTuple provided. Strip any duplicate in the process."""
    args = tuple(
        ensure_unique_extension_tuple(o=s, duplicate_processing=_formal_language.DuplicateProcessing.RAISE_ERROR) for s
        in args)
    flattened = tuple(element for sub_tuple in args for element in sub_tuple.elements)
    output = UniqueExtensionTuple(*flattened, duplicate_processing=_formal_language.DuplicateProcessing.STRIP)
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
     - D is UniqueExtensionTuple denoted as the domain,
     - C is ExtensionTuple denoted as the codomain,
     - the arity of D and C are equal.

    Map1 supports the get_image method that,
    given an element of D, returns the corresponding element of C at the same position.
    This leverages the fact that UniqueExtensionTuple is both a model of a set,
    for which elements order is not taken into account,
    and also a Formula, whose arguments are effectively ordered.
    """

    def __init__(self, domain: UniqueExtensionTuple, codomain: ExtensionTuple):
        if domain.arity != codomain.arity:
            raise ValueError(f'`d` and `c` do not have equal arity. `d`: {domain}. `c`: {codomain}.')
        super().__init__(c=_foundational_connectors.extension_map, a=(domain, codomain,))

    def __new__(cls, domain: UniqueExtensionTuple, codomain: ExtensionTuple):
        return super().__new__(cls, c=_foundational_connectors.extension_map, a=(domain, codomain,))

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

    def invert(self) -> ExtensionMap:
        """Returns the inverse map.

        Given a map `m(domain, codomain)`, the inverse map is `m(codomain, domain)`.

        If all elements of the map codomain are not unique, raises a `ValueError`.

        :return:
        """
        if not self.is_invertible:
            raise ValueError(f'This ExtensionMap is not invertible: {self}')
        new_domain = UniqueExtensionTuple(*self.codomain.elements)
        new_codomain = ExtensionTuple(*self.domain.elements)
        return ExtensionMap(domain=new_domain, codomain=new_codomain)

    def is_invertible(self) -> bool:
        """Returns `True` if the ExtensionMap can be inverted,
        that is its codomain is made of unique formulas
        such that we can create an ExtensionMap with switched domain and codomain."""
        return self.codomain.has_unique_arguments

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


def is_formula_equivalent_with_variables(formula_without_variables: _formal_language.Formula,
                                         formula_with_variables: _formal_language.Formula,
                                         variables: UniqueExtensionTuple) -> [bool, ExtensionMap]:
    formula_without_variables = _formal_language.ensure_formula(formula_without_variables)
    formula_with_variables = _formal_language.ensure_formula(formula_with_variables)
    variables = ensure_unique_extension_tuple(variables)
    # Validates that the formula_without_variables does not contain any variable.
    for variable in variables.elements:
        if formula_without_variables.tree_contains_formula(variable, include_root=True):
            raise ValueError(
                f'formula `{variable}` is a sub-formula of formula_without_variables `{formula_without_variables}`.')
    # Declare a python dictionary to collect variable values during parsing.
    m: dict[_formal_language.Formula, _formal_language.Formula] = dict.fromkeys(variables.elements, None)

    check, m = _is_formula_equivalent_with_variables(formula_without_variables=formula_without_variables,
                                                     formula_with_variables=formula_with_variables, m=m)

    # not all variables may be assigned.
    # filter all unassigned variables and return the map of variable assignments.
    all_values = tuple(m.values())
    all_keys = tuple(m.keys())
    values = tuple(value for value in all_values if value is not None)
    keys = tuple(all_keys[i] for i, value in enumerate(all_values) if value is not None)
    domain = UniqueExtensionTuple(*keys)
    codomain = ExtensionTuple(*values)
    m2 = ExtensionMap(domain=domain, codomain=codomain)

    return check, m2


def _is_formula_equivalent_with_variables(
        formula_without_variables: _formal_language.Formula, formula_with_variables: _formal_language.Formula,
        m: dict[_formal_language.Formula, _formal_language.Formula]) -> [
    bool,
    dict[_formal_language.Formula, _formal_language.Formula]]:
    """Internal function. Use public function `is_formula_equivalent_with_variables` instead."""
    if formula_without_variables.is_formula_equivalent(formula_with_variables):
        return True, m
    else:
        if formula_with_variables in m.keys():
            variable = formula_with_variables
            observed_value = formula_without_variables
            assigned_value = m[formula_with_variables]
            # formula_with_variables is a variable.
            if assigned_value is None:
                m[variable] = observed_value
                # the variable slot was not assigned yet, assign it now.
                return True, m
            elif assigned_value.is_formula_equivalent(observed_value):
                # matching variable value.
                return True, m
            else:
                # the variable values do not match,
                # it follows that the two formulas are not formula-equivalent-with-variables.
                return False, m
        else:
            # psi is not a variable.
            if not formula_without_variables.is_root_connector_equivalent(formula_with_variables):
                # if root connectors are not equivalent,
                # it follows that the two formulas are not formula-equivalent-with-variables.
                return False, m
            else:
                for phi_argument, psi_argument in zip(formula_without_variables.arguments,
                                                      formula_with_variables.arguments):
                    check, m = _is_formula_equivalent_with_variables(formula_without_variables=phi_argument,
                                                                     formula_with_variables=psi_argument, m=m)
                    if not check:
                        # if one sub-argument is not formula-equivalent-with-variables,
                        # it follows that the two formulas are not formula-equivalent-with-variables.
                        return False, m
                # if all sub-arguments are formula-equivalent-with-variables,
                # it follows that the two formulas are formula-equivalent-with-variables.
                return True, m


class InferenceRule1(_formal_language.Formula):

    def __init__(self, variables: UniqueExtensionTuple, premises: UniqueExtensionTuple,
                 conclusion: _formal_language.Formula):
        """
        :param variables: the variables.
        :param premises: the premises.
        :param conclusion: the conclusion.
        """
        super().__init__(c=_foundational_connectors.inference_rule_1, a=(variables, premises, conclusion,))

    def __new__(cls, variables: UniqueExtensionTuple, premises: UniqueExtensionTuple,
                conclusion: _formal_language.Formula):
        return super().__new__(cls, c=_foundational_connectors.inference_rule_1, a=(variables, premises, conclusion,))

    def _check_arguments_validity(self, arguments: ExtensionTuple, raise_error_if_false: bool = False) -> [bool,
                                                                                                           ExtensionTuple | None,
                                                                                                           ExtensionMap | None]:
        """Internal function. Factors validation code between `apply_rule` and `check_arguments_validity`."""
        if arguments.arity != self.premises.arity:
            if raise_error_if_false:
                raise ValueError(
                    f'The arity of the `arguments` ({arguments.arity})'
                    f' is not equal to the arity of the `premises` ({self.premises.arity}).'
                    f' `arguments`: `{arguments}`.'
                    f' `premises`: {self.premises}.')
            return False, None, None

        # the arguments are passed as an ExtensionTuple.
        # in order to check formula-equivalence-with-variables between
        # arguments and premises, we must convert premises to ExtensionTuple.
        premises_as_extension_tuple: ExtensionTuple = self.premises.to_extension_tuple()

        # the arguments must be formula-equivalent-with variables to the premises.
        # simultaneously, infer the variable values.
        check, m = is_formula_equivalent_with_variables(
            formula_without_variables=arguments,
            variables=self.variables,
            formula_with_variables=premises_as_extension_tuple
        )
        check: bool
        if not check:
            if raise_error_if_false:
                raise ValueError(
                    f'The `arguments` ({arguments})'
                    f' are not equal formula-equivalent-with-variables with the  `premises` ({self.premises}).'
                    f' `variables`: `{self.variables}`.')
            return False, None, None

        # confirm that all variables have been assigned a value.
        for variable in self.variables.elements:
            if variable not in m.domain.elements:
                if raise_error_if_false:
                    raise ValueError(
                        f'The inference of variable values from the `arguments` ({arguments}) failed.'
                        f' Some variables are left without values `m` ({m}).'
                        f' `premises`: `{self.premises}`.')
                return False, None, None

        return True, premises_as_extension_tuple, m

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
        check, premises_as_extension_tuple, m = self._check_arguments_validity(arguments=arguments,
                                                                               raise_error_if_false=True)

        # transform the conclusion.
        conclusion_with_variable_assignments: _formal_language.Formula = substitute_formulas(
            phi=self.conclusion,
            m=m,
            include_root=True
        )

        return conclusion_with_variable_assignments

    def check_arguments_validity(self, arguments: ExtensionTuple) -> bool:
        """Returns `True` if `arguments` are valid for this InferenceRule."""
        check, _, _ = self._check_arguments_validity(arguments=arguments)
        return check
