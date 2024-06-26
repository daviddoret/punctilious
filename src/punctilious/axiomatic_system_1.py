from __future__ import annotations

import abc
import collections
import logging
import typing
import warnings
# import threading
import sys
# import random
import itertools

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
                   message='OBSOLETE REUSE'),
    e101=ErrorCode(event_type=event_types.error, code='e101',
                   message='Formula.__new__: Unsupported type for the terms argument.'),
    e102=ErrorCode(event_type=event_types.error, code='e102',
                   message='Formula.term_0: Attempt to access property term_0 but formula does not contain a term at '
                           'index 0.'),
    e103=ErrorCode(event_type=event_types.error, code='e103',
                   message='Formula.term_1: Attempt to access property term_1 but formula does not contain a term at '
                           'index 0.'),
    e104=ErrorCode(event_type=event_types.warning, code='e104',
                   message='OBSOLETE, REUSE'),
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
                   message='OBSOLETE REUSE'),
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
        return get_index_of_first_equivalent_term_in_formula(term=phi, formula=self)

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
        return is_term_of_formula(term=phi, phi=self)

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


def coerce_formula(phi: FlexibleFormula) -> Formula:
    if isinstance(phi, Formula):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula()
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        # Implicit conversion of generators to tuple formulas.
        return Tupl(elements=(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        # Implicit conversion of iterators to tuple formulas.
        return Tupl(elements=phi)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Formula, phi_type=type(phi), phi=phi)


def coerce_variable(x: FlexibleFormula) -> Formula:
    """Any formula of arity 0 can be used as a variable.

    :param x:
    :return:
    """
    x = coerce_formula(phi=x)
    if x.arity != 0:
        raise Exception('coerce_variable: x.arity != 0')
    return x


def coerce_enumeration(e: FlexibleEnumeration, strip_duplicates: bool = False) -> Enumeration:
    """Coerce elements to an enumeration.
    If elements is None, coerce it to an empty enumeration."""
    if strip_duplicates:
        # this should not be necessary, because duplicate stripping
        # takes place in Enumeration __init__. but there must be some kind of implicit conversion
        # too early in the process which leads to an error being raised.
        e = strip_duplicate_formulas_in_python_tuple(t=e)
    if isinstance(e, Enumeration):
        return e
    elif isinstance(e, Formula) and is_well_formed_enumeration(e=e):
        # phi is a well-formed enumeration,
        # it can be safely re-instantiated as an Enumeration and returned.
        return Enumeration(elements=e, connective=e.connective, strip_duplicates=strip_duplicates)
    elif e is None:
        return Enumeration(elements=None, strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Generator) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(elements=tuple(element for element in e), strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Iterable) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(elements=e, strip_duplicates=strip_duplicates)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Enumeration, phi_type=type(e), phi=e)


def coerce_enumeration_of_variables(e: FlexibleEnumeration) -> Enumeration:
    e = coerce_enumeration(e=e)
    e2 = Enumeration()
    for element in e:
        element = coerce_variable(x=element)
        e2 = Enumeration(elements=(*e2, element,))
    return e2


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
    phi: Enumeration = coerce_enumeration(e=phi)
    psi: Enumeration = coerce_enumeration(e=psi)
    e: Enumeration = Enumeration(elements=(*phi, *psi,), strip_duplicates=True)
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
    phi: Theory = coerce_theory(t=phi)
    psi: Theory = coerce_theory(t=psi)
    t2: Theory = Theory(derivations=(*phi, *psi,))
    return t2


def coerce_map(m: FlexibleMap) -> Map:
    if isinstance(m, Map):
        return m
    elif m is None:
        return Map(domain=None, codomain=None)
    # TODO: coerce_map: Implement with isinstance(phi, FlexibleFormula) and is_well_formed...
    elif isinstance(m, dict):
        domain: Enumeration = coerce_enumeration(e=m.keys())
        codomain: Tupl = coerce_tupl(t=m.values())
        return Map(domain=domain, codomain=codomain)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Map, phi_type=type(m), phi=m)


def coerce_tupl(t: FlexibleTupl) -> Tupl:
    if isinstance(t, Tupl):
        return t
    elif t is None:
        return Tupl(elements=None)
    elif isinstance(t, collections.abc.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return Tupl(elements=t)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Tupl, phi_type=type(t), phi=t)


FlexibleFormula = typing.Optional[typing.Union[Connective, Formula]]


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


def is_term_of_formula(term: FlexibleFormula, phi: FlexibleFormula) -> bool:
    """Returns True if and only if there exists a term t of phi such that phi ~formula the given term.

    When this condition is satisfied, we say that phi is a term of psi.

    :param term: A formula.
    :type term: FlexibleFormula
    :param phi: A formula.
    :type phi: FlexibleFormula
    ...
    :return: True if phi is a term of psi, False otherwise.
    :rtype: bool
    """
    term: Formula = coerce_formula(phi=term)
    phi: Formula = coerce_formula(phi=phi)
    return any(is_formula_equivalent(phi=term, psi=psi_term) for psi_term in phi)


def is_element_of_enumeration(element: FlexibleFormula, enumeration: FlexibleEnumeration) -> bool:
    """Returns True if and only if there exists an element e2 of enumeration E,
     such that the given element e ~formula e2.

    When this condition is satisfied, we say that e1 is an element of enumeration E.

    :param element: A formula.
    :type element: FlexibleFormula
    :param enumeration: An enumeration.
    :type enumeration: FlexibleEnumeration
    ...
    :return: True if element is a term of psi, False otherwise.
    :rtype: bool
    """
    element: Formula = coerce_formula(phi=element)
    enumeration: Enumeration = coerce_enumeration(e=enumeration)
    return is_term_of_formula(term=element, phi=enumeration)


def is_axiom_of_theory(a: FlexibleAxiom, t: FlexibleTheory):
    a: Axiom = coerce_axiom(a=a)
    t: Theory = coerce_theory(t=t)
    return any(is_formula_equivalent(phi=a, psi=a2) for a2 in t.axioms)


def is_inference_rule_of_theory(ir: FlexibleInferenceRule, t: FlexibleTheory):
    ir: InferenceRule = coerce_inference_rule(i=ir)
    t: Theory = coerce_theory(t=t)
    return any(is_formula_equivalent(phi=ir, psi=ir2) for ir2 in t.inference_rules)


def is_theorem_of_theory(thrm: FlexibleTheorem, t: FlexibleTheory):
    thrm: Theorem = coerce_theorem(t=thrm)
    t: Theory = coerce_theory(t=t)
    return any(is_formula_equivalent(phi=thrm, psi=thrm2) for thrm2 in t.theorems)


def get_index_of_first_equivalent_term_in_formula(term: FlexibleFormula, formula: FlexibleFormula) -> int:
    """Return the o-based index of the first occurrence of a term in the terms of a formula,
     such that they are formula-equivalent.

    :param term: The formula being searched.
    :type term: FlexibleFormula
    :param formula: The formula whose terms are being searched.
    :type formula: FlexibleFormula
    ...
    :raises CustomException: Raise exception e109 if the term is not a term of the formula.
    ...
    :return: the 0 based-based index of the first occurrence of the term in the formula, such that they are
    formula-equivalent.
    :rtype: int
    """
    term = coerce_formula(phi=term)
    formula = coerce_formula(phi=formula)
    n: int = 0
    for mapped_term in iterate_formula_terms(phi=formula):
        if is_formula_equivalent(phi=term, psi=mapped_term):
            # This is the first match
            return n
        n = n + 1
    # No match was found
    raise u1.ApplicativeException(code='e109',
                                  msg=f'Trying to get the index of the term "{term}" in the formula "{formula}", '
                                      f'but this term is not a term of the formula.')


def get_index_of_first_equivalent_element_in_enumeration(element: FlexibleFormula,
                                                         enumeration: FlexibleEnumeration) -> int:
    """Return the o-based index of the first occurrence of an element in an enumeration,
     such that they are formula-equivalent.

    :param element:
    :param enumeration:
    :return:
    """
    element: Formula = coerce_formula(phi=element)
    enumeration: Enumeration = coerce_enumeration(e=enumeration)
    return get_index_of_first_equivalent_term_in_formula(term=element, formula=enumeration)


def get_index_of_first_equivalent_element_in_tuple(element: FlexibleFormula, tupl: FlexibleTupl) -> int:
    """Return the o-based index of the first occurrence of an element in a tuple,
     such that they are formula-equivalent.

    :param element:
    :param tupl:
    :return:
    """
    element: Formula = coerce_formula(phi=element)
    tupl: Tupl = coerce_tupl(t=tupl)
    return get_index_of_first_equivalent_term_in_formula(term=element, formula=tupl)


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


class MetaVariable(SimpleObject):
    """A variable is defined as a simple-object that is not declared in the theory with a is-a operator.

    The justification for a dedicated python class is the implementation of the __enter__ and __exit__ methods,
    which allow the usage of variables with the python with statement."""

    def __new__(cls, connective: NullaryConnective):
        o: tuple
        o = super().__new__(cls, connective=connective)
        return o

    def __init__(self, connective: NullaryConnective):
        super().__init__(connective=connective)

    def __enter__(self) -> MetaVariable:
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


def let_x_be_a_meta_variable(
        formula_typesetter: pl1.FlexibleTypesetter | typing.Iterable[pl1.FlexibleTypesetter, ...]) -> (
        MetaVariable | tuple[MetaVariable, ...]):
    """A meta-variable is a nullary-connective formula (*) that is not declared in the theory with a is-a operator."""
    if formula_typesetter is None or isinstance(formula_typesetter, pl1.FlexibleTypesetter):
        return MetaVariable(connective=NullaryConnective(formula_typesetter=formula_typesetter))
    elif isinstance(formula_typesetter, typing.Iterable):
        return tuple(MetaVariable(connective=NullaryConnective(formula_typesetter=ts)) for ts in formula_typesetter)
    else:
        raise TypeError  # TODO: Implement event code.


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
        theory: FlexibleTheory = coerce_theory(t=theory)

    if inference_rule is None and premises is not None and conclusion is not None and variables is not None:
        transformation: Transformation = Transformation(premises=premises, conclusion=conclusion, variables=variables)
        inference_rule: InferenceRule = InferenceRule(transformation=transformation)

    if isinstance(theory, Axiomatization):
        theory = Axiomatization(derivations=(*theory, inference_rule,))
        u1.log_info(inference_rule.typeset_as_string(theory=theory))
        return theory, inference_rule
    elif isinstance(theory, Theory):
        theory = Theory(derivations=(*theory, inference_rule,))
        u1.log_info(inference_rule.typeset_as_string(theory=theory))
        return theory, inference_rule
    else:
        raise Exception('oops')


def let_x_be_an_axiom_deprecated(valid_statement: FlexibleFormula):
    return Axiom(valid_statement=valid_statement)


def let_x_be_an_axiom(t: FlexibleTheory, valid_statement: typing.Optional[FlexibleFormula] = None,
                      axiom: typing.Optional[FlexibleAxiom] = None):
    """

    :param t: An axiomatization or a theory. If None, the empty axiom-collection is implicitly used.
    :param valid_statement: The statement claimed by the new axiom. Either the claim or axiom parameter
    must be provided, and not both.
    :param axiom: An existing axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :return: a pair (t, a) where t is an extension of the input theory, with a new axiom claiming the
    input statement, and a is the new axiom.
    """
    if t is None:
        t = Axiomatization(derivations=None)
    else:
        t: FlexibleTheory = coerce_theory(t=t)
    if valid_statement is not None and axiom is not None:
        raise Exception('oops 1')
    elif valid_statement is None and axiom is None:
        raise Exception('oops 2')
    elif valid_statement is not None:
        axiom: Axiom = Axiom(valid_statement=valid_statement)

    if isinstance(t, Axiomatization):
        t = Axiomatization(derivations=(*t, axiom,), decorations=(t,))
        u1.log_info(axiom.typeset_as_string(theory=t))
        return t, axiom
    elif isinstance(t, Theory):
        t = Theory(derivations=(*t, axiom,), decorations=(t,))
        u1.log_info(axiom.typeset_as_string(theory=t))
        return t, axiom
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
                                         variables_fixed_values: FlexibleMap = None,
                                         raise_event_if_false: bool = False) -> bool:
    """Two formulas phi and psi are formula-equivalent-with-variables in regard to variables V if and only if:
     - Variables in V are not sub-formula of phi,
     - We declare a new formula psi' where every sub-formula that is an element of V,
       is substituted by the formula that is at the exact same position in the tree.
     - phi and psi' are formula-equivalent.

     Note: is-formula-equivalent-with-variables is not commutative.

    :param phi: a formula that does not contain any element of variables.
    :param psi: a formula that may contain some elements of variables.
    :param variables: an enumeration of formulas called variables.
    :param variables_fixed_values: (conditional) a mapping between variables and their assigned values. used internally
     for recursive calls. leave it to None.
    :param raise_event_if_false:
    :return:
    """
    is_equivalent, _ = is_formula_equivalent_with_variables_2(phi=phi, psi=psi, variables=variables,
                                                              variables_fixed_values=variables_fixed_values,
                                                              raise_event_if_false=raise_event_if_false)
    return is_equivalent


def is_formula_equivalent_with_variables_2(phi: FlexibleFormula, psi: FlexibleFormula, variables: FlexibleEnumeration,
                                           variables_fixed_values: FlexibleMap = None,
                                           raise_event_if_false: bool = False) -> typing.Tuple[
    bool, typing.Optional[Map]]:
    """Given that:
     - phi is a formula,
     - psi is a formula,
     - X is an enumeration of formulas named variables,
     - every variable x in X is an atomic formula (i.e. a formula whose arity = 0),
     - every variable x in X is not a sub-formula of phi,
     Then, phi and psi are formula-equivalent-with-variables if and only if:
     - by substitution of sub-formula x in psi with their counterpart in psi at the same position in the formula tree,
       every variable x can only be mapped to a single other formula,
     - and if with these substitutions phi and psi are formula-equivalent,
     Otherwise they are not formula-equivalent-with-variables.

     If the conditions under "given that" above are not satisfied, the result is undetermined
     and this python-function raises an exception.

     Note: is-formula-equivalent-with-variables is not commutative.

    :param phi: a formula that does not contain any element of variables.
    :param psi: a formula that may contain some elements of variables.
    :param variables: an enumeration of formulas called variables.
    :param variables_fixed_values: (conditional) a mapping between variables and their assigned values. used internally for recursive calls.
      leave it to None.
    :param raise_event_if_false:
    :return:
    """
    variables_fixed_values: Map = coerce_map(m=variables_fixed_values)
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    variables: Enumeration = coerce_enumeration(e=variables)
    # check that all variables are atomic formulas
    for x in variables:
        x: Formula = coerce_formula(phi=x)
        if x.arity != 0:
            raise u1.ApplicativeException(f'the arity of variable "{x}" in variables is not equal to 0.')
        if is_subformula_of_formula(formula=phi, subformula=x):
            raise u1.ApplicativeException(f'variable "{x}" is a sub-formula of phi.')
    # check that all variables in the map are atomic formulas and are correctly listed in variables
    for x in variables_fixed_values.domain:
        x: Formula = coerce_formula(phi=x)
        if x.arity != 0:
            raise u1.ApplicativeException(f'the arity of variable {x} in variables_fixed_values is not equal to 0.')
        if not is_element_of_enumeration(element=x, enumeration=variables):
            raise u1.ApplicativeException(f'variable {x} is present in the domain of the map variables_fixed_values, '
                                          f'but it is not an element of the enumeration variables.')
    if is_element_of_enumeration(element=psi, enumeration=variables):
        # psi is a variable
        if is_in_map_domain(phi=psi, m=variables_fixed_values):
            # psi is in the domain of the map of fixed values
            psi_value: Formula = variables_fixed_values.get_assigned_value(phi=psi)
            if is_formula_equivalent(phi=phi, psi=psi_value):
                return True, variables_fixed_values
            else:
                if raise_event_if_false:
                    raise u1.ApplicativeException(f'formula "{phi}" is not formula-equivalent to '
                                                  f'the assigned value "{psi_value}" of variable "{psi}".')
                return False, variables_fixed_values
        else:
            # psi is not defined in the domain of the map of fixed values
            psi_value: Formula = phi
            # extend the map of fixed values
            variables_fixed_values: Map = Map(domain=(*variables_fixed_values.domain, psi,),
                                              codomain=(*variables_fixed_values.codomain, psi_value,))
            return True, variables_fixed_values
    else:
        # psi is not a variable
        if not phi.connective is psi.connective or phi.arity != psi.arity:
            if raise_event_if_false:
                raise u1.ApplicativeException(f'the connective or arity of "{phi}" are not equal '
                                              f'to the connective or aritity of "{psi}".')
            return False, variables_fixed_values
        else:
            for phi_term, psi_term in zip(phi, psi):
                # check recursively the sub-formulas,
                # and enrich variables_fixed_values in the process.
                check, variables_fixed_values = is_formula_equivalent_with_variables_2(
                    phi=phi_term, psi=psi_term, variables=variables, variables_fixed_values=variables_fixed_values,
                    raise_event_if_false=False)
                if not check:
                    if raise_event_if_false:
                        raise u1.ApplicativeException(f'term "{phi_term}" "{phi}" is not formula-equivalent '
                                                      f'to the term {psi_term} of "{psi}".')
                    return False, variables_fixed_values
            # all term pairs have been checked
            return True, variables_fixed_values


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
    phi: Formula = coerce_enumeration(e=phi)
    psi: Formula = coerce_enumeration(e=psi)

    test_1 = all(any(is_formula_equivalent(phi=phi_prime, psi=psi_prime) for psi_prime in psi) for phi_prime in phi)
    test_2 = all(any(is_formula_equivalent(phi=psi_prime, psi=phi_prime) for phi_prime in phi) for psi_prime in psi)

    return test_1 and test_2


def replace_formulas(phi: FlexibleFormula, m: FlexibleMap) -> Formula:
    """Performs a top-down, left-to-right replacement of formulas in formula phi."""
    phi: Formula = coerce_formula(phi=phi)
    m: Map = coerce_map(m=m)
    if is_in_map_domain(phi=phi, m=m):
        # phi must be replaced at its root.
        # the replacement algorithm stops right there (i.e.: no more recursion).
        assigned_value: Formula = m.get_assigned_value(phi=phi)
        return assigned_value
    else:
        # build the replaced formula.
        fb: Formula = Formula(connective=phi.connective)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = replace_formulas(phi=term, m=m)
            fb: Formula = extend_formula(formula=fb, term=term_substitute)
        return fb


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
        return is_term_of_formula(term=phi, phi=self)


FlexibleTupl = typing.Optional[typing.Union[Tupl, typing.Iterable[FlexibleFormula]]]
"""FlexibleTupl is a flexible python type that may be safely coerced into a Tupl."""


def reduce_map(m: FlexibleFormula, preimage: FlexibleFormula) -> Map:
    """Return a new map such that the preimage is no longer an element of its domain."""
    m: Map = coerce_map(m=m)
    preimage: Formula = coerce_formula(phi=preimage)
    if is_element_of_enumeration(element=preimage, enumeration=m.domain):
        index: int = get_index_of_first_equivalent_term_in_formula(term=preimage, formula=m.domain)
        reduced_domain: tuple[Formula, ...] = (*m.domain[0:index], *m.domain[index + 1:])
        reduced_codomain: tuple[Formula, ...] = (*m.codomain[0:index], *m.codomain[index + 1:])
        reduced_map: Map = Map(domain=reduced_domain, codomain=reduced_codomain)
        return reduced_map
    else:
        return m


def extend_enumeration(enumeration: FlexibleEnumeration, element: FlexibleFormula) -> Enumeration:
    """Return a new extended enumeration such that element is an element of it.
    If the element is already a member of the enumeration, the function returns the original enumeration.
    """
    enumeration: Enumeration = coerce_enumeration(e=enumeration)
    element: Formula = coerce_formula(phi=element)
    if is_element_of_enumeration(element=element, enumeration=enumeration):
        # The element is already in the enumeration.
        return enumeration
    else:
        extended_enumeration: Enumeration = Enumeration(elements=(*enumeration, element,))
        return extended_enumeration


def extend_tupl(tupl: FlexibleTupl, element: FlexibleFormula) -> Tupl:
    """Return a new extended punctilious-tuple such that element is a new element appended to its existing elements.
    """
    tupl: Tupl = coerce_tupl(t=tupl)
    element: Formula = coerce_formula(phi=element)
    extended_tupl: Tupl = Tupl(elements=(*tupl, element,))
    return extended_tupl


def extend_formula(formula: FlexibleFormula, term: FlexibleFormula) -> Formula:
    """Return a new extended formula such that term is a new term appended to its existing terms.
    """
    formula: Formula = coerce_formula(phi=formula)
    term: Formula = coerce_formula(phi=term)
    extended_formula: Formula = Formula(terms=(*formula, term,), connective=formula.connective)
    return extended_formula


def extend_map(m: FlexibleMap, preimage: FlexibleFormula, image: FlexibleFormula) -> Map:
    """Return a new map m2 with a new (preimage, image) pair.
    If the preimage is already defined in m, replace it.

    :param m:
    :param preimage:
    :param image:
    :return:
    """
    m: Map = coerce_map(m=m)
    preimage: Formula = coerce_formula(phi=preimage)
    # Reduce the map to assure the preimage is no longer an element of its domain.
    m: Map = reduce_map(m=m, preimage=preimage)
    extended_domain: tuple[Formula, ...] = (*m.domain, preimage)
    extended_codomain: tuple[Formula, ...] = (*m.codomain, image)
    m: Map = Map(domain=extended_domain, codomain=extended_codomain)
    return m


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
        domain: Enumeration = coerce_enumeration(e=domain)
        codomain: Tupl = coerce_tupl(t=codomain)
        if len(domain) != len(codomain):
            raise ValueError('Map: |keys| != |values|')
        o: tuple = super().__new__(cls, connective=connectives.map, terms=(domain, codomain,))
        return o

    def __init__(self, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        domain: Enumeration = coerce_enumeration(e=domain)
        codomain: Tupl = coerce_tupl(t=codomain)
        super().__init__(connective=connectives.map, terms=(domain, codomain,))

    @property
    def codomain(self) -> Tupl:
        return coerce_tupl(t=self.term_1)

    @property
    def domain(self) -> Enumeration:
        return coerce_enumeration(e=self.term_0)

    def get_assigned_value(self, phi: Formula) -> Formula:
        """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
        if is_in_map_domain(phi=phi, m=self):
            index_position: int = self.domain.get_element_index(phi=phi)
            return self.codomain[index_position]
        else:
            raise IndexError('Map domain does not contain this element')

    def is_defined_in(self, phi: Formula) -> bool:
        """Return True if phi is formula-equivalent to an element of the map domain."""
        return self.domain.has_element(phi=phi)


FlexibleMap = typing.Optional[typing.Union[Map, typing.Dict[Formula, Formula]]]
"""FlexibleMap is a flexible python type that may be safely coerced into a Map."""


def strip_duplicate_formulas_in_python_tuple(t: tuple[Formula, ...]) -> tuple[Formula, ...]:
    """Strip a python-tuple from formulas that are duplicate because of formula-equivalence.
    Order is preserved.
    Only the first formula is maintained, all consecutive formulas are discarded."""
    # Do not reuse the Enumeration constructor here,
    # because enumerate_formula_terms is called in the Enumeration constructor to strip duplicates.
    t2: tuple = ()
    if t is None:
        return t2
    else:
        for element in t:
            if not any(is_formula_equivalent(phi=element, psi=existing_element) for existing_element in t2):
                t2: tuple = (*t2, element,)
    return t2


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

    def __new__(cls, elements: FlexibleEnumeration = None, connective: Connective = None,
                strip_duplicates: bool = False):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        connective: Connective = connectives.enumeration if connective is None else connective
        if strip_duplicates:
            elements = strip_duplicate_formulas_in_python_tuple(t=elements)
        if not is_well_formed_enumeration(e=elements):
            raise_error(error_code=error_codes.e110, elements_type=type(elements), elements=elements)
        o: tuple = super().__new__(cls, connective=connective, terms=elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None, connective: Connective = None,
                 strip_duplicates: bool = False):
        global connectives
        connective: Connective = connectives.enumeration if connective is None else connective
        if strip_duplicates:
            elements = strip_duplicate_formulas_in_python_tuple(t=elements)
        super().__init__(connective=connective, terms=elements)

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


enumeration = Enumeration
"""A shortcut for Enumeration."""

FlexibleEnumeration = typing.Optional[typing.Union[Enumeration, typing.Iterable[FlexibleFormula]]]
"""FlexibleEnumeration is a flexible python type that may be safely coerced into an Enumeration."""


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
        premises: Tupl = coerce_tupl(t=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(e=variables)
        o: tuple = super().__new__(cls, connective=connectives.transformation,
                                   terms=(premises, conclusion, variables,))
        return o

    def __init__(self, premises: FlexibleTupl, conclusion: FlexibleFormula,
                 variables: FlexibleEnumeration):
        premises: Tupl = coerce_tupl(t=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(e=variables)
        super().__init__(connective=connectives.transformation, terms=(premises, conclusion, variables,))

    def __call__(self, arguments: FlexibleTupl) -> Formula:
        """A shortcut for self.apply_transformation()"""
        return self.apply_transformation(arguments=arguments)

    def apply_transformation(self, arguments: FlexibleTupl) -> Formula:
        """

        :param arguments: A tuple of arguments, whose order matches the order of the transformation premises.
        :return:
        """
        arguments = coerce_tupl(t=arguments)
        # step 1: confirm every argument is compatible with its premises,
        # and seize the opportunity to retrieve the mapped variable values.
        success, variables_map = is_formula_equivalent_with_variables_2(phi=arguments, psi=self.premises,
                                                                        variables=self.variables,
                                                                        variables_fixed_values=None)
        if not success:
            raise u1.ApplicativeException(code='e117', msg='Applying a transformation with incorrect premises.',
                                          target_formula=arguments, transformation_premises=self.premises,
                                          transformation_variables=self.variables, transformation=self)

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


def coerce_transformation(t: FlexibleFormula) -> Transformation:
    if isinstance(t, Transformation):
        return t
    elif isinstance(t, Formula) and is_well_formed_transformation(t=t):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        return Transformation(premises=t.term_0, conclusion=t.term_1, variables=t.term_2)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Transformation, phi_type=type(t), phi=t)


def coerce_inference(i: FlexibleFormula) -> Inference:
    if isinstance(i, Inference):
        return i
    elif isinstance(i, Formula) and is_well_formed_inference(i=i):
        transformation: Transformation = coerce_transformation(t=i.term_1)
        return Inference(premises=i.term_0, transformation_rule=transformation)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Inference, phi_type=type(i), phi=i)


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


def is_well_formed_tupl(t: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed tuple, False otherwise.

    Note: by definition, all formulas are also tuples. Hence, return True if phi converts smoothly to a well-formed
    formula.

    :param t:
    :return: bool
    """
    # TODO: Do we want to signal tuples formally with a dedicated connective?
    t: Formula = coerce_formula(phi=t)
    return True


def is_well_formed_inference(i: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed inference, False otherwise.

    :param i: A formula.
    :return: bool.
    """
    i = coerce_formula(phi=i)
    if i.connective is not connectives.inference or not is_well_formed_enumeration(
            e=i.term_0) or not is_well_formed_transformation(t=i.term_1):
        return False
    else:
        return True


def is_well_formed_transformation(t: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed transformation, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if (t.connective is not connectives.transformation or
            t.arity != 3 or
            not is_well_formed_tupl(t=t.term_0) or
            not is_well_formed_formula(phi=t.term_1) or
            not is_well_formed_enumeration(e=t.term_2)):
        return False
    else:
        return True


def is_well_formed_enumeration(e: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed enumeration, False otherwise.

    :param e: A formula.
    :return: bool.
    """
    if e is None:
        # Implicit conversion of None to the empty enumeration.
        return True
    else:
        e = coerce_formula(phi=e)
        for i in range(0, e.arity):
            if i != e.arity - 1:
                for j in range(i + 1, e.arity):
                    if is_formula_equivalent(phi=e[i], psi=e[j]):
                        # We found a pair of duplicates, i.e.: phi_i ~formula phi_j.
                        return False
        return True


def is_well_formed_inference_rule(i: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed inference-rule, False otherwise.

    :param i: A formula.
    :return: bool.
    """
    i = coerce_formula(phi=i)
    if isinstance(i, InferenceRule):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif (i.connective is connectives.follows_from and
          i.arity == 2 and
          is_well_formed_transformation(t=i.term_0) and
          i.term_1.connective is connectives.inference_rule):
        return True
    else:
        return False


def is_valid_statement_in_theory(phi: FlexibleFormula, t: FlexibleTheory) -> bool:
    """Return True if formula phi is a valid-statement with regard to theory t, False otherwise.

    A formula phi is a valid-statement with regard to a theory t, if and only if:
     - phi is the valid-statement of an axiom in t,
     - or phi is the valid-statement of a theorem in t.
    """
    phi: Formula = coerce_formula(phi=phi)
    t: Theory = coerce_theory(t=t)
    return any(is_formula_equivalent(phi=phi, psi=valid_statement) for valid_statement in t.iterate_valid_statements())


def iterate_formula_terms(phi: FlexibleFormula) -> typing.Generator[Formula, None, None]:
    """Iterates the terms of a formula in order.
    """
    phi: Formula = coerce_formula(phi=phi)
    yield from phi  # super(phi) is a native python tuple.


def iterate_tuple_elements(phi: FlexibleTupl) -> typing.Generator[Formula, None, None]:
    """Iterates the elements of a tuple in canonical order.
    """
    phi = coerce_tupl(t=phi)
    yield from iterate_formula_terms(phi=phi)


def iterate_enumeration_elements(e: FlexibleEnumeration) -> typing.Generator[Formula, None, None]:
    """Iterates the elements of an enumeration.

    :param e:
    :return:
    """
    e: Enumeration = coerce_enumeration(e=e)
    yield from iterate_formula_terms(phi=e)


def are_valid_statements_in_theory(s: FlexibleTupl, t: FlexibleTheory) -> bool:
    """Return True if every formula phi in enumeration s is a valid-statement in theory t, False otherwise.
    """
    s: Tupl = coerce_tupl(t=s)
    t: Theory = coerce_theory(t=t)
    return all(is_valid_statement_in_theory(phi=phi, t=t) for phi in iterate_tuple_elements(s))


def iterate_permutations_of_enumeration_elements_with_fixed_size(e: FlexibleEnumeration, n: int) -> typing.Generator[
    Enumeration, None, None]:
    """Iterate all distinct tuples (order matters) of exactly n elements in enumeration e.

    :param n:
    :param e:
    :return:
    """
    e: Enumeration = coerce_enumeration(e=e)
    if n > e.arity:
        raise Exception('n > |e|')
    if n < 0:
        raise Exception('n < 0')
    if n == 0:
        # nothing will be yield from the function.
        # note that itertools.permutations would yield one empty tuple.
        return
    else:
        generator = itertools.permutations(iterate_enumeration_elements(e=e), n)
        for python_tuple in generator:
            permutation: Enumeration = Enumeration(elements=python_tuple)
            yield permutation
        return


def iterate_derivations_in_theory(t: FlexibleTheory) -> typing.Generator[Formula, None, None]:
    t = coerce_theory(t=t)
    for derivation in t:
        derivation = coerce_derivation(d=derivation)
        yield derivation
    return


def iterate_valid_statements_in_theory(t: FlexibleTheory) -> typing.Generator[Formula, None, None]:
    t = coerce_theory(t=t)
    derivations = iterate_derivations_in_theory(t=t)
    for derivation in derivations:
        if is_well_formed_axiom(a=derivation):
            derivation: Axiom = coerce_axiom(a=derivation)
            valid_statement: Formula = derivation.valid_statement
            yield valid_statement
        elif is_well_formed_theorem(t=derivation):
            derivation: Theorem = coerce_theorem(t=derivation)
            valid_statement: Formula = derivation.valid_statement
            yield valid_statement
    return


def are_valid_statements_in_theory_with_variables(
        s: FlexibleTupl, t: FlexibleTheory,
        variables: FlexibleEnumeration,
        variables_values: FlexibleMap, debug: bool = False) \
        -> tuple[bool, typing.Optional[Tupl]]:
    """Return True if every formula phi in tuple s is a valid-statement in theory t,
    considering some variables, and some variable values.
    If a variable in variables has not an assigned value, then it is a free variable.
    Return False otherwise.

    Performance warning: this may be a very expansive algorithm, because multiple
    recursive iterations may be required to find a solution.

    TODO: retrieve and return the final map of variable values as well? is this really needed?

    """
    s: Tupl = coerce_tupl(t=s)
    t: Theory = coerce_theory(t=t)
    variables: Enumeration = coerce_enumeration(e=variables, strip_duplicates=True)
    variables_values: Map = coerce_map(m=variables_values)

    # list the free variables.
    # these are the variables that are in "variables" that are not in the domain of "variables_values".
    free_variables: Enumeration = Enumeration()
    for x in iterate_enumeration_elements(e=variables):
        if not is_in_map_domain(phi=x, m=variables_values):
            free_variables: Enumeration = Enumeration(elements=(*free_variables, x,))

    if debug:
        u1.log_info(f'are_valid_statements_in_theory_with_variables: free-variables:{free_variables}')

    permutation_size: int = free_variables.arity

    if permutation_size == 0:
        # there are no free variables.
        # but there may be some or no variables with assigned values.
        # it follows that 1) there will be no permutations,
        # and 2) are_valid_statements_in_theory() is equivalent.
        s_with_variable_substitution: Formula = replace_formulas(phi=s, m=variables_values)
        s_with_variable_substitution: Tupl = coerce_tupl(t=s_with_variable_substitution)
        valid: bool = are_valid_statements_in_theory(s=s_with_variable_substitution, t=t)
        if valid:
            return valid, s_with_variable_substitution
        else:
            return valid, None
    else:
        valid_statements = iterate_valid_statements_in_theory(t=t)
        for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                        n=permutation_size):
            variable_substitution: Map = Map(domain=free_variables, codomain=permutation)
            s_with_variable_substitution: Formula = replace_formulas(phi=s, m=variable_substitution)
            s_with_variable_substitution: Tupl = coerce_tupl(t=s_with_variable_substitution)
            s_with_permutation: Tupl = Tupl(elements=(*s_with_variable_substitution,))
            if are_valid_statements_in_theory(s=s_with_permutation, t=t):
                return True, s_with_permutation
        return False, None


def is_valid_statement_with_free_variables_in_theory(phi: FlexibleFormula, t: FlexibleTheory,
                                                     free_variables: FlexibleEnumeration) -> bool:
    """Return True if formula phi is a valid-statement with regard to theory t, False otherwise.

    A formula phi is a valid-statement with regard to a theory t, if and only if:
     - phi is the valid-statement of an axiom in t,
     - or phi is the valid-statement of a theorem in t.
    """
    phi: Formula = coerce_formula(phi=phi)
    t: Theory = coerce_theory(t=t)
    free_variables: Enumeration = coerce_enumeration_of_variables(e=free_variables)
    for valid_statement in t.iterate_valid_statements():
        output, _, = is_formula_equivalent_with_variables_2(phi=valid_statement, psi=phi, variables=free_variables)
        if output:
            return True
    return False


def is_well_formed_axiom(a: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed axiom, False otherwise.

    :param a: A formula.
    :return: bool.
    """
    a = coerce_formula(phi=a)
    if a.arity != 2:
        return False
    if a.connective is not connectives.follows_from:
        return False
    if not is_well_formed_formula(phi=a.term_0):
        return False
    if a.term_1.arity != 0:
        return False
    if a.term_1.connective != connectives.axiom:
        return False
    # All tests were successful.
    return True


def is_well_formed_theorem(t: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed theorem, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if isinstance(t, Theorem):
        # the Theorem python-type assure the well-formedness of the object.
        return True
    if (t.connective is not connectives.follows_from or
            not t.arity == 2 or
            not is_well_formed_formula(phi=t.term_0) or
            not is_well_formed_inference(i=t.term_1)):
        return False
    else:
        i: Inference = coerce_inference(i=t.term_1)
        f_of_p: Formula = i.transformation_rule(i.premises)
        if not is_formula_equivalent(phi=t.term_0, psi=f_of_p):
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            # issue a warning to facilitate troubleshooting and analysis.
            raise_error(error_code=error_codes.e106, phi=t, psi_expected=t.term_0, psi_inferred=f_of_p,
                        inference_rule=i)
            return False
        return True


def is_well_formed_derivation(d: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed theorem, False otherwise.

    :param d: A formula.
    :return: bool.
    """
    d: Formula = coerce_formula(phi=d)
    if is_well_formed_theorem(t=d):
        return True
    elif is_well_formed_inference_rule(i=d):
        return True
    elif is_well_formed_axiom(a=d):
        return True
    else:
        return False


def is_well_formed_theory(t: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
    """Return True if phi is a well-formed theory, False otherwise.

    :param t: A formula.
    :param raise_event_if_false:
    :return: bool.
    """
    t = coerce_enumeration(e=t)

    if isinstance(t, Theory):
        # the Derivation class assure the well-formedness of the theory.
        return True

    # check the well-formedness of the individual derivations.
    # and retrieve the terms claimed as proven in the theory, preserving order.
    # by the definition of a theory, these are the left term (term_0) of the formulas.
    valid_statements: Tupl = Tupl(elements=None)
    derivations: Tupl = Tupl(elements=None)
    for derivation in t:
        if not is_well_formed_derivation(d=derivation):
            return False
        else:
            derivation: Derivation = coerce_derivation(d=derivation)
            derivations: Tupl = extend_tupl(tupl=derivations, element=derivation)
            # retrieve the formula claimed as valid from the theorem
            valid_statement: Formula = derivation.valid_statement
            valid_statements: Tupl = extend_tupl(tupl=valid_statements, element=valid_statement)
    # now the derivations and valid_statements have been retrieved, and proved well-formed individually,
    for i in range(0, derivations.arity):
        derivation = derivations[i]
        valid_statement = valid_statements[i]
        if is_well_formed_axiom(a=derivation):
            # This is an axiom.
            derivation: Axiom = coerce_axiom(a=derivation)
            pass
        elif is_well_formed_inference_rule(i=derivation):
            # This is an inference-rule.
            derivation: InferenceRule = coerce_inference_rule(i=derivation)
            pass
        elif is_well_formed_theorem(t=derivation):
            theorem_by_inference: Theorem = coerce_theorem(t=derivation)
            inference: Inference = theorem_by_inference.inference
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


def is_well_formed_axiomatization(a: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed axiomatization, False otherwise."""
    a = coerce_formula(phi=a)
    if a.connective is not connectives.axiomatization:
        return False
    for element in a:
        if not is_well_formed_axiom(a=element) and not is_well_formed_inference_rule(i=element):
            return False
    return True


def coerce_derivation(d: FlexibleFormula) -> Derivation:
    """Validate that p is a well-formed theorem and returns it properly typed as Proof, or raise exception e123.

    :param d:
    :return:
    """
    d: Formula = coerce_formula(phi=d)
    if is_well_formed_theorem(t=d):
        return coerce_theorem(t=d)
    elif is_well_formed_inference_rule(i=d):
        return coerce_inference_rule(i=d)
    elif is_well_formed_axiom(a=d):
        return coerce_axiom(a=d)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Derivation, phi_type=type(d), phi=d)


def coerce_axiom(a: FlexibleFormula) -> Axiom:
    """Validate that p is a well-formed axiom and returns it properly typed as an instance of Axiom,
    or raise exception e123.

    :param a:
    :return:
    """
    if isinstance(a, Axiom):
        return a
    elif isinstance(a, Formula) and is_well_formed_axiom(a=a):
        proved_formula: Formula = a.term_0
        return Axiom(valid_statement=proved_formula)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=InferenceRule, phi_type=type(a), phi=a)


def coerce_inference_rule(i: FlexibleFormula) -> InferenceRule:
    """Validate that p is a well-formed inference-rule and returns it properly typed as an instance of InferenceRule,
    or raise exception e123.

    :param i:
    :return:
    """
    if isinstance(i, InferenceRule):
        return i
    elif isinstance(i, Formula) and is_well_formed_inference_rule(i=i):
        transfo: Transformation = coerce_transformation(t=i.term_0)
        return InferenceRule(transformation=transfo)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=InferenceRule, phi_type=type(i), phi=i)


def coerce_theorem(t: FlexibleFormula) -> Theorem:
    """Validate that p is a well-formed theorem-by-inference and returns it properly typed as ProofByInference,
    or raise exception e123.

    :param t:
    :return:
    """
    if isinstance(t, Theorem):
        return t
    elif isinstance(t, Formula) and is_well_formed_theorem(t=t):
        proved_formula: Formula = coerce_formula(phi=t.term_0)
        inference: Inference = coerce_inference(i=t.term_1)
        return Theorem(valid_statement=proved_formula, i=inference)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Theorem, phi_type=type(t), phi=t)


def coerce_theory(t: FlexibleTheory) -> Theory:
    """Validate that phi is a well-formed theory and returns it properly typed as Demonstration,
    or raise exception e123.

    :param t:
    :return:
    """
    if isinstance(t, Theory):
        return t
    elif isinstance(t, Formula) and is_well_formed_theory(t=t):
        return Theory(derivations=t)
    elif t is None:
        return Theory(derivations=None)
    elif isinstance(t, typing.Generator) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(derivations=tuple(element for element in t))
    elif isinstance(t, typing.Iterable) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(derivations=t)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Theory, phi_type=type(t), phi=t)


def coerce_axiomatization(a: FlexibleFormula) -> Axiomatization:
    """Validate that phi is a well-formed axiomatization and returns it properly typed as Axiomatization,
    or raise exception e123.

    :param a:
    :return:
    """
    if isinstance(a, Axiomatization):
        return a
    elif isinstance(a, Formula) and is_well_formed_axiomatization(a=a):
        return Axiomatization(derivations=a)
    else:
        raise_error(error_code=error_codes.e123, coerced_type=Axiomatization, phi_type=type(a), phi=a)


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
        transformation: Transformation = coerce_transformation(t=transformation)
        o: tuple = super().__new__(cls, valid_statement=transformation, justification=connectives.inference_rule)
        return o

    def __init__(self, transformation: FlexibleTransformation):
        self._transformation: Transformation = coerce_transformation(t=transformation)
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
        premises: Tupl = coerce_tupl(t=premises)
        transformation_rule: Transformation = coerce_transformation(t=transformation_rule)
        c: Connective = connectives.inference
        o: tuple = super().__new__(cls, connective=c, terms=(premises, transformation_rule,))
        return o

    def __init__(self, premises: FlexibleTupl, transformation_rule: FlexibleTransformation):
        self._premises: Tupl = coerce_tupl(t=premises)
        self._transformation_rule: Transformation = coerce_transformation(t=transformation_rule)
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
        i: Inference = coerce_inference(i=i)
        o: tuple = super().__new__(cls, valid_statement=valid_statement, justification=i)
        return o

    def __init__(self, valid_statement: FlexibleFormula, i: FlexibleInference):
        valid_statement: Formula = coerce_formula(phi=valid_statement)
        i: Inference = coerce_inference(i=i)
        self._phi: Formula = valid_statement
        self._inference: Inference = i
        # complete object initialization to assure that we have a well-formed formula with connective, etc.
        super().__init__(valid_statement=valid_statement, justification=i)
        # check the validity of the theorem
        f_of_p: Formula = i.transformation_rule(i.premises)
        try:
            is_formula_equivalent(phi=valid_statement, psi=f_of_p, raise_event_if_false=True)
        except CustomException as error:
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            # raise an exception to prevent the creation of this ill-formed theorem-by-inference.
            raise_error(error_code=error_codes.e105, error=error, valid_statement=valid_statement,
                        algorithm_output=f_of_p,
                        inference=i, inference_transformation_rule=i.transformation_rule, inference_premises=i.premises)

    @property
    def inference(self) -> Inference:
        """The inference of the theorem."""
        return self._inference

    @property
    def phi(self) -> Formula:
        """The proven formula."""
        return self._phi


FlexibleTheorem = typing.Union[Theorem, Formula]
FlexibleDerivation = typing.Union[FlexibleAxiom, FlexibleTheorem, FlexibleInferenceRule]


class Heuristic(abc.ABC):
    """A heuristic is a method that facilitates proofs. It recognizes a conjecture pattern to check if the
    conjecture is a conjecture that it is able to process, and then it applies an algorithm to attempt to automatically
    derive the conjecture.

    Heuristics can be attached to theories to simplify proofs.
    """

    @abc.abstractmethod
    def process_conjecture(self, conjecture: FlexibleFormula, t: FlexibleTheory) -> tuple[Theory, bool,]:
        """

        :param conjecture:
        :param t:
        :return:
        """
        pass


class Theory(Enumeration):
    """A theory is a justified enumeration of axioms, inference-rules, and theorems.

    Syntactic definition:
    A well-formed theory is an enumeration such that:
     - all element phi of the enumeration is a well-formed theorem,
     - all premises of all theorem-by-inferences are predecessors of their parent theorem-by-inference.

    TODO: Consider the following data-model change: a derivation is only an axiom or an inference-rule. In
        effect, stating that in inference-rule is a derivation seems to be a bit of a semantic stretch.

    """

    def __new__(cls, connective: Connective | None = None, derivations: FlexibleEnumeration = None,
                decorations: FlexibleDecorations = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(e=derivations)
        # use coerce_derivation() to assure that every derivation is properly types as Axiom, InferenceRule or Theorem.
        derivations: Enumeration = coerce_enumeration(
            e=(coerce_derivation(d=p) for p in derivations))
        try:
            is_well_formed_theory(t=derivations, raise_event_if_false=True)

        except Exception as error:
            # well-formedness verification failure, the theorem is ill-formed.
            raise_error(error_code=error_codes.e120, error=error, derivations=derivations)
        o: tuple = super().__new__(cls, elements=derivations)
        return o

    def __init__(self, connective: Connective | None = None, derivations: FlexibleEnumeration = None,
                 decorations: FlexibleDecorations = None):
        if connective is None:
            connective: Connective = connectives.theory
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(e=derivations)
        # coerce all elements of the enumeration to theorem
        derivations: Enumeration = coerce_enumeration(
            e=(coerce_derivation(d=p) for p in derivations))
        self._heuristics: set[Heuristic, ...] | set[{}] = set()
        super().__init__(connective=connective, elements=derivations)
        copy_theory_decorations(target=self, decorations=decorations)

    @property
    def axioms(self) -> Enumeration:
        """Return an enumeration of all axioms in the theory.

        Note: order is preserved."""
        return Enumeration(elements=tuple(self.iterate_axioms()))

    @property
    def heuristics(self) -> set[Heuristic, ...] | set[{}]:
        """A python-set of heuristics.

        Heuristics are not formally part of a theory. They are decorative objects used to facilitate proof derivations.
        """
        return self._heuristics

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

FlexibleDecorations = typing.Optional[typing.Union[typing.Tuple[Theory, ...], typing.Tuple[()]]]


def copy_theory_decorations(target: FlexibleTheory, decorations: FlexibleDecorations = None):
    """Copy the decorative-properties of a source theory onto a target theory.

    :param target:
    :param decorations:
    :return:
    """
    if decorations is not None:
        for decorative_theory in decorations:
            # Copies all heuristics
            target.heuristics.update(decorative_theory.heuristics)


class Axiomatization(Theory):
    """An axiomatization is a theory that is only composed of axioms,
    and/or inference-rules.

    Syntactic definition:
    A well-formed axiomatization is an enumeration such that:
     - all element phi of the enumeration is a well-formed axiom or an inference-rule.

    """

    def __new__(cls, derivations: FlexibleEnumeration = None, decorations: FlexibleDecorations = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(e=derivations)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_derivations: Enumeration = Enumeration(elements=None)
        for derivation in derivations:
            if is_well_formed_inference_rule(i=derivation):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(i=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, inference_rule,))
            elif is_well_formed_axiom(a=derivation):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(a=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, axiom,))
            else:
                # Incorrect form.
                raise_error(error_code=error_codes.e123, phi=derivation, phi_type_1=InferenceRule,
                            phi_type_2=Axiom)
        o: tuple = super().__new__(cls, derivations=coerced_derivations)
        return o

    def __init__(self, derivations: FlexibleEnumeration = None, decorations: FlexibleDecorations = None):
        # coerce to enumeration
        derivations: Enumeration = coerce_enumeration(e=derivations)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_derivations: Enumeration = Enumeration(elements=None)
        for derivation in derivations:
            if is_well_formed_inference_rule(i=derivation):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(i=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, inference_rule,))
            elif is_well_formed_axiom(a=derivation):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(a=derivation)
                coerced_derivations: Enumeration = Enumeration(elements=(*coerced_derivations, axiom,))
            else:
                # Incorrect form.
                raise_error(error_code=error_codes.e123, phi=derivation, phi_type_1=InferenceRule,
                            phi_type_2=Axiom)
        super().__init__(connective=connectives.axiomatization, derivations=coerced_derivations,
                         decorations=decorations)


def is_subformula_of_formula(subformula: FlexibleFormula, formula: FlexibleFormula) -> bool:
    """Return True if and only if formula subformula is a sub-formula of formula formula, False otherwise.

    :param subformula:
    :param formula:
    :return: True if and only if formula subformula is a sub-formula of formula formula, False otherwise.
    :rtype: bool
    """
    subformula: Formula = coerce_formula(phi=subformula)
    formula: Formula = coerce_formula(phi=formula)
    if is_formula_equivalent(phi=subformula, psi=formula):
        return True
    for term in formula:
        if is_subformula_of_formula(subformula=subformula, formula=term):
            return True
    return False


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


def get_leaf_formulas(phi: FlexibleFormula, eb: Enumeration = None) -> Enumeration:
    """Return the enumeration of leaf-formulas in phi.

    Note: if phi is a leaf-formula, return phi.

    :param phi:
    :param eb: (conditional) An enumeration-builder for recursive call.
    :return:
    """
    phi: Formula = coerce_formula(phi=phi)
    if eb is None:
        eb: Enumeration = Enumeration(elements=None)
    if not eb.has_element(phi=phi) and is_leaf_formula(phi=phi):
        eb = extend_enumeration(element=phi, enumeration=eb)
    else:
        for term in phi:
            # Recursively call get_leaf_formulas,
            # which complete eb with any remaining leaf formulas.
            eb = union_enumeration(phi=eb, psi=get_leaf_formulas(phi=term, eb=eb))
    return eb


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
    t = coerce_theory(t=t)
    if args is None:
        return t
    else:
        for argument in args:
            if is_well_formed_theory(t=argument):
                # recursively append all derivations of t2 in t
                t2: Theory = coerce_theory(t=argument)
                for d in t2.derivations:
                    t: Theory = extend_theory(d, t=t)
            elif is_well_formed_axiom(a=argument):
                a: Axiom = coerce_axiom(a=argument)
                if not is_axiom_of_theory(a=a, t=t):
                    t: Theory = Theory(derivations=(*t, a,))
            elif is_well_formed_inference_rule(i=argument):
                ir: InferenceRule = coerce_inference_rule(i=argument)
                if not is_inference_rule_of_theory(ir=ir, t=t):
                    t: Theory = Theory(derivations=(*t, ir,))
            elif is_well_formed_theorem(t=argument):
                thrm: Theorem = coerce_theorem(t=argument)
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
    premises: Enumeration = Enumeration(elements=None)
    variables_map: Map = Map(domain=None, codomain=None)
    for x in propositional_variables:
        rep: str = x.typeset_as_string() + '\''
        # automatically append the axiom: x is-a propositional-variable
        with let_x_be_a_propositional_variable_OBSOLETE(rep=rep) as x2:
            premises: Enumeration = extend_enumeration(
                enumeration=premises, element=x2 | connectives.is_a | connectives.propositional_variable)
            variables_map: Map = extend_map(m=variables_map, preimage=x, image=x2)
    variables: Enumeration = Enumeration(elements=variables_map.codomain)

    # elaborate a new formula psi where all variables have been replaced with the new variables
    psi = replace_formulas(phi=phi, m=variables_map)

    # translate the antecedent of the implication to the main premises
    # note: we could further split conjunctions into multiple premises
    antecedent: Formula = psi.term_0
    premises: Enumeration = extend_enumeration(
        enumeration=premises, element=antecedent)

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


def derive_1(t: FlexibleTheory, c: FlexibleFormula, p: FlexibleTupl,
             i: FlexibleInferenceRule) -> typing.Tuple[Theory, Theorem]:
    """Given a theory t, derives a new theory t' that extends t with a new theorem derived by applying inference-rule i.

    :param c: A propositional formula posed as a conjecture.
    :param t: A theory.
    :param p: A tuple of premises.
    :param i: An inference-rule.
    :return: A python-tuple (t′, theorem)
    """
    # parameters validation
    t: Theory = coerce_theory(t=t)
    c: Formula = coerce_formula(phi=c)
    p: Tupl = coerce_tupl(t=p)
    i: InferenceRule = coerce_inference_rule(i=i)

    for premise in p:
        # The validity of the premises is checked during theory initialization,
        # but re-checking it here "in advance" helps provide more context in the exception that is being raised.
        if not is_valid_statement_in_theory(phi=premise, t=t):
            raise u1.ApplicativeException(
                msg=f'Conjecture: \n\t{c} \n...cannot be derived because premise: \n\t{premise}'
                    f' \n...is not a valid-statement in theory t. The inference-rule used to try this derivation was: '
                    f'\n\t{i} \nThe complete theory is: \n\t{t}', c=c, premise=premise, p=p, i=i, t=t)

    # Configure the inference that derives the theorem.
    inference: Inference = Inference(premises=p, transformation_rule=i.transformation)

    # Prepare the new theorem.
    theorem: Theorem = Theorem(valid_statement=c, i=inference)

    # Extends the theory with the new theorem.
    # The validity of the premises will be checked during theory initialization.
    t: Theory = Theory(derivations=(*t, theorem,), decorations=(t,))

    u1.log_info(theorem.typeset_as_string(theory=t))

    return t, theorem


def is_in_formula_tree(phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Return True if phi is formula-equivalent to psi or a sub-formula of psi."""
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    if is_formula_equivalent(phi=phi, psi=psi):
        return True
    else:
        for term in iterate_formula_terms(phi=psi):
            if is_in_formula_tree(phi=phi, psi=term):
                return True
    return False


def is_in_map_domain(phi: FlexibleFormula, m: FlexibleMap) -> bool:
    """Return True if phi is a formula in the domain of map m, False otherwise."""
    phi = coerce_formula(phi=phi)
    m = coerce_map(m=m)
    return is_element_of_enumeration(element=phi, enumeration=m.domain)


def derive_0(t: FlexibleTheory, conjecture: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """An algorithm that attempts to automatically prove a conjecture in a theory.

    The auto_derive_0 algorithm "proving the obvious":
    1). Check if the conjecture is already a valid statement in the theory.

    Note: the tuple returned by the function comprises theory t as its first element. This is not necessary because
    a new theory is not derived by auto_derive_0, but it provides consistency with the return values of the other
    auto_derive functions.

    :param t:
    :param conjecture:
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    t = coerce_theory(t=t)
    conjecture = coerce_formula(phi=conjecture)
    if debug:
        u1.log_debug(f'auto_derive_0: start. conjecture:{conjecture}.')
    if is_valid_statement_in_theory(phi=conjecture, t=t):  # this first check is superfluous
        # loop through derivations
        for derivation in t.iterate_derivations():
            if is_formula_equivalent(phi=conjecture, psi=derivation.valid_statement):
                # the valid-statement of this derivation matches phi,
                # the auto_derive is successful.
                # if debug:
                # u1.log_info(f'auto_derive_0 successful: {derivation}')
                return t, True, derivation
    # all derivations have been tested and none matched phi,
    # it follows that the auto_derive failed.
    return t, False, None


def derive_2(t: FlexibleTheory, c: FlexibleFormula, i: FlexibleInferenceRule,
             debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """Derive a new theory t′ that extends t, where conjecture c is a new theorem derived from inference-rule i.

    Note: in contrast, derive_1 requires the explicit list of premises. derive_2 is more convenient to use because it
     automatically finds a set of premises among the valid-statements in theory t, such that conjecture c can be
     derived.

    :param t: a theory.
    :param c: the conjecture to be proven.
    :param i: the inference-rule from which the conjecture can be derived.
    :param debug:
    :return: A python-tuple (t′, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    t = coerce_theory(t=t)
    c = coerce_formula(phi=c)
    i = coerce_inference_rule(i=i)
    if debug:
        u1.log_debug(f'derive_2: Derivation started. conjecture:{c}. inference_rule:{i}.')

    if not is_inference_rule_of_theory(ir=i, t=t):
        # The inference_rule is not in the theory,
        # it follows that it is impossible to derive the conjecture from that inference_rule in this theory.
        u1.log_debug(
            f'derive_2: The derivation failed because the inference-rule is not contained in the theory. '
            f'conjecture:{c}. inference_rule:{i}. ')
        return t, False, None

    # First try the less expansive auto_derive_0 algorithm
    t, successful, derivation, = derive_0(t=t, conjecture=c, debug=debug)
    if successful:
        return t, successful, derivation

    # In order to list what would be the required premises to yield the conjecture,
    # the inference-rule must be "reverse-engineered".

    # By comparing the inference-rule conclusion and the conjecture,
    # we can retrieve some known variable values.
    # Function is_formula_equivalent_with_variables_2 returns this map directly.
    conclusion_is_compatible_with_conjecture, known_variable_values = is_formula_equivalent_with_variables_2(
        phi=c,
        psi=i.transformation.conclusion,
        variables=i.transformation.variables,
        variables_fixed_values=None)
    if conclusion_is_compatible_with_conjecture:
        # The conclusion of the inference-rule is compatible with the conjecture.
        # It is thus worth pursuing the attempt.

        # By contrast, the unknown variable values can be listed.
        unknown_variable_values: Enumeration = Enumeration()
        for x in i.transformation.variables:
            if not is_element_of_enumeration(element=x, enumeration=known_variable_values.domain):
                unknown_variable_values = Enumeration(elements=(*unknown_variable_values, x,))

        # Using substitution for the known_variable_values,
        # a more accurate set of premises can be computed, denoted necessary_premises.
        necessary_premises: Tupl = Tupl(
            elements=replace_formulas(phi=i.transformation.premises, m=known_variable_values))
        # necessary_premises: Tupl = Tupl(elements=None)
        # for original_premise in inference_rule.transformation.premises:
        #    necessary_premise = replace_formulas(phi=original_premise, m=known_variable_values)
        #    necessary_premises: Tupl = Tupl(elements=(*necessary_premises, necessary_premise,))

        # Find a set of valid_statements in theory t, such that they match the necessary_premises.
        success, effective_premises = are_valid_statements_in_theory_with_variables(
            s=necessary_premises, t=t, variables=i.transformation.variables,
            variables_values=known_variable_values)

        if success:
            # All required premises are present in theory t, the conjecture can be proven.
            t, derivation = derive_1(t=t, c=c, p=effective_premises,
                                     i=i)
            return t, True, derivation
        else:
            # The required premises are not present in theory t, report failure.
            return t, False, None

    # The conclusion of the inference_rule is not compatible with the conjecture.
    return t, False, None


def auto_derive_with_heuristics(t: FlexibleTheory, conjecture: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[Theory, bool]:
    """Attempt to derive automatically a conjecture using the heuristics attached to the theory.

    :param t:
    :param conjecture:
    :param debug:
    :return: a tuple (t, success)
    """
    for heuristic in t.heuristics:
        t, success = heuristic.process_conjecture(conjecture=conjecture, t=t)
        if success:
            return t, True
    return t, False


def auto_derive_2(t: FlexibleTheory, conjecture: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """An algorithm that attempts to automatically prove a conjecture in a theory.

    The auto_derive_2 algorithm "wide and shallow inference" builds on auto_derive_1 and:
    1) loop through all inference-rules in theory t, and try the auto_derive_1 algorithm.

    Note: this algorithm is still trivial as it does not rely on recursion to look for solutions.

    :param t:
    :param conjecture:
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    t = coerce_theory(t=t)
    conjecture = coerce_formula(phi=conjecture)
    if debug:
        u1.log_debug(f'auto_derive_2: start. conjecture:{conjecture}.')

    # Loop through all inference_rules in theory t.
    for inference_rule in t.iterate_inference_rules():
        t, success, d = derive_2(t=t, c=conjecture, i=inference_rule)
        if success:
            # Eureka, the conjecture was proven.
            return t, success, d

    # Unfortunately, we tried to prove the conjecture from all inference_rules without success.
    return t, False, None


auto_derivation_max_formula_depth_preference = 4


def auto_derive_3(
        t: FlexibleTheory, conjectures: FlexibleTupl) -> \
        typing.Tuple[Theory, bool]:
    """An auto-derivation algorithm that receives a tuple (basically an ordered list) of conjectures,
    and that applies auto-derivation-2 to derive these conjectures in sequence.

    :param t:
    :param conjectures:
    :return:
    """
    t: Theory = coerce_theory(t=t)
    conjectures: Tupl = coerce_tupl(t=conjectures)
    for conjecture in iterate_tuple_elements(phi=conjectures):
        t, success, _ = auto_derive_2(t=t, conjecture=conjecture)
        if not success:
            return t, False
    return t, True


def auto_derive_4(
        t: FlexibleTheory, conjecture: FlexibleFormula, max_recursion: int = 3,
        conjecture_exclusion_list: FlexibleEnumeration = None, debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation], FlexibleEnumeration]:
    """An algorithm that attempts to automatically prove a conjecture in a theory.

    The auto_derive_3 algorithm "wide and deep inference" builds upon auto_derive_2 and:
    1) loop through all inference-rules in theory t, and recursively calls itself to attempt to prove premises,
       until max_recursion is reached at which point call auto_derive_1 algorithm.

    auto_derive_3 is a depth-first algorithm, which makes it often very inefficient because
    if max_recursion is increased, the search space increases dramatically.
    a width-first algorithm would probably be more interesting in most practical situations.

    recursively try to auto_derive the premises,
    and this is complex because of free-variables.
    proposed approach:
           loop on candidate inference-rules:
               loop on all combinations of premises, taking into account free variables,
               that may yield the conclusion.
               recursively call auto_derive_2 for more depth,
               or call auto_derive_1 to stop at the next level.

    :param t:
    :param conjecture:
    :param max_recursion:
    :param conjecture_exclusion_list:
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    global auto_derivation_max_formula_depth_preference
    t: Theory = coerce_theory(t=t)
    conjecture: Formula = coerce_formula(phi=conjecture)
    conjecture_exclusion_list: Enumeration = coerce_enumeration(e=conjecture_exclusion_list)
    indent: str = ' ' * (auto_derivation_max_formula_depth_preference - max_recursion + 1)
    if max_recursion == 2:
        pass
    if debug:
        u1.log_debug(f'{indent}auto_derive_3: start. conjecture:{conjecture}.')

    # As a first step, attempt to auto_derive the conjecture with the less powerful,
    # but less expansive auto_derive_2 method:
    t, successful, derivation, = auto_derive_2(t=t, conjecture=conjecture)
    if successful:
        if debug:
            u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{conjecture}.')
        return t, successful, derivation, None

    # To prevent infinite loops, populate an exclusion list of conjectures that are already
    # being searched in higher recursions.
    conjecture_exclusion_list = Enumeration(elements=(*conjecture_exclusion_list, conjecture,))

    max_recursion = max_recursion - 1
    if max_recursion < 1:
        # We reached the max_recursion threshold, it follows that auto_derive failed.
        if debug:
            u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{conjecture}.')
        return t, False, None, conjecture_exclusion_list

    # Loop through all theory inference-rules to find those that could potentially prove the conjecture.
    # These are the inference-rules whose conclusions are formula-equivalent-with-variables to the conjecture.
    for inference_rule in t.iterate_inference_rules():
        inference_rule_success: bool = False
        is_equivalent, m = is_formula_equivalent_with_variables_2(phi=conjecture,
                                                                  psi=inference_rule.transformation.conclusion,
                                                                  variables=inference_rule.transformation.variables)
        if is_equivalent:
            # This inference-rule is compatible with the conjecture.

            # To list what would be the required premises to derive the conjecture,
            # the inference_rule must be "reverse-engineered".

            # first determine what are the necessary variable values in the transformation.
            # to do this, we have a trick, we can call is_formula_equivalent_with_variables and pass it
            # an empty map-builder:
            output, m, = is_formula_equivalent_with_variables_2(phi=conjecture,
                                                                psi=inference_rule.transformation.conclusion,
                                                                variables=inference_rule.transformation.variables,
                                                                variables_fixed_values=None)

            # then we list the variables for which we don't have an assigned value,
            # called the free-variables.
            free_variables: Enumeration = Enumeration()
            for x in inference_rule.transformation.variables:
                if not is_element_of_enumeration(element=x, enumeration=m.domain):
                    free_variables = Enumeration(elements=(*free_variables, x,))
            # u1.log_info(f'\t\t free-variables: {free_variables}')

            # now that we know what are the necessary variable values, we can determine what
            # are the necessary premises by substituting the variable values.
            necessary_premises: Tupl = Tupl(elements=None)
            for original_premise in inference_rule.transformation.premises:
                # we must find a set of premises in the theory
                # with free-variables.
                # I see two possible strategies:
                # 1) elaborate a new single proposition with the conjunction P1 and P2 and ... and Pn with all premises
                #    and then try to find that proposition in the theory, taking into account variables.
                # 2) develop an algorithm that given a set of premises returns true if they are all valid,
                #    and then extend this algorithm to support variables.
                # to avoid the burden of all these conjunctions in the theory, I start with the second approach.
                necessary_premise: Formula = replace_formulas(phi=original_premise, m=m)
                necessary_premises: Tupl = Tupl(elements=(*necessary_premises, necessary_premise,))

            # the following step is where auto_derive_2 is different from auto_derive_1.
            # we are not assuming that there should exist valid premises to derive the target statement,
            # but instead we recursively auto_derive all required effective premises
            # hoping to eventually derive the target statement.

            # **********************************************
            permutation_size: int = free_variables.arity

            if permutation_size == 0:
                inference_rule_success: bool = True
                # there are no free variables.
                # but there may be some or no variables with assigned values.
                # it follows that 1) there will be no permutations,
                # and 2) are_valid_statements_in_theory() is equivalent.
                effective_premises: Formula = replace_formulas(phi=necessary_premises, m=m)
                effective_premises: Tupl = Tupl(elements=effective_premises)
                for premise_target_statement in effective_premises:
                    if not is_element_of_enumeration(element=premise_target_statement,
                                                     enumeration=conjecture_exclusion_list):
                        # recursively try to auto_derive the premise
                        t, derivation_success, _, conjecture_exclusion_list = auto_derive_4(
                            t=t,
                            conjecture=premise_target_statement,
                            conjecture_exclusion_list=conjecture_exclusion_list,
                            max_recursion=max_recursion - 1,
                            debug=debug)
                        if not derivation_success:
                            inference_rule_success = False
                            break
                if inference_rule_success:
                    # all premises have been successfully proven.
                    t, derivation = derive_1(t=t, c=conjecture,
                                             p=effective_premises,
                                             i=inference_rule)
                    if debug:
                        u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{conjecture}.')
                    return t, True, derivation, conjecture_exclusion_list
            else:
                valid_statements = iterate_valid_statements_in_theory(t=t)
                for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                                n=permutation_size):
                    permutation_success: bool = True
                    variable_substitution: Map = Map(domain=free_variables, codomain=permutation)
                    effective_premises: Formula = replace_formulas(phi=necessary_premises, m=variable_substitution)
                    effective_premises: Tupl = Tupl(elements=(*effective_premises, permutation,))
                    for premise_target_statement in effective_premises:
                        if not is_element_of_enumeration(element=premise_target_statement,
                                                         enumeration=conjecture_exclusion_list):
                            # recursively try to auto_derive the premise
                            t, derivation_success, _, conjecture_exclusion_list = auto_derive_4(
                                t=t, conjecture=premise_target_statement,
                                conjecture_exclusion_list=conjecture_exclusion_list,
                                max_recursion=max_recursion - 1, debug=debug)
                            if not derivation_success:
                                permutation_success = False
                                break
                    if permutation_success:
                        # all premises have been successfully proven.
                        t, derivation = derive_1(t=t, c=conjecture,
                                                 p=effective_premises,
                                                 i=inference_rule)
                        if debug:
                            u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{conjecture}.')
                        return t, True, derivation, conjecture_exclusion_list
    if debug:
        u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{conjecture}.')
    return t, False, None, conjecture_exclusion_list


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
                yield from pl1.symbols.comma.typeset_from_generator(**kwargs)
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
        phi: Transformation = coerce_transformation(t=phi)

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


class MapTypesetter(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: Formula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Map = coerce_map(m=phi)
        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True

        yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        first = True
        for domain_element, codomain_element in zip(phi.domain, phi.codomain):
            if not first:
                yield from pl1.symbols.comma.typeset_from_generator(**kwargs)
                yield from pl1.symbols.space.typeset_from_generator(**kwargs)
            first = False
            yield from domain_element.typeset_from_generator(**kwargs)
            yield from pl1.symbols.space.typeset_from_generator(**kwargs)
            yield from pl1.symbols.maps_to.typeset_from_generator(**kwargs)
            yield from pl1.symbols.space.typeset_from_generator(**kwargs)
            yield from codomain_element.typeset_from_generator(**kwargs)
        yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class DerivationTypesetter(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleDerivation, theory: typing.Optional[FlexibleTheory] = None,
                               **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Derivation = coerce_derivation(d=phi)
        if theory is not None:
            i: int = 1 + get_index_of_first_equivalent_term_in_formula(term=phi, formula=theory)
            yield f'({i})\t'
        yield from phi.valid_statement.typeset_from_generator(**kwargs)
        if is_well_formed_axiom(a=phi):
            phi: Axiom = coerce_axiom(a=phi)
            yield '\t\t| Axiom.'
        elif is_well_formed_inference_rule(i=phi):
            phi: InferenceRule = coerce_inference_rule(i=phi)
            yield '\t\t| Inference rule.'
        elif is_well_formed_theorem(t=phi):
            phi: Theorem = coerce_theorem(t=phi)
            inference: Inference = phi.inference
            transformation: Transformation = inference.transformation_rule
            yield '\t\t| Follows from '
            if theory is not None:
                # yield from phi.inference.transformation_rule.typeset_as_string(**kwargs)
                i = 0
                j = 0
                for ir in theory:
                    if is_well_formed_inference_rule(i=ir):
                        ir: InferenceRule
                        if is_formula_equivalent(phi=ir.transformation, psi=transformation):
                            j = i
                    i = i + 1
                yield f'({j}) given '
                # yield from phi.inference.premises.typeset_as_string(**kwargs)
                first = True
                for premise in phi.inference.premises:
                    i: int = 1 + get_index_of_first_equivalent_term_in_formula(term=premise,
                                                                               formula=theory.valid_statements)
                    if not first:
                        yield ', '
                    yield f'({i})'
                    first = False
            else:
                yield from inference.typeset_as_string(**kwargs)
            # for premise in phi.inference.premises:
            #    i: int = 1 + get_index_of_first_equivalent_term_in_formula(phi=premise, psi=theory)
            #    yield f'({i})\t'
            yield '.'


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

    def map(self) -> MapTypesetter:
        return MapTypesetter()

    def transformation(self) -> TransformationTypesetter:
        return TransformationTypesetter()

    def derivation(self) -> DerivationTypesetter:
        return DerivationTypesetter()


typesetters = Typesetters()
