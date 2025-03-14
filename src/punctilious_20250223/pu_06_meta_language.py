# special features
from __future__ import annotations

import abc
# external modules
import typing
import collections.abc

# internal modules
import punctilious_20250223.constants as _cst
import punctilious_20250223.pu_01_utilities as _utl
import punctilious_20250223.pu_02_unique_identifiers as _uid
import punctilious_20250223.pu_03_representation as _rpr
import punctilious_20250223.pu_04_formal_language as _fml


class WellFormedFormulaConnector(_fml.Connector):
    """A `WellFormedFormulaConnector` is a well-known `Connector` that is dedicated to
    signalling formulas of a well-defined form.
    """

    def __init__(self, uid: _uid.FlexibleUniqueIdentifier,
                 validation_function: typing.Callable,
                 ensurance_function: typing.Callable,
                 well_formed_formula_python_type: type,
                 syntactic_rules=_fml.SyntacticRules(),
                 connector_representation: _rpr.AbstractRepresentation | None = None,
                 formula_representation: _rpr.AbstractRepresentation | None = None
                 ):
        self._validation_function: typing.Callable = validation_function
        self._ensurance_function: typing.Callable = ensurance_function
        self._well_formed_formula_python_type: type = well_formed_formula_python_type
        super().__init__(uid=uid,
                         syntactic_rules=syntactic_rules,
                         connector_representation=connector_representation,
                         formula_representation=formula_representation)

    def validate_formula_well_formedness(self,
                                         formula: _fml.Formula, raise_error_if_false: bool = False,
                                         return_typed_arguments: bool = False
                                         ) -> bool:
        """Returns :obj:`True` if :paramref:`formula` is well-formed
        for the formula structure expected by this connector."""
        return self._validation_function(formula, raise_error_if_false=raise_error_if_false,
                                         return_typed_arguments=return_typed_arguments)

    def ensure_well_formed_formula(self, formula: _fml.Formula) -> WellFormedFormula:
        """Given a presumably well-formed :paramref:`formula`,
        returns a strongly typed WellFormedFormula of the `well_formed_formula_python_type`."""
        return self._ensurance_function(formula)

    @property
    def well_formed_formula_python_type(self) -> type:
        """The `well_formed_formula_python_type` of the connector is a Python type that enforces well-formedness."""
        return self._well_formed_formula_python_type


class WellFormedFormula(_fml.Formula):
    """A `WellFormedFormula` is a formula that is well-formed
    according to some definition.
    """

    def __init__(self, connector: WellFormedFormulaConnector, arguments=None):
        """

        :param connector: A connector.
        :param arguments: A (possibly empty) collection of arguments.
        """
        super().__init__(connector=connector, arguments=arguments)

    def __new__(cls, connector: WellFormedFormulaConnector, arguments=None):
        connector: WellFormedFormulaConnector = ensure_well_formed_formula_connector(connector)
        arguments: _fml.FormulaArguments = _fml.ensure_formula_arguments(arguments)
        # Declares a raw formula to check its well-formedness.
        raw_formula: _fml.Formula = _fml.Formula(connector=connector, arguments=arguments)
        # Validates the well-formedness of the raw-formula.
        arguments: _fml.FormulaArguments
        _, arguments = connector.validate_formula_well_formedness(
            formula=raw_formula, raise_error_if_false=True, return_typed_arguments=True)
        return super().__new__(cls, connector=connector, arguments=arguments)

    @property
    def connector(self) -> WellFormedFormulaConnector:
        return typing.cast(WellFormedFormulaConnector, super().connector)

    def ensure_formula_well_formed_type(self, formula: _fml.Formula) -> _fml.Formula:
        """Given a :paramref:`formula`
        presumably well-formed for the formula structure expected by this connector,
        returns a formula object of the `well_formed_type`."""
        return self.ensure_formula_well_formed_type(formula)

    def validate_formula_well_formedness(self, formula: _fml.Formula,
                                         raise_error_if_false: bool = False,
                                         return_typed_arguments: bool = False) -> bool:
        """Returns :obj:`True` if :paramref:`formula` is well-formed
        for the formula structure expected by this connector."""
        return self.connector.validate_formula_well_formedness(
            formula, raise_error_if_false=raise_error_if_false, return_typed_arguments=return_typed_arguments)

    @property
    def well_formed_formula_python_type(self) -> type:
        """The `well_formed_python_type` of the connector is a Python type that enforces well-formedness."""
        return self.connector.well_formed_formula_python_type


class WellFormedTheoryComponent(WellFormedFormula, abc.ABC):
    """A :class:`WellFormedTheoryComponent` is a :class:`WellFormedFormula` that is an element of a :class:`Theory`.
    3 categories of :class:`WellFormedTheoryComponent` are well-known and implemented:
    - :class:`Axiom`.
    - :class:`InferenceRule`.
    - :class:`DerivationStep`.

    """

    def __init__(self, connector: WellFormedFormulaConnector, arguments=None):
        super().__init__(connector=connector, arguments=arguments)

    def __new__(cls, connector: WellFormedFormulaConnector, arguments=None):
        return super().__new__(cls, connector=connector, arguments=arguments)


class WellFormedAssertion(WellFormedTheoryComponent, abc.ABC):
    """An :class:`WellFormedAssertion` is a model of a mathematical theory assertion, i.e.: an axiom or a theorem.

    2 categories of :class:`WellFormedAssertion` are well-known and implemented:
    - :class:`WellFormedAxiom`.
    - :class:`WellFormedTheorem`.

    """

    def __init__(self, connector: WellFormedFormulaConnector, arguments=None):
        super().__init__(connector=connector, arguments=arguments)

    def __new__(cls, connector: WellFormedFormulaConnector, arguments=None):
        return super().__new__(cls, connector=connector, arguments=arguments)

    @property
    @abc.abstractmethod
    def valid_statement(self) -> _fml.Formula:
        """The valid statement that is asserted.

        :return: A formula.
        """
        raise _utl.PunctiliousError(
            title='Abstract method not implemented',
            details='Python object `o` inherits from abstract class `WellFormedAssertion`,'
                    ' but method `valid_statement` is not implemented.',
            o=self)


class WellFormedInferenceRule(WellFormedTheoryComponent, abc.ABC):
    """

    """

    def __init__(self, connector: WellFormedFormulaConnector, arguments=None):
        super().__init__(connector=connector, arguments=arguments)

    def __new__(cls, connector: WellFormedFormulaConnector, arguments=None):
        return super().__new__(cls, connector=connector, arguments=arguments)

    @abc.abstractmethod
    def apply_rule(self, inputs: typing.Iterable[_fml.Formula]) -> _fml.Formula:
        raise _utl.PunctiliousError(
            title='Abstract method not implemented',
            details='Python object `o` inherits from abstract class `WellFormedInferenceRule`,'
                    ' but method `apply_rule` is not implemented.',
            o=self)


class WellFormedTheory(WellFormedFormula):

    def __init__(self, *theory_components,
                 duplicate_processing: _cst.ExtraneousElementOptions = _cst.ExtraneousElementOptions.RAISE_ERROR):
        global theory_connector
        super().__init__(connector=theory_connector, arguments=theory_components)

    def __new__(cls, *theory_components,
                duplicate_processing: _cst.ExtraneousElementOptions = _cst.ExtraneousElementOptions.RAISE_ERROR):
        global theory_connector
        # Strip duplicates if required, before well-formedness validation.
        if duplicate_processing == _cst.ExtraneousElementOptions.STRIP:
            theory_components = _fml.ensure_unique_formulas(*theory_components,
                                                            duplicate_processing=duplicate_processing)
        return super().__new__(cls, connector=theory_connector, arguments=theory_components)

    @property
    def theory_components(self) -> collections.abc.Iterable[WellFormedTheoryComponent]:
        return (typing.cast(theory_component, WellFormedTheoryComponent) for theory_component in self.arguments)

    def has_top_level_theory_component(self, theory_component: _fml.Formula) -> bool:
        """Returns :obj:`True` if `theory_component` is a theory-component of this theory."""
        return self.has_top_level_argument(argument=theory_component)

    def is_theory_equivalent_to(self, other: FlexibleUniqueExtensionTuple) -> bool:
        """Returns :obj:`True` if this set is equal to the `other` set."""
        raise NotImplementedError('oops')

    def to_well_formed_extension_tuple(self) -> WellFormedExtensionTuple:
        """Returns an ExtensionTuple with the same elements, preserving order."""
        return WellFormedExtensionTuple(*self.theory_components)

    def to_well_formed_unique_extension_tuple(self) -> WellFormedUniqueExtensionTuple:
        """Returns an UniqueExtensionTuple with the same elements, preserving order."""
        return WellFormedUniqueExtensionTuple(*self.theory_components)


class WellFormedAxiom(WellFormedAssertion):
    """A :class:`WellFormedAxiom` is a model of a mathematical axiom.

    Form
    ------------
    A :class:`WellFormedAxiom` is a formula of the form:

    .. math::

        \mathrm{axiom}(\phi)

    where:
      - :math:`\mathrm{axiom}` is the well-known :obj:`axiom_connector`.
      - :math:`\phi` is a formula denoted as the valid statement asserted by the axiom.

    """

    def __init__(self, valid_statement: _fml.Formula):
        global axiom_connector
        super().__init__(connector=axiom_connector, arguments=(valid_statement,))

    def __new__(cls, valid_statement: _fml.Formula):
        global axiom_connector
        return super().__new__(cls, connector=axiom_connector, arguments=(valid_statement,))

    @property
    def valid_statement(self) -> _fml.Formula:
        return self.arguments[_cst.AXIOM_VALID_STATEMENT_INDEX]


class WellFormedExtensionTuple(WellFormedFormula):
    """A :class:`WellFormedExtensionTuple` is a model of a mathematical tuple,
    with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.

    Form
    ------------
    A :class:`WellFormedExtensionTuple` is a formula of the well-defined form:

    .. math::

        \mathrm{extension-tuple}(\phi_1, \phi_2, \ldots, \phi_n)

    where:
      - :math:`\mathrm{extension-tuple}` is the well-known :obj:`extension_tuple_connector`.
      - :math:`\phi_i` are some (possibly no) formulas, denoted as the elements of the tuple.

    """

    def __init__(self, *arguments):
        global extension_tuple_connector
        super().__init__(connector=extension_tuple_connector, arguments=arguments)

    def __new__(cls, *arguments):
        global extension_tuple_connector
        return super().__new__(cls, connector=extension_tuple_connector, arguments=arguments)

    @property
    def arity(self) -> int:
        return super().arity

    @property
    def elements(self) -> collections.abc.Iterable[_fml.Formula]:
        return (element for element in self.arguments)

    def has_top_level_element(self, element: _fml.Formula) -> bool:
        """Returns :obj:`True` if `element` is an element of the tuple, :obj:`False` otherwise.

        Note that `element` may be multiple times an element of the tuple."""
        return self.has_top_level_argument(argument=element)

    @property
    def has_unique_elements(self) -> bool:
        """Returns :obj:`True` if all the elements of this ExtensionTuple are unique, :obj:`False` otherwise."""
        return self.has_unique_arguments

    def is_tuple_equivalent_to(self, other: WellFormedExtensionTuple) -> bool:
        """Returns :obj:`True` if this tuple is equal to the `other` tuple, :obj:`False` otherwise.

        This is equivalent to formula-equivalence."""
        return self.is_formula_equivalent(other_formula=other)

    def to_unique_extension_tuple(self, duplicate_processing: _cst.ExtraneousElementOptions =
    _cst.ExtraneousElementOptions.RAISE_ERROR) -> WellFormedUniqueExtensionTuple:
        if duplicate_processing == _cst.ExtraneousElementOptions.RAISE_ERROR and not self.has_unique_arguments:
            raise ValueError(f'All the elements of this `ExtensionTuple` are not unique: {self}')
        return WellFormedUniqueExtensionTuple(self.elements, duplicate_processing=duplicate_processing)


class WellFormedUniqueExtensionTuple(WellFormedFormula):
    """A UniqueTuple is a model of a pseudo-set from set theory with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension,
     - its elements are ordered but unique-tuple-equivalence makes it possible to compare
       UniqueTuples without taking order in consideration.
     - its elements are unique, i.e. there exists no pair (x, y) of elements such that
       x ~formula y.

    It is implemented as a formula with a well-known `unique_tuple` connector,
    whose arguments are denoted as the elements of the UniqueExtensionTuple,
    and for which no two arguments are formula-equivalent to each other.

    UniqueTuple supports the is_unique_extension_tuple_equivalent method that,
    contrary to formulas and tuples, does not take into account
    the order of the arguments.
    """

    def __init__(self, *arguments,
                 duplicate_processing: _cst.ExtraneousElementOptions =
                 _cst.ExtraneousElementOptions.RAISE_ERROR):
        global unique_extension_tuple_connector
        super().__init__(connector=unique_extension_tuple_connector, arguments=arguments)

    def __new__(cls, *arguments,
                duplicate_processing: _cst.ExtraneousElementOptions =
                _cst.ExtraneousElementOptions.RAISE_ERROR):
        global unique_extension_tuple_connector
        # Strip duplicates if required, before well-formedness validation.
        if duplicate_processing == _cst.ExtraneousElementOptions.STRIP:
            arguments = _fml.ensure_unique_formulas(*arguments, duplicate_processing=duplicate_processing)
        return super().__new__(cls, connector=unique_extension_tuple_connector, arguments=arguments)

    @property
    def arity(self) -> int:
        """Returns the number of elements in this unique-extension-tuple."""
        return super().arity

    @property
    def elements(self) -> collections.abc.Iterable[_fml.Formula]:
        return (element for element in self.arguments)

    def has_top_level_element(self, element: _fml.Formula) -> bool:
        """Returns :obj:`True` if `element` is an element of the tuple."""
        return self.has_top_level_argument(argument=element)

    def is_well_formed_unique_extension_tuple_equivalent_to(self, other: FlexibleUniqueExtensionTuple) -> bool:
        """Returns :obj:`True` if this set is equal to the `other` set."""
        other = ensure_well_formed_unique_extension_tuple(other)

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

    def to_well_formed_extension_tuple(self) -> WellFormedExtensionTuple:
        """Returns an ExtensionTuple with the same elements, preserving order."""
        return WellFormedExtensionTuple(*self.elements)


def ensure_well_formed_extension_tuple(formula: _fml.Formula) -> WellFormedExtensionTuple:
    """Ensures that :paramref:`formula` is a well-formed extension-tuple, raises an exception otherwise.

    :param formula: A formula.
    :return: A strongly-typed well-formed extension-tuple.
    """
    global extension_tuple_connector
    formula: _fml.Formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedExtensionTuple):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == extension_tuple_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedExtensionTuple(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed extension-tuple',
                                    details=f'`formula` is not a well-formed extension-tuple.',
                                    formula=formula)


def ensure_well_formed_unique_extension_tuple(
        formula: _fml.Formula,
        duplicate_processing: _cst.ExtraneousElementOptions = _cst.ExtraneousElementOptions.RAISE_ERROR) -> WellFormedUniqueExtensionTuple:
    """Ensures that :paramref:`formula` is a well-formed extension-tuple, raises an exception otherwise.

    :param formula: A formula.
    :param duplicate_processing: Instructions on how duplicates are processed.
    :return: A well-formed extension-tuple, strongly typed as :class:`WellFormedUniqueExtensionTuple`.
    """
    global unique_extension_tuple_connector
    formula: _fml.Formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedUniqueExtensionTuple):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == unique_extension_tuple_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedUniqueExtensionTuple(*formula.arguments, duplicate_processing=duplicate_processing)
    else:
        raise _utl.PunctiliousError(title='Ill-formed unique-extension-tuple',
                                    details=f'`formula` is not a well-formed unique-extension-tuple.',
                                    formula=formula)


def ensure_extension_map(o: FlexibleExtensionTuple) -> WellFormedExtensionMap:
    """Ensures that the input is an extension-map, and returns an instance of ExtensionMap.

    :param o:
    :return:
    """
    if isinstance(o, WellFormedExtensionMap):
        return o
    if isinstance(o, _fml.Formula) and o.connector == extension_map_connector:
        return WellFormedExtensionMap(*o.arguments)
    raise _utl.PunctiliousError(f'`o` is not an extension-tuple.', o=o)


def ensure_well_formed_natural_inference_rule(formula: _fml.Formula) -> WellFormedNaturalInferenceRule:
    """Ensures that :paramref:`formula` is a well-formed natural inference rule, raises an exception otherwise.

    :param formula: A formula.
    :return: A strongly-typed well-formed natural-inference-rule.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedNaturalInferenceRule):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == axiom_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedNaturalInferenceRule(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed natural inference rule',
                                    details=f'`formula` is not a well-formed natural inference rule.',
                                    formula=formula)


def ensure_well_formed_natural_inference_rules(o: typing.Iterable[FlexibleNaturalInferenceRule]) -> typing.Generator[
    WellFormedNaturalInferenceRule, None, None]:
    for i in o:
        yield ensure_well_formed_natural_inference_rule(i)


def ensure_theory_component(o: FlexibleTheoryComponent) -> WellFormedTheoryComponent:
    """Ensures that `o` is a theory-component.

    :param o:
    :return:
    """
    if isinstance(o, WellFormedTheoryComponent):
        return o
    if isinstance(o, _fml.Formula) and o.connector == natural_inference_rule_connector:
        return WellFormedNaturalInferenceRule(*o.arguments)
    raise _utl.PunctiliousError(title='Inconsistent theory component.',
                                details=f'`o` cannot be interpreted as an ITheoryComponent.',
                                o=o)


def ensure_well_formed_formula_connector(o: object) -> WellFormedFormulaConnector:
    if isinstance(o, WellFormedFormulaConnector):
        return o
    else:
        raise _utl.PunctiliousError(
            title='Invalid type.',
            details=f'`o` cannot be interpreted as a WellFormedFormulaConnector.',
            o=o)


def ensure_theory_components(o: typing.Iterable[FlexibleTheoryComponent]) -> typing.Generator[
    WellFormedTheoryComponent, None, None]:
    for x in o:
        yield ensure_theory_component(x)


def ensure_inference_step(o: FlexibleTheorem):
    """Ensures that the input is an inference-step, and returns an instance of InferenceStep.

    :param o:
    :return:
    """
    if isinstance(o, WellFormedTheorem):
        return o
    if isinstance(o, _fml.Formula) and o.connector == theorem_connector:
        return WellFormedTheorem(*o.arguments)
    raise _utl.PunctiliousError(f'`o` is not an inference-step.', o=o)


def ensure_well_formed_theory(formula: _fml.Formula) -> WellFormedTheory:
    """Ensures that :paramref:`formula` is a well-formed theory, raises an exception otherwise.

        :param formula: A formula.
        :return: A strongly-typed well-formed theory.
        """
    global theory_connector
    formula: _fml.Formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedTheory):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == theory_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedTheory(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed theory',
                                    details=f'`formula` is not a well-formed theory.',
                                    formula=formula)


def ensure_well_formed_axiom(formula: _fml.Formula) -> WellFormedAxiom:
    """Ensures that :paramref:`formula` is a well-formed axiom, raises an exception otherwise.

    :param formula: A formula.
    :return: A strongly-typed well-formed axiom.
    """
    global axiom_connector
    formula: _fml.Formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedAxiom):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == axiom_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedAxiom(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed axiom',
                                    details=f'`formula` is not a well-formed axiom.',
                                    formula=formula)


def ensure_well_formed_theorem(formula: _fml.Formula) -> WellFormedTheorem:
    """Ensures that :paramref:`formula` is a well-formed theorem, raises an exception otherwise.

    :param formula: A formula.
    :return: A strongly-typed well-formed theorem.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedTheorem):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == theorem_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedTheorem(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed theorem',
                                    details=f'`formula` is not a well-formed theorem.',
                                    formula=formula)


def ensure_well_formed_extension_map(formula: _fml.Formula) -> WellFormedExtensionMap:
    """Ensures that :paramref:`formula` is a well-formed extension-map, raises an exception otherwise.

    :param formula: A formula.
    :return: A strongly-typed well-formed extension-map.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedExtensionMap):
        # The type ensures well-formedness.
        return formula
    elif isinstance(formula, _fml.Formula) and formula.connector == extension_map_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        return WellFormedExtensionMap(*formula.arguments)
    else:
        raise _utl.PunctiliousError(title='Ill-formed extension-map',
                                    details=f'`formula` is not a well-formed extension-map.',
                                    formula=formula)


def ensure_well_formed_inference_rule(formula: _fml.Formula):
    """Ensures that :paramref:`formula` is a well-formed inference-rule, raises an exception otherwise.

    Note
    _____

    :class:`WellFormedInferenceRule` is an abstract Python class. Therefore, it is necessary
        to maintain this function to support all concrete Python classes implementing
        :class:`WellFormedInferenceRule`.

    :param formula: A formula.
    :return: A strongly-typed well-formed inference-rule.
    """
    formula: _fml.Formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedInferenceRule):
        # The type ensures well-formedness.
        return formula
    if isinstance(formula, _fml.Formula) and formula.connector == natural_inference_rule_connector:
        # The WellFormedFormula parent class initializer ensures well-formedness.
        # Well-known WellFormedInferenceRule Python subclass: WellFormedNaturalInferenceRule.
        formula: WellFormedNaturalInferenceRule = ensure_well_formed_natural_inference_rule(formula)
        return formula
    # CODE MAINTENANCE: Insert here explicit support for other WellFormedInferenceRule Python subclasses.
    if isinstance(formula, _fml.Formula):
        # The WellFormedFormula parent class initializer ensures well-formedness.
        # Potentially unknown WellFormedInferenceRule Python subclass.
        formula: WellFormedFormula = ensure_well_formed_formula(formula)
        if isinstance(formula, WellFormedInferenceRule):
            return formula
    # No solution found.
    raise _utl.PunctiliousError(title='Ill-formed inference rule',
                                details=f'`formula` is not a well-formed inference-rule.',
                                formula=formula)


def ensure_well_formed_formula(formula: _fml.Formula) -> WellFormedFormula:
    """Ensures that :paramref:`formula` is a well-formed formula, raises an exception otherwise.

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
    if isinstance(formula, _fml.Formula):
        if isinstance(formula.connector, WellFormedFormulaConnector):
            connector: WellFormedFormulaConnector = typing.cast(WellFormedFormulaConnector, formula.connector)
            return connector.ensure_well_formed_formula(formula=formula)
    raise _utl.PunctiliousError(title='Ill-formed formula',
                                details=f'`formula` could not be automatically interpreted as a well-formed formula.',
                                formula=formula)


def union_unique_tuples(*args: WellFormedUniqueExtensionTuple):
    """Returns the union of UniqueTuple provided. Strip any duplicate in the process."""
    args = tuple(
        ensure_well_formed_unique_extension_tuple(formula=s,
                                                  duplicate_processing=_cst.ExtraneousElementOptions.RAISE_ERROR)
        for s
        in args)
    flattened = tuple(element for sub_tuple in args for element in sub_tuple.elements)
    output = WellFormedUniqueExtensionTuple(*flattened, duplicate_processing=_cst.ExtraneousElementOptions.STRIP)
    return output


class WellFormedExtensionMap(WellFormedFormula):
    """A :class:`WellFormedExtensionMap` is a model of a mathematical map with the following constraints:
     - it is finite,
     - it is computable,
     - it is defined by extension.

    Form
    ------------
    A :class:`WellFormedExtensionMap` is a formula of the form:

    .. math::

        \mathrm{extension-map}( ⟨ \phi_1, \phi_2, \ldots, \phi_n ⟩, ( \psi_1, \psi_2, \ldots, \psi_n ) )

    where:
      - :math:`\mathrm{extension-map}` is the well-known :obj:`extension_map_connector`.
      - :math:`⟨ \phi_1, \phi_2, \ldots, \phi_n ⟩` is a unique-extension-tuple of zero or more formulas
        denoted as the domain of the extension-map.
      - :math:`( \psi_1, \psi_2, \ldots, \psi_n )` is an extension-tuple of zero or more formulas
        denoted as the codomain of the extension-map.
      - the arities of the domain and codomain are equal.

    Note
    ------------
    A :class:`WellFormedExtensionMap` supports the :meth:`WellFormedExtensionMap.get_image` method that,
     given an element of the domain, returns the corresponding element of the codomain,
     that is the element at the same position.
     This leverages the fact that :class:`WellFormedUniqueExtensionTuple` contains unique elements.
    """

    def __init__(self, domain: WellFormedUniqueExtensionTuple, codomain: WellFormedExtensionTuple):
        if domain.arity != codomain.arity:
            raise _utl.PunctiliousError(f'The arity of the `domain` is not equal to the arity of the `codomain`.',
                                        domain_arity=domain.arity, codomain_arity=codomain.arity,
                                        domain=domain, codomain=codomain)
        super().__init__(connector=extension_map_connector, arguments=(domain, codomain,))

    def __new__(cls, domain: WellFormedUniqueExtensionTuple, codomain: WellFormedExtensionTuple):
        return super().__new__(cls, connector=extension_map_connector, arguments=(domain, codomain,))

    @property
    def codomain(self) -> WellFormedExtensionTuple:
        return ensure_well_formed_extension_tuple(self.arguments[_cst.EXTENSION_MAP_CODOMAIN_INDEX])

    @property
    def domain(self) -> WellFormedUniqueExtensionTuple:
        return ensure_well_formed_unique_extension_tuple(
            self.arguments[_cst.EXTENSION_MAP_DOMAIN_INDEX])

    def get_image(self, x: _fml.Formula) -> _fml.Formula:
        if not self.domain.has_top_level_element(element=x):
            raise _utl.PunctiliousError(
                title='Map domain error',
                details=f'`x` is not an element of the `domain` of map `m`.',
                x=x,
                domain=self.domain,
                m=self)
        i: int = self.domain.get_argument_first_index(argument=x)
        return self.codomain.arguments[i]

    def invert(self) -> WellFormedExtensionMap:
        """Returns the inverse map.

        Given a map `m(domain, codomain)`, the inverse map is `m(codomain, domain)`.

        If all elements of the map codomain are not unique, raises a `ValueError`.

        :return:
        """
        if not self.is_invertible:
            raise ValueError(f'This ExtensionMap is not invertible: {self}')
        new_domain = WellFormedUniqueExtensionTuple(*self.codomain.elements)
        new_codomain = WellFormedExtensionTuple(*self.domain.elements)
        return WellFormedExtensionMap(domain=new_domain, codomain=new_codomain)

    def is_invertible(self) -> bool:
        """Returns :obj:`True` if the ExtensionMap can be inverted,
        that is its codomain is made of unique formulas
        such that we can create an ExtensionMap with switched domain and codomain."""
        return self.codomain.has_unique_arguments

    def is_map_equivalent(self, other: WellFormedExtensionMap):
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


def substitute_formulas(phi: _fml.Formula, m: WellFormedExtensionMap,
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
                                         variables: WellFormedUniqueExtensionTuple) -> [bool, WellFormedExtensionMap]:
    formula_without_variables = _fml.ensure_formula(formula_without_variables)
    formula_with_variables = _fml.ensure_formula(formula_with_variables)
    variables = ensure_well_formed_unique_extension_tuple(variables)
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
    domain = WellFormedUniqueExtensionTuple(*keys)
    codomain = WellFormedExtensionTuple(*values)
    m2 = WellFormedExtensionMap(domain=domain, codomain=codomain)

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


class WellFormedNaturalInferenceRule(WellFormedInferenceRule):

    def __init__(self, variables: WellFormedUniqueExtensionTuple, premises: WellFormedUniqueExtensionTuple,
                 conclusion: _fml.Formula):
        """
        :param variables: the variables.
        :param premises: the premises.
        :param conclusion: the conclusion.
        """
        variables: WellFormedUniqueExtensionTuple = ensure_well_formed_unique_extension_tuple(variables)
        premises: WellFormedUniqueExtensionTuple = ensure_well_formed_unique_extension_tuple(premises)
        conclusion: _fml.Formula = _fml.ensure_formula(conclusion)
        super().__init__(connector=natural_inference_rule_connector, arguments=(variables, premises,
                                                                                conclusion,))

    def __new__(cls, variables: WellFormedUniqueExtensionTuple, premises: WellFormedUniqueExtensionTuple,
                conclusion: _fml.Formula):
        return super().__new__(cls, connector=natural_inference_rule_connector,
                               arguments=(variables, premises,
                                          conclusion,))

    def _check_arguments_validity(self, inputs: WellFormedExtensionTuple, raise_error_if_false: bool = False) -> [bool,
                                                                                                                  WellFormedExtensionTuple | None,
                                                                                                                  WellFormedExtensionMap | None]:
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
        premises_as_extension_tuple: WellFormedExtensionTuple = self.premises.to_well_formed_extension_tuple()

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
        return self.arguments[_cst.NATURAL_INFERENCE_RULE_CONCLUSION_INDEX]

    @property
    def premises(self) -> WellFormedUniqueExtensionTuple:
        return ensure_well_formed_unique_extension_tuple(
            self.arguments[_cst.NATURAL_INFERENCE_RULE_PREMISES_INDEX])

    @property
    def variables(self) -> WellFormedUniqueExtensionTuple:
        return ensure_well_formed_unique_extension_tuple(
            self.arguments[_cst.NATURAL_INFERENCE_RULE_VARIABLES_INDEX])

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

    def check_arguments_validity(self, arguments: WellFormedExtensionTuple) -> bool:
        """Returns :obj:`True` if `arguments` are valid for this InferenceRule."""
        check, _, _ = self._check_arguments_validity(inputs=arguments)
        return check


class WellFormedTheorem(WellFormedAssertion):

    def __init__(self, inputs: FlexibleExtensionTuple,
                 inference_rule: FlexibleNaturalInferenceRule, valid_statement: _fml.Formula):
        global theorem_connector
        super().__init__(connector=theorem_connector, arguments=(valid_statement, inputs, inference_rule,))

    def __new__(cls, inputs: FlexibleExtensionTuple,
                inference_rule: FlexibleNaturalInferenceRule, valid_statement: _fml.Formula | None,
                ):
        global theorem_connector
        if valid_statement is None:
            # If the `valid_statement` is not provided, computes it.
            inference_rule: WellFormedNaturalInferenceRule = ensure_well_formed_natural_inference_rule(inference_rule)
            valid_statement: _fml.Formula = inference_rule.apply_rule(inputs)
        # Reminder: the consistency of `valid_statement` is always checked
        # by the :class:`WellFormedFormula` parent class.
        return super().__new__(cls, connector=theorem_connector, arguments=(valid_statement, inputs, inference_rule,))

    @property
    def inputs(self) -> WellFormedExtensionTuple:
        return ensure_well_formed_extension_tuple(self.arguments[_cst.THEOREM_INPUTS_INDEX])

    @property
    def inference_rule(self) -> WellFormedNaturalInferenceRule:
        return ensure_well_formed_natural_inference_rule(
            self.arguments[_cst.THEOREM_INFERENCE_RULE_INDEX])

    @property
    def valid_statement(self) -> _fml.Formula:
        return _fml.ensure_formula(self.arguments[_cst.THEOREM_STATEMENT_INDEX])


class Theory(WellFormedFormula):

    def __init__(self, *components: tuple[_fml.Formula] | typing.Iterable[_fml.Formula]):
        super().__init__(connector=theory_connector, arguments=components)

    def __new__(cls, *components: tuple[WellFormedTheoryComponent]):
        return super().__new__(cls, connector=theory_connector, arguments=components)

    @property
    def components(self):
        return self.arguments


def iterate_valid_statements(axioms: typing.Iterable[_fml.Formula],
                             inference_steps: typing.Iterable[WellFormedTheorem]) -> \
        typing.Generator[_fml.Formula, None, None]:
    """Given the components of a theory, that is a collection of axioms and a collection of inference_steps,
    yield all the valid statements."""
    for a in axioms:
        yield a
    for step in inference_steps:
        yield step.valid_statement


def ensure_theory(o) -> Theory:
    if isinstance(o, Theory):
        return o
    if isinstance(o, _fml.Formula) and o.connector == theory_connector:
        return Theory(*o.arguments)
    raise _utl.PunctiliousError(title='Inconsistent theory.',
                                details=f'`o` cannot be interpreted as a theory.',
                                o=o)


def is_valid_statement(statement: _fml.Formula, theory_components: typing.Iterable[WellFormedTheoryComponent]) -> bool:
    """Returns :obj:`True` if `statement` is valid given a collection of `theory_components`, :obj:`False` otherwise.

    Note 1:
    A statement is valid given a collection of theory components if and only if
    the statement is formula-equivalent to the statement claimed by at least
    one theory component.

    """
    statement: _fml.Formula = _fml.ensure_formula(statement)
    for theory_component in theory_components:
        theory_component: WellFormedTheoryComponent = ensure_theory_component(theory_component)
        if isinstance(theory_component, WellFormedAssertion):
            theory_statement: WellFormedAssertion = theory_component
            if statement.is_formula_equivalent(theory_statement.valid_statement):
                return True
    return False


FlexibleAxiom = typing.Union[WellFormedAxiom, _fml.Formula]
FlexibleStatement = typing.Union[WellFormedAssertion, _fml.Formula]
FlexibleExtensionMap = typing.Union[WellFormedExtensionMap, _fml.Formula]
FlexibleExtensionTuple = typing.Union[WellFormedExtensionTuple, _fml.Formula, collections.abc.Iterable]
FlexibleNaturalInferenceRule = typing.Union[WellFormedExtensionTuple, _fml.Formula]
FlexibleTheorem = typing.Union[WellFormedTheorem, _fml.Formula]
FlexibleUniqueExtensionTuple = typing.Union[WellFormedUniqueExtensionTuple, _fml.Formula, collections.abc.Iterable]
FlexibleTheory = typing.Union[Theory, _fml.Formula]
FlexibleTheoryComponent = typing.Union[_fml.Formula]


def is_well_formed_theory(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed theory, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If `:obj:`True`, returns a tuple (bool, FormulaArguments) where arguments are
        typed as :class:`WellFormedFormula` if applicable.
    :return: :obj:`True` if :paramref:`formula` is a well-formed unique-extension-tuple, :obj:`False` otherwise.
    """
    global theory_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedTheory):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != theory_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed theory',
                details='`formula` is not a well-formed theory,'
                        ' because its `root_connector` is not the well-known `theory_connector`.',
                formula=formula,
                root_connector=formula.connector,
                theory_connector=theory_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    # Ensures the uniqueness of theory components.
    formulas_are_unique: bool = _fml.formulas_are_unique(*formula.arguments, raise_error_if_false=raise_error_if_false)
    if not formulas_are_unique:
        if return_typed_arguments:
            return False, None
        else:
            return False
    # Declare an empty list to populate the validated arguments.
    typed_theory_components: list[WellFormedTheoryComponent] = list()
    for argument in formula.arguments:
        # Ensures the argument is a well-formed formula.
        if not is_well_formed_formula(argument):
            if raise_error_if_false:
                raise _utl.PunctiliousError(
                    title='Ill-formed theory',
                    details='`formula` is not a well-formed theory,'
                            ' because `argument` is not a well-formed formula.',
                    argument=argument,
                    formula=formula
                )
            if return_typed_arguments:
                return False, None
            else:
                return False
        well_formed_formula: WellFormedFormula = ensure_well_formed_formula(argument)
        # Ensures the well-formed formula is a theory-component.
        if not isinstance(well_formed_formula, WellFormedTheoryComponent):
            if raise_error_if_false:
                raise _utl.PunctiliousError(
                    title='Ill-formed theory',
                    details='`formula` is not a well-formed theory,'
                            ' because `argument` is not a well-formed theory-component.',
                    argument=argument,
                    formula=formula
                )
            if return_typed_arguments:
                return False, None
            else:
                return False
        # If the theory-component is a theorem,
        # ensures all of its inputs are antecedent valid-statements in the theory.
        if isinstance(well_formed_formula, WellFormedTheorem):
            for input in well_formed_formula.inputs:
                if not is_valid_statement(input, typed_theory_components):
                    if raise_error_if_false:
                        raise _utl.PunctiliousError(
                            title='Ill-formed theory',
                            details='`formula` is an ill-formed theory, '
                                    ' because an `input` of a `theorem` is not a valid-statement'
                                    ' in `predecessor-theory-components`.',
                            input=input,
                            theorem=well_formed_formula,
                            predecessor_theory_components=typed_theory_components,
                            formula=formula
                        )
                    if return_typed_arguments:
                        return False, None
                    else:
                        return False
        # Append the now validated theory component to the list
        typed_theory_components.append(well_formed_formula)
    # All theory components have been validated.
    if return_typed_arguments:
        return True, _fml.FormulaArguments(*typed_theory_components)
    else:
        return True


def is_well_formed_axiom(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed axiom, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If `:obj:`True`, returns a tuple (bool, FormulaArguments) where arguments are
        typed as WellFormedFormulas if applicable.
    :return: :class:`bool`: :obj:`True` if :paramref:`formula` is a well-formed axiom, :obj:`False` otherwise.
    """
    global axiom_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedAxiom):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != axiom_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed axiom',
                details='`formula` is not a well-formed axiom.'
                        'Its root connector is not the well-known `axiom_connector`.',
                formula=formula,
                axiom_connector=axiom_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if formula.arity != _cst.AXIOM_FIXED_ARITY:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed axiom',
                details=f'`formula` is not a well-formed axiom.'
                        f'Its arity is not equal `fixed_arity`.',
                formula=formula,
                fixed_arity=_cst.AXIOM_FIXED_ARITY
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    valid_statement: _fml.Formula = formula[_cst.AXIOM_VALID_STATEMENT_INDEX]
    if return_typed_arguments:
        return True, _fml.FormulaArguments(valid_statement)
    else:
        return True


def is_well_formed_formula(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-known well-formed formula, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If `:obj:`True`, returns a tuple (bool, FormulaArguments) where arguments are
        typed as WellFormedFormulas if applicable.
    :return: :class:`bool`: :obj:`True` if :paramref:`formula` is a well-formed formula, :obj:`False` otherwise.
    """
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedFormula):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if isinstance(formula.connector, WellFormedFormulaConnector):
        connector: WellFormedFormulaConnector = typing.cast(formula.connector, WellFormedFormulaConnector)
        check: bool
        arguments: _fml.FormulaArguments
        check, arguments = connector.validate_formula_well_formedness(formula, raise_error_if_false=False,
                                                                      return_typed_arguments=True)
        if check:
            if return_typed_arguments:
                return True, arguments
            else:
                return True
    # The formula could not be interpreted as a well-formed formula.
    if raise_error_if_false:
        raise _utl.PunctiliousError(
            title='Ill-formed axiom',
            details='`formula` is not a well-formed formula.',
            formula=formula
        )
    if return_typed_arguments:
        return False, None
    else:
        return False


def is_well_formed_extension_tuple(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed extension-tuple, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If `:obj:`True`, returns a tuple (bool, FormulaArguments) where arguments are
        typed as WellFormedFormulas if applicable.
    :return: :class:`bool`: :obj:`True` if :paramref:`formula` is a well-formed extension-tuple, :obj:`False` otherwise.
    """
    global extension_tuple_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedExtensionTuple):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != extension_tuple_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed extension-tuple',
                details='`formula` is not a well-formed extension-tuple.'
                        'Its root connector is not the well-known `extension_tuple_connector`.',
                formula=formula,
                extension_tuple_connector=extension_tuple_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if return_typed_arguments:
        return True, _fml.FormulaArguments(*formula.arguments)
    else:
        return True


def is_well_formed_unique_extension_tuple(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed unique-extension-tuple, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If `:obj:`True`, returns a tuple (bool, FormulaArguments) where arguments are
        typed as :class:`WellFormedFormula` if applicable.
    :return: :obj:`True` if :paramref:`formula` is a well-formed unique-extension-tuple, :obj:`False` otherwise.
    """
    global unique_extension_tuple_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedUniqueExtensionTuple):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != unique_extension_tuple_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed unique-extension-tuple',
                details='`formula` is not a well-formed unique-extension-tuple.'
                        'Its root connector is not the well-known `unique_extension_tuple_connector`.',
                formula=formula,
                unique_extension_tuple_connector=unique_extension_tuple_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    # Assures the uniqueness of elements.
    arguments: tuple[_fml.Formula, ...] = _fml.ensure_unique_formulas(
        *formula.arguments, duplicate_processing=_cst.ExtraneousElementOptions.RAISE_ERROR)
    if return_typed_arguments:
        return True, _fml.FormulaArguments(*arguments)
    else:
        return True


def is_well_formed_theorem(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False
) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed theorem, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If :obj:`True`, returns a tuple (bool, FormulaArguments|None)
        where arguments are properly typed as WellFormedFormulas as applicable.
    :return:
    """
    global theorem_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedTheorem):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != theorem_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed theorem',
                details='`formula` is not a well-formed theorem.'
                        ' Its root connector is not the well-known `theorem_connector`.',
                formula=formula,
                theorem_connector=theorem_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if formula.arity != _cst.THEOREM_FIXED_ARITY:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed theorem',
                details='`formula` is not a well-formed theorem.'
                        ' Its arity is not equal `fixed_arity`.',
                formula=formula,
                fixed_arity=_cst.THEOREM_FIXED_ARITY
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    statement: _fml.Formula = formula[_cst.THEOREM_STATEMENT_INDEX]
    inputs: WellFormedExtensionTuple = ensure_well_formed_extension_tuple(
        formula[_cst.THEOREM_INPUTS_INDEX])
    inference_rule: WellFormedInferenceRule = ensure_well_formed_inference_rule(
        formula[_cst.THEOREM_INFERENCE_RULE_INDEX])
    derived_statement: _fml.Formula = inference_rule.apply_rule(inputs)
    if not derived_statement.is_formula_equivalent(statement):
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed theorem',
                details='`formula` is not a well-formed theorem.'
                        ' Its claimed `statement` is not formula-equivalent'
                        ' to the `derived_statement`'
                        ' obtained by passing `inputs`'
                        ' to the `inference_rule`.',
                statement=statement,
                derived_statement=derived_statement,
                inputs=inputs,
                inference_rule=inference_rule,
                formula=formula
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if return_typed_arguments:
        return True, _fml.FormulaArguments(statement, inputs, inference_rule)
    else:
        return True


def is_well_formed_extension_map(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False
) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed extension-map, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If :obj:`True`, returns a tuple (bool, FormulaArguments|None)
        where arguments are properly typed as WellFormedFormulas as applicable.
    :return:
    """
    global extension_map_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedExtensionMap):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != extension_map_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed theorem',
                details='`formula` is not a well-formed extension-map.'
                        ' Its root connector is not the well-known `extension_map_connector`.',
                formula=formula,
                extension_map_connector=extension_map_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if formula.arity != _cst.EXTENSION_MAP_FIXED_ARITY:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed extension-map',
                details='`formula` is not a well-formed extension-map.'
                        ' Its arity is not equal `fixed_arity`.',
                formula=formula,
                fixed_arity=_cst.EXTENSION_MAP_FIXED_ARITY
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    domain: WellFormedUniqueExtensionTuple = ensure_well_formed_unique_extension_tuple(
        formula[_cst.EXTENSION_MAP_DOMAIN_INDEX])
    codomain: WellFormedExtensionTuple = ensure_well_formed_extension_tuple(
        formula[_cst.EXTENSION_MAP_CODOMAIN_INDEX])
    if domain.arity != codomain.arity:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed extension-map',
                details='The arity of the `domain`'
                        ' is not equal to the arity of the `codomain`.',
                domain_arity=domain.arity,
                codomain_arity=codomain.arity,
                domain=domain,
                codomain=codomain,
                formula=formula
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if return_typed_arguments:
        return True, _fml.FormulaArguments(domain, codomain)
    else:
        return True


def is_well_formed_natural_inference_rule(
        formula: _fml.Formula,
        raise_error_if_false: bool = False,
        return_typed_arguments: bool = False
) -> typing.Union[bool, tuple[bool, _fml.FormulaArguments | None]]:
    """Returns :obj:`True` if :paramref:`formula` is a well-formed natural inference rule, :obj:`False` otherwise.

    :param formula: A formula.
    :param raise_error_if_false: If :obj:`True`, raises an exception instead of returning :obj:`False`.
    :param return_typed_arguments: If :obj:`True`, returns a tuple (bool, FormulaArguments|None)
        where arguments are properly typed as WellFormedFormulas as applicable.
    :return:
    """
    global natural_inference_rule_connector
    formula = _fml.ensure_formula(formula)
    if isinstance(formula, WellFormedNaturalInferenceRule):
        # The type assure well-formedness and proper Python typing by design.
        if return_typed_arguments:
            return True, formula.arguments
        else:
            return True
    # For a raw formula, well-formedness and proper Python typing must be checked.
    if formula.connector != natural_inference_rule_connector:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed natural inference rule',
                details='`formula` is not a well-formed natural inference rule.'
                        ' Its root connector is not the well-known `natural_inference_rule_connector`.',
                formula=formula,
                natural_inference_rule_connector=natural_inference_rule_connector
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    if formula.arity != _cst.NATURAL_INFERENCE_RULE_FIXED_ARITY:
        if raise_error_if_false:
            raise _utl.PunctiliousError(
                title='Ill-formed natural inference rule',
                details='`formula` is not a well-formed natural inference rule.'
                        ' Its arity is not equal `fixed_arity`.',
                formula=formula,
                fixed_arity=_cst.NATURAL_INFERENCE_RULE_FIXED_ARITY
            )
        if return_typed_arguments:
            return False, None
        else:
            return False
    variables: WellFormedUniqueExtensionTuple = ensure_well_formed_unique_extension_tuple(
        formula[_cst.NATURAL_INFERENCE_RULE_VARIABLES_INDEX])
    premises: WellFormedUniqueExtensionTuple = ensure_well_formed_unique_extension_tuple(
        formula[_cst.NATURAL_INFERENCE_RULE_PREMISES_INDEX])
    conclusion = formula[_cst.NATURAL_INFERENCE_RULE_CONCLUSION_INDEX]
    if return_typed_arguments:
        return True, _fml.FormulaArguments(variables, premises, conclusion)
    else:
        return True


# well-known connectors
# the `tuple` connector is necessary to build complex formulas.
extension_tuple_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='extension_tuple', uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb'),
    validation_function=is_well_formed_extension_tuple,
    ensurance_function=ensure_well_formed_extension_tuple,
    well_formed_formula_python_type=WellFormedExtensionTuple)
"""The well-known extension-tuple connector.

See also
---------

- :class:`WellFormedExtensionTuple`
"""

unique_extension_tuple_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='unique_extension_tuple', uuid='8fd36cc9-8845-4cdf-ac24-1faf95ee44fc'),
    validation_function=is_well_formed_unique_extension_tuple,
    ensurance_function=ensure_well_formed_unique_extension_tuple,
    well_formed_formula_python_type=WellFormedUniqueExtensionTuple)
"""The well-known unique-extension-tuple connector.

See also
---------

- :class:`WellFormedUniqueExtensionTuple`
"""

extension_map_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='extension_map', uuid='2509dbf9-d636-431c-82d4-6d33b2de3bc4'),
    validation_function=is_well_formed_extension_map,
    ensurance_function=ensure_well_formed_extension_map,
    well_formed_formula_python_type=WellFormedExtensionMap)
"""The well-known extension-map connector.

See also
---------

- :class:`WellFormedExtensionMap`
"""

natural_inference_rule_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='natural_inference_rule', uuid='6f6c4c60-7129-4c60-801f-1454581f01fe'),
    validation_function=is_well_formed_natural_inference_rule,
    ensurance_function=ensure_well_formed_natural_inference_rule,
    well_formed_formula_python_type=WellFormedNaturalInferenceRule)
"""The well-known natural-inference-rule connector.

See also
---------

- :class:`WellFormedNaturalInferenceRule`
"""

theorem_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='theorem', uuid='b527b045-614b-49d6-95b3-9725f9143ba2'),
    validation_function=is_well_formed_theorem,
    ensurance_function=ensure_well_formed_theorem,
    well_formed_formula_python_type=WellFormedTheorem)
"""The well-known theorem meta-theory connector. 

See also
---------

- :class:`WellFormedTheorem`
"""

theory_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='theory', uuid='2724eebf-070d-459d-a097-de9889f118b9'),
    validation_function=is_well_formed_theory,
    ensurance_function=ensure_well_formed_theory,
    well_formed_formula_python_type=WellFormedTheory)
"""The well-known theory meta-theory connector.

See also
---------

- :class:`WellFormedTheory`
"""

axiom_connector = WellFormedFormulaConnector(
    uid=_uid.UniqueIdentifier(slug='axiom', uuid='0ead1815-8a20-4b02-bd06-1b5ae0295c92'),
    validation_function=is_well_formed_axiom,
    ensurance_function=ensure_well_formed_axiom,
    well_formed_formula_python_type=WellFormedAxiom)
"""The well-known axiom meta-theory connector.

See also
---------

- :class:`WellFormedAxiom`
"""

statement_connector = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='statement', uuid='254d104d-8746-415b-b146-279fcc7e037f'))
"""The well-known connector of the `Statement` object.
"""

true2 = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='true', uuid='dde98ed2-b7e0-44b2-bd10-5f59d61fd93e'))

false2 = _fml.Connector(
    uid=_uid.UniqueIdentifier(slug='false2', uuid='ffa97ce6-e320-4e5c-86c7-d7470c2d7c94'))


def declare_metavariable(variable_name: str | None = None) -> _fml.Connector:
    """Declares a variable for usage in a metalanguage."""
    if variable_name is None:
        variable_name = 'A'
    # if len(variable_name)
    return _fml.Connector(
        #    connector_representation=
        syntactic_rules=_fml.SyntacticRules(fixed_arity=0)
    )
