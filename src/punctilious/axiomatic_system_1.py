from __future__ import annotations

import collections
import logging
import typing
import warnings
# import threading
import sys

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


event_codes: ErrorCodes = _set_state(key='event_codes', value=ErrorCodes(
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
                           'formula. Here, the claimed formula is not formula-equivalent to the algorithm output. In '
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
                   message='While checking the well-formedness of a derivation, a premise is necessary to derive a '
                           'theorem, but it is absent from the derivation.'),
    e112=ErrorCode(event_type=event_types.error, code='e112',
                   message='While checking the well-formedness of a derivation, a premise is necessary to derive a '
                           'theorem, but its position in the derivation is posterior to the theorem.'),
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
                   message='While checking the well-formedness of a derivation, a transformation-rule is necessary '
                           'to derive a theorem, but it is absent from the derivation.'),
    e120=ErrorCode(event_type=event_types.error, code='e120',
                   message='During the initialization of a derivation (in the __new__ or __init__ methods of the '
                           'Derivation class), the well-formedness of the derivation is verified. This '
                           'verification failed, in consequence the derivation would be ill-formed. The error '
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

    def __init__(self, error_code: ErrorCode, **kwargs):
        self.error_code = error_code
        self.kwargs = kwargs
        super().__init__()

    def __str__(self) -> str:
        return self.rep()

    def __repr__(self) -> str:
        return self.rep()

    def rep(self) -> str:
        kwargs: str = '\n\t'.join(f'{key}: {value}' for key, value in self.kwargs.items())
        return f'{self.error_code.event_type} {self.error_code.code}\n\t{self.error_code.message}\n\t{kwargs}'


def raise_error(error_code: ErrorCode, **kwargs):
    """Raise a technical event.

    :param error_code:
    :param kwargs:
    :return:
    """
    exception: CustomException = CustomException(error_code=error_code, **kwargs)
    if error_code.event_type == event_types.error:
        logging.exception(msg=exception.rep())
        raise exception
    elif error_code.event_type == event_types.warning:
        logging.warning(msg=exception.rep())
        warnings.warn(message=exception.rep())


class TextTypesetter(pl1.Typesetter):
    """TODO: implement support for multiple font variants.

    """

    def __init__(self, text: str):
        super().__init__()
        self._text: str = text

    @property
    def text(self) -> str:
        return self._text

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        yield self.text


class Connective:
    """A node color in a formula tree."""

    def __init__(self, rep: typing.Optional[FlexibleRepresentation] = None, formula_typesetter: pl1.Typesetter = None):
        """

        :param rep: A default text representation.
        """
        self._rep = rep
        if formula_typesetter is None and rep is not None:
            # temporary fix
            # if len(rep) == 1:
            #    formula_typesetter = pl1.symbols.get_sans_serif_letter(letter=rep)
            # else:
            formula_typesetter = TextTypesetter(text=rep)
        self._formula_typesetter: pl1.Typesetter = formula_typesetter

    def __call__(self, *args):
        """Allows pseudo formal language in python."""
        return Formula(connective=self, terms=args)

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def formula_typesetter(self) -> pl1.Typesetter:
        return self._formula_typesetter

    @formula_typesetter.setter
    def formula_typesetter(self, formula_typesetter: pl1.Typesetter):
        self._formula_typesetter = formula_typesetter

    def rep(self, **kwargs):
        return self._rep

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
        self.c: typing.Optional[Connective] = c

        # When inheriting from list, we implement __init__ and not __new__.
        # Reference: https://stackoverflow.com/questions/9432719/python-how-can-i-inherit-from-the-built-in-list-type
        super().__init__(self)
        if isinstance(terms, collections.abc.Iterable):
            coerced_tuple = tuple(coerce_formula_builder(term) for term in terms)
            for term in coerced_tuple:
                self.append(term=term)
        elif terms is not None:
            raise_error(error_code=event_codes.e100, c=c, terms_type=type(terms), terms=terms)

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
        return self.rep()

    def __setitem__(self, i: int, phi: FlexibleFormula) -> None:
        self.set_term(i=i, phi=phi)

    def __str__(self):
        return self.rep()

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

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        if isinstance(self.c, NullaryConnective):
            return f'{self.c.rep()}'
        elif isinstance(self.c, BinaryConnective):
            term_0: str = self.term_0.rep(**kwargs) if self.term_0 is not None else '?'
            term_1: str = self.term_1.rep(**kwargs) if self.term_1 is not None else '?'
            return f'{'(' if parenthesis else ''}{term_0} {self.c.rep()} {term_1}{')' if parenthesis else ''}'
        else:
            c: str = self.c.rep(**kwargs) if self.c is not None else '?'
            terms: str = ', '.join(term.rep(**kwargs) if term is not None else '?' for term in self)
            return f'{'(' if parenthesis else ''}{c}({terms}){')' if parenthesis else ''}'

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
        if self.c is None:
            raise_error(error_code=event_codes.e113, formula_builder=self, c=self.c)
        terms: tuple[Formula, ...] = tuple(coerce_formula(phi=term) for term in self)
        phi: Formula = Formula(connective=self.c, terms=terms)
        return phi

    def validate_formula_builder(self) -> bool:
        """Validate the syntactical consistency of a candidate formula."""
        # TODO: validate_formula_builder: check no infinite loops
        # TODO: validate_formula_builder: check all nodes have a connective
        return True


class Formula(tuple):
    """An immutable formula modeled as an edge-ordered, node-colored tree."""

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed formula, False otherwise.

        Note: the Formula python class assures the well-formedness of formulas. Hence, this function is trivial: if
        phi coerces to Formula, it is a well-formed formula.

        :param phi: A formula.
        :return: bool.
        """
        # TODO: Formula.is_well_formed: review this to avoid raising an exception, but return False instead.
        phi: Formula = coerce_formula(phi=phi)
        return True

    def __new__(cls, connective: Connective, terms: FlexibleTupl = None,
                typesetting_configuration: typing.Optional[pl1.TypesettingConfiguration] = None):
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
            raise_error(error_code=event_codes.e101, c=connective, terms_type=type(terms), terms=terms)

    def __init__(self, connective: Connective, terms: FlexibleTupl = None,
                 typesetting_configuration: typing.Optional[pl1.TypesettingConfiguration] = None):
        super().__init__()
        self._connective = connective
        self._typesetter: typing.Optional[pl1.TypesettingConfiguration] = typesetting_configuration

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
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def arity(self) -> int:
        """The arity of a formula is equal to the number of terms that are direct children of its root node."""
        return len(self)

    @property
    def c(self) -> Connective:
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
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.
        :rtype: bool
        """
        return is_term_of_formula(phi=phi, psi=self)

    def rep(self, **kwargs) -> str:

        if self.get_typesetter(typesetter=None) is not pl1.typesetters.failsafe:
            # NEW METHOD
            return self.typeset_as_string(**kwargs)
        else:
            # OBSOLETE METHOD, TO BE PROGRESSIVELY PHASED OUT
            parenthesis = kwargs.get('parenthesis', False)
            kwargs['parenthesis'] = True
            if isinstance(self.c, NullaryConnective):
                return f'{self.c.rep()}'
            elif isinstance(self.c, BinaryConnective):
                return (f'{'(' if parenthesis else ''}'
                        f'{self.term_0.rep(**kwargs)} {self.c.rep()} {self.term_1.rep(**kwargs)}'
                        f'{')' if parenthesis else ''}')
            else:
                terms: str = ', '.join(term.rep(**kwargs) for term in self)
                return f'{'(' if parenthesis else ''}{self.c.rep(**kwargs)}({terms}){')' if parenthesis else ''}'

    @property
    def term_0(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 1:
            raise_error(error_code=event_codes.e103, c=self.c)
        return self[0]

    @property
    def term_1(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 2:
            raise_error(error_code=event_codes.e104, c=self.c)
        return self[1]

    @property
    def term_2(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 3:
            raise_error(error_code=event_codes.e104, c=self.c)
        return self[2]

    def to_formula_builder(self) -> FormulaBuilder:
        """Returns a formula-builder that is equivalent to this formula.
        This makes it possible to edit the formula-builder to elaborate new formulas."""
        terms: tuple[FormulaBuilder, ...] = tuple(coerce_formula_builder(phi=term) for term in self)
        phi: FormulaBuilder = FormulaBuilder(c=self.c, terms=terms)
        return phi

    def get_typesetter(self, typesetter: typing.Optional[
        pl1.Typesetter] = None) -> pl1.Typesetter:
        """

         - priority 1: parameter typesetter is passed explicitly.
         - priority 2: a typesetting-configuration is attached to the formula, and its typesetting-method is defined.
         - priority 3: a typesetting-configuration is attached to the formula connective, and its typesetting-method is defined.
         - priority 4: failsafe typesetting method.

        :param typesetter:
        :return:
        """

        if typesetter is None:
            if self.typesetter is not None:
                typesetter: pl1.Typesetter = self.typesetter
            elif self.c.formula_typesetter is not None:
                typesetter: pl1.Typesetter = self.c.formula_typesetter
            else:
                typesetter = pl1.typesetters.failsafe
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

    @property
    def typesetter(self) -> pl1.Typesetter:
        return self._typesetter

    @typesetter.setter
    def typesetter(self, typesetter: pl1.Typesetter):
        self._typesetter = typesetter


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
        raise_error(error_code=event_codes.e123, coerced_type=FormulaBuilder, phi_type=type(phi), phi=phi)


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
        raise_error(error_code=event_codes.e123, coerced_type=Formula, phi_type=type(phi), phi=phi)


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
        return Enumeration(elements=phi, connective=phi.c)
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
        # phi: Formula = Formula(c=connectives.e, terms=phi)
        return Enumeration(elements=phi)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Enumeration, phi_type=type(phi), phi=phi)


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


def union_derivation(phi: FlexibleDerivation, psi: FlexibleDerivation) -> Derivation:
    """Given two derivations phi, and psi, the union-derivation operator, noted phi ∪-derivation psi,
    returns a new derivation omega such that:
    - all valid-statements of phi are elements of omega,
    - all valid-statements of psi are elements of omega,
    - no other valid-statements are valid-statements of omega.
    Order is preserved, that is:
    - the valid-statements from phi keep their original order in omega
    - the valid-statements from psi keep their original order in omega providing they are not already present in phi,
        in which case they are skipped

    Under derivation-equivalence, the union-derivation operator is:
     - Idempotent: (phi ∪-derivation phi) ~derivation phi.
     - Symmetric: (phi ∪-derivation psi) ~derivation (psi ∪-derivation phi).

    Under formula-equivalence, the union-derivation operator is:
     - Idempotent: (phi ∪-derivation phi) ~formula phi.
     - Not symmetric if some element of psi are elements of phi: because of order.
    """
    phi: Derivation = coerce_derivation(phi=phi)
    psi: Derivation = coerce_derivation(phi=psi)
    db: DerivationBuilder = DerivationBuilder(valid_statements=None)
    for phi_prime in phi:
        db.append(term=phi_prime)
    for psi_prime in psi:
        db.append(term=psi_prime)
    d: Derivation = db.to_derivation()
    return d


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
        raise_error(error_code=event_codes.e123, coerced_type=EnumerationBuilder, phi_type=type(phi), phi=phi)


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
        raise_error(error_code=event_codes.e123, coerced_type=Map, phi_type=type(phi), phi=phi)


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
        raise_error(error_code=event_codes.e123, coerced_type=MapBuilder, phi_type=type(phi), phi=phi)


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
        raise_error(error_code=event_codes.e123, coerced_type=Tupl, phi_type=type(phi), phi=phi)


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
        raise_error(error_code=event_codes.e123, coerced_type=TuplBuilder, phi_type=type(phi), phi=phi)


FlexibleFormula = typing.Optional[typing.Union[Connective, Formula, FormulaBuilder]]


class FreeArityConnective(Connective):
    """A free-arity connective is a connective without constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self, rep: str):
        super().__init__(rep=rep)


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective with a constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self,
                 fixed_arity_constraint: int, formula_typesetter: pl1.Typesetter = None,
                 rep: FlexibleRepresentation = None):
        self._fixed_arity_constraint = fixed_arity_constraint
        super().__init__(formula_typesetter=formula_typesetter, rep=rep)

    @property
    def fixed_arity_constraint(self) -> int:
        return self._fixed_arity_constraint


class NullaryConnective(FixedArityConnective):

    def __init__(self, rep: FlexibleRepresentation = None):
        super().__init__(rep=rep, fixed_arity_constraint=0)


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

    def rep(self, **kwargs) -> str:
        kwargs['parenthesis'] = True
        return f'{self.c.rep(**kwargs)}'


class UnaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=1)


class InfixPartialFormula:
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and gluing all this together with the InfixPartialFormula class.
    """

    def __init__(self, c: Connective, term_1: FlexibleFormula):
        self._c = c
        self._term_1 = term_1

    def __or__(self, term_2: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        return Formula(connective=self._c, terms=(self.term_1, term_2,))

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def c(self) -> Connective:
        return self._c

    def rep(self, **kwargs):
        kwargs['parenthesis'] = True
        return f'{self.c.rep(**kwargs)}({self.term_1.rep(**kwargs)}, ?)'

    @property
    def term_1(self) -> Connective:
        return self._term_1


class BinaryConnective(FixedArityConnective):

    def __init__(self, rep: FlexibleRepresentation = None, formula_typesetter: pl1.Typesetter = None):
        super().__init__(formula_typesetter=formula_typesetter, rep=rep, fixed_arity_constraint=2)

    def __ror__(self, other: FlexibleFormula):
        """Pseudo math notation. x | p | ?."""
        return InfixPartialFormula(c=self, term_1=other)


def is_term_of_formula(phi: Formula, psi: Formula) -> bool:
    """Returns True if phi is a term of psi, False otherwise.

    :param phi: A formula.
    :type phi: FlexibleFormula
    :param psi: A formula.
    :type psi: FlexibleFormula
    ...
    :return: True if phi is a term of psi, False otherwise.
    :rtype: bool
    """
    phi = coerce_formula(phi=phi)
    psi = coerce_formula(phi=psi)
    return any(is_formula_equivalent(phi=phi, psi=psi_term) for psi_term in psi)


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
    raise_error(error_code=event_codes.e109, phi=phi, psi=psi)


class TernaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=3)


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


def let_x_be_a_variable(rep: FlexibleRepresentation) -> typing.Union[
    Variable, typing.Generator[Variable, typing.Any, None]]:
    if isinstance(rep, str):
        return Variable(connective=NullaryConnective(rep=rep))
    elif isinstance(rep, typing.Iterable):
        return (Variable(connective=NullaryConnective(rep=r)) for r in rep)
    else:
        raise TypeError  # TODO: Implement event code.


def let_x_be_a_propositional_variable_OBSOLETE(
        rep: FlexibleRepresentation,
        db: typing.Union[FlexibleDerivationBuilder, EnumerationBuilder] = None) -> \
        typing.Union[Variable, typing.Generator[Variable, typing.Any, None]]:
    """

    :param rep:
    :param db: If a derivation-builder is provided, append the axiom (x is-a proposition) where x is the new
        variable. Alternatively, an enumeration-builder may be provided.
    :return:
    """
    # TODO: RESUME IMPLEMENTATION OF PARAMETER DB HERE.
    # TODO: EITHER MOVE THIS FUNCTION TO INFERENCE_RULES_1 OR MOVE FUNDAMENTAL LOGIC CONNECTIVES HERE
    if db is not None:
        db = coerce_derivation_builder(phi=db)
    if isinstance(rep, str):
        x = Variable(connective=NullaryConnective(rep=rep))
        if db is not None:
            db.append(term=Axiom(claim=x | connectives.is_a | connectives.propositional_variable))
        return x
    elif isinstance(rep, typing.Iterable):
        t = tuple()
        for r in rep:
            x = Variable(connective=NullaryConnective(rep=r))
            if db is not None:
                db.append(term=Axiom(claim=x | connectives.is_a | connectives.propositional_variable))
            t = t + (x,)
        return t
    else:
        raise TypeError  # TODO: Implement event code.


def v(rep: FlexibleRepresentation) -> typing.Union[
    NullaryConnective, typing.Generator[NullaryConnective, typing.Any, None]]:
    """A shortcut for let_x_be_a_variable."""
    return let_x_be_a_variable(rep=rep)


FlexibleRepresentation = typing.Union[str, pl1.Symbol, pl1.Typesetter]
"""FlexibleRepresentation is a flexible python type that may be safely coerced to a symbolic representation."""

FlexibleMultiRepresentation = typing.Union[FlexibleRepresentation, typing.Iterable[FlexibleRepresentation]]
"""FlexibleMultiRepresentation is a flexible python type that may be safely coerced to a single or multiple symbolic 
representation."""


def let_x_be_a_simple_object(rep: typing.Optional[FlexibleMultiRepresentation] = None) -> typing.Union[
    SimpleObject, typing.Generator[SimpleObject, typing.Any, None]]:
    """A helper function to declare one or multiple simple-objects.

    :param rep: A string (or an iterable of strings) default representation for the simple-object(s).
    :return: A simple-object (if rep is a string), or a python-tuple of simple-objects (if rep is an iterable).
    """
    if isinstance(rep, FlexibleRepresentation):
        return SimpleObject(connective=NullaryConnective(rep=rep))
    elif isinstance(rep, typing.Iterable):
        return (SimpleObject(connective=NullaryConnective(rep=r)) for r in rep)
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


def let_x_be_a_binary_connective(rep: str):
    return BinaryConnective(rep=rep)


def let_x_be_a_ternary_connective(rep: str):
    return TernaryConnective(rep=rep)


def let_x_be_a_unary_connective(rep: str):
    return UnaryConnective(rep=rep)


def let_x_be_a_free_arity_connective(rep: str):
    return FreeArityConnective(rep=rep)


def let_x_be_an_inference_rule_deprecated(claim: FlexibleTransformation):
    return InferenceRule(transformation=claim)


def let_x_be_an_inference_rule(theory: FlexibleDerivation,
                               inference_rule: typing.Optional[FlexibleInferenceRule] = None,
                               premises: typing.Optional[FlexibleTupl] = None,
                               conclusion: typing.Optional[FlexibleFormula] = None,
                               variables: typing.Optional[FlexibleEnumeration] = None):
    if theory is None:
        theory = Axiomatization(axioms=None)
    else:
        theory: FlexibleDerivation = coerce_derivation(phi=theory)

    if inference_rule is None and premises is not None and conclusion is not None and variables is not None:
        transformation: Transformation = Transformation(premises=premises, conclusion=conclusion, variables=variables)
        inference_rule: InferenceRule = InferenceRule(transformation=transformation)

    if isinstance(theory, Axiomatization):
        theory = Axiomatization(axioms=(*theory, inference_rule,))
        return theory, inference_rule
    elif isinstance(theory, Derivation):
        theory = Derivation(valid_statements=(*theory, inference_rule,))
        return theory, inference_rule
    else:
        raise Exception('oops')


def let_x_be_an_axiom_deprecated(claim: FlexibleFormula):
    return Axiom(claim=claim)


def let_x_be_an_axiom(theory: FlexibleDerivation, claim: typing.Optional[FlexibleFormula] = None,
                      axiom: typing.Optional[FlexibleAxiom] = None):
    """

    :param theory: An axiom-collection or a derivation. If None, the empty axiom-collection is implicitly used.
    :param claim: The statement claimed by the new axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :param axiom: An existing axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :return: a pair (t, a,) where t is an extension of the input theory, with a new axiom claiming the
    input statement, and a is the new axiom.
    """
    if theory is None:
        theory = Axiomatization(axioms=None)
    else:
        theory: FlexibleDerivation = coerce_derivation(phi=theory)
    if claim is not None and axiom is not None:
        raise Exception('ooops 1')
    elif claim is None and axiom is None:
        raise Exception('oops 2')
    elif claim is not None:
        axiom: Axiom = Axiom(claim=claim)

    if isinstance(theory, Axiomatization):
        theory = Axiomatization(axioms=(*theory, axiom,))
        return theory, axiom
    elif isinstance(theory, Derivation):
        theory = Derivation(valid_statements=(*theory, axiom,))
        return theory, axiom
    else:
        raise Exception('oops 3')


def let_x_be_a_theory(valid_statements: typing.Optional[FlexibleEnumeration] = None):
    """

    :param valid_statements: an enumeration of valid-statements. If None, the empty theory is implicitly assumed.
    :return:
    """
    return Derivation(valid_statements=valid_statements)


def let_x_be_a_collection_of_axioms(axioms: FlexibleEnumeration):
    return Axiomatization(axioms=axioms)


def let_x_be_a_transformation(premises: FlexibleTupl, conclusion: FlexibleFormula,
                              variables: FlexibleEnumeration):
    return Transformation(premises=premises, conclusion=conclusion, variables=variables)


class Connectives(typing.NamedTuple):
    axiom: UnaryConnective
    derivation: FreeArityConnective
    e: FreeArityConnective
    """The enumeration connective, cf. the Enumeration class.
    """

    f: TernaryConnective
    """The transformation connective, cf. the Transformation class.
    """
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
    transformation: TernaryConnective
    tupl: FreeArityConnective


connectives: Connectives = _set_state(key='connectives', value=Connectives(
    axiom=let_x_be_a_unary_connective(rep='axiom'),
    derivation=let_x_be_a_free_arity_connective(rep='derivation'),
    e=let_x_be_a_free_arity_connective(rep='e'),  # enumeration
    f=let_x_be_a_ternary_connective(rep='f'),  # Transformation, # duplicate with transformation?
    follows_from=let_x_be_a_binary_connective(rep='follows-from'),
    implies=let_x_be_a_binary_connective(rep='implies'),
    inference=let_x_be_a_binary_connective(rep='inference'),
    inference_rule=let_x_be_a_unary_connective(rep='inference-rule'),
    is_a=let_x_be_a_binary_connective(rep='is-a'),
    land=let_x_be_a_binary_connective(rep='∧'),
    lnot=let_x_be_a_unary_connective(rep='¬'),
    lor=let_x_be_a_binary_connective(rep='∨'),
    map=let_x_be_a_binary_connective(rep='map'),
    proposition=let_x_be_a_simple_object(rep='proposition'),
    propositional_variable=let_x_be_a_simple_object(rep='propositional-variable'),
    transformation=let_x_be_a_ternary_connective(rep='-->'),  # duplicate with f?
    tupl=let_x_be_a_free_arity_connective(rep='tuple'),

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
    return phi.c is psi.c


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
            raise_error(error_code=event_codes.e122, phi=phi, psi=psi)
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
        raise_error(error_code=event_codes.e118, phi=phi, psi=psi, v=variables)
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
                    raise_error(error_code=event_codes.e121, variable=psi,
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
        fb: FormulaBuilder = FormulaBuilder(c=phi.c)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = replace_formulas(phi=term, m=m)
            fb.append(term=term_substitute)
        return fb.to_formula()


class TuplBuilder(FormulaBuilder):
    """A utility class to help build tuples. It is mutable and thus allows edition."""

    def __init__(self, elements: FlexibleTupl):
        super().__init__(c=connectives.tupl, terms=elements)

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        elements: str = ', '.join(element.rep(**kwargs) for element in self)
        return f'({elements})'

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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed tuple, False otherwise.

        Note: by definition, all formulas are also tuple. Hence, if phi is a formula, phi is a tuple.

        :param phi: A formula.
        :return: bool.
        """
        # TODO: Tupl.is_well_formed: review this to avoid raising an exception, but return False instead.
        phi: Formula = coerce_formula(phi=phi)
        return True

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

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        elements: str = ', '.join(element.rep(**kwargs) for element in self)
        return f'({elements})'

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

    def __init__(self, elements: FlexibleEnumeration):
        super().__init__(c=connectives.e, terms=None)
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
            raise_error(error_code=event_codes.e104, enumeration=self, term=term)
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
        enumeration: Enumeration = self.to_enumeration()
        return is_term_of_formula(phi=phi, psi=enumeration)

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        elements: str = ', '.join(element.rep(**kwargs) for element in self)
        return f'{{{elements}}}'

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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
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

    def __new__(cls, elements: FlexibleEnumeration = None, connective: Connective = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        connective: Connective = connectives.e if connective is None else connective
        if not is_well_formed_enumeration(phi=elements):
            raise_error(error_code=event_codes.e110, elements_type=type(elements), elements=elements)
        o: tuple = super().__new__(cls, connective=connectives.e, terms=elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None, connective: Connective = None):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        connective = connectives.e if connective is None else connective
        eb: EnumerationBuilder = EnumerationBuilder(elements=elements)
        super().__init__(connective=connectives.e, terms=eb)

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

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        elements: str = ', '.join(element.rep(**kwargs) for element in self)
        return f'{{{elements}}}'

    def to_enumeration_builder(self) -> EnumerationBuilder:
        return EnumerationBuilder(elements=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_enumeration_builder()


e = Enumeration
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


class EnumerationAccretor(EnumerationBuilder):
    """An enumeration-accretor is an enumeration-builder with additional constraints:
    it only allows appending new elements via the append-element and extend-with-elements operations,
    and it forbids the delete-element, insert-element, and set-element operations.


    """

    def __delitem__(self, phi: FlexibleFormula):
        """By definition, the delete-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e114."""
        raise_error(error_code=event_codes.e114, enumeration_accretor=self, phi=phi)

    def __setitem__(self, i, element):
        """By definition, the set-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e115."""
        raise_error(error_code=event_codes.e115, enumeration_accretor=self, index=i, element=element)

    def insert(self, index, element):
        """By definition, the insert-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e116."""
        raise_error(error_code=event_codes.e116, enumeration_accretor=self, index=index, element=element)

    def append(self, element: FlexibleFormula):
        """The append-element is the only operation allowed on enumeration-accretors that has the capability to
        modify its elements.

        This method is overridden for readability purposes."""
        super().append(term=element)

    def extend(self, elements: typing.Iterable[FlexibleFormula]):
        """The extend-with-elements operation is allowed on enumeration-accretors as a sequence of append-element
        operations.

        This method is overridden for readability purposes."""
        for element in elements:
            self.append(element=element)

    def pop(self, __index=-1):
        """By definition, the delete-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e114."""
        raise_error(error_code=event_codes.e114, enumeration_accretor=self, __index=__index)

    def remove(self, phi: FlexibleFormula) -> None:
        """By definition, the delete-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e114."""
        raise_error(error_code=event_codes.e114, enumeration_accretor=self, phi=phi)

    def remove_formula(self, phi: FlexibleFormula) -> None:
        """By definition, the delete-element operation is forbidden on enumeration-accretors.
        Calling this method raises exception e114."""
        raise_error(error_code=event_codes.e114, enumeration_accretor=self, phi=phi)


class TransformationBuilder(FormulaBuilder):

    def __init__(self, premises: FlexibleTupl, conclusion: FlexibleFormula,
                 variables: FlexibleTupl):
        premises: EnumerationBuilder = EnumerationBuilder(elements=premises)
        variables: EnumerationBuilder = EnumerationBuilder(elements=variables)
        super().__init__(c=connectives.inference, terms=(premises, conclusion, variables,))

    @property
    def conclusion(self) -> FormulaBuilder:
        return self[1]

    @property
    def premises(self) -> EnumerationBuilder:
        return self[0]

    def to_transformation(self) -> Transformation:
        premises = self.premises.to_enumeration()
        conclusion: Formula = self.conclusion.to_formula()
        variables = self.variables.to_enumeration()
        t: Transformation = Transformation(premises=premises, conclusion=conclusion, variables=variables)
        return t

    def to_formula(self) -> Formula:
        """Return a Transformation."""
        return self.to_transformation()

    @property
    def variables(self) -> EnumerationBuilder:
        return self[2]


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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed transformation, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_formula(phi=phi)
        if (phi.c is not connectives.transformation or
                phi.arity != 3 or
                not is_well_formed_tupl(phi=phi.term_0) or
                not is_well_formed_formula(phi=phi.term_1) or
                not is_well_formed_enumeration(phi=phi.term_2)):
            return False
        else:
            return True

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
            raise_error(error_code=event_codes.e117, error=error, arguments=arguments, premises=self.premises,
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

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        premises: str = ', '.join(premise.rep(**kwargs) for premise in self.premises)
        variables: str
        if self.variables.arity == 0:
            variables = ''
        elif self.variables.arity == 1:
            variables = f' where {self.variables.term_0} is a variable'
        else:
            variables = ', '.join(variable.rep(**kwargs) for variable in self.variables)
            variables = f' where {variables} are variables'
        return f'({premises}) --> ({self.conclusion}){variables}'

    def to_transformation_builder(self) -> TransformationBuilder:
        premises: TuplBuilder = self.premises.to_tupl_builder()
        conclusion: FormulaBuilder = self.conclusion.to_formula_builder()
        variables: EnumerationBuilder = self.variables.to_enumeration_builder()
        return TransformationBuilder(premises=premises, conclusion=conclusion, variables=variables)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_transformation_builder()

    @property
    def variables(self) -> Enumeration:
        return self[2]


FlexibleTransformation = typing.Optional[typing.Union[Transformation, TransformationBuilder]]


def coerce_transformation(phi: FlexibleTransformation) -> Transformation:
    if isinstance(phi, Transformation):
        return phi
    elif isinstance(phi, TransformationBuilder):
        return phi.to_transformation()
    elif isinstance(phi, Formula) and is_well_formed_transformation(phi=phi):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        return Transformation(premises=phi.term_0, conclusion=phi.term_1, variables=phi.term_2)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Transformation, phi_type=type(phi), phi=phi)


def coerce_transformation_builder(phi: FlexibleTransformation) -> TransformationBuilder:
    if isinstance(phi, TransformationBuilder):
        return phi
    elif isinstance(phi, Transformation):
        return phi.to_transformation_builder()
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Formula, phi_type=type(phi), phi=phi)


def coerce_inference(phi: FlexibleInference) -> Inference:
    if isinstance(phi, Inference):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_inference(phi=phi):
        transformation: Transformation = coerce_transformation(phi=phi.term_1)
        return Inference(premises=phi.term_0, transformation_rule=transformation)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Inference, phi_type=type(phi), phi=phi)


def is_well_formed_formula(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed formula, False otherwise.

    Note: the Formula python class assures the well-formedness of formulas.

    :param phi:
    :return: bool
    """
    return Formula.is_well_formed(phi=phi)


def is_well_formed_tupl(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed tuple, False otherwise.

    Note: by definition, all formulas are also tuples. Hence, return True if phi converts smoothly to a well-formed
    formula.

    :param phi:
    :return: bool
    """
    return Tupl.is_well_formed(phi=phi)


def is_well_formed_inference(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed inference, False otherwise."""
    return Inference.is_well_formed(phi=phi)


def is_well_formed_transformation(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed transformation, False otherwise."""
    return Transformation.is_well_formed(phi=phi)


def is_well_formed_enumeration(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed enumeration, False otherwise."""
    return Enumeration.is_well_formed(phi=phi)


def is_well_formed_inference_rule(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed inference-rule, False otherwise."""
    return InferenceRule.is_well_formed(phi=phi)


def is_well_formed_axiom(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed axiom, False otherwise."""
    return Axiom.is_well_formed(phi=phi)


def is_well_formed_theorem(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed theorem, False otherwise."""
    return Theorem.is_well_formed(phi=phi)


def is_well_formed_valid_statement(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed valid-statement, False otherwise."""
    return ValidStatement.is_well_formed(phi=phi)


def is_well_formed_derivation(phi: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
    """Returns True if phi is a well-formed derivation, False otherwise."""
    return Derivation.is_well_formed(phi=phi, raise_event_if_false=raise_event_if_false)


def is_well_formed_axiomatization(phi: FlexibleFormula) -> bool:
    """Returns True if phi is a well-formed axiomatization, False otherwise."""
    return Axiomatization.is_well_formed(phi=phi)


def coerce_valid_statement(phi: FlexibleFormula) -> ValidStatement:
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
        raise_error(error_code=event_codes.e123, coerced_type=ValidStatement, phi_type=type(phi), phi=phi)


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
        return Axiom(claim=proved_formula)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=InferenceRule, phi_type=type(phi), phi=phi)


def coerce_inference_rule(phi: FlexibleFormula) -> InferenceRule:
    """Validate that p is a well-formed inference-rule and returns it properly typed as an instance of InferenceRule,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, InferenceRule):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_inference_rule(phi=phi):
        proved_formula: Formula = phi.term_0
        return InferenceRule(transformation=proved_formula)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=InferenceRule, phi_type=type(phi), phi=phi)


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
        return Theorem(claim=proved_formula, i=inference)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Theorem, phi_type=type(phi), phi=phi)


def coerce_derivation(phi: FlexibleDerivation) -> Derivation:
    """Validate that phi is a well-formed derivation and returns it properly typed as Demonstration,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Derivation):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_derivation(phi=phi):
        return Derivation(valid_statements=phi)
    elif phi is None:
        return Derivation(valid_statements=None)
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Derivation(valid_statements=tuple(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        # phi: Formula = Formula(c=connectives.e, terms=phi)
        return Derivation(valid_statements=phi)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Derivation, phi_type=type(phi), phi=phi)


def coerce_derivation_builder(phi: FlexibleFormula) -> DerivationBuilder:
    """Validate that phi is a well-formed derivation-builder and returns it properly typed as
    DemonstrationBuilder, or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, DerivationBuilder):
        return phi
    elif isinstance(phi, Derivation):
        return phi.to_derivation_builder()
    elif phi is None:
        return DerivationBuilder(valid_statements=None)
    elif isinstance(phi, typing.Generator) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an derivation-builder
        whose valid-statements are the elements of the iterable."""
        return DerivationBuilder(valid_statements=tuple(theorem for theorem in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an derivation-builder
        whose valid-statements are the elements of the iterable."""
        return DerivationBuilder(valid_statements=phi)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=DerivationBuilder, phi_type=type(phi), phi=phi)


def coerce_axiomatization(phi: FlexibleFormula) -> Axiomatization:
    """Validate that phi is a well-formed axiomatization and returns it properly typed as Axiomatization,
    or raise exception e123.

    :param phi:
    :return:
    """
    if isinstance(phi, Axiomatization):
        return phi
    elif isinstance(phi, Formula) and is_well_formed_axiomatization(phi=phi):
        return Axiomatization(axioms=phi)
    else:
        raise_error(error_code=event_codes.e123, coerced_type=Axiomatization, phi_type=type(phi), phi=phi)


class TheoryState(Enumeration):
    """A theory-state is an enumeration of formulas."""

    def __new__(cls, elements: FlexibleEnumeration = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, elements=elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None):
        super().__init__(elements=elements)


class ValidStatement(Formula):
    """A valid-statement is a formula that justifies the existence of a statement in a well-formed theory.

    There are three types of valid-statements:
     - axioms,
     - inference-rules,
     - theorems.
     """

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
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

    def __new__(cls, claim: FlexibleFormula, justification: FlexibleFormula):
        claim = coerce_formula(phi=claim)
        justification = coerce_formula(phi=justification)
        c: Connective = connectives.follows_from
        o: tuple = super().__new__(cls, connective=c, terms=(claim, justification,))
        return o

    def __init__(self, claim: FlexibleFormula, justification: FlexibleFormula):
        self._claim = coerce_formula(phi=claim)
        self._justification = coerce_formula(phi=justification)
        c: Connective = connectives.follows_from
        super().__init__(connective=c, terms=(self._claim, self._justification,))

    @property
    def claim(self) -> Formula:
        """Return the formula claimed as valid by the theorem.

        This is equivalent to phi.term_0.

        :return: A formula.
        """
        return self._claim

    @property
    def justification(self) -> Formula:
        return self._justification


class Axiom(ValidStatement):
    """A well-formed axiom is a theorem that unconditionally justifies a statement.

    Syntactic definition:
    A formula is a well-formed axiom if and only if it is of the form:
        phi follows-from psi
    Where:
        - phi is a well-formed transformation, called the inference-rule,
        - psi is the axiomatic-postulation urelement,
        - follows-from is the follows-from binary connective.

    Semantic definition:
    An axiom is the statement that a formula is postulated as true in a theory.

    """

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed axiom, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_formula(phi=phi)
        if isinstance(phi, Axiom):
            # Shortcut: the class assures the well-formedness of the formula.
            return True
        elif (phi.c is not connectives.follows_from or
              not phi.arity == 2 or
              not is_well_formed_formula(phi=phi.term_0) or
              phi.term_1.c is not connectives.axiom):
            return False
        else:
            return True

    def __new__(cls, claim: FlexibleFormula = None):
        claim: Formula = coerce_formula(phi=claim)
        o: tuple = super().__new__(cls, claim=claim, justification=connectives.axiom)
        return o

    def __init__(self, claim: FlexibleFormula):
        claim: Formula = coerce_formula(phi=claim)
        super().__init__(claim=claim, justification=connectives.axiom)

    def rep(self, **kwargs) -> str:
        return f'({self.claim.rep(**kwargs)}) is an axiom.'


FlexibleAxiom = typing.Union[Axiom, Formula]


class InferenceRule(ValidStatement):
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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed axiom, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_formula(phi=phi)
        if isinstance(phi, InferenceRule):
            # Shortcut: the class assures the well-formedness of the formula.
            return True
        elif (not phi.c is connectives.follows_from or
              not phi.arity == 2 or
              not is_well_formed_transformation(phi=phi.term_0) or
              phi.term_1.c is not connectives.inference_rule):
            return False
        else:
            return True

    def __new__(cls, transformation: FlexibleTransformation = None):
        transformation: Formula = coerce_transformation(phi=transformation)
        o: tuple = super().__new__(cls, claim=transformation, justification=connectives.inference_rule)
        return o

    def __init__(self, transformation: FlexibleTransformation):
        self._transformation: Formula = coerce_transformation(phi=transformation)
        super().__init__(claim=self._transformation, justification=connectives.inference_rule)

    def rep(self, **kwargs) -> str:
        return f'Inference rule:\n\t{self.claim.rep(**kwargs)}'

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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed inference, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_formula(phi=phi)
        if phi.c is not connectives.inference or not is_well_formed_enumeration(
                phi=phi.term_0) or not is_well_formed_transformation(phi=phi.term_1):
            return False
        else:
            return True

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

    def rep(self, **kwargs) -> str:
        premises: str = '\n\t\t\t'.join(theorem.rep(**kwargs) for theorem in self.premises)
        return (f'Inference-rule:'
                f'\n\tPremises:'
                f'\n\t\t\t{premises}'
                f'\n\tTransformation-rule:'
                f'\n\t\t{self.transformation_rule.rep(**kwargs)}')

    @property
    def transformation_rule(self) -> Transformation:
        """The inference-rule of the inference."""
        return self._transformation_rule

    @property
    def premises(self) -> Tupl:
        """The premises of the inference."""
        return self._premises


FlexibleInference = typing.Optional[typing.Union[Inference]]


class Theorem(ValidStatement):
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

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if and only if phi is a well-formed theorem-by-inference, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_formula(phi=phi)
        if isinstance(phi, Theorem):
            # the type assure the well-formedness of the formula
            return True
        if (phi.c is not connectives.follows_from or
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
                raise_error(error_code=event_codes.e106, phi=phi, psi_expected=phi.term_0, psi_inferred=f_of_p,
                            inference_rule=i)
                return False
            return True

    def __new__(cls, claim: FlexibleFormula, i: FlexibleInference):
        claim: Formula = coerce_formula(phi=claim)
        i: Inference = coerce_inference(phi=i)
        o: tuple = super().__new__(cls, claim=claim, justification=i)
        return o

    def __init__(self, claim: FlexibleFormula, i: FlexibleInference):
        self._phi: Formula = coerce_formula(phi=claim)
        self._i: Inference = coerce_inference(phi=i)
        # check the validity of the theorem
        f_of_p: Formula = i.transformation_rule(i.premises)
        try:
            is_formula_equivalent(phi=claim, psi=f_of_p, raise_event_if_false=True)
        except CustomException as error:
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            # raise an exception to prevent the creation of this ill-formed theorem-by-inference.
            raise_error(error_code=event_codes.e105, error=error, theorem_claim=claim, algorithm_output=f_of_p,
                        inference=i)
        super().__init__(claim=claim, justification=i)

    @property
    def i(self) -> Inference:
        """The inference of the theorem."""
        return self._i

    @property
    def phi(self) -> Formula:
        """The proven formula."""
        return self._phi

    def rep(self, **kwargs) -> str:
        return (f'({self.claim.rep(**kwargs)})'
                f'\t| follows from premises {self.i.premises}'
                f' and inference-rule {self.i.transformation_rule}.')


FlexibleTheorem = typing.Union[Theorem, Formula]
FlexibleValidStatement = typing.Union[FlexibleAxiom, FlexibleTheorem, FlexibleInferenceRule]


class TheoryAccretor(EnumerationAccretor):
    pass


class DerivationBuilder(EnumerationBuilder):
    """A utility class to help build derivations. It is mutable and thus allows edition.

    The allowed operations on an enumeration-builder are:
     - appending axiom,
     - appending inference-rule,
     - appending theorem-from-inference.

    Note: """

    def __init__(self, valid_statements: FlexibleEnumeration):
        super().__init__(elements=None)
        if isinstance(valid_statements, typing.Iterable):
            for element in valid_statements:
                self.append(term=element)

    def append(self, term: FlexibleValidStatement) -> None:
        """
        Override the append method to assure the consistency of newly added elements.

        :param term:
        :return:
        """
        term: ValidStatement = coerce_valid_statement(phi=term)
        super().append(term=term)

    def append_axiom(self, axiom: FlexibleAxiom) -> None:
        axiom: Axiom = coerce_axiom(phi=axiom)
        self.append(term=axiom)

    def append_inference_rule(self, inference_rule: FlexibleInferenceRule) -> None:
        inference_rule: InferenceRule = coerce_inference_rule(phi=inference_rule)
        self.append(term=inference_rule)

    def append_theorem_by_inference(self, theorem: FlexibleTheorem) -> None:
        theorem: Theorem = coerce_theorem(phi=theorem)
        self.append(term=theorem)

    def rep(self, **kwargs) -> str:
        header: str = 'Derivation (elaborating):\n\t'
        valid_statements: str = '\n\t'.join(valid_statement.rep(**kwargs) for valid_statement in self)
        return f'{header}{valid_statements}'

    def to_derivation(self) -> Derivation:
        """If the derivation-builder is well-formed, return a derivation."""
        elements: tuple[Formula, ...] = tuple(coerce_valid_statement(phi=element) for element in self)
        phi: Derivation = Derivation(valid_statements=elements)
        return phi

    def to_formula(self) -> Formula:
        """If the derivation-builder is well-formed, return a derivation, which is a formula."""
        return self.to_derivation()


class Derivation(Enumeration):
    """A derivation is a justified enumeration of axioms, inference-rules, and theorems.

    Syntactic definition:
    A well-formed derivation is an enumeration such that:
     - all element phi of the enumeration is a well-formed theorem,
     - all premises of all theorem-by-inferences are predecessors of their parent theorem-by-inference.

    TODO: Consider the following data-model change: a valid-statement is only an axiom or an inference-rule. In
    effect, stating that in inference-rule is a valid-statement seems to be a bit of a semantic stretch.

    """

    @staticmethod
    def is_well_formed(phi: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
        """Return True if phi is a well-formed derivation, False otherwise.

        :param phi: A formula.
        :param raise_event_if_false:
        :return: bool.
        """
        phi = coerce_enumeration(phi=phi)

        if isinstance(phi, Derivation):
            # the Derivation class assure the well-formedness of the derivation.
            return True

        # check the well-formedness of the individual valid-statements.
        # and retrieve the terms claimed as proven in the derivation, preserving order.
        # by the definition of a derivation, these are the left term (term_0) of the formulas.
        claims: TuplBuilder = TuplBuilder(elements=None)
        valid_statements: TuplBuilder = TuplBuilder(elements=None)
        for theorem in phi:
            if not is_well_formed_valid_statement(phi=theorem):
                return False
            else:
                theorem: ValidStatement = coerce_valid_statement(phi=theorem)
                valid_statements.append(term=theorem)
                # retrieve the formula claimed as valid from the theorem
                claim: Formula = theorem.claim
                claims.append(term=claim)
        # now that the valid-statements and claims have been retrieved, and proved well-formed individually,
        # make the python objects immutable.
        valid_statements: Tupl = valid_statements.to_tupl()
        claims: Tupl = claims.to_tupl()
        for i in range(0, valid_statements.arity):
            theorem = valid_statements[i]
            claim = claims[i]
            if is_well_formed_axiom(phi=theorem):
                # This is an axiom.
                pass
            elif is_well_formed_inference_rule(phi=theorem):
                # This is an inference-rule.
                pass
            elif is_well_formed_theorem(phi=theorem):
                theorem_by_inference: Theorem = coerce_theorem(phi=theorem)
                inference: Inference = theorem_by_inference.i
                for premise in inference.premises:
                    # check that premise is a proven-formula (term_0) of a predecessor
                    if not claims.has_element(phi=premise):
                        # The premise is absent from the derivation
                        if raise_event_if_false:
                            raise_error(error_code=event_codes.e111, premise=premise, premise_index=i, theorem=theorem,
                                        claim=claim)
                        return False
                    else:
                        premise_index = claims.get_index_of_first_equivalent_element(phi=premise)
                        if premise_index >= i:
                            # The premise is not positioned before the conclusion.
                            if raise_event_if_false:
                                raise_error(error_code=event_codes.e112, premise=premise, premise_index=i,
                                            theorem=theorem,
                                            claim=claim)
                            return False
                if not claims.has_element(phi=inference.transformation_rule):
                    # The inference transformation-rule is absent from the derivation.
                    if raise_event_if_false:
                        raise_error(error_code=event_codes.e119, transformation_rule=inference.transformation_rule,
                                    inference=inference, premise_index=i, theorem=theorem,
                                    claim=claim)
                    return False
                else:
                    transformation_index = claims.get_index_of_first_equivalent_element(
                        phi=inference.transformation_rule)
                    if transformation_index >= i:
                        # The transformation is not positioned before the conclusion.
                        return False
                # And finally, confirm that the inference effectively yields phi.
                phi_prime = inference.transformation_rule.apply_transformation(arguments=inference.premises)
                if not is_formula_equivalent(phi=claim, psi=phi_prime):
                    return False
            else:
                # Incorrect form.
                return False
        # All tests were successful.
        return True

    def __new__(cls, valid_statements: FlexibleEnumeration = None):
        # coerce to enumeration
        valid_statements: Enumeration = coerce_enumeration(phi=valid_statements)
        try:
            is_well_formed_derivation(phi=valid_statements, raise_event_if_false=True)
        except Exception as error:
            # well-formedness verification failure, the theorem is ill-formed.
            raise_error(error_code=event_codes.e120, error=error, valid_statements=valid_statements)
        o: tuple = super().__new__(cls, elements=valid_statements)
        return o

    def __init__(self, valid_statements: FlexibleEnumeration = None):
        # coerce to enumeration
        valid_statements: Enumeration = coerce_enumeration(phi=valid_statements)
        # coerce all elements of the enumeration to theorem
        valid_statements: Enumeration = coerce_enumeration(
            phi=(coerce_valid_statement(phi=p) for p in valid_statements))
        super().__init__(elements=valid_statements)

    @property
    def axioms(self) -> Enumeration:
        """Return an enumeration of all axioms in the derivation, preserving order, filtering out inference-rules and
        theorems."""
        return Enumeration(elements=tuple(self.iterate_axioms()))

    @property
    def inference_rules(self) -> Enumeration:
        """Return an enumeration of all inference-rules in the derivation, preserving order, filtering out axioms and
        theorems."""
        return Enumeration(elements=tuple(self.iterate_theorems()))

    def is_valid_statement(self, phi: FlexibleFormula) -> bool:
        """Return True if phi is demonstrated as a valid-statement in this derivation, False otherwise."""
        phi = coerce_formula(phi=phi)
        for theorem in self:
            theorem: ValidStatement = coerce_valid_statement(phi=theorem)
            if is_formula_equivalent(phi=phi, psi=theorem.claim):
                return True
        return False
        # return any(is_formula_equivalent(phi=phi, psi=theorem) for theorem in self)

    def iterate_axioms(self) -> typing.Iterator[Axiom]:
        """Iterates over all axioms in the derivation, preserving order, filtering out inference-rules and theorems."""
        for element in self:
            if isinstance(element, Axiom):
                yield element

    def iterate_inference_rules(self) -> typing.Iterator[InferenceRule]:
        """Iterates over all inference-rules in the derivation, preserving order, filtering out axioms and theorems."""
        for element in self:
            if isinstance(element, Theorem):
                yield element

    def iterate_theorems(self) -> typing.Iterator[Theorem]:
        """Iterates over all theorems in the derivation, preserving order, filtering out axioms and inference-rules."""
        for element in self:
            if isinstance(element, Theorem):
                yield element

    def rep(self, **kwargs) -> str:
        header: str = 'Derivation:\n\t'
        valid_statements: str = '\n\t'.join(valid_statement.rep(**kwargs) for valid_statement in self)
        return f'{header}{valid_statements}'

    @property
    def theorems(self) -> Enumeration:
        """Return an enumeration of all theorems in the derivation, preserving order, filtering out axioms and
        inference-rules."""
        return Enumeration(elements=tuple(self.iterate_theorems()))

    def to_derivation_builder(self) -> DerivationBuilder:
        return DerivationBuilder(valid_statements=self)


FlexibleDerivation = typing.Optional[
    typing.Union[Derivation, DerivationBuilder, typing.Iterable[FlexibleValidStatement]]]
"""FlexibleDemonstration is a flexible python type that may be safely coerced into a Demonstration or a 
DemonstrationBuilder."""

FlexibleDerivationBuilder = typing.Optional[
    typing.Union[Derivation, DerivationBuilder, typing.Iterable[FlexibleValidStatement]]]


class Axiomatization(Derivation):
    """An axiomatization is a derivation that is only composed of axioms,
    and/or inference-rules.

    Syntactic definition:
    A well-formed axiomatization is an enumeration such that:
     - all element phi of the enumeration is a well-formed axiom or an inference-rule.

    """

    @staticmethod
    def is_well_formed(phi: FlexibleFormula) -> bool:
        """Return True if phi is a well-formed axiomatization, False otherwise.

        :param phi: A formula.
        :return: bool.
        """
        phi = coerce_enumeration(phi=phi)
        for i in range(0, phi.arity):
            psi = phi[i]
            if is_well_formed_inference_rule(phi=psi):
                # This is an inference-rule.
                pass
            elif is_well_formed_axiom(phi=psi):
                # This is an axiom.
                pass
            else:
                # Incorrect form.
                return False
        # All tests were successful.
        return True

    def __new__(cls, axioms: FlexibleEnumeration = None):
        # coerce to enumeration
        axioms: Enumeration = coerce_enumeration(phi=axioms)
        # coerce all elements of the enumeration to axioms or inference-rules.
        eb: EnumerationBuilder = EnumerationBuilder(elements=None)
        for valid_statement in axioms:
            if is_well_formed_inference_rule(phi=valid_statement):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(phi=valid_statement)
                eb.append(term=valid_statement)
            elif is_well_formed_axiom(phi=valid_statement):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(phi=valid_statement)
                eb.append(term=valid_statement)
            else:
                # Incorrect form.
                raise_error(error_code=event_codes.e123, phi=valid_statement, phi_type_1=InferenceRule,
                            phi_type_2=Axiom)
        valid_statements: Enumeration = eb.to_enumeration()
        o: tuple = super().__new__(cls, valid_statements=valid_statements)
        return o

    def __init__(self, axioms: FlexibleEnumeration = None):
        # coerce to enumeration
        axioms: Enumeration = coerce_enumeration(phi=axioms)
        # coerce all elements of the enumeration to axioms or inference-rules.
        eb: EnumerationBuilder = EnumerationBuilder(elements=None)
        for theorem in axioms:
            if is_well_formed_inference_rule(phi=theorem):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(phi=theorem)
                eb.append(term=theorem)
            elif is_well_formed_axiom(phi=theorem):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(phi=theorem)
                eb.append(term=theorem)
            else:
                # Incorrect form.
                raise Exception('invalid theorem')
        e: Enumeration = eb.to_enumeration()
        super().__init__(valid_statements=e)

    def rep(self, **kwargs) -> str:
        header: str = 'Axioms:\n\t'
        axioms: str = '\n\t'.join(axiom.rep(**kwargs) for axiom in self)
        return f'{header}{axioms}'


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


def translate_implication_to_axiom(phi: FlexibleFormula) -> InferenceRule:
    """Given a propositional formula phi that is an implication,
    translates phi to an equivalent axiomatic-system-1 inference-rule.

    Note: the initial need was to translate the original axioms of minimal-logic-1.

    :param phi:
    :return:
    """
    phi = coerce_formula(phi=phi)
    if phi.c is not connectives.implies:
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
        rep: str = x.rep() + '\''
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
    rule: TransformationBuilder = TransformationBuilder(premises=premises, conclusion=conclusion,
                                                        variables=variables)

    # build the inference-rule
    inference_rule: InferenceRule = InferenceRule(transformation=rule)

    return inference_rule


class AutoDerivation:
    def __init__(self, matching_template: Formula, template_variables: Enumeration):
        self._matching_template: Formula = matching_template
        self._template_variables: Enumeration = template_variables

    def match(self, missing_theorem: Formula) -> bool:
        """Return true if the structure of the

        :param phi:
        :return:
        """
        # if is_formula_equivalent_with_variables(phi=missing_theorem,psi=self.matching_template)
        pass

    @property
    def matching_template(self) -> Formula:
        return self._matching_template

    @property
    def template_variables(self) -> Enumeration:
        return self._template_variables


def derive(theory: FlexibleDerivation, claim: FlexibleFormula, premises: FlexibleTupl,
           inference_rule: FlexibleInferenceRule):
    """Given a derivation t, derives a new theory t' that extends t with a new theorem by applying an inference-rule.

    :param theory:
    :param premises:
    :param inference_rule:
    :return:
    """
    # parameters validation
    theory: Derivation = coerce_derivation(phi=theory)
    claim: Formula = coerce_formula(phi=claim)
    premises: Tupl = coerce_tupl(phi=premises)
    inference_rule: InferenceRule = coerce_inference_rule(phi=inference_rule)

    if 1 == 2:
        # TODO: Complete implementation
        for premise in premises:
            if not theory.has_element(phi=premise):
                # the premise is missing from the derivation
                # trigger auto-derivations
                for auto_derivation in theory.auto_derivations:
                    if auto_derivation.match(premise):
                        theory = auto_derivation.derive(theory=theory, premise=premise)

    # configure the inference
    inference: Inference = Inference(premises=premises, transformation_rule=inference_rule.transformation)

    # derive the new theorem
    theorem: ValidStatement = Theorem(claim=claim, i=inference)

    # extends the theory
    theory: Derivation = Derivation(valid_statements=(*theory, theorem,))

    return theory, theorem


# PRESENTATION LAYER

class ClassicalFormulaTypesetter(pl1.Typesetter):
    def __init__(self, symbol: pl1.Symbol):
        super().__init__()
        self._symbol: pl1.Symbol = symbol

    @property
    def symbol(self) -> pl1.Symbol:
        return self._symbol

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        yield from self.symbol.typeset_from_generator(**kwargs)
        yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        first = True
        for term in phi:
            if not first:
                yield from pl1.symbols.collection_separator.typeset_from_generator(**kwargs)
            else:
                first = False
            yield from term.typeset_from_generator(**kwargs)
        yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class InfixFormulaTypesetter(pl1.Typesetter):
    def __init__(self, symbol: pl1.Symbol):
        super().__init__()
        self._symbol: pl1.Symbol = symbol

    @property
    def symbol(self) -> pl1.Symbol:
        return self._symbol

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        yield from phi.term_0.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from self.symbol.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from phi.term_1.typeset_from_generator(**kwargs)


class SymbolTypesetter(pl1.Typesetter):
    def __init__(self, symbol: pl1.Symbol):
        super().__init__()
        self._symbol: pl1.Symbol = symbol

    @property
    def symbol(self) -> pl1.Symbol:
        return self._symbol

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        yield from self.symbol.typeset_from_generator(**kwargs)


class IndexedSymbolTypesetter(pl1.Typesetter):
    def __init__(self, symbol: pl1.Symbol, index: int):
        super().__init__()
        self._symbol: pl1.Symbol = symbol
        self._index: int = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def symbol(self) -> pl1.Symbol:
        return self._symbol

    def typeset_from_generator(self, phi: FlexibleFormula, encoding: typing.Optional[pl1.encodings], **kwargs) -> (
            typing.Generator)[str, None, None]:
        if encoding is None:
            encoding = pl1.encodings.default
        phi: Formula = coerce_formula(phi=phi)
        yield from self.symbol.typeset_from_generator(encoding=encoding, **kwargs)
        if encoding is pl1.encodings.latex_math:
            yield f'_{{{self.index}}}'
        elif encoding is pl1.encodings.unicode_extended:
            yield pl1.unicode_subscriptify(s=str(self.index))
        elif encoding is pl1.encodings.unicode_limited:
            yield str(self.index)
        else:
            raise ValueError('Unsupported encoding')


class Typesetters:
    """A factory of out-of-the-box encodings."""

    def __new__(cls):
        if st1.axiomatic_system_1_typesetters is None:
            st1.axiomatic_system_1_typesetters = super(Typesetters, cls).__new__(cls)
        return st1.axiomatic_system_1_typesetters

    def constant(self, symbol: pl1.Symbol) -> SymbolTypesetter:
        return SymbolTypesetter(symbol=symbol)

    def classical_formula(self, symbol: pl1.Symbol) -> ClassicalFormulaTypesetter:
        return ClassicalFormulaTypesetter(symbol=symbol)

    def text(self, text: str) -> TextTypesetter:
        return TextTypesetter(text=text)

    def indexed_symbol(self, symbol: pl1.Symbol, index: int) -> IndexedSymbolTypesetter:
        return IndexedSymbolTypesetter(symbol=symbol, index=index)

    def infix_formula(self, symbol: pl1.Symbol) -> InfixFormulaTypesetter:
        return InfixFormulaTypesetter(symbol=symbol)


typesetters = Typesetters()
