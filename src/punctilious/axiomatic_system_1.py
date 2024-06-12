from __future__ import annotations

import collections
import logging
import typing
import warnings
# import threading
import sys
# import random

import util_1 as u1
import state_1 as st1
import presentation_layer_1 as pl1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')
_state = dict() if not hasattr(_current_module, '_state') else getattr(_current_module, '_state')


def _set_state(key: str, value: object):
    """An internal utility function to store module state and avoid
    issues with global variables being re-instantiated if modules are re-loaded."""
    global _state
    if key in _state.items():
        value = _state.get(key)
    else:
        _state[key] = value
    return value


class EventType(str):
    pass


class EventTypes(typing.NamedTuple):
    error: EventType
    warning: EventType
    info: EventType
    debug: EventType


event_types: EventTypes = _set_state(key='event_types', value=EventTypes(
    error=EventType('error'),
    warning=EventType('warning'),
    info=EventType('info'),
    debug=EventType('debug')
))


class ErrorCode(typing.NamedTuple):
    event_type: EventType
    code: str
    message: str


class ErrorCodes(typing.NamedTuple):
    e100: ErrorCode
    e101: ErrorCode
    e102: ErrorCode
    e103: ErrorCode
    e104: ErrorCode
    e105: ErrorCode
    e106: ErrorCode
    e107: ErrorCode
    e108: ErrorCode
    e109: ErrorCode
    e110: ErrorCode
    e111: ErrorCode
    e112: ErrorCode
    e113: ErrorCode
    e114: ErrorCode
    e115: ErrorCode
    e116: ErrorCode
    e117: ErrorCode
    e118: ErrorCode
    e119: ErrorCode
    e120: ErrorCode
    e121: ErrorCode
    e122: ErrorCode
    e123: ErrorCode


error_codes: ErrorCodes = _set_state(key='event_codes', value=ErrorCodes(
    e100=ErrorCode(event_type=event_types.error, code='e100',
                   message='FormulaBuilder.__init__: Unsupported type for the terms argument.'),
    e101=ErrorCode(event_type=event_types.error, code='e101',
                   message='Formula.__new__: Unsupported type for the terms argument.'),
    e102=ErrorCode(event_type=event_types.error, code='e102',
                   message='Formula.term_0: Attempt to access property term_0 but formula does not contain a term at '
                           'index 0.'),
    e103=ErrorCode(event_type=event_types.error, code='e103',
                   message='Formula.term_1: Attempt to access property term_1 but formula does not contain a term at '
                           'index 0.'),
    e104=ErrorCode(event_type=event_types.warning, code='e104',
                   message='EnumerationBuilder.__init__: Attempt to add duplicate formula-equivalent formulas as '
                           'elements of the enumeration. The new element / term is ignored.'),
    e105=ErrorCode(event_type=event_types.error, code='e105',
                   message='During the initialization of a theorem (methods __init__ or __new__ of the Theorem class), '
                           'the well-formedness of the theorem is checked. One well-formedness rule is that applying '
                           'the transformation of the inference on the premises must effectively yield the claimed '
                           'valid-statement. Here, the claimed valid-statement is not formula-equivalent to the '
                           'algorithm output. In'
                           'consequence, the theorem would be ill-formed. The error parameter provides more detailed '
                           'information.'),
    e106=ErrorCode(event_type=event_types.warning, code='e106',
                   message='is_well_formed_theorem_by_inference: phi is an ill-formed theorem-by-inference because '
                           'psi_expected ~formula psi_inferred, '
                           'where psi_inferred = f(p), f the inference transformation, and p the inference premises.'),
    e107=ErrorCode(event_type=event_types.error, code='e107',
                   message='coerce_enumeration: The argument could not be coerced to a enumeration.'),
    e108=ErrorCode(event_type=event_types.error, code='e108',
                   message='Ill-formed formula: Formula phi is ill-formed, because of reason.'),
    e109=ErrorCode(event_type=event_types.error, code='e109',
                   message='get_index_of_first_term_in_formula: formula psi is not a term of formula phi.'),
    e110=ErrorCode(event_type=event_types.error, code='e110',
                   message='Enumeration.__new__: Attempt to create enumeration from invalid elements. Often this is '
                           'caused by a paid of elements that are formula-equivalent.'),
    e111=ErrorCode(event_type=event_types.error, code='e111',
                   message='While checking the well-formedness of a theory, a premise is necessary to derive a '
                           'theorem, but it is absent from the theory.'),
    e112=ErrorCode(event_type=event_types.error, code='e112',
                   message='While checking the well-formedness of a theory, a premise is necessary to derive a '
                           'theorem, but its position in the theory is posterior to the theorem.'),
    e113=ErrorCode(event_type=event_types.error, code='e113',
                   message='FormulaBuilder.to_formula: The connective property is None but it is mandatory to '
                           'elaborate formulas.'),
    e114=ErrorCode(event_type=event_types.error, code='e114',
                   message='EnumerationAccretor.__del_item__,pop,remove,remove_formula: The remove-formula operation '
                           'is forbidden on'
                           'enumeration-accretors.'),
    e115=ErrorCode(event_type=event_types.error, code='e115',
                   message='EnumerationAccretor.__set_item__: The set-element operation is forbidden on '
                           'enumeration-accretors.'),
    e116=ErrorCode(event_type=event_types.error, code='e116',
                   message='EnumerationAccretor.insert: The insert-element operation is forbidden on '
                           'enumeration-accretors.'),
    e117=ErrorCode(event_type=event_types.error, code='e117',
                   message='Before applying a transformation (method apply_transformation of the Transformation '
                           'class), the arguments passed to the transformation algorithm are verified to check that '
                           'they are formula-equivalent-with-variables with the premises of the transformation, '
                           'and with regards to the variables. The error parameter provides more detailed information '
                           'on the issue.'),
    e118=ErrorCode(event_type=event_types.error, code='e118',
                   message='is_formula_equivalent_with_variables: There exists a phi''sub-formula of phi that is an '
                           'element of variables.'),
    e119=ErrorCode(event_type=event_types.error, code='e119',
                   message='While checking the well-formedness of a theory, a transformation-rule is necessary '
                           'to derive a theorem, but it is absent from the theory.'),
    e120=ErrorCode(event_type=event_types.error, code='e120',
                   message='During the initialization of a theory (in the __new__ or __init__ methods of the '
                           'Derivation class), the well-formedness of the theory is verified. This '
                           'verification failed, in consequence the theory would be ill-formed. The error '
                           'parameter explains why.'),
    e121=ErrorCode(event_type=event_types.error, code='e121',
                   message='While checking if two formulas are formula-equivalent-with-variables, formulas are '
                           'automatically mapped to values. Of course, if a variable appears multiple times, '
                           'every instance must be mapped to the same value. Here, this verification failed. Some '
                           'variable was already mapped to a value, and then a distinct mapped value was found.'),
    e122=ErrorCode(event_type=event_types.error, code='e122',
                   message='While checking if two formulas are formula-equivalent, a difference was found. The '
                           'parameters phi and psi show two formulas or sub-formulas that are distinct.'),
    e123=ErrorCode(event_type=event_types.error, code='e123',
                   message='Coercion failure: phi of phi_type could not be coerced to coerced_type.'),
))


class CustomException(Exception):
    """A generic exception type for application custom exceptions."""

    def __init__(self, error_code: typing.Optional[ErrorCode] = None, **kwargs):
        self.error_code = error_code
        self.kwargs = kwargs
        super().__init__()

    def __str__(self) -> str:
        return self.typeset_as_string()

    def __repr__(self) -> str:
        return self.typeset_as_string()

    def typeset_as_string(self, **kwargs) -> str:
        return (f'{self.error_code.event_type} '
                f'{self.error_code.code}\n\t{self.error_code.message}\n\t{u1.force_str(o=kwargs)}')


def raise_error(error_code: ErrorCode, **kwargs):
    """Raise a technical event.

    :param error_code:
    :param kwargs:
    :return:
    """
    exception: CustomException = CustomException(error_code=error_code, **kwargs)
    if error_code.event_type == event_types.error:
        logging.exception(msg=exception.typeset_as_string())
        raise exception
    elif error_code.event_type == event_types.warning:
        logging.warning(msg=exception.typeset_as_string())
        warnings.warn(message=exception.typeset_as_string())


class Connective:
    """A connective is a symbol used as a signal to distinguish formulas in theories.

    Equivalent definition:
    A node color in a formula tree."""

    def __init__(self, formula_typesetter: pl1.FlexibleTypesetter = None):
        """

        :param formula_typesetter: A default text representation.
        """
        formula_typesetter: pl1.Typesetter = pl1.coerce_typesetter(ts=formula_typesetter)
        self._formula_typesetter: pl1.Typesetter = formula_typesetter

    def __call__(self, *args):
        """Allows pseudo formal language in python."""
        return Formula(connective=self, terms=args)

    def __str__(self):
        return f'{id(self)}-connective'

    def __repr__(self):
        return f'{id(self)}-connective'

    @property
    def formula_typesetter(self) -> pl1.Typesetter:
        return self._formula_typesetter

    @formula_typesetter.setter
    def formula_typesetter(self, formula_typesetter: pl1.Typesetter):
        self._formula_typesetter = formula_typesetter

    def to_formula(self) -> Formula:
        return Formula(connective=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return FormulaBuilder(c=self)


class FormulaBuilder(list):
    """A mutable object to edit and elaborate formulas.
    Note: formula-builder may be syntactically inconsistent."""

    def __init__(self, c: typing.Optional[Connective] = None, terms: FlexibleTupl = None):
        """
        :param FlexibleTerms terms: A collection of terms."""
        self.connective: typing.Optional[Connective] = c

        # When inheriting from list, we implement __init__ and not __new__.
        # Reference: https://stackoverflow.com/questions/9432719/python-how-can-i-inherit-from-the-built-in-list-type
        super().__init__(self)
        if isinstance(terms, collections.abc.Iterable):
            coerced_tuple = tuple(coerce_formula_builder(term) for term in terms)
            for term in coerced_tuple:
                self.append(term=term)
        elif terms is not None:
            raise_error(error_code=error_codes.e100, c=c, terms_type=type(terms), terms=terms)

    def __contains__(self, phi: FlexibleFormula):
        """Return True is there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.

        :param phi: A formula.
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.
        """
        return self.contain_formula(phi=phi)

    def __delitem__(self, phi):
        """Remove every sub-formula psi' from the formula psi, if and only psi' ~formula phi.

        Attention point: the native python list.remove() method removes only the first element from the list,
        which is a completely different behavior.

        :param phi: A formula
        :return: None
        """
        self.remove_formula(phi=phi)

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    def __setitem__(self, i: int, phi: FlexibleFormula) -> None:
        self.set_term(i=i, phi=phi)

    def append(self, term: FlexibleFormula) -> FormulaBuilder:
        """Append a new term to the formula."""
        term = coerce_formula_builder(phi=term)
        super().append(term)
        return term

    @property
    def arity(self) -> int:
        return len(self)

    def assure_term(self, i: int) -> None:
        """Assure the presence of an i-th term (i being the 0-based index).
        Nodes are initialized with None connective."""
        while len(self) <= i:
            self.append(FormulaBuilder())

    def contain_formula(self, phi: FlexibleFormula) -> bool:
        """Return True is there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.

        :param phi: A formula.
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.
        """
        return any(is_formula_equivalent(phi=phi, psi=psi_prime) for psi_prime in self)

    def get_typesetter(self, typesetter: typing.Optional[pl1.Typesetter] = None) -> pl1.Typesetter:
        """

         - priority 1: parameter typesetter is passed explicitly.
         - priority 2: a typesetting-configuration is attached to the formula, and its typesetting-method is defined.
         - priority 3: a typesetting-configuration is attached to the formula connective, and its typesetting-method is
           defined.
         - priority 4: failsafe typesetting method.

        :param typesetter:
        :return:
        """

        if typesetter is None:
            typesetter: pl1.Typesetter = self.connective.formula_typesetter
        return typesetter

    def iterate_canonical(self):
        """A top-down, left-to-right iteration."""
        yield self
        for t in self:
            yield from t.iterate_canonical()

    def remove(self, phi: FlexibleFormula) -> None:
        """Remove every sub-formula psi' from the formula psi, if and only psi' ~formula phi.

        Attention point: the native python list.remove() method removes only the first element from the list,
        which is a completely different behavior.

        :param phi: A formula
        :return: None
        """
        self.remove_formula(phi=phi)

    def remove_formula(self, phi: FlexibleFormula) -> None:
        """Remove every sub-formula psi' from the formula psi, if and only psi' ~formula phi.

        Attention point: the native python list.remove() method removes only the first element from the list,
        which is a completely different behavior.

        :param phi: A formula
        :return: None
        """
        phi = coerce_formula(phi=phi)
        for psi_prime in self:
            if is_formula_equivalent(phi=phi, psi=psi_prime):
                super().remove(psi_prime)

    def set_term(self, i: int, phi: FlexibleFormula) -> None:
        """Set term / sub-formula at index position i to be formula phi.

        If the sub-formulas of the current formula do not extend to position i, populate the intermediary sub-formulas
        with None.

        :param i: A zero-based index position.
        :param phi: The term / sub-formula.
        :return: None.
        """
        """"""
        phi = coerce_formula(phi=phi)
        self.assure_term(i=i)
        super().__setitem__(i, phi)

    @property
    def term_0(self) -> FormulaBuilder:
        self.assure_term(i=0)
        return self[0]

    @term_0.setter
    def term_0(self, term: FlexibleFormula):
        term = coerce_formula_builder(phi=term)
        if len(self) == 0:
            self.append(term)
        else:
            self[0] = term

    @property
    def term_1(self) -> FormulaBuilder:
        self.assure_term(i=1)
        return self[1]

    @term_1.setter
    def term_1(self, term: FlexibleFormula):
        term = coerce_formula_builder(phi=term)
        if len(self) < 2:
            if len(self) == 0:
                self.assure_term(i=0)
            self.append(term)
        else:
            self[1] = term

    def to_formula(self) -> Formula:
        if self.connective is None:
            raise_error(error_code=error_codes.e113, formula_builder=self, c=self.connective)
        terms: tuple[Formula, ...] = tuple(coerce_formula(phi=term) for term in self)
        phi: Formula = Formula(connective=self.connective, terms=terms)
        return phi

    def typeset_as_string(self, typesetter: typing.Optional[pl1.Typesetter] = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        typesetter = self.get_typesetter(typesetter=typesetter)
        return typesetter.typeset_as_string(phi=self, **kwargs)

    def typeset_from_generator(self, typesetter: typing.Optional[pl1.Typesetter] = None, **kwargs) -> \
            typing.Generator[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        typesetter = self.get_typesetter(typesetter=typesetter)
        yield from typesetter.typeset_from_generator(phi=self, **kwargs)

    def validate_formula_builder(self) -> bool:
        """Validate the syntactical consistency of a candidate formula."""
        # TODO: validate_formula_builder: check no infinite loops
        # TODO: validate_formula_builder: check all nodes have a connective
        return True


class Formula(tuple):
    """An immutable formula modeled as an edge-ordered, node-colored tree."""

    def __new__(cls, connective: Connective, terms: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple
        if isinstance(terms, collections.abc.Iterable):
            elements = tuple(coerce_formula(phi=term) for term in terms)
            o = super().__new__(cls, elements)
            return o
        elif terms is None:
            o = super().__new__(cls)
            return o
        else:
            raise_error(error_code=error_codes.e101, c=connective, terms_type=type(terms), terms=terms)

    def __init__(self, connective: Connective, terms: FlexibleTupl = None):
        super().__init__()
        self._connective = connective

    def __contains__(self, phi: FlexibleFormula):
        """Return True is there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.

        :param phi: A formula.
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.
        """
        return self.has_term(phi=phi)

    def __eq__(self, other):
        """python-equality of formulas is not formula-equivalence."""
        return self is other

    def __hash__(self):
        """python-equality of formulas is not formula-equivalence."""
        return hash(id(self))

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    @property
    def arity(self) -> int:
        """The arity of a formula is equal to the number of terms that are direct children of its root node."""
        return len(self)

    @property
    def connective(self) -> Connective:
        return self._connective

    def get_index_of_first_equivalent_term(self, phi: FlexibleFormula) -> int:
        """Returns the o-based index of the first occurrence of a formula psi among the terms of the current formula,
         such that psi ~formula phi.

        :param phi: The formula being searched.
        :type phi: FlexibleFormula
        ...
        :raises CustomException: Raise exception e109 if psi is not a term of the current formula.
        ...
        :return: the 0 based-based index of the first occurrence of phi in the current formula terms.
        :rtype: int
        """
        return get_index_of_first_equivalent_term_in_formula(phi=phi, psi=self)

    def has_term(self, phi: FlexibleFormula) -> bool:
        """Return True if there exists a term psi of the current formula terms,
        such that phi ~formula psi', False otherwise.

        :param phi: A formula.
        :type phi: FlexibleFormula
        ...
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi2. False
          otherwise.
        :rtype: bool
        """
        return is_term_of_formula(phi=phi, psi=self)

    @property
    def term_0(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 1:
            raise_error(error_code=error_codes.e103, c=self.connective)
        return self[0]

    @property
    def term_1(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 2:
            raise_error(error_code=error_codes.e104, c=self.connective)
        return self[1]

    @property
    def term_2(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 3:
            raise_error(error_code=error_codes.e104, c=self.connective)
        return self[2]

    def to_formula_builder(self) -> FormulaBuilder:
        """Returns a formula-builder that is equivalent to this formula.
        This makes it possible to edit the formula-builder to elaborate new formulas."""
        terms: tuple[FormulaBuilder, ...] = tuple(coerce_formula_builder(phi=term) for term in self)
        phi: FormulaBuilder = FormulaBuilder(c=self.connective, terms=terms)
        return phi

    def get_typesetter(self, typesetter: typing.Optional[pl1.FlexibleTypesetter] = None) -> pl1.Typesetter:
        """

         - priority 1: parameter typesetter is passed explicitly.
         - priority 2: a typesetting-configuration is attached to the formula, and its typesetting-method is defined.
         - priority 3: a typesetting-configuration is attached to the formula connective, and its typesetting-method is
           defined.
         - priority 4: failsafe typesetting method.

        :param typesetter:
        :return:
        """
        if typesetter is None:
            typesetter: pl1.Typesetter = self.connective.formula_typesetter
        return typesetter

    def typeset_as_string(self, typesetter: typing.Optional[pl1.Typesetter] = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        typesetter = self.get_typesetter(typesetter=typesetter)
        return typesetter.typeset_as_string(phi=self, **kwargs)

    def typeset_from_generator(self, typesetter: typing.Optional[pl1.Typesetter] = None, **kwargs) -> \
            typing.Generator[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        typesetter = self.get_typesetter(typesetter=typesetter)
        yield from typesetter.typeset_from_generator(phi=self, **kwargs)
        # yield_string_from_typesetter(x=self, **kwargs)


def yield_string_from_typesetter(x, **kwargs):
    # TODO: ?????
    if isinstance(x, str):
        yield x
    elif isinstance(x, pl1.Typesetter):
        for y in x.typeset_from_generator(**kwargs):
            yield_string_from_typesetter(x=y, **kwargs)


def coerce_formula_builder(phi: FlexibleFormula = None) -> FormulaBuilder:
    if isinstance(phi, FormulaBuilder):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula_builder()
    elif isinstance(phi, Formula):
        return phi.to_formula_builder()
    elif phi is None:
        return FormulaBuilder(c=None, terms=None)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=FormulaBuilder, phi_type=type(phi), phi=phi)


def coerce_formula(phi: FlexibleFormula) -> Formula:
    if isinstance(phi, Formula):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula()
    elif isinstance(phi, FormulaBuilder):
        return phi.to_formula()
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        # Implicit conversion of generators to tuple formulas.
        return Tupl(elements=(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        # Implicit conversion of iterators to tuple formulas.
        return Tupl(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Formula, phi_type=type(phi), phi=phi)


def coerce_enumeration(phi: FlexibleEnumeration) -> Enumeration:
    """Coerce elements to an enumeration.
    If elements is None, coerce it to an empty enumeration."""
    if isinstance(phi, Enumeration):
        return phi
    elif isinstance(phi, EnumerationBuilder):
        return phi.to_enumeration()
    elif isinstance(phi, Formula) and is_well_formed_enumeration(phi=phi):
        # phi is a well-formed enumeration,
        # it can be safely re-instantiated as an Enumeration and returned.
        return Enumeration(elements=phi, connective=phi.connective)
    elif phi is None:
        return Enumeration(elements=None)
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(elements=tuple(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Enumeration, phi_type=type(phi), phi=phi)


def union_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration) -> Enumeration:
    """Given two enumerations phi, and psi, the union-enumeration operator, noted phi ∪-enumeration psi,
    returns a new enumeration omega such that:
    - all elements of phi are elements of omega,
    - all elements of psi are elements of omega,
    - no other elements are elements of omega.
    Order is preserved, that is:
    - the elements from phi keep their original order in omega
    - the elements from psi keep their original order in omega providing they are not already present in phi,
        in which case they are skipped

    Under enumeration-equivalence, the union-enumeration operator is:
     - Idempotent: (phi ∪-enumeration phi) ~enumeration phi.
     - Symmetric: (phi ∪-enumeration psi) ~enumeration (psi ∪-enumeration phi).

    Under formula-equivalence, the union-enumeration operator is:
     - Idempotent: (phi ∪-formula phi) ~formula phi.
     - Not symmetric if some element of psi are elements of phi: because of order.
    """
    phi: Enumeration = coerce_enumeration(phi=phi)
    psi: Enumeration = coerce_enumeration(phi=psi)
    eb: EnumerationBuilder = EnumerationBuilder(elements=None)
    for phi_prime in phi:
        eb.append(term=phi_prime)
    for psi_prime in psi:
        eb.append(term=psi_prime)
    e: Enumeration = eb.to_enumeration()
    return e


def union_theory(phi: FlexibleTheory, psi: FlexibleTheory) -> Theory:
    """Given two theories phi, and psi, the union-theory operator, noted phi ∪-theory psi,
    returns a new theory omega such that:
    - all derivations of phi are elements of omega,
    - all derivations of psi are elements of omega,
    - no other derivations are derivations of omega.
    Order is preserved, that is:
    - the derivations from phi keep their original order in omega
    - the derivations from psi keep their original order in omega providing they are not already present in phi,
        in which case they are skipped

    Under theory-equivalence, the union-theory operator is:
     - Idempotent: (phi ∪-theory phi) ~theory phi.
     - Symmetric: (phi ∪-theory psi) ~theory (psi ∪-theory phi).

    Under formula-equivalence, the union-theory operator is:
     - Idempotent: (phi ∪-theory phi) ~formula phi.
     - Not symmetric if some element of psi are elements of phi: because of order.
    """
    phi: Theory = coerce_theory(phi=phi)
    psi: Theory = coerce_theory(phi=psi)
    t2: Theory = Theory(derivations=(*phi, *psi,))
    return t2


def coerce_enumeration_builder(phi: FlexibleEnumeration) -> EnumerationBuilder:
    if isinstance(phi, EnumerationBuilder):
        return phi
    elif isinstance(phi, Enumeration):
        return phi.to_enumeration_builder()
    elif phi is None:
        return EnumerationBuilder(elements=None)
    elif isinstance(phi, typing.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return EnumerationBuilder(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=EnumerationBuilder, phi_type=type(phi), phi=phi)


def coerce_map(phi: FlexibleMap) -> Map:
    if isinstance(phi, Map):
        return phi
    elif isinstance(phi, MapBuilder):
        return phi.to_map()
    elif phi is None:
        return Map(domain=None, codomain=None)
    # TODO: coerce_map: Implement with isinstance(phi, FlexibleFormula) and is_well_formed...
    elif isinstance(phi, dict):
        domain: Enumeration = coerce_enumeration(phi=phi.keys())
        codomain: Tupl = coerce_tupl(phi=phi.values())
        return Map(domain=domain, codomain=codomain)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Map, phi_type=type(phi), phi=phi)


def coerce_map_builder(phi: FlexibleMap) -> MapBuilder:
    if isinstance(phi, MapBuilder):
        return phi
    elif isinstance(phi, Map):
        return phi.to_map_builder()
    elif phi is None:
        return MapBuilder(domain=None, codomain=None)
    elif isinstance(phi, dict):
        domain: EnumerationBuilder = coerce_enumeration_builder(phi=phi.keys())
        codomain: TuplBuilder = coerce_tupl_builder(phi=phi.values())
        return MapBuilder(domain=domain, codomain=codomain)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=MapBuilder, phi_type=type(phi), phi=phi)


def coerce_tupl(phi: FlexibleTupl) -> Tupl:
    if isinstance(phi, Tupl):
        return phi
    elif isinstance(phi, TuplBuilder):
        return phi.to_tupl()
    elif phi is None:
        return Tupl(elements=None)
    elif isinstance(phi, collections.abc.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return Tupl(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Tupl, phi_type=type(phi), phi=phi)


def coerce_tupl_builder(phi: FlexibleTupl) -> TuplBuilder:
    if isinstance(phi, TuplBuilder):
        return phi
    elif isinstance(phi, Tupl):
        return phi.to_tupl_builder()
    elif phi is None:
        return TuplBuilder(elements=None)
    elif isinstance(phi, collections.abc.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return TuplBuilder(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=TuplBuilder, phi_type=type(phi), phi=phi)


FlexibleFormula = typing.Optional[typing.Union[Connective, Formula, FormulaBuilder]]


class FreeArityConnective(Connective):
    """A free-arity connective is a connective without constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self, formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(formula_typesetter=formula_typesetter)


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective with a constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self,
                 fixed_arity_constraint: int, formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
        self._fixed_arity_constraint = fixed_arity_constraint
        super().__init__(formula_typesetter=formula_typesetter)

    @property
    def fixed_arity_constraint(self) -> int:
        return self._fixed_arity_constraint


class NullaryConnective(FixedArityConnective):

    def __init__(self, formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(fixed_arity_constraint=0, formula_typesetter=formula_typesetter)


class SimpleObject(Formula):
    """A simple-object is a formula composed of a nullary-connective."""

    def __new__(cls, connective: NullaryConnective):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple
        o = super().__new__(cls, connective=connective, terms=None)
        return o

    def __init__(self, connective: NullaryConnective):
        super().__init__(connective=connective, terms=None)


class UnaryConnective(FixedArityConnective):

    def __init__(self, formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(fixed_arity_constraint=1, formula_typesetter=formula_typesetter)


class InfixPartialFormula:
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and gluing all this together with the InfixPartialFormula class.
    """

    def __init__(self, c: Connective, term_1: FlexibleFormula):
        self._connective = c
        self._term_1 = term_1

    def __or__(self, term_2: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        return Formula(connective=self._connective, terms=(self.term_1, term_2,))

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    @property
    def connective(self) -> Connective:
        return self._connective

    def typeset_as_string(self, **kwargs):
        # TODO: Enrich the representation of partial-formulas
        return f'{self.connective}(???,{self.term_1})'

    @property
    def term_1(self) -> Connective:
        return self._term_1


class BinaryConnective(FixedArityConnective):

    def __init__(self, formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(formula_typesetter=formula_typesetter, fixed_arity_constraint=2)

    def __ror__(self, other: FlexibleFormula):
        """Pseudo math notation. x | p | ?."""
        return InfixPartialFormula(c=self, term_1=other)


def is_term_of_formula(phi: Formula, psi: Formula) -> bool:
    """Returns True if and only if there exists a term t of psi such that phi ~formula t.

    When this condition is satisfied, we say that phi is a term of psi.

    :param phi: A formula.
    :type phi: FlexibleFormula
    :param psi: A formula.
    :type psi: FlexibleFormula
    ...
    :return: True if phi is a term of psi, False otherwise.
    :rtype: bool
    """
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    return any(is_formula_equivalent(phi=phi, psi=psi_term) for psi_term in psi)


def is_axiom_of_theory(a: FlexibleAxiom, t: FlexibleTheory):
    a: Axiom = coerce_axiom(phi=a)
    t: Theory = coerce_theory(phi=t)
    return any(is_formula_equivalent(phi=a, psi=a2) for a2 in t.axioms)


def is_inference_rule_of_theory(ir: FlexibleInferenceRule, t: FlexibleTheory):
    ir: InferenceRule = coerce_inference_rule(phi=ir)
    t: Theory = coerce_theory(phi=t)
    return any(is_formula_equivalent(phi=ir, psi=ir2) for ir2 in t.inference_rules)


def is_theorem_of_theory(thrm: FlexibleTheorem, t: FlexibleTheory):
    thrm: Theorem = coerce_theorem(phi=thrm)
    t: Theory = coerce_theory(phi=t)
    return any(is_formula_equivalent(phi=thrm, psi=thrm2) for thrm2 in t.theorems)


def get_index_of_first_equivalent_term_in_formula(phi: FlexibleFormula, psi: FlexibleFormula) -> int:
    """Returns the o-based index of the first occurrence of a formula phi in the terms of a formula psi,
     such that psi ~formula phi.

    :param phi: The formula being searched.
    :type phi: FlexibleFormula
    :param psi: The formula whose terms are being searched.
    :type psi: FlexibleFormula
    ...
    :raises CustomException: Raise exception e109 if phi is not a term of psi.
    ...
    :return: the 0 based-based index of the first occurrence of phi in psi terms, such that they are equivalent.
    :rtype: int
    """
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    if is_term_of_formula(phi=phi, psi=psi):
        # two formulas that are formula-equivalent may not be equal.
        # for this reason we must first find the first formula-equivalent element in the tuple.
        n: int = 0
        for psi_term in psi:
            if is_formula_equivalent(phi=phi, psi=psi_term):
                return n
            n = n + 1
    raise_error(error_code=error_codes.e109, phi=phi, psi=psi)


class TernaryConnective(FixedArityConnective):

    def __init__(self,
                 formula_typesetter: typing.Optional[pl1.Typesetter] = None):
        super().__init__(fixed_arity_constraint=3, formula_typesetter=formula_typesetter)


class Variable(SimpleObject):
    """A variable is defined as a simple-object.

    Question: a variable could be alternatively defined as any arbitrary formula, but using simple-objects look
    sufficient and much more readable.

    The justification for a dedicated python class is the implementation of the __enter__ and __exit__ methods,
    which allow the usage of variables with the python with statement."""

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed variable, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        # TODO: Reimplement this properly
        phi: Formula = coerce_formula(phi=phi)
        if phi.arity != 0:
            return False
        return True

    def __new__(cls, connective: NullaryConnective):
        o: tuple
        o = super().__new__(cls, connective=connective)
        return o

    def __init__(self, connective: NullaryConnective):
        super().__init__(connective=connective)

    def __enter__(self) -> Variable:
        return self

    def __exit__(self, exc_type: typing.Optional[type], exc: typing.Optional[BaseException],
                 exc_tb: typing.Any) -> None:
        return


def let_x_be_a_variable(formula_typesetter: pl1.FlexibleTypesetter) -> typing.Union[
    Variable, typing.Generator[Variable, typing.Any, None]]:
    if formula_typesetter is None or isinstance(formula_typesetter, pl1.FlexibleTypesetter):
        return Variable(connective=NullaryConnective(formula_typesetter=formula_typesetter))
    elif isinstance(formula_typesetter, typing.Iterable):
        return (Variable(connective=NullaryConnective(formula_typesetter=ts)) for ts in formula_typesetter)
    else:
        raise TypeError  # TODO: Implement event code.


def v(rep: FlexibleRepresentation) -> typing.Union[
    NullaryConnective, typing.Generator[NullaryConnective, typing.Any, None]]:
    """A shortcut for let_x_be_a_variable."""
    return let_x_be_a_variable(formula_typesetter=rep)


FlexibleRepresentation = typing.Union[str, pl1.Symbol, pl1.Typesetter]
"""FlexibleRepresentation is a flexible python type that may be safely coerced to a symbolic representation."""

FlexibleMultiRepresentation = typing.Union[FlexibleRepresentation, typing.Iterable[FlexibleRepresentation]]
"""FlexibleMultiRepresentation is a flexible python type that may be safely coerced to a single or multiple symbolic 
representation."""


def let_x_be_a_simple_object(formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None) -> typing.Union[
    SimpleObject, typing.Generator[SimpleObject, typing.Any, None]]:
    """A helper function to declare one or multiple simple-objects.

    :param formula_typesetter: A string (or an iterable of strings) default representation for the simple-object(s).
    :return: A simple-object (if rep is a string), or a python-tuple of simple-objects (if rep is an iterable).
    """
    if isinstance(formula_typesetter, FlexibleRepresentation):
        return SimpleObject(connective=NullaryConnective(formula_typesetter=formula_typesetter))
    elif isinstance(formula_typesetter, typing.Iterable):
        return (SimpleObject(connective=NullaryConnective(formula_typesetter=r)) for r in formula_typesetter)
    else:
        raise TypeError  # TODO: Implement event code.


def formula_to_tuple(phi: FlexibleFormula) -> Enumeration:
    """A canonical transformation of formulas to the tuple of the formula terms.

    f:  Phi --> E
        phi |-> e(t0, t1, ..., tn)
    Where:
     - Phi is the class of formulas,
     - E is the class of enumerations,
     - phi is a formula,
     - e is the enumeration connective,
     - ti is the i-th term of phi.

    :param phi: A formula.
    :return: The enumeration of the formula terms.
    """
    phi = coerce_formula(phi=phi)
    return Enumeration(elements=phi)


def let_x_be_a_binary_connective(
        formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
    return BinaryConnective(formula_typesetter=formula_typesetter)


def let_x_be_a_ternary_connective(
        formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
    return TernaryConnective(formula_typesetter=formula_typesetter)


def let_x_be_a_unary_connective(
        formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
    return UnaryConnective(formula_typesetter=formula_typesetter)


def let_x_be_a_free_arity_connective(
        formula_typesetter: typing.Optional[pl1.FlexibleTypesetter] = None):
    return FreeArityConnective(formula_typesetter=formula_typesetter)


def let_x_be_an_inference_rule(theory: FlexibleTheory,
                               inference_rule: typing.Optional[FlexibleInferenceRule] = None,
                               premises: typing.Optional[FlexibleTupl] = None,
                               conclusion: typing.Optional[FlexibleFormula] = None,
                               variables: typing.Optional[FlexibleEnumeration] = None):
    if theory is None:
        theory = Axiomatization(derivations=None)
    else:
        theory: FlexibleTheory = coerce_theory(phi=theory)

    if inference_rule is None and premises is not None and conclusion is not None and variables is not None:
        transformation: Transformation = Transformation(premises=premises, conclusion=conclusion, variables=variables)
        inference_rule: InferenceRule = InferenceRule(transformation=transformation)

    if isinstance(theory, Axiomatization):
        theory = Axiomatization(derivations=(*theory, inference_rule,))
        return theory, inference_rule
    elif isinstance(theory, Theory):
        theory = Theory(derivations=(*theory, inference_rule,))
        return theory, inference_rule
    else:
        raise Exception('oops')


def let_x_be_an_axiom_deprecated(valid_statement: FlexibleFormula):
    return Axiom(valid_statement=valid_statement)


def let_x_be_an_axiom(theory: FlexibleTheory, valid_statement: typing.Optional[FlexibleFormula] = None,
                      axiom: typing.Optional[FlexibleAxiom] = None):
    """

    :param theory: An axiom-collection or a theory. If None, the empty axiom-collection is implicitly used.
    :param valid_statement: The statement claimed by the new axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :param axiom: An existing axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :return: a pair (t, a) where t is an extension of the input theory, with a new axiom claiming the
    input statement, and a is the new axiom.
    """
    if theory is None:
        theory = Axiomatization(derivations=None)
    else:
        theory: FlexibleTheory = coerce_theory(phi=theory)
    if valid_statement is not None and axiom is not None:
        raise Exception('oops 1')
    elif valid_statement is None and axiom is None:
        raise Exception('oops 2')
    elif valid_statement is not None:
        axiom: Axiom = Axiom(valid_statement=valid_statement)

    if isinstance(theory, Axiomatization):
        theory = Axiomatization(derivations=(*theory, axiom,))
        return theory, axiom
    elif isinstance(theory, Theory):
        theory = Theory(derivations=(*theory, axiom,))
        return theory, axiom
    else:
        raise Exception('oops 3')


def let_x_be_a_theory(derivations: typing.Optional[FlexibleEnumeration] = None):
    """

    :param derivations: an enumeration of derivations. If None, the empty theory is implicitly assumed.
    :return:
    """
    return Theory(derivations=derivations)


def let_x_be_a_collection_of_axioms(axioms: FlexibleEnumeration):
    return Axiomatization(derivations=axioms)


def let_x_be_a_transformation(premises: FlexibleTupl, conclusion: FlexibleFormula,
                              variables: FlexibleEnumeration):
    return Transformation(premises=premises, conclusion=conclusion, variables=variables)


class Connectives(typing.NamedTuple):
    axiom: UnaryConnective
    axiomatization: FreeArityConnective
    enumeration: FreeArityConnective
    follows_from: BinaryConnective
    implies: BinaryConnective
    inference: BinaryConnective
    inference_rule: UnaryConnective
    is_a: BinaryConnective
    land: BinaryConnective
    lnot: UnaryConnective
    lor: BinaryConnective
    map: BinaryConnective
    proposition: SimpleObject
    propositional_variable: SimpleObject
    theory: FreeArityConnective
    theorem: FreeArityConnective  # TODO: arity is wrong, correct it.
    transformation: TernaryConnective
    tupl: FreeArityConnective


connectives: Connectives = _set_state(key='connectives', value=Connectives(
    axiom=let_x_be_a_unary_connective(formula_typesetter='axiom'),
    axiomatization=let_x_be_a_free_arity_connective(formula_typesetter='axiomatization'),
    enumeration=let_x_be_a_free_arity_connective(formula_typesetter='enumeration'),
    follows_from=let_x_be_a_binary_connective(formula_typesetter='follows-from'),
    implies=let_x_be_a_binary_connective(formula_typesetter='implies'),
    inference=let_x_be_a_binary_connective(formula_typesetter='inference'),
    inference_rule=let_x_be_a_unary_connective(formula_typesetter='inference-rule'),
    is_a=let_x_be_a_binary_connective(formula_typesetter='is-a'),
    land=let_x_be_a_binary_connective(formula_typesetter='∧'),
    lnot=let_x_be_a_unary_connective(formula_typesetter='¬'),
    lor=let_x_be_a_binary_connective(formula_typesetter='∨'),
    map=let_x_be_a_binary_connective(formula_typesetter='map'),
    proposition=let_x_be_a_simple_object(formula_typesetter='proposition'),
    propositional_variable=let_x_be_a_simple_object(formula_typesetter='propositional-variable'),
    theorem=let_x_be_a_free_arity_connective(formula_typesetter='theorem'),
    theory=let_x_be_a_free_arity_connective(formula_typesetter='theory'),
    transformation=let_x_be_a_ternary_connective(formula_typesetter='transformation'),
    tupl=let_x_be_a_free_arity_connective(formula_typesetter='tuple'),

))


# TODO: Rename Enumeration to HorizontalEnumeration, then implement VerticalEnumeration and parent class Enumeration.
# TODO: Implement EnumerationAccretor.

def is_symbol_equivalent(phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Two formulas phi and psi are symbol-equivalent, noted phi ~symbol psi, if and only if they are the same symbol.

    By "the same symbol", we mean that the symbol's reference is the same.

    Formally, is-symbol-equivalence is an equivalence class, that is, if phi, psi, and omega are formulas:
     - It is reflexive: phi ~symbol phi.
     - It is symmetric: phi ~symbol psi ⇒ psi ~symbol phi.
     - It is transitive: phi ~symbol psi ∧ psi ~symbol omega ⇒ phi ~symbol omega.

    Note: two formulas phi and psi may have the same textual representations (e.g.: "x"),
    and may not be symbol-equivalent. This happens when two distinct objects have been declared
    in the language with identical textual representations.

    :param phi: A formula.
    :param psi: A formula.
    :return: True if phi ~symbol psi. False otherwise.
    """
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    return id(phi) == id(psi)


def is_connective_equivalent(phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Two formulas phi and psi are connective-equivalent, noted phi ~connective psi, if and only if they have the
    same root connective.

    By "the same connective", we mean that the connective's reference is the same.

    Formally, ~connective is an equivalence class, that is, if phi, psi, and omega are formulas:
     - It is reflexive: phi ~connective phi.
     - It is symmetric: phi ~connective psi ⇒ psi ~connective phi.
     - It is transitive: phi ~connective psi ∧ psi ~connective omega ⇒ phi ~connective omega.

    Note: two formulas phi and psi may have connectives with the same textual representations (e.g.: "+"),
    and may not be connective-equivalent. This happens when two distinct connectives
    in the language have identical textual representations.

    :param phi: A formula.
    :param psi: A formula.
    :return: True if phi ~connective psi. False otherwise.
    """
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    return phi.connective is psi.connective


def is_formula_equivalent(phi: FlexibleFormula, psi: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
    """Two formulas phi and psi are formula-equivalent, noted phi ~formula psi, if and only if:
    Base case:
     - phi ~connective psi
     - phi arity = 0
     - psi arity = 0
     Inductive step:
     - phi ~connective psi
     - phi arity = psi arity
     - following canonical order, for all pairs of children formulas phi' in phi psi' in psi,
       phi ~formula psi
     Extreme case:
     - all other pairs for formulas are not formula-equivalent.

    Formally, ~formula is an equivalence class, that is, if phi, psi, and omega are formulas:
     - It is reflexive: phi ~formula phi.
     - It is symmetric: phi ~formula psi ⇒ psi ~formula phi.
     - It is transitive: phi ~formula psi ∧ psi ~formula omega ⇒ phi ~formula omega.

    :param phi: A formula.
    :param psi: A formula.
    :param raise_event_if_false:
    :return: True if phi ~formula psi. False otherwise.
    """
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    if (is_connective_equivalent(phi=phi, psi=psi)) and (phi.arity == 0) and (psi.arity == 0):
        # Base case
        return True
    elif (is_connective_equivalent(phi=phi, psi=psi)) and (phi.arity == psi.arity) and all(
            is_formula_equivalent(phi=phi_prime, psi=psi_prime) for phi_prime, psi_prime in zip(phi, psi)):
        # Inductive step
        return True
    else:
        # Extreme case
        if raise_event_if_false:
            raise_error(error_code=error_codes.e122, phi=phi, psi=psi)
        return False


def is_formula_equivalent_with_variables(phi: FlexibleFormula, psi: FlexibleFormula, variables: FlexibleEnumeration,
                                         m: FlexibleMap = None, raise_event_if_false: bool = False) -> bool:
    """Two formulas phi and psi are formula-equivalent-with-variables in regard to variables V if and only if:
     - All formulas in V are not sub-formula of phi,
     - We declare a new formula psi' where every sub-formula that is an element of V,
       is substituted by the formula that is at the exact same position in the tree.
     - And the phi and psi' are formula-equivalent.

     Note: is-formula-equivalent-with-variables is not commutative.

    :param phi: a formula that does not contain any element of variables.
    :param psi: a formula that may contain some elements of variables.
    :param variables: an enumeration of formulas called variables.
    :param m: (conditional) a mapping between variables and their assigned values. used internally for recursive calls.
      leave it to None.
    :param raise_event_if_false:
    :return:
    """
    m: MapBuilder = coerce_map_builder(phi=m)
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    psi_value: Formula = psi
    variables: Tupl = coerce_tupl(phi=variables)
    if variables.has_element(phi=phi):
        # The sub-formulas of left-hand formula phi can't be elements of the variables enumeration.
        raise_error(error_code=error_codes.e118, phi=phi, psi=psi, v=variables)
    if variables.has_element(phi=psi):
        # psi is a variable.
        if m.is_defined_in(phi=psi):
            # psi's value is already mapped.
            already_mapped_value: Formula = m.get_assigned_value(phi=psi)
            if is_formula_equivalent(phi=phi, psi=already_mapped_value):
                # phi is consistent with the already mapped value.
                # we can safely substitute the variable with its value.
                psi_value: Formula = already_mapped_value
                # print(f'    substituted with {psi}.')
            else:
                # psi is not consistent with its already mapped value.
                # it follows that phi and psi are not formula-equivalent-with-variables.
                if raise_event_if_false:
                    raise_error(error_code=error_codes.e121, variable=psi,
                                already_mapped_value=already_mapped_value, distinct_value=phi)
                return False
        else:
            # psi's value has not been mapped yet.
            # substitute the variable with its newly mapped value.
            psi_value = phi
            m.set_pair(phi=psi, psi=psi_value)
    # print(f'    psi_value:{psi_value}')
    # at this point, variable substitution has been completed at the formula-root level.
    if (is_connective_equivalent(phi=phi, psi=psi_value)) and (phi.arity == 0) and (psi_value.arity == 0):
        # Base case
        return True
    elif (is_connective_equivalent(phi=phi, psi=psi_value)) and (phi.arity == psi_value.arity) and all(
            is_formula_equivalent_with_variables(phi=phi_prime, psi=psi_prime, variables=variables, m=m) for
            phi_prime, psi_prime in zip(phi, psi_value)):
        # Inductive step
        return True
    else:
        # Extreme case
        return False


def is_tuple_equivalent(phi: FlexibleEnumeration, psi: FlexibleEnumeration) -> bool:
    """Two formula or tuples phi and psi is tuple-equivalent, denoted phi ~tuple psi, if and only if:
     - |phi| = |psi|
     - for n = 0 to |phi|: the n-th element of phi is formula-equivalent with the n-th element of psi.

    Question #1: with the definition above, elements of phi and psi must be formula-equivalent,
    which is stricter than tuple-equivalence. We may wish to distinguish superficial-tuple-equivalence
    from recursive-tuple-equivalence.

    :param phi: A tuple.
    :param psi: A tuple.
    :return: True if phi ~enumeration psi, False otherwise.
    """
    raise NotImplementedError('To be analysed further.')


def is_enumeration_equivalent(phi: FlexibleEnumeration, psi: FlexibleEnumeration) -> bool:
    """Two enumerations phi and psi are enumeration-equivalent, denoted phi ~enumeration psi, if and only if:
     - for all sub-formula phi' in phi, there exists a sub-formula psi' in psi such that phi' ~formula psi'.
     - for all sub-formula psi' in psi, there exists a sub-formula phi' in phi such that psi' ~formula phi'.

    :param phi: An enumeration.
    :param psi: An enumeration.
    :return: True if phi ~enumeration psi, False otherwise.
    """
    phi: Formula = coerce_enumeration(phi=phi)
    psi: Formula = coerce_enumeration(phi=psi)

    test_1 = all(any(is_formula_equivalent(phi=phi_prime, psi=psi_prime) for psi_prime in psi) for phi_prime in phi)
    test_2 = all(any(is_formula_equivalent(phi=psi_prime, psi=phi_prime) for phi_prime in phi) for psi_prime in psi)

    return test_1 and test_2


def replace_formulas(phi: FlexibleFormula, m: FlexibleMap) -> Formula:
    """Performs a top-down, left-to-right replacement of formulas in formula phi."""
    phi: Formula = coerce_formula(phi=phi)
    m: Map = coerce_map(phi=m)
    if m.is_defined_in(phi=phi):
        # phi must be replaced at its root.
        # the replacement algorithm stops right there (i.e.: no more recursion).
        assigned_value: Formula = m.get_assigned_value(phi=phi)
        return assigned_value
    else:
        # build the replaced formula.
        fb: FormulaBuilder = FormulaBuilder(c=phi.connective)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = replace_formulas(phi=term, m=m)
            fb.append(term=term_substitute)
        return fb.to_formula()


class TuplBuilder(FormulaBuilder):
    """A utility class to help build tuples. It is mutable and thus allows edition."""

    def __init__(self, elements: FlexibleTupl):
        super().__init__(c=connectives.tupl, terms=elements)

    def to_tupl(self) -> Tupl:
        elements: tuple[Formula, ...] = tuple(coerce_formula(phi=element) for element in self)
        phi: Tupl = Tupl(elements=elements)
        return phi

    def to_formula(self) -> Formula:
        """Return a Collection."""
        return self.to_tupl()


class Tupl(Formula):
    """A tuple is a synonym for formula.

    The rationale for a dedicated class is semantic. When considering tuples, we do not take into account the
    root connective. Also, formula terms are called elements. Finally, notation is distinct: a formula is
    typically denoted as f(t0, t1, ..., tn) while a tuple is denoted as (t0, t1, ..., tn).

     The empty-tuple is the tuple ().

     Python implementation: in python, the word 'tuple' is reserved. For this reason, the word 'tupl' is used instead
     to implement this object."""

    def __new__(cls, elements: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, connective=connectives.tupl, terms=elements)
        return o

    def __init__(self, elements: FlexibleTupl = None):
        super().__init__(connective=connectives.tupl, terms=elements)

    def get_index_of_first_equivalent_element(self, phi: Formula) -> typing.Optional[int]:
        """Returns the o-based index of the first occurrence of a formula psi in the tuple such that psi ~formula phi.

        :param phi: A formula.
        :return:
        """
        return self.get_index_of_first_equivalent_term(phi=phi)

    def has_element(self, phi: Formula) -> bool:
        """Return True if the tuple has phi as one of its elements."""
        return is_term_of_formula(phi=phi, psi=self)

    def to_tupl_builder(self) -> TuplBuilder:
        return TuplBuilder(elements=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_tupl_builder()


FlexibleTupl = typing.Optional[typing.Union[Tupl, TuplBuilder, typing.Iterable[FlexibleFormula]]]
"""FlexibleTupl is a flexible python type that may be safely coerced into a Tupl or a TupleBuilder."""


class MapBuilder(FormulaBuilder):
    """A utility class to help build maps. It is mutable and thus allows edition."""

    def __init__(self, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        domain: EnumerationBuilder = coerce_enumeration_builder(phi=domain)
        codomain: TuplBuilder = coerce_tupl_builder(phi=codomain)
        super().__init__(c=connectives.map, terms=(domain, codomain,))

    def set_pair(self, phi: FlexibleFormula, psi: FlexibleFormula) -> None:
        """Set the pair (phi, psi) to the map-builder.

        :param phi: a formula that will become an element of the domain.
        :param psi: a formula that will become an element of the codomain mapped with phi.
        :return: None.
        """
        phi: Formula = coerce_formula(phi=phi)
        psi: Formula = coerce_formula(phi=psi)
        if self.is_defined_in(phi=phi):
            # phi is already defined in the map, we consequently overwrite it.
            index_position: int = self.domain.get_index_of_equivalent_term(phi=phi)
            self.codomain[index_position] = psi
        else:
            # phi is not already defined in the map, we can append it.
            if len(self.domain) != len(self.codomain):
                raise ValueError('map is inconsistent!')
            self.domain.append(term=phi)
            self.codomain.append(term=psi)

    @property
    def codomain(self) -> TuplBuilder:
        """The co-domain of the map is its second formula term."""
        return coerce_tupl_builder(phi=self.term_1)

    @property
    def domain(self) -> EnumerationBuilder:
        """The domain of the map is its first formula term."""
        return coerce_enumeration_builder(phi=self.term_0)

    def get_assigned_value(self, phi: FlexibleFormula) -> FlexibleFormula:
        """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
        if self.is_defined_in(phi=phi):
            index_position: int = self.domain.get_index_of_equivalent_term(phi=phi)
            return self.codomain[index_position]
        else:
            raise IndexError('Map domain does not contain this element')

    def is_defined_in(self, phi: FlexibleFormula) -> bool:
        """Return True if phi is formula-equivalent to an element of the map domain."""
        return self.domain.has_element(phi=phi)

    def to_map(self) -> Map:
        """Convert this map-builder to a map."""
        keys: Tupl = coerce_tupl(phi=self.term_0)
        values: Tupl = coerce_tupl(phi=self.term_1)
        phi: Map = Map(domain=keys, codomain=values)
        return phi

    def to_formula(self) -> Formula:
        """Return a formula."""
        return self.to_map()


class Map(Formula):
    """A map is a formula m(t0(k0, k1, ..., kn), t1(l0, l1, ..., ln)) where:
     - m is a node with the map connective.
     - t0 is an enumeration named the keys' enumeration.
     - t1 is a tuple named the values tuple.
     - the cardinality of t0 is equal to the cardinality of 1.

     The empty-map is the map m(t0(), t1()).

    """

    def __new__(cls, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        domain: Enumeration = coerce_enumeration(phi=domain)
        codomain: Tupl = coerce_tupl(phi=codomain)
        if len(domain) != len(codomain):
            raise ValueError('Map: |keys| != |values|')
        o: tuple = super().__new__(cls, connective=connectives.map, terms=(domain, codomain,))
        return o

    def __init__(self, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        domain: Enumeration = coerce_enumeration(phi=domain)
        codomain: Tupl = coerce_tupl(phi=codomain)
        super().__init__(connective=connectives.map, terms=(domain, codomain,))

    @property
    def codomain(self) -> Tupl:
        return coerce_tupl(phi=self.term_1)

    @property
    def domain(self) -> Enumeration:
        return coerce_enumeration(phi=self.term_0)

    def get_assigned_value(self, phi: Formula) -> Formula:
        """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
        if self.is_defined_in(phi=phi):
            index_position: int = self.domain.get_element_index(phi=phi)
            return self.codomain[index_position]
        else:
            raise IndexError('Map domain does not contain this element')

    def is_defined_in(self, phi: Formula) -> bool:
        """Return True if phi is formula-equivalent to an element of the map domain."""
        return self.domain.has_element(phi=phi)

    def to_map_builder(self) -> MapBuilder:
        return MapBuilder(domain=self.term_0, codomain=self.term_1)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_map_builder()


FlexibleMap = typing.Optional[typing.Union[Map, MapBuilder, typing.Dict[Formula, Formula]]]
"""FlexibleMap is a flexible python type that may be safely coerced into a Map or a MapBuilder."""


class EnumerationBuilder(FormulaBuilder):
    """A utility class to help build enumerations. It is mutable and thus allows edition.

    Note: """

    def __init__(self, elements: FlexibleEnumeration = None, connective: Connective = None):
        if connective is None:
            connective = connectives.enumeration

        super().__init__(c=connective, terms=None)
        if isinstance(elements, typing.Iterable):
            for element in elements:
                self.append(term=element)

    def append(self, term: FlexibleFormula) -> None:
        """

        Override the append method to assure the unicity of newly added elements.

        :param term:
        :return:
        """
        term = coerce_formula(phi=term)
        if any(is_formula_equivalent(phi=term, psi=element) for element in self):
            raise_error(error_code=error_codes.e104, enumeration=self, term=term)
        else:
            super().append(term=term)

    def get_index_of_equivalent_term(self, phi: FlexibleFormula) -> typing.Optional[int]:
        """Return the index of phi if phi is formula-equivalent with an element of the enumeration, None otherwise.

        This method is not available on formulas because duplicate elements are possible on formulas,
        but are not possible on enumerations."""
        return get_index_of_first_equivalent_term_in_formula(phi=phi, psi=self)

    def has_element(self, phi: FlexibleFormula) -> bool:
        """Return True if and only if there exists a formula psi that is an element of the enumeration, and such that
        phi ∼formula psi. False otherwise."""
        e: Enumeration = self.to_enumeration()
        return is_term_of_formula(phi=phi, psi=e)

    def to_enumeration(self) -> Enumeration:
        elements: tuple[Formula, ...] = tuple(coerce_formula(phi=element) for element in self)
        phi: Enumeration = Enumeration(elements=elements)
        return phi

    def to_formula(self) -> Formula:
        """Return a Collection."""
        return self.to_enumeration()


class Enumeration(Formula):
    """An enumeration is formula whose terms, called elements, are unique over the ~formula operator.

    Syntactic definition:
    A well-formed enumeration is a formula of the form:
        e(phi_0, phi_1, ..., phi_n)
    where:
     - e is some connective,
     - phi_i is a term of the formula called an element of the enumeration,
     - for all formula phi_a element of the formula terms,
       and for all formula phi_b element of the formula terms such that a ≠ b,
       ¬(phi_a ~formula phi_b).

    Shortcut: e

    Note: by default, enumerations are denoted with the e enumeration connective, but this is not necessary.

    Note: by definition, formula terms are not unique over the ~formula operator, but enumeration elements are.

    Note: by definition, both formula terms and enumeration elements are ordered.

    Note: see the enumeration-equivalence-class and the  ~enumeration operator for the canonical equivalence class
    over enumerations, which makes enumerations equivalent to finite or computable sets.

    Distinctive objects:
     - The empty-enumeration is the formula c(). See EmptyEnumeration for a specialized class.

    See also:
     - ~enumeration operator
     - enumeration-equivalence-class
     - union-enumeration

    """

    def __new__(cls, elements: FlexibleEnumeration = None, connective: Connective = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        connective: Connective = connectives.enumeration if connective is None else connective
        if not is_well_formed_enumeration(phi=elements):
            raise_error(error_code=error_codes.e110, elements_type=type(elements), elements=elements)
        o: tuple = super().__new__(cls, connective=connective, terms=elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None, connective: Connective = None):
        global connectives
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        eb: EnumerationBuilder = EnumerationBuilder(elements=elements)
        connective: Connective = connectives.enumeration if connective is None else connective
        super().__init__(connective=connective, terms=eb)

    def get_element_index(self, phi: FlexibleFormula) -> typing.Optional[int]:
        """Return the index of phi if phi is formula-equivalent with an element of the enumeration, None otherwise.

        Note: not to be confused with get_first_element_index on formulas and tuples.

        This method is not available on formulas because duplicate elements are possible on formulas,
        but are not possible on enumerations. The two methods are algorithmically equivalent but their
        intent is distinct."""
        phi = coerce_formula(phi=phi)
        if self.has_element(phi=phi):
            # two formulas that are formula-equivalent may not be equal.
            # for this reason we must first find the first formula-equivalent element in the enumeration.
            n: int = 0
            for phi_prime in self:
                if is_formula_equivalent(phi=phi, psi=phi_prime):
                    return n
                n = n + 1
        else:
            return None

    def has_element(self, phi: Formula) -> bool:
        """Return True if and only if there exists a formula psi that is an element of the enumeration, and such that
        phi ∼formula psi. False otherwise."""
        phi = coerce_formula(phi=phi)
        return any(is_formula_equivalent(phi=phi, psi=term) for term in self)

    def to_enumeration_builder(self) -> EnumerationBuilder:
        return EnumerationBuilder(elements=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_enumeration_builder()


enumeration = Enumeration
"""A shortcut for Enumeration."""

FlexibleEnumeration = typing.Optional[typing.Union[Enumeration, EnumerationBuilder, typing.Iterable[FlexibleFormula]]]
"""FlexibleEnumeration is a flexible python type that may be safely coerced into an Enumeration or a 
EnumerationBuilder."""


class EmptyEnumeration(Enumeration):
    """An empty-enumeration is an enumeration that has no element.
    """

    def __new__(cls):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        return super().__new__(cls=cls, elements=None)

    def __init__(self):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        super().__init__(elements=None)


class SingletonEnumeration(Enumeration):
    """A singleton-enumeration is an enumeration that has exactly one element.
    """

    def __new__(cls, element: FlexibleFormula):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        element: Formula = coerce_formula(phi=element)
        return super().__new__(cls=cls, elements=(element,))

    def __init__(self, element: FlexibleFormula):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        element: Formula = coerce_formula(phi=element)
        super().__init__(elements=element)


class Transformation(Formula):
    """A formula-transformation, or transformation, is a map from the class of formulas to itself.

    Mathematical definition:
    f:  Phi --> Phi
        phi |-> psi
    Where:
     - Phi is the class of formulas,
     - phi is a formula,
     - psi is a formula.

    Syntactically, a transformation is a formula f(P, c, V) where:
     - f is the transformation connective,
     - P is an enumeration whose children are called premises,
     - c is a formula called the conclusion,
     - V is a enumeration whose children are the variables.

    Algorithm:
    From a transformation, the following algorithm is derived:
    Phi --> psi
    t(Phi) --> psi
    map every formula in Phi collection in-order with the premises
    confirm that they are formula-with-variables-equivalent
    confirm that every variable has strictly one mapped formula
    map all variables with their respective formulas
    return the conclusion by substituting variables with formulas
    # TODO: Transformation: rewrite the above clearly

    Note 1: when a transformation is a theorem, it becomes an inference-rule for that theory.

    Note 2: when a transformation is a theorem, it is very similar to an intuitionistic sequent (cf. Mancosu et al,
    2021, p. 170), i.e.: "In intuitionistic-sequent, there may be at most one formula to the right of ⇒ .", with
    some distinctive properties:
        - a transformation comprises an explicit and finite set of variables,
          while an intuitionistic-sequent uses only formula variables.
        - the order of the premises in a transformation does not matter a priori because it is an enumeration,
          while the order of the formulas in the antecedent of an intuitionistic-sequent matter a priori,
          even though this constraint is immediately relieved by the interchange structural rule.
    """

    def __new__(cls, premises: FlexibleTupl, conclusion: FlexibleFormula,
                variables: FlexibleEnumeration):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        premises: Tupl = coerce_tupl(phi=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(phi=variables)
        o: tuple = super().__new__(cls, connective=connectives.transformation,
                                   terms=(premises, conclusion, variables,))
        return o

    def __init__(self, premises: FlexibleTupl, conclusion: FlexibleFormula,
                 variables: FlexibleEnumeration):
        premises: Tupl = coerce_tupl(phi=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(phi=variables)
        super().__init__(connective=connectives.transformation, terms=(premises, conclusion, variables,))

    def __call__(self, arguments: FlexibleTupl) -> Formula:
        """A shortcut for self.apply_transformation()"""
        return self.apply_transformation(arguments=arguments)

    def apply_transformation(self, arguments: FlexibleTupl) -> Formula:
        """

        :param arguments: A tuple of arguments, whose order matches the order of the transformation premises.
        :return:
        """
        arguments = coerce_tupl(phi=arguments)
        # step 1: confirm every argument is compatible with its premises,
        # and seize the opportunity to retrieve the mapped variable values.
        variables_map: MapBuilder = MapBuilder()
        try:
            is_formula_equivalent_with_variables(phi=arguments, psi=self.premises, variables=self.variables,
                                                 m=variables_map, raise_event_if_false=True)
        except Exception as error:
            raise_error(error_code=error_codes.e117, error=error, arguments=arguments, premises=self.premises,
                        variables=self.variables)

        # step 2:
        outcome: Formula = replace_formulas(phi=self.conclusion, m=variables_map)

        return outcome

    @property
    def conclusion(self) -> Formula:
        return self[1]

    @property
    def premises(self) -> Tupl:
        return self[0]

    @property
    def variables(self) -> Enumeration:
        return self[2]


FlexibleTransformation = typing.Optional[typing.Union[Transformation]]


def coerce_transformation(phi: FlexibleFormula) -> Transformation:
    if isinstance(phi, Transformation):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_transformation(phi=phi):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        return Transformation(premises=phi.term_0, conclusion=phi.term_1, variables=phi.term_2)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Transformation, phi_type=type(phi), phi=phi)


def coerce_inference(phi: FlexibleFormula) -> Inference:
    if isinstance(phi, Inference):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_inference(phi=phi):
        transformation: Transformation = coerce_transformation(phi=phi.term_1)
        return Inference(premises=phi.term_0, transformation_rule=transformation)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Inference, phi_type=type(phi), phi=phi)


def is_well_formed_formula(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed formula, False otherwise.

    Note: the Formula python class assures the well-formedness of formulas.

    :param phi:
    :return: bool
    """
    """Return True if and only if phi is a well-formed formula, False otherwise.

    Note: the Formula python class assures the well-formedness of formulas. Hence, this function is trivial: if
    phi coerces to Formula, it is a well-formed formula.

    :param phi: A formula.
    :return: bool.
    """
    # TODO: review this to avoid raising an exception, but return False instead.
    coerce_formula(phi=phi)
    return True


def is_well_formed_tupl(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed tuple, False otherwise.

    Note: by definition, all formulas are also tuples. Hence, return True if phi converts smoothly to a well-formed
    formula.

    :param phi:
    :return: bool
    """
    # TODO: Tupl.is_well_formed: review this to avoid raising an exception, but return False instead.
    # TODO: Do we want to signal tuples formally with a dedicated connective?
    phi: Formula = coerce_formula(phi=phi)
    return True


def is_well_formed_inference(phi: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed inference, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi = coerce_formula(phi=phi)
    if phi.connective is not connectives.inference or not is_well_formed_enumeration(
            phi=phi.term_0) or not is_well_formed_transformation(phi=phi.term_1):
        return False
    else:
        return True


def is_well_formed_transformation(phi: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed transformation, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi = coerce_formula(phi=phi)
    if (phi.connective is not connectives.transformation or
            phi.arity != 3 or
            not is_well_formed_tupl(phi=phi.term_0) or
            not is_well_formed_formula(phi=phi.term_1) or
            not is_well_formed_enumeration(phi=phi.term_2)):
        return False
    else:
        return True


def is_well_formed_enumeration(phi: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed enumeration, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    if phi is None:
        # Implicit conversion of None to the empty enumeration.
        return True
    else:
        phi = coerce_formula(phi=phi)
        for i in range(0, phi.arity):
            if i != phi.arity - 1:
                for j in range(i + 1, phi.arity):
                    if is_formula_equivalent(phi=phi[i], psi=phi[j]):
                        # We found a pair of duplicates, i.e.: phi_i ~formula phi_j.
                        return False
        return True


def is_well_formed_inference_rule(phi: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed inference-rule, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi = coerce_formula(phi=phi)
    if isinstance(phi, InferenceRule):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif (phi.connective is not connectives.follows_from or
          not phi.arity == 2 or
          not is_well_formed_transformation(phi=phi.term_0) or
          phi.term_1.connective is not connectives.inference_rule):
        return False
    else:
        return True


def is_valid_statement_with_regard_to_theory(phi: FlexibleFormula, t: FlexibleTheory) -> bool:
    """Return True if formula phi is a valid-statement with regard to theory t, False otherwise.

    A formula phi is a valid-statement with regard to a theory t, if and only if:
     - phi is the valid-statement of an axiom in t,
     - or phi is the valid-statement of a theorem in t.
    """
    return any(is_formula_equivalent(phi=phi, psi=valid_statement) for valid_statement in t.iterate_valid_statements())


def is_well_formed_axiom(phi: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed axiom, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi = coerce_formula(phi=phi)
    if phi.arity != 2:
        return False
    if phi.connective is not connectives.follows_from:
        return False
    if not is_well_formed_formula(phi=phi.term_0):
        return False
    if phi.term_1.arity != 0:
        return False
    if phi.term_1.connective != connectives.axiom:
        return False
    # All tests were successful.
    return True


def is_well_formed_theorem(phi: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed theorem, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi = coerce_formula(phi=phi)
    if isinstance(phi, Theorem):
        # the Theorem python-type assure the well-formedness of the object.
        return True
    if (phi.connective is not connectives.follows_from or
            not phi.arity == 2 or
            not is_well_formed_formula(phi=phi.term_0) or
            not is_well_formed_inference(phi=phi.term_1)):
        return False
    else:
        i: Inference = coerce_inference(phi=phi.term_1)
        f_of_p: Formula = i.transformation_rule(i.premises)
        if not is_formula_equivalent(phi=phi.term_0, psi=f_of_p):
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            # issue a warning to facilitate troubleshooting and analysis.
            raise_error(error_code=error_codes.e106, phi=phi, psi_expected=phi.term_0, psi_inferred=f_of_p,
                        inference_rule=i)
            return False
        return True


def is_well_formed_derivation(phi: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed theorem, False otherwise.

    :param phi: A formula.
    :return: bool.
    """
    phi: Formula = coerce_formula(phi=phi)
    if is_well_formed_theorem(phi=phi):
        return True
    elif is_well_formed_inference_rule(phi=phi):
        return True
    elif is_well_formed_axiom(phi=phi):
        return True
    else:
        return False


def is_well_formed_theory(phi: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
    """Return True if phi is a well-formed theory, False otherwise.

    :param phi: A formula.
    :param raise_event_if_false:
    :return: bool.
    """
    phi = coerce_enumeration(phi=phi)

    if isinstance(phi, Theory):
        # the Derivation class assure the well-formedness of the theory.
        return True

    # check the well-formedness of the individual derivations.
    # and retrieve the terms claimed as proven in the theory, preserving order.
    # by the definition of a theory, these are the left term (term_0) of the formulas.
    valid_statements: TuplBuilder = TuplBuilder(elements=None)
    derivations: TuplBuilder = TuplBuilder(elements=None)
    for derivation in phi:
        if not is_well_formed_derivation(phi=derivation):
            return False
        else:
            derivation: Derivation = coerce_derivation(phi=derivation)
            derivations.append(term=derivation)
            # retrieve the formula claimed as valid from the theorem
            valid_statement: Formula = derivation.valid_statement
            valid_statements.append(term=valid_statement)
    # now that the derivations and valid_statements have been retrieved, and proved well-formed individually,
    # make the python objects immutable.
    derivations: Tupl = derivations.to_tupl()
    valid_statements: Tupl = valid_statements.to_tupl()
    for i in range(0, derivations.arity):
        derivation = derivations[i]
        valid_statement = valid_statements[i]
        if is_well_formed_axiom(phi=derivation):
            # This is an axiom.
            derivation: Axiom = coerce_axiom(phi=derivation)
            pass
        elif is_well_formed_inference_rule(phi=derivation):
            # This is an inference-rule.
            derivation: InferenceRule = coerce_inference_rule(phi=derivation)
            pass
        elif is_well_formed_theorem(phi=derivation):
            theorem_by_inference: Theorem = coerce_theorem(phi=derivation)
            inference: Inference = theorem_by_inference.i
            for premise in inference.premises:
                # check that premise is a proven-formula (term_0) of a predecessor
                if not valid_statements.has_element(phi=premise):
                    # The premise is absent from the theory
                    if raise_event_if_false:
                        raise_error(error_code=error_codes.e111, premise=premise, premise_index=i,
                                    theorem=derivation,
                                    valid_statement=valid_statement)
                    return False
                else:
                    premise_index = valid_statements.get_index_of_first_equivalent_element(phi=premise)
                    if premise_index >= i:
                        # The premise is not positioned before the conclusion.
                        if raise_event_if_false:
                            raise_error(error_code=error_codes.e112, premise=premise, premise_index=i,
                                        theorem=derivation,
                                        valid_statement=valid_statement)
                        return False
            if not valid_statements.has_element(phi=inference.transformation_rule):
                # The inference transformation-rule is absent from the theory.
                if raise_event_if_false:
                    raise_error(error_code=error_codes.e119, transformation_rule=inference.transformation_rule,
                                inference=inference, premise_index=i, theorem=derivation,
                                valid_statement=valid_statement)
                return False
            else:
                transformation_index = valid_statements.get_index_of_first_equivalent_element(
                    phi=inference.transformation_rule)
                if transformation_index >= i:
                    # The transformation is not positioned before the conclusion.
                    return False
            # And finally, confirm that the inference effectively yields phi.
            phi_prime = inference.transformation_rule.apply_transformation(arguments=inference.premises)
            if not is_formula_equivalent(phi=valid_statement, psi=phi_prime):
                return False
        else:
            # Incorrect form.
            return False
    # All tests were successful.
    return True


def is_well_formed_axiomatization(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed axiomatization, False otherwise."""
    phi = coerce_formula(phi=phi)
    if phi.connective is not connectives.axiomatization:
        return False
    for element in phi:
        if not is_well_formed_axiom(phi=element) and not is_well_formed_inference_rule(phi=element):
            return False
    return True


def coerce_derivation(phi: FlexibleFormula) -> Derivation:
    """Validate that p is a well-formed theorem and returns it properly typed as Proof, or raise exception e123.

    :param phi:
    :return:
    """
    phi = coerce_formula(phi=phi)
    if is_well_formed_theorem(phi=phi):
        return coerce_theorem(phi=phi)
    elif is_well_formed_inference_rule(phi=phi):
        return coerce_inference_rule(phi=phi)
    elif is_well_formed_axiom(phi=phi):
        return coerce_axiom(phi=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Derivation, phi_type=type(phi), phi=phi)


def coerce_axiom(phi: FlexibleFormula) -> Axiom:
    """Validate that p is a well-formed axiom and returns it properly typed as an instance of Axiom,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Axiom):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_axiom(phi=phi):
        proved_formula: Formula = phi.term_0
        return Axiom(valid_statement=proved_formula)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=InferenceRule, phi_type=type(phi), phi=phi)


def coerce_inference_rule(phi: FlexibleFormula) -> InferenceRule:
    """Validate that p is a well-formed inference-rule and returns it properly typed as an instance of InferenceRule,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, InferenceRule):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_inference_rule(phi=phi):
        transfo: Transformation = coerce_transformation(phi=phi.term_0)
        return InferenceRule(transformation=transfo)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=InferenceRule, phi_type=type(phi), phi=phi)


def coerce_theorem(phi: FlexibleFormula) -> Theorem:
    """Validate that p is a well-formed theorem-by-inference and returns it properly typed as ProofByInference,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Theorem):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_theorem(phi=phi):
        proved_formula: Formula = coerce_formula(phi=phi.term_0)
        inference: Inference = coerce_inference(phi=phi.term_1)
        return Theorem(valid_statement=proved_formula, i=inference)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Theorem, phi_type=type(phi), phi=phi)


def coerce_theory(phi: FlexibleTheory) -> Theory:
    """Validate that phi is a well-formed theory and returns it properly typed as Demonstration,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Theory):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_theory(phi=phi):
        return Theory(derivations=phi)
    elif phi is None:
        return Theory(derivations=None)
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(derivations=tuple(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(derivations=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Theory, phi_type=type(phi), phi=phi)


def coerce_axiomatization(phi: FlexibleFormula) -> Axiomatization:
    """Validate that phi is a well-formed axiomatization and returns it properly typed as Axiomatization,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Axiomatization):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_axiomatization(phi=phi):
        return Axiomatization(derivations=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Axiomatization, phi_type=type(phi), phi=phi)


class TheoryState(Enumeration):
    """A theory-state is an enumeration of formulas."""

    def __new__(cls, elements: FlexibleEnumeration = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, elements=elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None):
        super().__init__(elements=elements)


class Derivation(Formula):
    """A derivation has two definitions: a local definition with regard to a theory t, and a global definition.

    Local definition (with regard to a theory t):
    A well-formed derivation s with regard to a theory t is a formula that is:
     - a term of theory t,
     - a well-formed (global) derivation,
     - and whose justification with regard to theory t is a proper-justification.

    Global definition:
    A well-formed derivation s is a formula of the form:
     - phi follows-from psi,
    where:
     - phi is a formula,
     - follows-from is the derivation connector,
     - and psi is a proper-justification.

    There are three mutually exclusive categories of derivations:
     - axioms,
     - inference-rules,
     - theorems.

    See their respective definitions for the local and global definitions of proper-justification.
    """

    def __new__(cls, valid_statement: FlexibleFormula, justification: FlexibleFormula):
        valid_statement = coerce_formula(phi=valid_statement)
        justification = coerce_formula(phi=justification)
        c: Connective = connectives.follows_from
        o: tuple = super().__new__(cls, connective=c, terms=(valid_statement, justification,))
        return o

    def __init__(self, valid_statement: FlexibleFormula, justification: FlexibleFormula):
        self._valid_statement = coerce_formula(phi=valid_statement)
        self._justification = coerce_formula(phi=justification)
        c: Connective = connectives.follows_from
        super().__init__(connective=c, terms=(self._valid_statement, self._justification,))

    @property
    def valid_statement(self) -> Formula:
        """Return the formula claimed as valid by the theorem.

        This is equivalent to phi.term_0.

        :return: A formula.
        """
        return self._valid_statement

    @property
    def justification(self) -> Formula:
        return self._justification


class Axiom(Derivation):
    """An axiom has two definitions: a local definition with regard to a theory t, and a global definition.

    Intuitive definition:
    An axiom is a statement that unconditionally justifies a statement.

    Local definition (with regard to a theory t):
    An axiom is a derivation with regard to a theory t if and only if:
     - it is a term of theory t,
     - it is a well-formed (global) axiom.

     Global definition:
     An axiom is a well-formed derivation if and only if:
      - it is a formula of the form phi follows-from axiom
     where:
      - phi is a formula,
      - follows-from is the derivation connective,
      - axiom it the axiom connective.

    TODO: An axiom may be viewed as an inference-rule without premises. Thus, Axiom could derive from InferenceRule.

    """

    def __new__(cls, valid_statement: FlexibleFormula = None):
        valid_statement: Formula = coerce_formula(phi=valid_statement)
        o: tuple = super().__new__(cls, valid_statement=valid_statement, justification=connectives.axiom)
        return o

    def __init__(self, valid_statement: FlexibleFormula):
        valid_statement: Formula = coerce_formula(phi=valid_statement)
        super().__init__(valid_statement=valid_statement, justification=connectives.axiom)


FlexibleAxiom = typing.Union[Axiom, Formula]


class InferenceRule(Derivation):
    """A well-formed inference-rule is a theorem that justifies the derivation of theorems in a theory,
    under certain conditions called premises.

    Syntactic definition:
    A formula is a well-formed inference-rule if and only if it is of the form:
        phi follows-from psi
    Where:
        - phi is a well-formed transformation, called the inference-rule,
        - psi is the inference-rule urelement,
        - follows-from is the follows-from binary connective.

    Semantic definition:
    An inference-rule is the statement that a transformation is a valid inference-rule in a theory,
    i.e.: all formulas derived from that inference-rule are valid in the theory.

    Note: if an inference-rule has no premises, it is equivalent to an axiom.

    """

    def __new__(cls, transformation: FlexibleTransformation = None):
        transformation: Transformation = coerce_transformation(phi=transformation)
        o: tuple = super().__new__(cls, valid_statement=transformation, justification=connectives.inference_rule)
        return o

    def __init__(self, transformation: FlexibleTransformation):
        self._transformation: Transformation = coerce_transformation(phi=transformation)
        super().__init__(valid_statement=self._transformation, justification=connectives.inference_rule)

    @property
    def transformation(self) -> Transformation:
        return self._transformation


FlexibleInferenceRule = typing.Union[InferenceRule, Formula]


class Inference(Formula):
    """An inference is the description of a usage of an inference-rule.

    Syntactic definition:
    An inference is a formula of the form:
        inference(P, f)
    Where:
        - inference is the inference connective,
        - P is an enumeration called the premises,
        - f is a transformation called the inference-rule.

    Semantic definition:
    An inference is a formal description of one usage of an inference-rule."""

    def __new__(cls, premises: FlexibleTupl, transformation_rule: FlexibleTransformation):
        premises: Tupl = coerce_tupl(phi=premises)
        transformation_rule: Transformation = coerce_transformation(phi=transformation_rule)
        c: Connective = connectives.inference
        o: tuple = super().__new__(cls, connective=c, terms=(premises, transformation_rule,))
        return o

    def __init__(self, premises: FlexibleTupl, transformation_rule: FlexibleTransformation):
        self._premises: Tupl = coerce_tupl(phi=premises)
        self._transformation_rule: Transformation = coerce_transformation(phi=transformation_rule)
        c: Connective = connectives.inference
        super().__init__(connective=c, terms=(self._premises, self._transformation_rule,))

    @property
    def transformation_rule(self) -> Transformation:
        """The inference-rule of the inference."""
        return self._transformation_rule

    @property
    def premises(self) -> Tupl:
        """The premises of the inference."""
        return self._premises


FlexibleInference = typing.Optional[typing.Union[Inference]]


class Theorem(Derivation):
    """A theorem-by-inference is a theorem that is proven by inference.

    Syntactic definition:
    A formula is a well-formed theorem-by-inference if and only if it is a formula of the form:
        phi follows-from inference(P, f)
    Where:
        - phi is a well-formed formula,
        - follows-from is the follows-from connective,
        - inference is the inference binary connective,
        - P is a tuple of well-formed formulas called the premises,
        - f is a transformation,
        - f(P) = phi.

    Semantic definition:
    A theorem-by-inference is a statement that justifies the validity of phi by providing the premises and
    the transformation-rule that yield phi, i.e.:
    t(P) ~formula phi
    """

    def __new__(cls, valid_statement: FlexibleFormula, i: FlexibleInference):
        valid_statement: Formula = coerce_formula(phi=valid_statement)
        i: Inference = coerce_inference(phi=i)
        o: tuple = super().__new__(cls, valid_statement=valid_statement, justification=i)
        return o

    def __init__(self, valid_statement: FlexibleFormula, i: FlexibleInference):
        self._phi: Formula = coerce_formula(phi=valid_statement)
        self._i: Inference = coerce_inference(phi=i)
        # check the validity of the theorem
        f_of_p: Formula = i.transformation_rule(i.premises)
        try:
            is_formula_equivalent(phi=valid_statement, psi=f_of_p, raise_event_if_false=True)
        except CustomException as error:
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            # raise an exception to prevent the creation of this ill-formed theorem-by-inference.
            raise_error(error_code=error_codes.e105, error=error, valid_statement=valid_statement,
                        algorithm_output=f_of_p,
                        inference=i)
        super().__init__(valid_statement=valid_statement, justification=i)

    @property
    def i(self) -> Inference:
        """The inference of the theorem."""
        return self._i

    @property
    def phi(self) -> Formula:
        """The proven formula."""
        return self._phi


FlexibleTheorem = typing.Union[Theorem, Formula]
FlexibleDerivation = typing.Union[FlexibleAxiom, FlexibleTheorem, FlexibleInferenceRule]


class Theory(Enumeration):
    """A theory is a justified enumeration of axioms, inference-rules, and theorems.

    Syntactic definition:
    A well-formed theory is an enumeration such that:
     - all element phi of the enumeration is a well-formed theorem,
     - all premises of all theorem-by-inferences are predecessors of their parent theorem-by-inference.

    TODO: Consider the following data-model change: a derivation is only an axiom or an inference-rule. In
    effect, stating that in inference-rule is a derivation seems to be a bit of a semantic stretch.

    """

    # TODO: Theory does not contain typed axioms, inference-rules, etc. but formulas!!!!!!

    def __new__(cls, connective: typing.Optional[Connective] = None, derivations: FlexibleEnumeration = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(phi=derivations)
        # use coerce_derivation() to assure that every derivation is properly types as Axiom, InferenceRule or Theorem.
        derivations: Enumeration = coerce_enumeration(
            phi=(coerce_derivation(phi=p) for p in derivations))
        try:
            is_well_formed_theory(phi=derivations, raise_event_if_false=True)

        except Exception as error:
            # well-formedness verification failure, the theorem is ill-formed.
            raise_error(error_code=error_codes.e120, error=error, derivations=derivations)
        o: tuple = super().__new__(cls, elements=derivations)
        return o

    def __init__(self, connective: typing.Optional[Connective] = None, derivations: FlexibleEnumeration = None):
        if connective is None:
            connective: Connective = connectives.theory
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(phi=derivations)
        # coerce all elements of the enumeration to theorem
        derivations: Enumeration = coerce_enumeration(
            phi=(coerce_derivation(phi=p) for p in derivations))
        super().__init__(connective=connective, elements=derivations)

    @property
    def axioms(self) -> Enumeration:
        """Return an enumeration of all axioms in the theory.

        Note: order is preserved."""
        return Enumeration(elements=tuple(self.iterate_axioms()))

    @property
    def valid_statements(self) -> Enumeration:
        """Return an enumeration of all axiom and theorem valid-statements in the theory, preserving order."""
        python_tuple: tuple = tuple(self.iterate_valid_statements())
        e: Enumeration = Enumeration(elements=python_tuple)
        return e

    @property
    def inference_rules(self) -> Enumeration:
        """Return an enumeration of all inference-rules in the theory, preserving order, filtering out axioms and
        theorems."""
        return Enumeration(elements=tuple(self.iterate_inference_rules()))

    def iterate_axioms(self) -> typing.Iterator[Axiom]:
        """Iterates over all axioms in the theory, preserving order, filtering out inference-rules and theorems."""
        for element in self:
            if isinstance(element, Axiom):
                yield element

    def iterate_valid_statements(self) -> typing.Iterator[Formula]:
        """Iterates over all axiom and theorem valid-statements in the theory, preserving order."""
        for derivation in self.iterate_derivations():
            if isinstance(derivation, Axiom):
                derivation: Axiom
                yield derivation.valid_statement
            elif isinstance(derivation, Theorem):
                derivation: Theorem
                yield derivation.valid_statement

    def iterate_inference_rules(self) -> typing.Iterator[InferenceRule]:
        """Iterates over all inference-rules in the theory, preserving order, filtering out axioms and theorems."""
        for element in self:
            if isinstance(element, InferenceRule):
                yield element

    def iterate_theorems(self) -> typing.Iterator[Theorem]:
        """Iterates over all theorems in the theory, preserving order, filtering out axioms and inference-rules."""
        for element in self:
            if isinstance(element, Theorem):
                yield element

    def iterate_derivations(self) -> typing.Iterator[Derivation]:
        """Iterates over all derivations, preserving order"""
        for element in self:
            yield element

    @property
    def derivations(self) -> Enumeration:
        """Return an enumeration of all derivations in the theory, preserving order."""
        return Enumeration(elements=tuple(self.iterate_derivations()))

    @property
    def theorems(self) -> Enumeration:
        """Return an enumeration of all theorems in the theory, preserving order, filtering out axioms and
        inference-rules."""
        return Enumeration(elements=tuple(self.iterate_theorems()))


FlexibleTheory = typing.Optional[
    typing.Union[Theory, typing.Iterable[FlexibleDerivation]]]
"""FlexibleTheory is a flexible python type that may be safely coerced into a Theory."""


class Axiomatization(Theory):
    """An axiomatization is a theory that is only composed of axioms,
    and/or inference-rules.

    Syntactic definition:
    A well-formed axiomatization is an enumeration such that:
     - all element phi of the enumeration is a well-formed axiom or an inference-rule.

    """

    def __new__(cls, derivations: FlexibleEnumeration = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(phi=derivations)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_derivations: Enumeration = Enumeration(elements=None)
        for derivation in derivations:
            if is_well_formed_inference_rule(phi=derivation):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(phi=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, inference_rule,))
            elif is_well_formed_axiom(phi=derivation):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(phi=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, axiom,))
            else:
                # Incorrect form.
                raise_error(error_code=error_codes.e123, phi=derivation, phi_type_1=InferenceRule,
                            phi_type_2=Axiom)
        o: tuple = super().__new__(cls, derivations=coerced_derivations)
        return o

    def __init__(self, derivations: FlexibleEnumeration = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(phi=derivations)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_derivations: Enumeration = Enumeration(elements=None)
        for derivation in derivations:
            if is_well_formed_inference_rule(phi=derivation):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(phi=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, inference_rule,))
            elif is_well_formed_axiom(phi=derivation):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(phi=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, axiom,))
            else:
                # Incorrect form.
                raise_error(error_code=error_codes.e123, phi=derivation, phi_type_1=InferenceRule,
                            phi_type_2=Axiom)
        super().__init__(connective=connectives.axiomatization, derivations=coerced_derivations)


def is_leaf_formula(phi: FlexibleFormula) -> bool:
    """Return True if phi is a leaf formula, False otherwise.

    A formula phi is a leaf-formula if and only if phi has arity 0,
    or equivalently if it has no terms.

    :param phi:
    :return: True if phi is a leaf formula, False otherwise.
    :rtype: bool
    """
    phi = coerce_formula(phi=phi)
    return phi.arity == 0


def get_leaf_formulas(phi: FlexibleFormula, eb: EnumerationBuilder = None) -> Enumeration:
    """Return the enumeration of leaf-formulas in phi.

    Note: if phi is a leaf-formula, return phi.

    :param phi:
    :param eb: (conditional) An enumeration-builder for recursive call.
    :return:
    """
    phi: Formula = coerce_formula(phi=phi)
    if eb is None:
        eb: EnumerationBuilder = EnumerationBuilder(elements=None)
    if not eb.has_element(phi=phi) and is_leaf_formula(phi=phi):
        eb.append(term=phi)
    else:
        for term in phi:
            # Recursively call get_leaf_formulas,
            # which complete eb with any remaining leaf formulas.
            get_leaf_formulas(phi=term, eb=eb)
    e: Enumeration = eb.to_enumeration()
    return e


def get_formula_depth(phi: FlexibleFormula) -> int:
    """The depth of a formula is the number of sub-formula layers it has.

    :param phi:
    :return:
    """
    phi = coerce_formula(phi=phi)
    if phi.arity == 0:
        return 1
    else:
        return max(get_formula_depth(phi=term) for term in phi) + 1


def extend_theory(*args, t: FlexibleTheory) -> Theory:
    """

    :param args:
    :param t:
    :return:
    """
    t = coerce_theory(phi=t)
    if args is None:
        return t
    else:
        for argument in args:
            if is_well_formed_theory(phi=argument):
                # recursively append all derivations of t2 in t
                t2: Theory = coerce_theory(phi=argument)
                for d in t2.derivations:
                    t: Theory = extend_theory(d, t=t)
            elif is_well_formed_axiom(phi=argument):
                a: Axiom = coerce_axiom(phi=argument)
                if not is_axiom_of_theory(a=a, t=t):
                    t: Theory = Theory(derivations=(*t, a,))
            elif is_well_formed_inference_rule(phi=argument):
                ir: InferenceRule = coerce_inference_rule(phi=argument)
                if not is_inference_rule_of_theory(ir=ir, t=t):
                    t: Theory = Theory(derivations=(*t, ir,))
            elif is_well_formed_theorem(phi=argument):
                thrm: Theorem = coerce_theorem(phi=argument)
                if not is_theorem_of_theory(thrm=thrm, t=t):
                    t: Theory = Theory(derivations=(*t, thrm,))
            else:
                raise ValueError(f'Invalid argument: ({type(argument)}) {argument}.')
        return t


def translate_implication_to_axiom(phi: FlexibleFormula) -> InferenceRule:
    """Given a propositional formula phi that is an implication,
    translates phi to an equivalent axiomatic-system-1 inference-rule.

    Note: the initial need was to translate the original axioms of minimal-logic-1.

    :param phi:
    :return:
    """
    phi = coerce_formula(phi=phi)
    if phi.connective is not connectives.implies:
        raise Exception('this is not an implication')
    # TODO: translate_implication_to_axiom: check that all sub-formulas in phi are either:
    # - valid propositional formulas (negation, conjunction, etc.)
    # - atomic elements that can be mapped to propositional variables

    # Now we have the assurance that phi is a well-formed propositional formula.
    # Retrieve the list of propositional-variables in phi:
    propositional_variables: Enumeration = get_leaf_formulas(phi=phi)
    premises: EnumerationBuilder = EnumerationBuilder(elements=None)
    variables_map: MapBuilder = MapBuilder(domain=None, codomain=None)
    for x in propositional_variables:
        rep: str = x.typeset_as_string() + '\''
        # automatically append the axiom: x is-a propositional-variable
        with let_x_be_a_propositional_variable_OBSOLETE(rep=rep) as x2:
            premises.append(term=x2 | connectives.is_a | connectives.propositional_variable)
            variables_map.set_pair(phi=x, psi=x2)
    variables_map: Map = variables_map.to_map()
    variables: Enumeration = Enumeration(elements=variables_map.codomain)

    # elaborate a new formula psi where all variables have been replaced with the new variables
    psi = replace_formulas(phi=phi, m=variables_map)

    # translate the antecedent of the implication to the main premises
    # note: we could further split conjunctions into multiple premises
    antecedent: Formula = psi.term_0
    premises.append(term=antecedent)

    # retrieve the conclusion
    conclusion: Formula = psi.term_1

    # build the rule
    rule: Transformation = Transformation(premises=premises, conclusion=conclusion,
                                          variables=variables)

    # build the inference-rule
    inference_rule: InferenceRule = InferenceRule(transformation=rule)

    return inference_rule


class AutoDerivationFailure(Exception):
    """Auto-derivation was required but failed to succeed."""

    def __init__(self, msg: str, **kwargs):
        super().__init__(msg)
        self.kwargs = kwargs


def derive(theory: FlexibleTheory, valid_statement: FlexibleFormula, premises: FlexibleTupl,
           inference_rule: FlexibleInferenceRule) -> typing.Tuple[Theory, Theorem]:
    """Given a theory t, derives a new theory t2 that extends t with a new theorem by applying an inference-rule.

    :param valid_statement:
    :param theory:
    :param premises:
    :param inference_rule:
    :return:
    """
    # parameters validation
    theory: Theory = coerce_theory(phi=theory)
    valid_statement: Formula = coerce_formula(phi=valid_statement)
    premises: Tupl = coerce_tupl(phi=premises)
    inference_rule: InferenceRule = coerce_inference_rule(phi=inference_rule)

    for premise in premises:
        if not theory.has_element(phi=premise):
            # the premise is missing from the theory
            # trigger auto-derivations
            pass
            # try:
            #    theory = auto_derive(theory=theory, valid_statement=premise)
            # except AutoDerivationFailure:
            #    raise DerivationFailure()

    # configure the inference
    inference: Inference = Inference(premises=premises, transformation_rule=inference_rule.transformation)

    # derive the new theorem
    theorem: Theorem = Theorem(valid_statement=valid_statement, i=inference)

    # extends the theory
    theory: Theory = Theory(derivations=(*theory, theorem,))

    u1.log_info(theorem.typeset_as_string())

    return theory, theorem


def is_in_formula_tree(phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Return True if phi is formula-equivalent to psi or a sub-formula of psi."""
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    if is_formula_equivalent(phi=phi, psi=psi):
        return True
    else:
        for term in psi:
            if is_in_formula_tree(phi=phi, psi=term):
                return True
    return False


def auto_derive_1(t: FlexibleTheory, phi: FlexibleFormula) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """Try to automatically derive phi as a valid-statement from t, without specifying the premises and inference-rule,
    enriching t with new theorems as necessary to demonstrate phi.

    auto_derive_1 is a very limited algorithm that will not recursively attempt to derive phi. It is assumed that
    phi can be automatically derived in a single step. It may be considered as a shortcut to perform step by step
    derivations, avoiding the necessity to expressly mention all premises.
    """
    t = coerce_theory(phi=t)
    phi = coerce_formula(phi=phi)

    if is_valid_statement_with_regard_to_theory(phi=phi, t=t):
        # phi is already a valid-statement with regard to t,
        # no complementary derivation is necessary.

        for derivation in t.iterate_derivations():
            if is_formula_equivalent(phi=phi, psi=derivation.valid_statement):
                return t, True, derivation
        raise AutoDerivationFailure('Inconsistent behavior during auto-derivation')
    else:
        # phi is not a valid-statement with regard to t,
        # thus it may be possible to derive phi with complementary theorems in t.

        # find the inference-rules in t that could derive phi.
        # these are the inference-rules whose conclusions are formula-equivalent-with-variables to phi.
        # ir_list = list(t.inference_rules)
        # random.shuffle(ir_list)
        # for ir in ir_list:
        for ir in t.iterate_inference_rules():
            ir_success: bool = True
            ir: InferenceRule
            u1.log_info(f'\tinference-rule: {ir.transformation}')
            transfo: Transformation = ir.transformation
            if is_formula_equivalent_with_variables(phi=phi, psi=transfo.conclusion, variables=transfo.variables):
                # this inference-rule may potentially yield target phi as a valid-statement,

                # we want to list what would be the required premises to yield phi.
                # for this we need to "reverse-engineer" the inference-rule.

                # first we should determine what are the necessary variable values in the transformation.
                # to do this, we have a trick, we can call is_formula_equivalent_with_variables and pass it
                # an empty map-builder:
                m: MapBuilder = MapBuilder()
                is_formula_equivalent_with_variables(phi=phi, psi=transfo.conclusion, variables=transfo.variables,
                                                     m=m)

                # now that we know what are the necessary variable values, we can determine what
                # are the necessary premises by substituting the variable values.
                necessary_premises: EnumerationBuilder = EnumerationBuilder(elements=None)
                for original_premise in transfo.premises:
                    necessary_premise = replace_formulas(phi=original_premise, m=m)
                    necessary_premises.append(term=necessary_premise)
                necessary_premises: Enumeration = necessary_premises.to_enumeration()

                # now that we have a list of necessary premises,
                # we can recursively auto-derive these premises.
                for necessary_premise in necessary_premises:
                    if not is_valid_statement_with_regard_to_theory(phi=necessary_premise, t=t):
                        ir_success = False

                if ir_success:
                    # if we reach this, it means that all necessary premises
                    # are either already present in the theory, or were successfully auto-derived recursively.
                    # in consequence, we can now safely derive phi.
                    t, derivation = derive(theory=t, valid_statement=phi, premises=necessary_premises,
                                           inference_rule=ir)
                    return t, True, derivation
                else:
                    # u1.log_info(f'\tir was not conclusive: {ir.transformation}')
                    # ir_success = False
                    pass
            else:
                # the conclusion of this inference-rule is not interesting
                # u1.log_info(f'\tir has not interesting conclusion: {ir.transformation}')
                # ir_success = False
                pass

        if not is_valid_statement_with_regard_to_theory(phi=phi, t=t):
            # we recursively tried to derive phi using all the inference-rules in the theory.
            # it follows that we are unable to derive phi.
            return t, False, None
        else:
            for derivation in t.iterate_derivations():
                if is_formula_equivalent(phi=phi, psi=derivation.valid_statement):
                    return t, True, derivation
            raise AutoDerivationFailure('Inconsistent behavior during auto-derivation')


auto_derivation_max_formula_depth_preference = 4


def auto_derive_2(t: FlexibleTheory, phi: FlexibleFormula) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    global auto_derivation_max_formula_depth_preference
    max_formula_depth = 3
    while max_formula_depth <= auto_derivation_max_formula_depth_preference:
        u1.log_info(f'\tauto-derive max_formula_depth {max_formula_depth}.')

        t, success, derivation, = _auto_derive_2(t=t, phi=phi, premise_exclusion_list=None,
                                                 max_formula_depth=max_formula_depth)
        if not success:
            max_formula_depth = max_formula_depth + 1
        else:
            return t, success, derivation
    u1.log_info(f'\tstop max_formula_depth {max_formula_depth}.')
    return t, False, None


def _auto_derive_2(t: FlexibleTheory, phi: FlexibleFormula, premise_exclusion_list: FlexibleEnumeration = None,
                   max_formula_depth: int = 1) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """Try to automatically derive phi as a valid-statement from t, without specifying the premises and inference-rule,
    enriching t with new theorems as necessary to demonstrate phi.

    Raise an AutoDerivationFailure if the derivation is not successful.
    """
    u1.log_info(f'auto-derivation target: max-depth:{max_formula_depth} {phi}')
    if get_formula_depth(phi=phi) > max_formula_depth:
        u1.log_info(f'\tmax-depth reached, postponing search to next iteration.')
        return t, False, None
    if premise_exclusion_list is None:
        premise_exclusion_list: EnumerationBuilder = EnumerationBuilder(elements=None)

    if premise_exclusion_list.has_element(phi=phi):
        return t, False, None

    # append phi to the exclusion list of premises,
    # to avoid circular attempts to auto-derive theorems.
    premise_exclusion_list.append(term=phi)

    if is_valid_statement_with_regard_to_theory(phi=phi, t=t):
        # phi is already a valid-statement with regard to t,
        # no complementary derivation is necessary.

        for derivation in t.iterate_derivations():
            if is_formula_equivalent(phi=phi, psi=derivation.valid_statement):
                return t, True, derivation
        raise AutoDerivationFailure('Inconsistent behavior during auto-derivation')
    else:
        # phi is not a valid-statement with regard to t,
        # thus it may be possible to derive phi with complementary theorems in t.

        # find the inference-rules in t that could derive phi.
        # these are the inference-rules whose conclusions are formula-equivalent-with-variables to phi.
        # ir_list = list(t.inference_rules)
        # random.shuffle(ir_list)
        # for ir in ir_list:
        for ir in t.iterate_inference_rules():
            ir_success: bool = True
            ir: InferenceRule
            u1.log_info(f'\tinference-rule: {ir.transformation}')
            transfo: Transformation = ir.transformation
            if any(is_in_formula_tree(phi=variable, psi=phi) for variable in transfo.variables):
                u1.log_info(f'\tsome variable is present in the target {phi}')
                ir_success = False
            elif is_formula_equivalent_with_variables(phi=phi, psi=transfo.conclusion, variables=transfo.variables):
                # this inference-rule may potentially yield a valid-statement,
                # that would be formula-equivalent to phi.
                # u1.log_info(f'\t\t good candidate')

                # we want to list what would be the required premises to yield phi.
                # for this we need to "reverse-engineer" the inference-rule.

                # first we should determine what are the necessary variable values in the transformation.
                # to do this, we have a trick, we can call is_formula_equivalent_with_variables and pass it
                # an empty map-builder:
                m: MapBuilder = MapBuilder()
                is_formula_equivalent_with_variables(phi=phi, psi=transfo.conclusion, variables=transfo.variables,
                                                     m=m)

                # now that we know what are the necessary variable values, we can determine what
                # are the necessary premises by substituting the variable values.
                necessary_premises: EnumerationBuilder = EnumerationBuilder(elements=None)
                for original_premise in transfo.premises:
                    necessary_premise = replace_formulas(phi=original_premise, m=m)
                    necessary_premises.append(term=necessary_premise)
                necessary_premises: Enumeration = necessary_premises.to_enumeration()

                # now that we have a list of necessary premises,
                # we can recursively auto-derive these premises.
                for necessary_premise in necessary_premises:
                    # u1.log_info(f'\t\t\t necessary_premise: {necessary_premise}')

                    necessary_premise_success: bool = False
                    t, necessary_premise_success, _ = _auto_derive_2(t=t, phi=necessary_premise,
                                                                     premise_exclusion_list=premise_exclusion_list,
                                                                     max_formula_depth=max_formula_depth)
                    if not necessary_premise_success:
                        ir_success = False

                if ir_success:
                    # if we reach this, it means that all necessary premises
                    # are either already present in the theory, or were successfully auto-derived recursively.
                    # in consequence, we can now safely derive phi.
                    # u1.log_info(f'\twe should now be able to derive: {phi}')
                    # u1.log_info(f'\t\twith necessary_premises: {necessary_premises}')
                    # u1.log_info(f'\t\t and inference-rule: {ir}')
                    t, derivation = derive(theory=t, valid_statement=phi, premises=necessary_premises,
                                           inference_rule=ir)
                    # u1.log_info(f'\t auto-derivation success: {derivation}')
                    return t, True, derivation
                else:
                    # u1.log_info(f'\tir was not conclusive: {ir.transformation}')
                    ir_success = False
            else:
                # the conclusion of this inference-rule is not interesting
                # u1.log_info(f'\tir has not interesting conclusion: {ir.transformation}')
                ir_success = False

        if not is_valid_statement_with_regard_to_theory(phi=phi, t=t):
            # we recursively tried to derive phi using all the inference-rules in the theory.
            # it follows that we are unable to derive phi.
            return t, False, None
        else:
            for derivation in t.iterate_derivations():
                if is_formula_equivalent(phi=phi, psi=derivation.valid_statement):
                    return t, True, derivation
            raise AutoDerivationFailure('Inconsistent behavior during auto-derivation')


# PRESENTATION LAYER


class ClassicalFormulaTypesetter(pl1.Typesetter):
    def __init__(self, connective_typesetter: pl1.Typesetter):
        super().__init__()
        connective_typesetter = pl1.coerce_typesetter(ts=connective_typesetter)
        self._connective_typesetter: pl1.Typesetter = connective_typesetter

    @property
    def connective_typesetter(self) -> pl1.Typesetter:
        """The typesetter for the connective's representation."""
        return self._connective_typesetter

    @connective_typesetter.setter
    def connective_typesetter(self, ts: pl1.FlexibleTypesetter):
        self._connective_typesetter = ts

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True
        yield from self.connective_typesetter.typeset_from_generator(**kwargs)
        yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        first = True
        for term in phi:
            if not first:
                yield from pl1.symbols.collection_separator.typeset_from_generator(**kwargs)
                yield from pl1.symbols.space.typeset_from_generator(**kwargs)
            else:
                first = False
            yield from term.typeset_from_generator(**kwargs)
        yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class InfixFormulaTypesetter(pl1.Typesetter):
    def __init__(self, connective_typesetter: pl1.FlexibleTypesetter):
        super().__init__()
        connective_typesetter = pl1.coerce_typesetter(ts=connective_typesetter)
        self._connective_typesetter: pl1.Typesetter = connective_typesetter

    @property
    def connective_typesetter(self) -> pl1.Typesetter:
        return self._connective_typesetter

    @connective_typesetter.setter
    def connective_typesetter(self, ts: pl1.FlexibleTypesetter):
        ts = pl1.coerce_typesetter(ts=ts)
        self._connective_typesetter = ts

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True
        if is_sub_formula:
            yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        yield from phi.term_0.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from self.connective_typesetter.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from phi.term_1.typeset_from_generator(**kwargs)
        if is_sub_formula:
            yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class TransformationTypesetter(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleTransformation, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Transformation = coerce_transformation(phi=phi)

        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True
        if is_sub_formula:
            yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        yield from phi.premises.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from pl1.symbols.rightwards_arrow.typeset_from_generator(**kwargs)
        yield from phi.variables.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from phi.conclusion.typeset_from_generator(**kwargs)
        if is_sub_formula:
            yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class BracketedListTypesetter(pl1.Typesetter):
    def __init__(self, open_bracket: pl1.Symbol, separator: pl1.Symbol, close_bracket: pl1.Symbol):
        self.open_bracket = open_bracket
        self.separator = separator
        self.close_bracket = close_bracket
        super().__init__()

    def typeset_from_generator(self, phi: Formula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True

        yield from self.open_bracket.typeset_from_generator(**kwargs)
        first = True
        for term in phi:
            if not first:
                yield from self.separator.typeset_from_generator(**kwargs)
                yield from pl1.symbols.space.typeset_from_generator(**kwargs)
            first = False
            yield from term.typeset_from_generator(**kwargs)
        yield from self.close_bracket.typeset_from_generator(**kwargs)


class Typesetters:
    """A factory of out-of-the-box encodings."""

    def __new__(cls):
        if st1.axiomatic_system_1_typesetters is None:
            st1.axiomatic_system_1_typesetters = super(Typesetters, cls).__new__(cls)
        return st1.axiomatic_system_1_typesetters

    def bracketed_list(self, open_bracket: pl1.Symbol, separator: pl1.Symbol, close_bracket: pl1.Symbol):
        return BracketedListTypesetter(open_bracket=open_bracket, separator=separator, close_bracket=close_bracket)

    def symbol(self, symbol: pl1.Symbol) -> pl1.SymbolTypesetter:
        return pl1.typesetters.symbol(symbol=symbol)

    def classical_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> ClassicalFormulaTypesetter:
        return ClassicalFormulaTypesetter(connective_typesetter=connective_typesetter)

    def text(self, text: str) -> pl1.TextTypesetter:
        return pl1.typesetters.text(text=text)

    def indexed_symbol(self, symbol: pl1.Symbol, index: int) -> pl1.IndexedSymbolTypesetter:
        return pl1.typesetters.indexed_symbol(symbol=symbol, index=index)

    def infix_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> InfixFormulaTypesetter:
        return InfixFormulaTypesetter(connective_typesetter=connective_typesetter)

    def transformation(self) -> TransformationTypesetter:
        return TransformationTypesetter()


typesetters = Typesetters()
