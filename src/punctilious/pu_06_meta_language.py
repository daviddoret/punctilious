# special features
from __future__ import annotations

import abc
# external modules
import typing
import collections.abc

# internal modules
import punctilious.pu_01_utilities as _utl
import punctilious.pu_02_unique_identifiers as _uid
import punctilious.pu_03_representation as _rpr
import punctilious.pu_04_formal_language as _fml


class FormSignalConnector(_fml.Connector):
    """A `FormSignalConnector` is a well-known `Connector` that is dedicated to
    signalling a formula of a defined form in a meta-language.
    """

    def __init__(self, uid: _uid.FlexibleUniqueIdentifier,
                 well_formedness_validator_function: typing.Callable,
                 well_formed_type_ensurer_function: typing.Callable,
                 well_formed_type: type,
                 syntactic_rules=_fml.SyntacticRules(),
                 connector_representation: _rpr.AbstractRepresentation | None = None,
                 formula_representation: _rpr.AbstractRepresentation | None = None
                 ):
        self._well_formedness_validator_function = well_formedness_validator_function
        self._well_formed_type_ensurer_function = well_formed_type_ensurer_function
        self._well_formed_type = well_formed_type
        super().__init__(uid=uid,
                         syntactic_rules=syntactic_rules,
                         connector_representation=connector_representation,
                         formula_representation=formula_representation)

    def check_formula_well_formedness(self, formula: _fml.Formula) -> bool:
        """Returns `True` if `formula` is well-formed
        for the formula structure expected by this connector."""
        return self._well_formedness_validator_function(formula)

    def ensure_formula_well_formed_type(self, formula: _fml.Formula) -> _fml.Formula:
        """Given a `formula`
        presumably well-formed for the formula structure expected by this connector,
        returns a formula object of the `well_formed_type`."""
        return self._well_formed_type_ensurer_function(formula)

    @property
    def well_formed_python_type(self) -> type:
        """The `well_formed_python_type` of the connector is a Python type that enforces well-formedness."""
        return self._well_formed_type


class WellFormedFormula(abc.ABC):
    """A `WellFormedFormula` is a formula that is well-formed
    according to some definition.
    """

    def __init__(self, connector, arguments=None):
        """

        :param connector: A connector.
        :param arguments: A (possibly empty) collection of arguments.
        """
        super().__init__()

    def __new__(cls, connector, arguments=None):
        connector: _fml.Connector = _fml.ensure_connector(connector)
        arguments: _fml.FormulaArguments = _fml.ensure_formula_arguments(arguments)
        phi: tuple[_fml.Connector, _fml.FormulaArguments] = (connector, arguments,)
        return super().__new__(cls, phi)


class ITheoryComponent(abc.ABC):
    pass


class IClaim(ITheoryComponent, abc.ABC):
    """An `IClaim` is a theory component that claims a statement as valid in some theoretical context.
    """

    @property
    @abc.abstractmethod
    def claimed_statement(self) -> _fml.Formula:
        """The statement claimed as valid in some theoretical context.

        :return: A formula.
        """
        raise _utl.PunctiliousError(
            title='Abstract method not implemented.',
            details='Python object `o` inherits from abstract class `IClaim`,'
                    ' but method `claimed_statement` is not implemented.',
            o=self)


class IInferenceRule(abc.ABC):
    """

    """

    @abc.abstractmethod
    def apply_rule(self, inputs: typing.Iterable[_fml.Formula]) -> _fml.Formula:
        raise _utl.PunctiliousError(
            title='Abstract method not implemented.',
            details='Python object `o` inherits from abstract class `IInferenceRule`,'
                    ' but method `apply_rule` is not implemented.',
            o=self)


class WellFormedAxiom(_fml.Formula, IClaim):
    """An `Axiom` is a model of a mathematical axiom.

    It is implemented as a unary formula with a well-known `axiom` connector,
    whose argument is the statement content.
    """
    _AXIOM_STATEMENT_INDEX: int = 0

    def __init__(self, statement: _fml.Formula):
        super().__init__(connector=axiom_connector, arguments=(statement,))

    def __new__(cls, statement: _fml.Formula):
        """

        Note: this method must be consistent with function :func:`is_well_formed_axiom`.

        :param statement:
        """
        statement = _fml.ensure_formula(statement)
        return super().__new__(cls, connector=axiom_connector, arguments=(statement,))

    @property
    def claimed_statement(self) -> _fml.Formula:
        return self.arguments[WellFormedAxiom._AXIOM_STATEMENT_INDEX]


class ExtensionTuple(_fml.Formula):
    """A `ExtensionTuple` is a model of a mathematical tuple with the following constraints:
         - it is finite,
         - it is computable,
         - it is defined by extension.

    It is implemented as a formula with a well-known `extension_tuple` connector,
    whose arguments are denoted as the elements of the tuple.
    """

    def __init__(self, *arguments):
        super().__init__(connector=extension_tuple_connector, arguments=arguments)

    def __new__(cls, *arguments):
        arguments = _fml.ensure_formulas(*arguments)
        return super().__new__(cls, connector=extension_tuple_connector, arguments=arguments)

    @property
    def arity(self) -> int:
        return _fml.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_fml.Formula]:
        return (element for element in self.arguments)

    def has_top_level_element(self, element: _fml.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple, `False` otherwise.

        Note that `element` may be multiple times an element of the tuple."""
        return self.has_top_level_argument(argument=element)

    @property
    def has_unique_elements(self) -> bool:
        """Returns `True` if all the elements of this ExtensionTuple are unique, `False` otherwise."""
        return self.has_unique_arguments

    def is_tuple_equivalent_to(self, other: ExtensionTuple) -> bool:
        """Returns `True` if this tuple is equal to the `other` tuple, `False` otherwise.

        This is equivalent to formula-equivalence."""
        return self.is_formula_equivalent(other_formula=other)

    def iterate_elements(self) -> typing.Generator[_fml.Formula, None, None]:
        yield from self.iterate_top_level_arguments()

    def to_python_list(self) -> list[_fml.Formula]:
        return list(self.elements)

    def to_python_tuple(self) -> tuple[_fml.Formula, ...]:
        return tuple(self.elements)

    def to_unique_extension_tuple(self, duplicate_processing: _fml.DuplicateProcessing =
    _fml.DuplicateProcessing.RAISE_ERROR) -> UniqueExtensionTuple:
        if duplicate_processing == _fml.DuplicateProcessing.RAISE_ERROR and not self.has_unique_arguments:
            raise ValueError(f'All the elements of this `ExtensionTuple` are not unique: {self}')
        return UniqueExtensionTuple(self.elements, duplicate_processing=duplicate_processing)


class UniqueExtensionTuple(_fml.Formula):
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
                 duplicate_processing: _fml.DuplicateProcessing =
                 _fml.DuplicateProcessing.RAISE_ERROR):
        """

        :param elements:
        :param duplicate_processing: 'raise_error' (default), or 'strip'.
        """
        elements = _fml.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        super().__init__(connector=unique_extension_tuple_connector, arguments=elements)

    def __new__(cls, *elements,
                duplicate_processing: _fml.DuplicateProcessing =
                _fml.DuplicateProcessing.RAISE_ERROR):
        elements = _fml.ensure_unique_formulas(*elements, duplicate_processing=duplicate_processing)
        return super().__new__(cls, connector=unique_extension_tuple_connector, arguments=elements)

    @property
    def arity(self) -> int:
        return _fml.Formula.arity.__get__(self)

    @property
    def elements(self) -> collections.abc.Iterable[_fml.Formula]:
        return (element for element in self.arguments)

    def has_top_level_element(self, element: _fml.Formula) -> bool:
        """Returns `True` if `element` is an element of the tuple."""
        return self.has_top_level_argument(argument=element)

    def is_unique_extension_tuple_equivalent_to(self, other: FlexibleUniqueExtensionTuple) -> bool:
        """Returns `True` if this set is equal to the `other` set."""
        other = ensure_unique_extension_tuple(other)

        # Check condition for all elements in self.
        for x in self.elements:
            if not other.has_top_level_element(element=x):
                return False

        # Check condition for all elements in `other`
        for x in other.elements:
            if not self.has_top_level_element(element=x):
                return False

        return True

    def iterate_top_level_elements(self) -> typing.Generator[_fml.Formula, None, None]:
        yield from self.iterate_top_level_arguments()

    def to_python_list(self) -> list[_fml.Formula]:
        return list(self.elements)

    def to_python_tuple(self) -> tuple[_fml.Formula, ...]:
        return tuple(self.elements)

    def to_python_set(self) -> set[_fml.Formula]:
        return set(self.elements)

    def to_extension_tuple(self) -> ExtensionTuple:
        """Returns an ExtensionTuple with the same elements, preserving order."""
        return ExtensionTuple(*self.elements)


def ensure_extension_tuple(o: FlexibleExtensionTuple) -> ExtensionTuple:
    """Ensures that the input is an extension-tuple, and returns an instance of ExtensionTuple.

    :param o:
    :return:
    """
    if isinstance(o, ExtensionTuple):
        return o
    if isinstance(o, _fml.Formula) and o.connector == extension_tuple_connector:
        return ExtensionTuple(*o.arguments)
    raise _utl.PunctiliousError(f'`o` is not an extension-tuple.', o=o)


def ensure_unique_extension_tuple(
        o: FlexibleUniqueExtensionTuple,
        duplicate_processing: _fml.DuplicateProcessing = _fml.DuplicateProcessing.RAISE_ERROR) -> UniqueExtensionTuple:
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
    if isinstance(o, _fml.Formula) and o.connector == unique_extension_tuple_connector:
        return UniqueExtensionTuple(*o.arguments, duplicate_processing=duplicate_processing)
    raise _utl.PunctiliousError(f'`o` is not a unique-extension-tuple.', o=o)


def ensure_extension_map(o: FlexibleExtensionTuple) -> ExtensionMap:
    """Ensures that the input is an extension-map, and returns an instance of ExtensionMap.

    :param o:
    :return:
    """
    if isinstance(o, ExtensionMap):
        return o
    if isinstance(o, _fml.Formula) and o.connector == extension_map_connector:
        return ExtensionMap(*o.arguments)
    raise _utl.PunctiliousError(f'`o` is not an extension-tuple.', o=o)


def ensure_natural_inference_rule(o: FlexibleNaturalInferenceRule) -> NaturalInferenceRule:
    """Ensures that the input is a natural-inference-rule, and returns an instance of NaturalInferenceRule.

    :param o:
    :return:
    """
    if isinstance(o, NaturalInferenceRule):
        return o
    if isinstance(o, _fml.Formula) and o.connector == natural_inference_rule_connector:
        return NaturalInferenceRule(*o.arguments)
    raise _utl.PunctiliousError(title='Inconsistent natural-inference-rule.',
                                details=f'`o` cannot be interpreted as a natural-inference-rule.',
                                o=o)


def ensure_natural_inference_rules(o: typing.Iterable[FlexibleNaturalInferenceRule]) -> typing.Generator[
    NaturalInferenceRule, None, None]:
    for i in o:
        yield ensure_natural_inference_rule(i)


def ensure_inference_step(o: FlexibleInferenceStep):
    """Ensures that the input is an inference-step, and returns an instance of InferenceStep.

    :param o:
    :return:
    """
    if isinstance(o, InferenceStep):
        return o
    if isinstance(o, _fml.Formula) and o.connector == inference_step_connector:
        return InferenceStep(*o.arguments)
    raise _utl.PunctiliousError(f'`o` is not an inference-step.', o=o)


def ensure_well_formed_axiom(formula: _fml.Formula):
    """Ensures that `formula` is a well-formed axiom, raises an exception otherwise.

    :param formula: A formula.
    :return: An axiom, typed as WellFormedAxiom.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedAxiom):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == axiom_connector:
        # The class initializer ensures well-formedness.
        return WellFormedAxiom(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Non-supported type',
                                    details=f'The Python type of `formula` is not supported.',
                                    formula=formula)


def ensure_well_formed_formula(formula: _fml.Formula) -> WellFormedFormula:
    """Ensures that `formula` is a well-formed formula, raises an exception otherwise.

    A well-formed formula is a formula that is well-formed according to some definition.

    Well-formed formulas are implemented with Python IWellFormedFormula abstract-class.

    Canonically well-formed formulas can be automatically identified if they are composed with a
    dedicated WellFormingConnector connector that signals their presence.

    :param formula: A formula.
    :return: A canonically well-formed formula.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedFormula):
        # The type ensures well-formedness.
        return formula
    elif (isinstance(formula, _fml.Formula) and
          isinstance(formula.connector, _fml.FormSignalConnector) and
          formula.connector.is_well_formed(formula)):
        # A
        return formula.connector.ensure_well_formed_type(formula)
    else:
        raise _utl.PunctiliousError(title='Non-supported type',
                                    details=f'The Python type of `formula` is not supported.',
                                    formula=formula)


def union_unique_tuples(*args: UniqueExtensionTuple):
    """Returns the union of UniqueTuple provided. Strip any duplicate in the process."""
    args = tuple(
        ensure_unique_extension_tuple(o=s, duplicate_processing=_fml.DuplicateProcessing.RAISE_ERROR) for s
        in args)
    flattened = tuple(element for sub_tuple in args for element in sub_tuple.elements)
    output = UniqueExtensionTuple(*flattened, duplicate_processing=_fml.DuplicateProcessing.STRIP)
    return output


class ExtensionMap(_fml.Formula):
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
    DOMAIN_INDEX: int = 0  # The index-position of the `domain` element in the `arguments` tuple.
    CODOMAIN_INDEX: int = 1  # The index-position of the `codomain` element in the `arguments` tuple.
    _FORMULA_FIXED_ARITY: int = 2  # A syntactic-rule.

    def __init__(self, domain: UniqueExtensionTuple, codomain: ExtensionTuple):
        if domain.arity != codomain.arity:
            raise _utl.PunctiliousError(f'The arity of the `domain` is not equal to the arity of the `codomain`.',
                                        domain_arity=domain.arity, codomain_arity=codomain.arity,
                                        domain=domain, codomain=codomain)
        super().__init__(connector=extension_map_connector, arguments=(domain, codomain,))

    def __new__(cls, domain: UniqueExtensionTuple, codomain: ExtensionTuple):
        return super().__new__(cls, connector=extension_map_connector, arguments=(domain, codomain,))

    @property
    def codomain(self) -> ExtensionTuple:
        return ensure_extension_tuple(self.arguments[self.__class__.CODOMAIN_INDEX])

    @property
    def domain(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(self.arguments[self.__class__.DOMAIN_INDEX])

    def get_image(self, x: _fml.Formula) -> _fml.Formula:
        if not self.domain.has_top_level_element(element=x):
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
            if not self.domain.has_top_level_element(element=element):
                return False
            if not other.domain.has_top_level_element(element=element):
                return False
            if not self.get_image(x=element).is_formula_equivalent(other.get_image(x=element)):
                return False
        return True

    def to_python_dict(self) -> dict[_fml.Formula, _fml.Formula]:
        return dict(zip(self.domain.elements, self.codomain.elements))


def substitute_formulas(phi: _fml.Formula, m: ExtensionMap,
                        include_root: bool = True) -> _fml.Formula:
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
    if include_root and m.domain.has_top_level_element(phi):
        return m.get_image(x=phi)
    substituted_arguments = tuple(substitute_formulas(phi=x, m=m, include_root=True) for x in phi.arguments)
    return _fml.Formula(connector=phi.connector, arguments=substituted_arguments)


def is_formula_equivalent_with_variables(formula_without_variables: _fml.Formula,
                                         formula_with_variables: _fml.Formula,
                                         variables: UniqueExtensionTuple) -> [bool, ExtensionMap]:
    formula_without_variables = _fml.ensure_formula(formula_without_variables)
    formula_with_variables = _fml.ensure_formula(formula_with_variables)
    variables = ensure_unique_extension_tuple(variables)
    # Validates that the formula_without_variables does not contain any variable.
    for variable in variables.elements:
        if formula_without_variables.tree_contains_formula(variable, include_root=True):
            raise ValueError(
                f'formula `{variable}` is a sub-formula of formula_without_variables `{formula_without_variables}`.')
    # Declare a python dictionary to collect variable values during parsing.
    m: dict[_fml.Formula, _fml.Formula] = dict.fromkeys(variables.elements, None)

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
        formula_without_variables: _fml.Formula, formula_with_variables: _fml.Formula,
        m: dict[_fml.Formula, _fml.Formula]) -> [
    bool,
    dict[_fml.Formula, _fml.Formula]]:
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


class NaturalInferenceRule(_fml.Formula, ITheoryComponent, IInferenceRule):
    _NATURAL_INFERENCE_RULE_VARIABLES_INDEX: int = 0
    _NATURAL_INFERENCE_RULE_PREMISES_INDEX: int = 1
    _NATURAL_INFERENCE_RULE_CONCLUSION_INDEX: int = 2
    _NATURAL_INFERENCE_RULE_FIXED_ARITY: int = 3

    def __init__(self, variables: UniqueExtensionTuple, premises: UniqueExtensionTuple,
                 conclusion: _fml.Formula):
        """
        :param variables: the variables.
        :param premises: the premises.
        :param conclusion: the conclusion.
        """
        variables: UniqueExtensionTuple = ensure_unique_extension_tuple(variables)
        premises: UniqueExtensionTuple = ensure_unique_extension_tuple(premises)
        conclusion: _fml.Formula = _fml.ensure_formula(conclusion)
        super().__init__(connector=natural_inference_rule_connector, arguments=(variables, premises,
                                                                                conclusion,))

    def __new__(cls, variables: UniqueExtensionTuple, premises: UniqueExtensionTuple,
                conclusion: _fml.Formula):
        return super().__new__(cls, connector=natural_inference_rule_connector,
                               arguments=(variables, premises,
                                          conclusion,))

    def _check_arguments_validity(self, inputs: ExtensionTuple, raise_error_if_false: bool = False) -> [bool,
                                                                                                        ExtensionTuple | None,
                                                                                                        ExtensionMap | None]:
        """Internal function. Factors validation code between `apply_rule` and `check_arguments_validity`."""
        if inputs.arity != self.premises.arity:
            if raise_error_if_false:
                raise _utl.PunctiliousError(
                    'Inconsistent natural-inference-rule.'
                    '\n\tThe arity of the `inputs`'
                    ' is not equal to the arity of the `premises`.',
                    inputs=inputs,
                    premises=self.premises)
            return False, None, None

        # the arguments are passed as an ExtensionTuple.
        # in order to check formula-equivalence-with-variables between
        # arguments and premises, we must convert premises to ExtensionTuple.
        premises_as_extension_tuple: ExtensionTuple = self.premises.to_extension_tuple()

        # the arguments must be formula-equivalent-with variables to the premises.
        # simultaneously, infer the variable values.
        check, m = is_formula_equivalent_with_variables(
            formula_without_variables=inputs,
            variables=self.variables,
            formula_with_variables=premises_as_extension_tuple
        )
        check: bool
        if not check:
            if raise_error_if_false:
                raise _utl.PunctiliousError(
                    f'Inconsistent natural-inference-rule. The `inputs`'
                    f' are not formula-equivalent-with-variables with the `premises`, '
                    f' given the `variables`.',
                    inputs=inputs,
                    premises=premises_as_extension_tuple,
                    variables=self.variables)
            return False, None, None

        # confirm that all variables have been assigned a value.
        for variable in self.variables.elements:
            if variable not in m.domain.elements:
                if raise_error_if_false:
                    raise _utl.PunctiliousError(
                        title='Inconsistent natural-inference',
                        details=f'The value of the `variable` could not be inferred from the `inputs`.',
                        variable=variable,
                        inputs=inputs,
                        premises=self.premises,
                        inference_rule=self)
                return False, None, None

        return True, premises_as_extension_tuple, m

    @property
    def conclusion(self) -> _fml.Formula:
        return self.arguments[NaturalInferenceRule._NATURAL_INFERENCE_RULE_CONCLUSION_INDEX]

    @property
    def premises(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(
            self.arguments[NaturalInferenceRule._NATURAL_INFERENCE_RULE_PREMISES_INDEX])

    @property
    def variables(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(
            self.arguments[NaturalInferenceRule._NATURAL_INFERENCE_RULE_VARIABLES_INDEX])

    def apply_rule(self, inputs: typing.Iterable[_fml.Formula]) -> _fml.Formula:
        check, premises_as_extension_tuple, m = self._check_arguments_validity(inputs=inputs,
                                                                               raise_error_if_false=True)

        # transform the conclusion.
        conclusion_with_variable_assignments: _fml.Formula = substitute_formulas(
            phi=self.conclusion,
            m=m,
            include_root=True
        )

        return conclusion_with_variable_assignments

    def check_arguments_validity(self, arguments: ExtensionTuple) -> bool:
        """Returns `True` if `arguments` are valid for this InferenceRule."""
        check, _, _ = self._check_arguments_validity(inputs=arguments)
        return check


class InferenceStep(_fml.Formula, IClaim):
    _INFERENCE_STEP_STATEMENT_INDEX: int = 0
    _INFERENCE_STEP_INPUTS: int = 1
    _INFERENCE_STEP_INFERENCE_RULE_INDEX: int = 2
    _INFERENCE_STEP_FIXED_ARITY: int = 3

    def __init__(self, statement: _fml.Formula, inputs: FlexibleExtensionTuple,
                 inference_rule: FlexibleNaturalInferenceRule):
        super().__init__(connector=theory_connector, arguments=(statement, inputs, inference_rule,))

    def __new__(cls, statement: _fml.Formula, inputs: FlexibleExtensionTuple,
                inference_rule: FlexibleNaturalInferenceRule,
                ):
        statement: _fml.Formula = _fml.ensure_formula(statement)
        inputs: ExtensionTuple = ensure_extension_tuple(inputs)
        inference_rule: NaturalInferenceRule = ensure_natural_inference_rule(inference_rule)
        infered_statement: _fml.Formula = inference_rule.apply_rule(inputs)
        if not infered_statement.is_formula_equivalent(statement):
            raise _utl.PunctiliousError(f'Inconsistent inference-step. Applying the `inference_rule` on the `arguments`'
                                        f' yields a `conclusion` that is distinct from the `statement`.',
                                        statement=statement,
                                        conclusion=infered_statement,
                                        arguments=inputs,
                                        inference_rule=inference_rule)
        return super().__new__(cls, connector=theory_connector, arguments=(statement, inputs, inference_rule,))

    @property
    def inputs(self) -> ExtensionTuple:
        return ensure_extension_tuple(self.arguments[InferenceStep._INFERENCE_STEP_INPUTS])

    @property
    def inference_rule(self) -> NaturalInferenceRule:
        return ensure_natural_inference_rule(self.arguments[InferenceStep._INFERENCE_STEP_INFERENCE_RULE_INDEX])

    @property
    def claimed_statement(self) -> _fml.Formula:
        return _fml.ensure_formula(self.arguments[InferenceStep._INFERENCE_STEP_STATEMENT_INDEX])


class Theory(_fml.Formula):
    _THEORY_AXIOMS_INDEX: int = 0
    _THEORY_INFERENCE_RULES_INDEX: int = 1
    _THEORY_INFERENCE_STEPS_INDEX: int = 2
    _THEORY_FIXED_ARITY: int = 3

    def __init__(self, axioms: UniqueExtensionTuple, inference_rules: UniqueExtensionTuple,
                 inference_steps: UniqueExtensionTuple):
        super().__init__(connector=theory_connector, arguments=(axioms, inference_rules, inference_steps,))

    def __new__(cls, axioms: UniqueExtensionTuple, inference_rules: UniqueExtensionTuple,
                inference_steps: UniqueExtensionTuple):
        axioms = ensure_unique_extension_tuple(axioms)
        # QUESTION: The following approach will systematically create objects
        # instead of using the existing one if adequate. Is this avoidable?
        inference_rules = ensure_unique_extension_tuple(inference_rules)
        inference_rules = UniqueExtensionTuple(
            *tuple(ensure_natural_inference_rule(x) for x in inference_rules.iterate_top_level_elements()))
        inference_steps = ensure_unique_extension_tuple(inference_steps)
        inference_steps = UniqueExtensionTuple(
            *tuple(ensure_inference_step(x) for x in inference_steps.iterate_top_level_elements()))
        for inference_step in inference_steps.iterate_top_level_elements():
            inference_step: InferenceStep
            inference_rule: NaturalInferenceRule = inference_step.inference_rule

            XXXXX
            # TODO: CHECK ---> UP TO THIS THEORY LIMIT
            if not is_valid_inference_rule(inference_rule=inference_rule, assumptioms=iterate_valid_inference_rules(
                    inference_rules=inference_rules, inference_steps=inference_steps)):
                raise _utl.PunctiliousError(title='Inconsistent theory.',
                                            details='The `inference_step` is based on an `inference_rule`'
                                                    ' that is not valid in the `theory`.',
                                            inference_rule=inference_rule,
                                            inference_step=inference_step,
                                            axioms=axioms)
            for argument in inference_step.iterate_top_level_arguments():
                # Check that the argument is valid in the theory.
                XXXXX
                # TODO: CHECK ---> UP TO THIS THEORY LIMIT
                if not is_valid_statement(statement=argument, theory_components=iterate_valid_statements(axioms=axioms,
                                                                                                         inference_steps=inference_steps)):
                    raise _utl.PunctiliousError(title='Inconsistent theory.',
                                                details='The `inference_step` is based on an `argument`'
                                                        ' that is not valid in the `theory`.',
                                                argument=argument,
                                                inference_step=inference_step,
                                                axioms=axioms)
        return super().__new__(cls, connector=theory_connector, arguments=(axioms, inference_rules, inference_steps,))

    @property
    def axioms(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(self.arguments[Theory._THEORY_AXIOMS_INDEX])

    @property
    def inference_rules(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(self.arguments[Theory._THEORY_INFERENCE_RULES_INDEX])

    @property
    def inference_steps(self) -> UniqueExtensionTuple:
        return ensure_unique_extension_tuple(self.arguments[Theory._THEORY_INFERENCE_STEPS_INDEX])

    def is_valid_statement(self, formula: _fml.Formula) -> bool:
        """Returns `True` if `formula` is a valid statement in the theory, `False` otherwise.

        Note: `False` does not imply that `formula` is not a valid statement in the theory,
        `False` only implies that the theory does not prove `formula` yet.
        """
        formula: _fml.Formula = _fml.ensure_formula(formula)
        return is_valid_statement(statement=formula, theory_components=self.iterate_valid_statements())

    def iterate_valid_statements(self) -> typing.Generator[_fml.Formula, None, None]:
        """Iterates the theory valid statements in canonical order.

        :return:
        """
        yield from iterate_valid_statements(axioms=self.axioms, inference_steps=self.inference_steps)


def iterate_valid_statements(axioms: typing.Iterable[_fml.Formula], inference_steps: typing.Iterable[InferenceStep]) -> \
        typing.Generator[_fml.Formula, None, None]:
    """Given the components of a theory, that is a collection of axioms and a collection of inference_steps,
    yield all the valid statements."""
    for a in axioms:
        yield a
    for step in inference_steps:
        yield step.claimed_statement


def ensure_theory(o) -> Theory:
    if isinstance(o, Theory):
        return o
    if isinstance(o, _fml.Formula) and o.connector == theory_connector:
        return Theory(*o.arguments)
    raise _utl.PunctiliousError(title='Inconsistent theory.',
                                details=f'`o` cannot be interpreted as a theory.',
                                o=o)


def is_valid_statement(statement: _fml.Formula, theory_components: typing.Iterable[ITheoryComponent]) -> bool:
    """Returns `True` if `statement` is valid given a collection of `theory_components`, `False` otherwise.

    Note 1:
    A statement is valid given a collection of theory components if and only if
    the statement is formula-equivalent to the statement claimed by at least
    one theory component.

    """
    statement: _fml.Formula = _fml.ensure_formula(statement)
    for theory_component in theory_components:
        theory_component: ITheoryComponent = ensure_theory_component(theory_component)
        if isinstance(theory_component, IClaim):
            theory_statement: IClaim = theory_component
            if statement.is_formula_equivalent(theory_statement.claimed_statement):
                return True
    return False


FlexibleAxiom = typing.Union[WellFormedAxiom, _fml.Formula]
FlexibleStatement = typing.Union[IClaim, _fml.Formula]
FlexibleExtensionMap = typing.Union[ExtensionMap, _fml.Formula]
FlexibleExtensionTuple = typing.Union[ExtensionTuple, _fml.Formula, collections.abc.Iterable]
FlexibleNaturalInferenceRule = typing.Union[ExtensionTuple, _fml.Formula]
FlexibleInferenceStep = typing.Union[InferenceStep, _fml.Formula]
FlexibleUniqueExtensionTuple = typing.Union[UniqueExtensionTuple, _fml.Formula, collections.abc.Iterable]
FlexibleTheory = typing.Union[Theory, _fml.Formula]


def is_well_formed_axiom(formula: _fml.Formula, raise_error_if_false: bool = False) -> bool:
    """Returns `True` if `formula` is a well-formed axiom, `False` otherwise.

    Note: this function must be consistent with method :meth:`WellFormedAxiom.__new__`.

    :param formula: A formula.
    :param raise_error_if_false: Raises an exception instead of returning `False`.
    :return:
    """
    formula = _fml.ensure_formula(formula)
    if formula.connector != axiom_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed axiom',
                details='`formula` is not a well-formed axiom.'
                        'Its root connector is not the well-known `axiom_connector`.',
                formula=formula,
                axiom_connector=axiom_connector
            )
        return False
    if formula.arity != 1:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed axiom',
                details='`formula` is not a well-formed axiom.'
                        'Its arity is not equal 1.',
                formula=formula
            )
        return False
    return True


# well-known connectors
# the `tuple` connector is necessary to build complex formulas.
extension_tuple_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='extension_tuple', uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb'))
"""The well-known connector of the `Tuple1` object.
"""

unique_extension_tuple_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='unique_extension_tuple', uuid='8fd36cc9-8845-4cdf-ac24-1faf95ee44fc'))
"""The well-known connector of the `UniqueTuple` object.
"""

extension_map_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='extension_map', uuid='2509dbf9-d636-431c-82d4-6d33b2de3bc4'))
"""The well-known connector of the `Map1` object.
"""

natural_inference_rule_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='inference_rule_1', uuid='6f6c4c60-7129-4c60-801f-1454581f01fe'))
"""The well-known connector of the `InferenceRule1` object.
"""

inference_step_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='inference_step', uuid='b527b045-614b-49d6-95b3-9725f9143ba2'))
"""The well-known connector of the `InferenceStep` object.
"""

theory_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='theory', uuid='2724eebf-070d-459d-a097-de9889f118b9'))
"""The well-known connector of the `Theory` object.
"""

axiom_connector = FormSignalConnector(
    uid=_uid.UniqueIdentifier(slug='axiom', uuid='0ead1815-8a20-4b02-bd06-1b5ae0295c92'),
    well_formedness_validator_function=is_well_formed_axiom,
    well_formed_type_ensurer_function=ensure_well_formed_axiom,
    well_formed_type=WellFormedAxiom)
"""The well-known connector of the `Axiom` object.
"""

statement_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='statement', uuid='254d104d-8746-415b-b146-279fcc7e037f'))
"""The well-known connector of the `Statement` object.
"""

true2 = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='true', uuid='dde98ed2-b7e0-44b2-bd10-5f59d61fd93e'))

false2 = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='false2', uuid='ffa97ce6-e320-4e5c-86c7-d7470c2d7c94'))
