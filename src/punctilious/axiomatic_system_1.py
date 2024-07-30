from __future__ import annotations

import abc
import collections
# import logging
import typing
# import warnings
# import threading
import sys
# import random
import itertools
import re
from abc import ABC

import constants_1 as c1
import util_1 as u1
import state_1 as st1
import presentation_layer_1 as pl1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_001,
                              msg='This module does not support being directly executed as a script. '
                                  'Please use the import statement.')


class Connective:
    """A connective is a symbol used as a signal to distinguish formulas in theories.

    Equivalent definition:
    A node color in a formula tree."""

    def __init__(self, formula_ts: pl1.FlexibleTypesetter | None = None,
                 **kwargs):
        """

        :param formula_ts: A default text representation.
        """
        formula_ts: pl1.Typesetter = pl1.coerce_typesetter(ts=formula_ts)
        self._formula_typesetter: pl1.Typesetter = formula_ts
        self._ts: dict[str, pl1.Typesetter] = pl1.extract_typesetters(t=kwargs)

    def __call__(self, *args):
        """Allows pseudo formal language in python."""
        return Formula(con=self, t=args)

    def __str__(self):
        return f'{id(self)}-connective'

    def __repr__(self):
        return f'{id(self)}-connective'

    @property
    def formula_ts(self) -> pl1.Typesetter:
        return self._formula_typesetter

    @formula_ts.setter
    def formula_ts(self, formula_typesetter: pl1.Typesetter):
        self._formula_typesetter = formula_typesetter

    def to_formula(self) -> Formula:
        return Formula(con=self)

    @property
    def ts(self) -> dict[str, pl1.Typesetter]:
        """A dictionary of typesetters that may output representations of this object, or linked objects."""
        return self._ts


class Formula(tuple):
    """A python-class modeling a formula.

    Definition (sequence of formulas):
    "" is an empty sequence of formulas.
    If "phi" is a formula, then "phi" is a non-empty sequence of formulas.
    If `s` is a sequence of formulas, and "phi" is a formula, then "s, phi" is a non-empty sequence of formulas.
    Nothing else is a sequence of formulas.

    Definition (formula):
    If "c" is a connective, then "(c())" is a nullary formula.
    If "c" is a connective, and `s` is a non-empty sequence of formulas, then "(c(s))" is an n-ary formula.

    Conventions:
    Assuming unambiguous representation:
    "(c())" can be written "(c)".
    "(c(phi, psi)" can be written "phi c psi", this is called infix notation.
    "c(d)" can be written "cd", this is called prefix notation.
    "c(d)" can be written "dc", this is called postfix notation.

    Equivalent definition (formula):
    A finite tree whose nodes are colored, and where edges are fully ordered under their edge.
    """

    @staticmethod
    def _data_validation(con: Connective, t: FlexibleTupl = None) -> tuple[Connective, tuple]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param con:
        :param t:
        :return:
        """
        if isinstance(t, collections.abc.Iterable):
            t = tuple(coerce_formula(phi=term) for term in t)
        elif t is None:
            t: tuple = tuple()
        else:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_002, c=con, t=t)
        return con, t

    def __new__(cls, con: Connective, t: FlexibleTupl = None, **kwargs):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        con, t = Formula._data_validation(con=con, t=t)
        if len(t) == 0:
            return super().__new__(cls)
        elif len(t) > 0:
            return super().__new__(cls, t)

    def __init__(self, con: Connective, t: FlexibleTupl = None, **kwargs):
        con, t = Formula._data_validation(con=con, t=t)
        super().__init__()
        self._connective = con
        self._ts: dict[str, pl1.Typesetter] = pl1.extract_typesetters(t=kwargs)

    def __contains__(self, phi: FlexibleFormula):
        """Return True is there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.

        :param phi: A formula.
        :return: True if there exists a formula psi' in the current formula psi, such that phi ~formula psi'. False
          otherwise.
        """
        return is_term_of_formula(x=phi, phi=self)

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

    @property
    def term_0(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 1:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_003, c=self.connective)
        return self[0]

    @property
    def term_1(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 2:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_004, c=self.connective)
        return self[1]

    @property
    def term_2(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 3:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_005, c=self.connective)
        return self[2]

    @property
    def term_3(self) -> Formula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 4:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_005, c=self.connective)
        return self[3]

    @property
    def ts(self) -> dict[str, pl1.Typesetter]:
        """A dictionary of typesetters that may output representations of this object."""
        return self._ts

    def get_typesetter(self, typesetter: typing.Optional[pl1.FlexibleTypesetter] = None,
                       ts_key: str | None = None, **kwargs) -> pl1.Typesetter:
        """

         - priority 1: parameter typesetter is passed explicitly.
         - priority 2: a typesetting-configuration is attached to the formula, and its typesetting-method is defined.
         - priority 3: a typesetting-configuration is attached to the formula connective, and its typesetting-method is
           defined.
         - priority 4: failsafe typesetting method.

        :param ts_key:
        :param typesetter:
        :return:
        """
        # If typesetter is provided directly in argument, it is used in priority.
        if typesetter is None:
            if ts_key is not None and ts_key in self.ts:
                # If ts_key argument was provided, return the typesetter from the
                return self.ts.get(ts_key)
            is_sub_formula: bool = kwargs.get('is_sub_formula', False)
            if is_sub_formula and pl1.REF_TS in self.ts:
                # This is a sub-formula and there is a reference that can be used
                # to make long formulas more readable.
                return self.ts.get(pl1.REF_TS)
            else:
                # Otherwise return the typesetter attached to the formula's connective.
                typesetter: pl1.Typesetter = self.connective.formula_ts
        return typesetter

    def typeset_as_string(self, ts: typing.Optional[pl1.Typesetter] = None, ts_key: str | None = None, **kwargs) -> str:
        """Returns a python-string from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        ts = self.get_typesetter(typesetter=ts, ts_key=ts_key, **kwargs)
        return ts.typeset_as_string(phi=self, **kwargs)

    def typeset_from_generator(self, ts: typing.Optional[pl1.Typesetter] = None,
                               ts_key: str | None = None, **kwargs) -> \
            typing.Generator[str, None, None]:
        """Generates a stream of python-string chunks from the typesetting-method.

        If the typesetting-method returns content of reasonable length, typeset_as_string() is an adequate solution.
        If the typesetting-method returns too lengthy content, you may prefer typeset_from_generator() to avoid
        loading all the content in memory.
        """
        ts = self.get_typesetter(typesetter=ts, ts_key=ts_key, **kwargs)
        yield from ts.typeset_from_generator(phi=self, **kwargs)


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
        return Tupl(e=(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, Formula):
        # Implicit conversion of iterators to tuple formulas.
        return Tupl(e=phi)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_006,
            msg=f'Argument "phi" of python-type {str(type(phi))} could not be coerced to a formula of python-type '
                f'Formula. The string representation of "phi" is: {u1.force_str(o=phi)}.',
            phi=phi, t_python_type=type(phi))


def coerce_variable(x: FlexibleFormula) -> Formula:
    """Any nullary formula can be used as a variable.

    In a meta-theory, a variable is signaled with the is-well-formed-variable predicate.

    :param x:
    :return:
    """
    x = coerce_formula(phi=x)
    if x.arity != 0:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_007, msg='coerce_variable: x.arity != 0')
    return x


def coerce_enumeration_OBSOLETE(e: FlexibleEnumeration, strip_duplicates: bool = False,
                                interpret_none_as_empty: bool = True) -> Enumeration:
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
        return Enumeration(e=e, strip_duplicates=strip_duplicates)
    elif interpret_none_as_empty and e is None:
        return Enumeration(e=None, strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Generator) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(e=tuple(element for element in e), strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Iterable) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(e=e, strip_duplicates=strip_duplicates)
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_008, coerced_type=Enumeration, phi_type=type(e), phi=e)


def coerce_enumeration(e: FlexibleEnumeration, strip_duplicates: bool = False,
                       interpret_none_as_empty: bool = False,
                       canonic_conversion: bool = False) -> Enumeration:
    """Coerce "e" to an enumeration.
    """
    if isinstance(e, Enumeration):
        return e
    elif is_well_formed_enumeration(e=e):
        # phi is a well-formed enumeration,
        # it can be safely re-instantiated as an Enumeration and returned.
        return Enumeration(e=e)
    elif interpret_none_as_empty and e is None:
        return Enumeration(e=None)
    elif canonic_conversion and is_well_formed_formula(phi=e):
        return transform_formula_to_enumeration(phi=e, strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Generator) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(e=tuple(element for element in e), strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Iterable) and not isinstance(e, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Enumeration(e=e, strip_duplicates=strip_duplicates)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_008,
            msg='"e" cannot be coerced to an enumeration.',
            e=e,
            interpret_none_as_empty=interpret_none_as_empty,
            canonic_conversion=canonic_conversion,
            strip_duplicates=strip_duplicates)


def coerce_tuple(t: FlexibleTupl, interpret_none_as_empty: bool = False, canonic_conversion: bool = False) -> Tupl:
    if isinstance(t, Tupl):
        return t
    elif is_well_formed_tupl(t=t, interpret_none_as_empty=interpret_none_as_empty):
        return Tupl(e=t)
    elif interpret_none_as_empty and t is None:
        return Tupl(e=None)
    elif canonic_conversion and is_well_formed_formula(phi=t):
        # Every formula can be transformed to a tuple using canonical transformation.
        return transform_formula_to_tuple(phi=t)
    elif isinstance(t, typing.Generator) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Tupl(e=tuple(x for x in t))
    elif isinstance(t, typing.Iterable) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Tupl(e=t)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_065,
            msg='No solution found to coerce `t` to tupl.',
            t=t,
            interpret_none_as_empty=interpret_none_as_empty)


def coerce_enumeration_of_variables(e: FlexibleEnumeration) -> Enumeration:
    e = coerce_enumeration(e=e, interpret_none_as_empty=True)
    e2 = Enumeration()
    for element in e:
        element = coerce_variable(x=element)
        e2 = Enumeration(e=(*e2, element,))
    return e2


def union_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                      interpret_none_as_empty: bool = True, canonic_conversion: bool = True) -> Enumeration:
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
    phi: Enumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    psi: Enumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    e: Enumeration = Enumeration(e=(*phi, *psi,), strip_duplicates=strip_duplicates)
    return e


def intersection_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                             interpret_none_as_empty: bool = True, canonic_conversion: bool = True) -> Enumeration:
    """Given two enumerations phi, and psi, the intersection-enumeration operator, noted phi ∩-enumeration psi,
    returns a new enumeration omega such that:
    - all elements of the resulting enumeration are elements of phi and of psi.
    Order is preserved, that is:
    - the elements from phi keep their original relative order

    Under enumeration-equivalence, the intersection-enumeration operator is:
     - Idempotent: (phi ∩-enumeration phi) ~enumeration phi.
     - Symmetric: (phi ∩-enumeration psi) ~enumeration (psi ∩-enumeration phi).
    """
    phi: Enumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    psi: Enumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    common_elements: list = [x for x in iterate_enumeration_elements(e=phi) if is_element_of_enumeration(x=x, e=psi)]
    e: Enumeration = Enumeration(e=common_elements, strip_duplicates=strip_duplicates)
    return e


def difference_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                           interpret_none_as_empty: bool = True, canonic_conversion: bool = True) -> Enumeration:
    """Given two enumerations phi, and psi, the difference-enumeration operator, noted phi ∖-enumeration psi,
    returns a new enumeration omega such that:
    - all elements of the resulting enumeration are elements of phi but not psi.
    Order is preserved, that is:
    - the elements from phi keep their original relative order
    """
    phi: Enumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    psi: Enumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                          strip_duplicates=strip_duplicates,
                                          canonic_conversion=canonic_conversion)
    different_elements: list = [x for x in iterate_enumeration_elements(e=phi) if
                                not is_element_of_enumeration(x=x, e=psi)]
    e: Enumeration = Enumeration(e=different_elements, strip_duplicates=strip_duplicates)
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
    t2: Theory = Theory(d=(*phi, *psi,))
    return t2


def coerce_map(m: FlexibleMap, interpret_none_as_empty: bool = False) -> Map:
    if isinstance(m, Map):
        return m
    elif interpret_none_as_empty and m is None:
        # implicit conversion of None to the empty map.
        return Map(d=None, c=None)
    elif is_well_formed_map(m=m):
        # `m` is improperly python-typed, but it is a well-formed map.
        return Map(d=m[Map.DOMAIN_INDEX], c=m[Map.CODOMAIN_INDEX])
    elif isinstance(m, dict):
        # implicit conversion of python dict to Map.
        domain: Enumeration = coerce_enumeration(e=m.keys())
        codomain: Tupl = coerce_tuple(t=m.values())
        return Map(d=domain, c=codomain)
    else:
        # no coercion solution found.
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_009,
            msg='Argument `m` could not be coerced to a map.',
            coerced_type=Map, m_type=type(m), m=m)


FlexibleFormula = typing.Optional[typing.Union[Connective, Formula]]


class FreeArityConnective(Connective):
    """A free-arity connective is a connective without constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(formula_ts=formula_ts)


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective with a constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self,
                 fixed_arity_constraint: int, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        self._fixed_arity_constraint = fixed_arity_constraint
        super().__init__(formula_ts=formula_ts)

    @property
    def fixed_arity_constraint(self) -> int:
        return self._fixed_arity_constraint


class NullaryConnective(FixedArityConnective):

    def __init__(self, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(fixed_arity_constraint=0, formula_ts=formula_ts)


class SimpleObject(Formula):
    """A simple-object is a formula composed of a nullary-connective."""

    # TODO: Implement _data_validation(...) for the sake of consistency.

    def __new__(cls, c: NullaryConnective):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple
        o = super().__new__(cls, con=c, t=None)
        return o

    def __init__(self, c: NullaryConnective):
        super().__init__(con=c, t=None)


class UnaryConnective(FixedArityConnective):

    def __init__(self, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(fixed_arity_constraint=1, formula_ts=formula_ts)


class InfixPartialLeftHandFormula(pl1.Typesetter):
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and gluing all this together with the InfixPartialFormula class.
    """

    def __init__(self, con: Connective, term_0: FlexibleFormula):
        self._connective = con
        self._term_0 = term_0

    def __or__(self, term_1: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        return Formula(con=self._connective, t=(self.term_0, term_1,))

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    @property
    def connective(self) -> Connective:
        return self._connective

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield f'{self.connective}(???,{self.term_0})'

    @property
    def term_0(self) -> Connective:
        return self._term_0


class BinaryConnective(FixedArityConnective):

    def __init__(self, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(formula_ts=formula_ts, fixed_arity_constraint=2)

    def __ror__(self, other: FlexibleFormula):
        """Pseudo math notation. x | p | ?."""
        return InfixPartialLeftHandFormula(con=self, term_0=other)


def is_term_of_formula(x: FlexibleFormula, phi: FlexibleFormula) -> bool:
    """Returns True if x is a term of formula phi, False otherwise.

    Definition (term of a formula):
    Cf. definition of formula.
    If "(c(phi))" is a formula where c is a connective, and phi a formula, then "phi" is a term of "(c(phi))".
    If "(c(s, phi))" is a formula where c is a connective, s is a non-empty sequence of formulas, and phi a formula,
    then "phi" is a term of "(c(phi))".
    Nothing else is a term of a formula.

    :param x: A formula.
    :type x: FlexibleFormula
    :param phi: A formula.
    :type phi: FlexibleFormula
    ...
    :return: True if phi is a term of psi, False otherwise.
    :rtype: bool
    """
    x: Formula = coerce_formula(phi=x)
    phi: Formula = coerce_formula(phi=phi)
    return any(is_formula_equivalent(phi=x, psi=psi_term) for psi_term in iterate_formula_terms(phi=phi))


def is_element_of_enumeration(x: FlexibleFormula, e: FlexibleEnumeration) -> bool:
    """Returns True if x is an element of enumeration e, False otherwise.

    Definition:
    A formula x is an element of an enumeration e if and only if there exists a formula y that is a term of formula e,
    such that x ~ y.
    Nothing else is an element of e.

    When this condition is satisfied, we say that formula x is an element of enumeration e.

    :param x: A formula.
    :type x: FlexibleFormula
    :param e: An enumeration.
    :type e: FlexibleEnumeration
    ...
    :return: True if element is a term of psi, False otherwise.
    :rtype: bool
    """
    x: Formula = coerce_formula(phi=x)
    e: Enumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    return is_term_of_formula(x=x, phi=e)


def is_axiom_of(a: FlexibleAxiom, t: FlexibleTheory, max_derivations: int | None = None) -> bool:
    """Returns `True` if `a` is an axiom in axiomatization or theory `t`, `False` otherwise.

    :param a: An axiom.
    :param t: An axiomatization or a theory.
    :param max_derivations: If `None`, considers all derivations in `t`. If an integer, considers only that number
        of derivations in `t` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: `True` if `a` is an axiom `t`, `False` otherwise.
    """
    a: Axiom = coerce_axiom(a=a)
    t: Theory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    return any(
        is_formula_equivalent(phi=a, psi=a2) for a2 in iterate_theory_axioms(t=t, max_derivations=max_derivations))


def is_inference_rule_of(i: FlexibleInferenceRule, t: FlexibleTheory, max_derivations: int | None = None):
    """Returns `True` if `i` is an inference-rule in axiomatization or theory `t`, `False` otherwise.

    :param i: An inference-rule.
    :param t: An axiomatization or a theory.
    :param max_derivations: If `None`, considers all derivations in `t`. If an integer, considers only that number
        of derivations in `t` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: `True` if `a` is an inference-rule `t`, `False` otherwise.
    """
    i: InferenceRule = coerce_inference_rule(i=i)
    t: Theory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    return any(is_formula_equivalent(phi=i, psi=ir2) for ir2 in
               iterate_theory_inference_rules(t=t, max_derivations=max_derivations))


def is_theorem_of(m: FlexibleTheorem, t: FlexibleTheory, max_derivations: int | None = None):
    """Returns `True` if `m` is a theorem in theory `t`, `False` otherwise.

    :param m: A theorem.
    :param t: A theory.
    :param max_derivations: If `None`, considers all derivations in `t`. If an integer, considers only that number
        of derivations in `t` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: `True` if `m` is a theorem in `t`, `False` otherwise.
    """
    m: Theorem = coerce_theorem(t=m)
    t: Theory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    return any(is_formula_equivalent(phi=m, psi=thrm2) for thrm2 in
               iterate_theory_theorems(t=t, max_derivations=max_derivations))


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
    raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_011,
                              msg=f'Trying to get the index of the term "{term}" in the formula "{formula}", '
                                  f'but this term is not a term of the formula.')


def get_index_of_first_equivalent_element_in_enumeration(x: FlexibleFormula,
                                                         e: FlexibleEnumeration) -> int:
    """Given a formula `x` and an enumeration `e`, returns the o-based index of the first occurrence
    of an element `y` in `e` such that `x` formula-equivalent `y`.

    :param x:
    :param e:
    :return:
    """
    """Return the index of phi if phi is formula-equivalent with an element of the enumeration, None otherwise.

    Note: not to be confused with get_first_element_index on formulas and tuples.

    This method is not available on formulas because duplicate elements are possible on formulas,
    but are not possible on enumerations. The two methods are algorithmically equivalent but their
    intent is distinct."""
    x: Formula = coerce_formula(phi=x)
    e: Enumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    return get_index_of_first_equivalent_term_in_formula(term=x, formula=e)


def get_index_of_first_equivalent_element_in_tuple(x: FlexibleFormula, t: FlexibleTupl) -> int:
    """If formula "x" is a term of tuple `t`, return the o-based index of the first occurrence of the term "x"
    in `t`.

    :param x: A formula.
    :param t: A tuple.
    :return: The 0-based index of "x" in `t`.
    """
    x: Formula = coerce_formula(phi=x)
    t: Tupl = coerce_tuple(t=t, interpret_none_as_empty=True)
    return get_index_of_first_equivalent_term_in_formula(term=x, formula=t)


class TernaryConnective(FixedArityConnective):

    def __init__(self,
                 formula_ts: typing.Optional[pl1.Typesetter] = None):
        super().__init__(fixed_arity_constraint=3, formula_ts=formula_ts)


class QuaternaryConnective(FixedArityConnective):

    def __init__(self,
                 formula_ts: typing.Optional[pl1.Typesetter] = None):
        super().__init__(fixed_arity_constraint=4, formula_ts=formula_ts)


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

    def __new__(cls, c: NullaryConnective):
        o: tuple
        o = super().__new__(cls, c=c)
        return o

    def __init__(self, c: NullaryConnective):
        super().__init__(c=c)

    def __enter__(self) -> Variable:
        return self

    def __exit__(self, exc_type: typing.Optional[type], exc: typing.Optional[BaseException],
                 exc_tb: typing.Any) -> None:
        return


class MetaVariable(SimpleObject):
    """A variable is defined as a simple-object that is not declared in the theory with a "is-a" operator.

    The justification for a dedicated python class is the implementation of the __enter__ and __exit__ methods,
    which allow the usage of variables with the python with statement."""

    def __new__(cls, c: NullaryConnective):
        o: tuple
        o = super().__new__(cls, c=c)
        return o

    def __init__(self, c: NullaryConnective):
        super().__init__(c=c)

    def __enter__(self) -> MetaVariable:
        return self

    def __exit__(self, exc_type: typing.Optional[type], exc: typing.Optional[BaseException],
                 exc_tb: typing.Any) -> None:
        return


def let_x_be_a_variable(formula_ts: pl1.FlexibleTypesetter) -> (
        typing.Union)[Variable, typing.Generator[Variable, typing.Any, None]]:
    if formula_ts is None or isinstance(formula_ts, pl1.FlexibleTypesetter):
        return Variable(c=NullaryConnective(formula_ts=formula_ts))
    elif isinstance(formula_ts, typing.Iterable):
        return (Variable(c=NullaryConnective(formula_ts=ts)) for ts in formula_ts)
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_012, msg='Non supported arguments.',
                                  formula_typesetter=formula_ts)


def let_x_be_a_meta_variable(
        formula_ts: pl1.FlexibleTypesetter | typing.Iterable[pl1.FlexibleTypesetter, ...]) -> (
        MetaVariable | tuple[MetaVariable, ...]):
    """A meta-variable is a nullary-connective formula (*) that is not declared in the theory with a "is-a" operator."""
    if formula_ts is None or isinstance(formula_ts, pl1.FlexibleTypesetter):
        return MetaVariable(c=NullaryConnective(formula_ts=formula_ts))
    elif isinstance(formula_ts, typing.Iterable):
        return tuple(MetaVariable(c=NullaryConnective(formula_ts=ts)) for ts in formula_ts)
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_013, msg='Non supported arguments.',
                                  formula_typesetter=formula_ts)


FlexibleRepresentation = typing.Union[str, pl1.Symbol, pl1.Typesetter]
"""FlexibleRepresentation is a flexible python type that may be safely coerced to a symbolic representation."""

FlexibleMultiRepresentation = typing.Union[FlexibleRepresentation, typing.Iterable[FlexibleRepresentation]]
"""FlexibleMultiRepresentation is a flexible python type that may be safely coerced to a single or multiple symbolic 
representation."""


def let_x_be_a_simple_object(formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None) -> SimpleObject:
    """A helper function to declare one or multiple simple-objects.

    :param formula_ts: A string (or an iterable of strings) default representation for the simple-object(s).
    :return: A simple-object (if rep is a string), or a python-tuple of simple-objects (if rep is an iterable).
    """
    return SimpleObject(c=NullaryConnective(formula_ts=formula_ts))


def let_x_be_some_simple_objects(
        reps: tuple[pl1.FlexibleTypesetter, ...]) -> typing.Generator[SimpleObject, typing.Any, None]:
    """A helper function to declare one or multiple simple-objects.

    :param reps: A string (or an iterable of strings) default representation for the simple-object(s).
    :return: A simple-object (if rep is a string), or a python-tuple of simple-objects (if rep is an iterable).
    """
    return (let_x_be_a_simple_object(formula_ts=rep) for rep in reps)


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
    return Enumeration(e=phi)


def let_x_be_a_binary_connective(
        formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
    return BinaryConnective(formula_ts=formula_ts)


def let_x_be_a_ternary_connective(
        formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
    return TernaryConnective(formula_ts=formula_ts)


def let_x_be_a_quaternary_connective(
        formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
    return QuaternaryConnective(formula_ts=formula_ts)


def let_x_be_a_unary_connective(
        formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
    return UnaryConnective(formula_ts=formula_ts)


def let_x_be_a_free_arity_connective(
        formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
    return FreeArityConnective(formula_ts=formula_ts)


def let_x_be_an_inference_rule(t: FlexibleTheory,
                               i: FlexibleInferenceRule | None = None,
                               f: FlexibleTransformation | None = None,
                               c: FlexibleFormula | None = None,
                               v: FlexibleEnumeration | None = None,
                               d: FlexibleEnumeration | None = None,
                               p: FlexibleTupl | None = None,
                               a: typing.Optional[typing.Callable] | None = None,
                               i2: typing.Optional[typing.Callable] | None = None
                               ) -> tuple[Theory, InferenceRule]:
    """

    :param t: A theory.
    :param i: An inference-rule.
    :param f: A transformation.
    :param c: A formula denoted as the conclusion.
    :param v: An enumeration of variables used in premises.
    :param d: An enumeration of variables used for new object declarations.
    :param p: A tuple of formulas denoted as premises.
    :param a: (conditional) An external algorithm.
    :param i2: (conditional) An external algorithm.
    :return: A python-tuple (t,i) where t is a theory, and i and inference-rule.
    """
    t: FlexibleTheory = coerce_theory(t=t)
    # Signature #1: provide the inference-rule
    if i is not None:
        i: InferenceRule = coerce_inference_rule(i=i)
    # Signature #2: provide the transformation upon which the inference-rule can be built
    elif f is not None:
        f: Transformation = coerce_transformation(f=f)
        i: InferenceRule = InferenceRule(f=f)
    # Signature #3: provide the arguments upon which the transformation can be built upon which ...
    elif c is not None:
        c: Formula = coerce_formula(phi=c)
        v: Enumeration = coerce_enumeration(e=v, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        d: Enumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        p: Tupl = coerce_tuple(t=p, interpret_none_as_empty=True, canonic_conversion=True)
        if a is None:
            # Signature 3: This is a transformation-by-variable-transformation:
            f: TransformationByVariableSubstitution = TransformationByVariableSubstitution(o=c, v=v, d=d, i=p)
            i: InferenceRule = InferenceRule(f=f)
        else:
            # Signature 4: This is an algorithmic transformation:
            f: TransformationByExternalAlgorithm = TransformationByExternalAlgorithm(algo=a, check=i2, o=c, v=v,
                                                                                     d=d, i=p)
            i: InferenceRule = InferenceRule(f=f)
    else:
        raise u1.ApplicativeError(msg='inconsistent arguments')

    t: Theory = append_to_theory(i, t=t)
    # u1.log_info(i.typeset_as_string(theory=t))
    return t, i


def let_x_be_an_axiom(t: FlexibleTheory, s: typing.Optional[FlexibleFormula] = None,
                      a: typing.Optional[FlexibleAxiom] = None, **kwargs):
    """

    :param t: An axiomatization or a theory. If None, the empty axiom-collection is implicitly used.
    :param s: The statement claimed by the new axiom. Either the claim or axiom parameter
    must be provided, and not both.
    :param a: An existing axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :return: a pair (t, a) where t is an extension of the input theory, with a new axiom claiming the
    input statement, and `a` is the new axiom.
    """
    if t is None:
        t = Axiomatization(d=None)
    else:
        t: FlexibleTheory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    if s is not None and a is not None:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_016,
            msg='Both `s` and `a` are not None. It is mandatory to provide only one of these two arguments.')
    elif s is None and a is None:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_017,
            msg='Both `s` and `a` are None. It is mandatory to provide one of these two arguments.')
    elif s is not None:
        a: Axiom = Axiom(s=s, **kwargs)

    if isinstance(t, Axiomatization):
        t = Axiomatization(a=t, d=(a,))
        # TODO: Implement similar constructor than Theory A(a,d,...)
        u1.log_info(a.typeset_as_string(theory=t))
        return t, a
    elif isinstance(t, Theory):
        t = Theory(d=(*t, a,))
        # TODO: Implement similar constructor than Theory A(a,d,...)
        u1.log_info(a.typeset_as_string(theory=t))
        return t, a
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_018, msg='oops 3')


def let_x_be_a_theory(
        t: FlexibleTheory | None = None,
        d: FlexibleEnumeration | None = None,
        **kwargs) -> Theory:
    """Declares a new theory `t`.

    :param t:
    :param d: an enumeration of derivations to initialize T. If None, the empty theory is implicitly assumed.
    :return: A python-tuple (m, t).
    """
    # if 'formula_name_ts' not in kwargs:
    #    kwargs['formula_name_ts'] = pl1.Script(text='T')
    t: Theory = Theory(t=t, d=d, **kwargs)

    return t


def let_x_be_a_meta_theory(m: FlexibleTheory | None = None,
                           d: FlexibleEnumeration | None = None,
                           **kwargs) -> Theory:
    """Declares a new meta-theory `m`.

    T is declared as a sub-theory of M. To formalize this relation, the following axiom is added to M:
        (T is-a theory)
    Note that M does not self-references itself (i.e. we don't use the formula (T is-a sub-theory of M)),
    this reference is implicit in (T is-a theory) because it is a derivation in M.

    :param m: a meta-theory M such that T is a sub-theory of M.
    :param d: an enumeration of derivations to initialize T. If None, the empty theory is implicitly assumed.
    :return: A python-tuple (m, t).
    """
    # if 'formula_name_ts' not in kwargs:
    #    kwargs['formula_name_ts'] = pl1.Script(text='T')
    m: Theory = Theory(t=m, d=d, **kwargs)

    # TODO: Load automatically mt1

    return m


def let_x_be_a_sub_theory_of_y(m: FlexibleTheory, t: FlexibleTheory) -> tuple[Theory, Theory]:
    """

    :param t:
    :param m:
    :return:
    """
    m = coerce_theory(t=t)
    t = coerce_theory(t=t)
    # Move this to mt1 and redevelop it to use derivation from mt1 inference-rule.
    m, a = let_x_be_an_axiom(t=m, s=is_well_formed_theory_connective(t))
    return m, t


def let_x_be_a_collection_of_axioms(axioms: FlexibleEnumeration):
    return Axiomatization(d=axioms)


def let_x_be_a_transformation_by_variable_substitution(c: FlexibleFormula,
                                                       v: FlexibleEnumeration | None = None,
                                                       d: FlexibleEnumeration | None = None,
                                                       p: FlexibleTupl | None = None
                                                       ):
    return TransformationByVariableSubstitution(o=c, v=v, d=d,
                                                i=p)


def let_x_be_a_transformation_by_external_algorithm(
        a: typing.Callable,
        c: FlexibleFormula,
        i: typing.Callable = None,
        v: FlexibleEnumeration | None = None,
        d: FlexibleEnumeration | None = None,
        p: FlexibleTupl | None = None
):
    return TransformationByExternalAlgorithm(algo=a, check=i, o=c, v=v, d=d,
                                             i=p)


# Declare fundamental connectives.
axiom_connective = let_x_be_a_unary_connective(formula_ts='axiom')
axiomatization_connective = let_x_be_a_free_arity_connective(formula_ts='axiomatization')
enumeration_connective = let_x_be_a_free_arity_connective(formula_ts='enumeration')
implies_connective = let_x_be_a_binary_connective(formula_ts='implies')
inference_connective = let_x_be_a_ternary_connective(formula_ts='inference')
inference_rule_connective = let_x_be_a_unary_connective(formula_ts='inference-rule')
is_well_formed_formula_connective = let_x_be_a_unary_connective(formula_ts='is-well-formed-formula')
is_well_formed_inference_rule_connective = let_x_be_a_unary_connective(formula_ts='is-well-formed-inference-rule')
is_well_formed_theory_connective = let_x_be_a_unary_connective(formula_ts='is-well-formed-theory')
logical_conjunction_connective = let_x_be_a_binary_connective(formula_ts='∧')
logical_negation_connective = let_x_be_a_unary_connective(formula_ts='¬')
logical_disjunction_connective = let_x_be_a_binary_connective(formula_ts='∨')

algorithm_connective = NullaryConnective(formula_ts='algorithm')
derivation_connective = let_x_be_a_binary_connective(formula_ts='derivation')
hypothesis_connective = let_x_be_a_free_arity_connective(formula_ts='hypothesis')
is_a_connective = let_x_be_a_binary_connective(formula_ts='is-a')
is_a_proposition_connective = UnaryConnective(formula_ts='is-a-proposition')
is_a_propositional_variable_connective = UnaryConnective(formula_ts='is-a-propositional-variable')
is_a_valid_proposition_in_connective = BinaryConnective(formula_ts='is-a-valid-proposition-in')
# DUPLICATE WITH PROVES...
is_inconsistent_connective = UnaryConnective(formula_ts='is-inconsistent')
map_connective = let_x_be_a_binary_connective(formula_ts='map')
theorem_connective = let_x_be_a_free_arity_connective(formula_ts='theorem')
theory_connective = let_x_be_a_free_arity_connective(formula_ts='theory-formula')
proves_connective = let_x_be_a_binary_connective(formula_ts='⊢')
tupl_connective = let_x_be_a_free_arity_connective(formula_ts='tuple')
transformation_by_variable_substitution_connective = let_x_be_a_quaternary_connective(
    formula_ts='transformation-by-variable-substitution')


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


def is_formula_equivalent(phi: FlexibleFormula, psi: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
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
    :param raise_error_if_false:
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
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_019,
                msg='`phi` is not formula-equivalent to `psi`.',
                phi=phi,
                psi=psi,
                raise_error_if_false=raise_error_if_false)
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


def is_formula_equivalent_with_variables_2(
        phi: FlexibleFormula, psi: FlexibleFormula, variables: FlexibleEnumeration,
        variables_fixed_values: FlexibleMap = None, raise_event_if_false: bool = False) -> (
        typing.Tuple)[bool, typing.Optional[Map]]:
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
    :param variables_fixed_values: (conditional) a mapping between variables and their assigned values. used
    internally for recursive calls. leave it to None.
    :param raise_event_if_false:
    :return:
    """
    variables_fixed_values: Map = coerce_map(m=variables_fixed_values, interpret_none_as_empty=True)
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    variables: Enumeration = coerce_enumeration(e=variables, interpret_none_as_empty=True)
    # check that all variables are atomic formulas
    for x in variables:
        x: Formula = coerce_formula(phi=x)
        if x.arity != 0:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_020,
                                      msg=f'the arity of variable "{x}" in variables is not equal to 0.')
        if is_recursively_included_in(f=phi, s=x):
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_021,
                msg=f'variable x is a sub-formula of phi.',
                x=x,
                phi=phi)
    # check that all variables in the map are atomic formulas and are correctly listed in variables
    for x in variables_fixed_values.domain:
        x: Formula = coerce_formula(phi=x)
        if x.arity != 0:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_022,
                                      msg=f'the arity of variable {x} in variables_fixed_values is not equal to 0.')
        if not is_element_of_enumeration(x=x, e=variables):
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_023,
                                      msg=f'variable {x} is present in the domain of the map '
                                          f'variables_fixed_values, '
                                          f'but it is not an element of the enumeration variables.')
    if is_element_of_enumeration(x=psi, e=variables):
        # psi is a variable
        if is_in_map_domain(phi=psi, m=variables_fixed_values):
            # psi is in the domain of the map of fixed values
            psi_value: Formula = get_image_from_map(m=variables_fixed_values, preimage=psi)
            if is_formula_equivalent(phi=phi, psi=psi_value):
                return True, variables_fixed_values
            else:
                if raise_event_if_false:
                    raise u1.ApplicativeError(
                        code=c1.ERROR_CODE_AS1_024,
                        msg=f'formula "{phi}" is not formula-equivalent to '
                            f'the assigned value "{psi_value}" of variable "{psi}".')
                return False, variables_fixed_values
        else:
            # psi is not defined in the domain of the map of fixed values
            psi_value: Formula = phi
            # extend the map of fixed values
            variables_fixed_values: Map = Map(d=(*variables_fixed_values.domain, psi,),
                                              c=(*variables_fixed_values.codomain, psi_value,))
            return True, variables_fixed_values
    else:
        # psi is not a variable
        if phi.connective is not psi.connective or phi.arity != psi.arity:
            if raise_event_if_false:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_025,
                                          msg=f'the connective or arity of "{phi}" are not equal '
                                              f'to the connective or arity of "{psi}".')
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
                        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_026,
                                                  msg=f'term "{phi_term}" "{phi}" is not formula-equivalent '
                                                      f'to the term {psi_term} of "{psi}".')
                    return False, variables_fixed_values
            # all term pairs have been checked
            return True, variables_fixed_values


def is_any_formula_equivalent_with_variables(e: FlexibleEnumeration, psi: FlexibleFormula, v: FlexibleEnumeration
                                             ) -> bool:
    """Returns True if any of the formulas in enumeration "e" is formula-compatible-with-variables with
    formula "psi" with regards to variables "v".

    This is a shortcut function to test a series of potential equivalences. It should be useful
    to develop is_compatible methods for algorithmic transformations and further develop meta-theory.

    :param e:
    :param psi:
    :param v:
    :return:
    """
    e = coerce_enumeration(e=e, strip_duplicates=True, interpret_none_as_empty=True, canonic_conversion=True)
    psi = coerce_formula(phi=psi)
    v = coerce_enumeration(e=v, strip_duplicates=True, interpret_none_as_empty=True, canonic_conversion=True)
    for phi in iterate_enumeration_elements(e=e):
        yes, _ = is_formula_equivalent_with_variables_2(phi=phi, psi=psi, variables=v,
                                                        raise_event_if_false=False)
        if yes:
            return True
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


def is_sub_enumeration(s: FlexibleEnumeration, e: FlexibleEnumeration,
                       strip_duplicates: bool = True,
                       interpret_none_as_empty: bool = True,
                       canonic_conversion: bool = True) -> bool:
    """Returns `True` if enumeration `s` is a sub-enumeration of enumeration `e`, `False` otherwise.

    Notation:
    :math:`s \\subseteq e`

    Definition:
    An enumeration `s` is a sub-enumeration of an enumeration `e` if and only if:
     - every element of `s` is an element of `e`.

    Some immediate consequences:
    :math:`s ~_{f} f \\implies  s \\subseteq e`.
    :math:`∅ \\subseteq e`.
    :math:`∅ \\subseteq ∅`.

    :param s: An enumeration that is possibly a sub-enumeration of `e`.
    :param e: An enumeration.
    :param canonic_conversion:
    :param strip_duplicates:
    :param interpret_none_as_empty:
    :return:
    """
    s = coerce_enumeration(e=s, strip_duplicates=strip_duplicates, interpret_none_as_empty=interpret_none_as_empty,
                           canonic_conversion=canonic_conversion)
    e = coerce_enumeration(e=e)
    if all(is_element_of_enumeration(x=x, e=e) for x in iterate_enumeration_elements(e=s)):
        return True
    else:
        return False


def is_enumeration_equivalent(phi: FlexibleEnumeration, psi: FlexibleEnumeration) -> bool:
    """Two enumerations phi and psi are enumeration-equivalent, denoted phi ~enumeration psi, if and only if:
     - for all sub-formula phi' in phi, there exists a sub-formula psi' in psi such that phi' ~formula psi'.
     - for all sub-formula psi' in psi, there exists a sub-formula phi' in phi such that psi' ~formula phi'.

    :param phi: An enumeration.
    :param psi: An enumeration.
    :return: True if phi ~enumeration psi, False otherwise.
    """
    phi: Formula = coerce_enumeration(e=phi, interpret_none_as_empty=True)
    psi: Formula = coerce_enumeration(e=psi, interpret_none_as_empty=True)

    test_1 = all(any(is_formula_equivalent(phi=phi_prime, psi=psi_prime) for psi_prime in psi) for phi_prime in phi)
    test_2 = all(any(is_formula_equivalent(phi=psi_prime, psi=phi_prime) for phi_prime in phi) for psi_prime in psi)

    return test_1 and test_2


def replace_formulas(phi: FlexibleFormula, m: FlexibleMap) -> Formula:
    """Performs a top-down, left-to-right replacement of formulas in formula phi."""
    phi: Formula = coerce_formula(phi=phi)
    m: Map = coerce_map(m=m, interpret_none_as_empty=True)
    if is_in_map_domain(phi=phi, m=m):
        # phi must be replaced at its root.
        # the replacement algorithm stops right there (i.e.: no more recursion).
        assigned_value: Formula = get_image_from_map(m=m, preimage=phi)
        return assigned_value
    else:
        # build the replaced formula.
        fb: Formula = Formula(con=phi.connective)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = replace_formulas(phi=term, m=m)
            fb: Formula = append_term_to_formula(f=fb, t=term_substitute)
        return fb


def replace_connectives(phi: FlexibleFormula, m: FlexibleMap) -> Formula:
    """Given a formula phi, return a new formula psi structurally equivalent to phi,
    where all connectives are substituted according to the map m.

    :param phi:
    :param m: A map of connectives, where connectives are represented as atomic formulas (c).
    :return:
    """
    phi: Formula = coerce_formula(phi=phi)
    m: Map = coerce_map(m=m, interpret_none_as_empty=True)
    # TODO: Check that the map domain and codomain are composed of simple objects.
    con: Connective = phi.connective
    c_formula: Formula = Formula(con=con)
    if is_in_map_domain(phi=c_formula, m=m):
        preimage: Formula = Formula(con=con)
        image: Formula = get_image_from_map(m=m, preimage=preimage)
        con: Connective = image.connective
    # Build the new formula psi with the new connective,
    # and by calling replace_connectives recursively on all terms.
    psi: Formula = Formula(con=con, t=(replace_connectives(phi=term, m=m) for term in phi))
    return psi


class Tupl(Formula):
    """A tuple is a synonym for formula.

    The rationale for a dedicated class is semantic. When considering tuples, we do not take into account the
    root connective. Also, formula terms are called elements. Finally, notation is distinct: a formula is
    typically denoted as f(t0, t1, ..., tn) while a tuple is denoted as (t0, t1, ..., tn).

     The empty-tuple is the tuple ().

     Python implementation: in python, the word 'tuple' is reserved. For this reason, the word 'tupl' is used instead
     to implement this object."""

    # TODO: Implement _data_validation(...) for the sake of consistency.

    def __new__(cls, e: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, con=tupl_connective, t=e)
        return o

    def __init__(self, e: FlexibleTupl = None):
        """Creates a new tupl instance.

        :param e: The elements of the tupl.
        """
        super().__init__(con=tupl_connective, t=e)

    def get_index_of_first_equivalent_element(self, phi: Formula) -> typing.Optional[int]:
        """Returns the o-based index of the first occurrence of a formula psi in the tuple such that psi ~formula phi.

        :param phi: A formula.
        :return:
        """
        return self.get_index_of_first_equivalent_term(phi=phi)

    def has_element(self, phi: Formula) -> bool:
        """Return True if the tuple has phi as one of its elements."""
        return is_term_of_formula(x=phi, phi=self)


FlexibleTupl = typing.Optional[typing.Union[Tupl, typing.Iterable[FlexibleFormula], tuple, None]]
"""FlexibleTupl is a flexible python type that may be safely coerced into a Tupl."""


def reduce_map(m: FlexibleFormula, preimage: FlexibleFormula) -> Map:
    """Return a new map such that the preimage is no longer an element of its domain."""
    m: Map = coerce_map(m=m, interpret_none_as_empty=True)
    preimage: Formula = coerce_formula(phi=preimage)
    if is_element_of_enumeration(x=preimage, e=m.domain):
        index: int = get_index_of_first_equivalent_term_in_formula(term=preimage, formula=m.domain)
        reduced_domain: tuple[Formula, ...] = (*m.domain[0:index], *m.domain[index + 1:])
        reduced_codomain: tuple[Formula, ...] = (*m.codomain[0:index], *m.codomain[index + 1:])
        reduced_map: Map = Map(d=reduced_domain, c=reduced_codomain)
        return reduced_map
    else:
        return m


def append_element_to_enumeration(e: FlexibleEnumeration, x: FlexibleFormula) -> Enumeration:
    """Return a new enumeration e′ such that:
     - all elements of e are elements of e′,
     - x is an element of e′.

    Note: if "x" is an element of "e", then: e ~ e′.

    Definition (extend an enumeration "e" with an element "x"):
    Cf. the definition of enumeration.
    If "x" is an element of "e", return "e".
    If "x" is not an element of "e", and `s` is the sequence of terms in "e", return "(s, e)".
    """
    e: Enumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    x: Formula = coerce_formula(phi=x)
    if is_element_of_enumeration(x=x, e=e):
        # "x" is an element of "e":
        return e
    else:
        # "x" is not an element of "e":
        extended_enumeration: Enumeration = Enumeration(e=(*e, x,))
        return extended_enumeration


def append_element_to_tuple(t: FlexibleTupl, x: FlexibleFormula) -> Tupl:
    """Return a new extended punctilious-tuple such that element is a new element appended to its existing elements.
    """
    t: Tupl = coerce_tuple(t=t, interpret_none_as_empty=True)
    x: Formula = coerce_formula(phi=x)
    extended_tupl: Tupl = Tupl(e=(*t, x,))
    return extended_tupl


def append_tuple_to_tuple(t1: FlexibleTupl, t2: FlexibleTupl) -> Tupl:
    """Return a new tuple which appends all the elements of `t2` to `t1`.
    """
    t1: Tupl = coerce_tuple(t=t1, interpret_none_as_empty=True, canonic_conversion=True)
    t2: Tupl = coerce_tuple(t=t2, interpret_none_as_empty=True, canonic_conversion=True)
    t3: Tupl = Tupl(e=(*t1, *t2,))
    return t3


def append_term_to_formula(f: FlexibleFormula, t: FlexibleFormula) -> Formula:
    """Return a new extended formula such that term is a new term appended to its existing terms.
    """
    f: Formula = coerce_formula(phi=f)
    t: Formula = coerce_formula(phi=t)
    extended_formula: Formula = Formula(t=(*f, t,), con=f.connective)
    return extended_formula


def append_pair_to_map(m: FlexibleMap, preimage: FlexibleFormula, image: FlexibleFormula) -> Map:
    """Return a new map m2 with a new (preimage, image) pair.
    If the preimage is already defined in m, replace it.

    :param m:
    :param preimage:
    :param image:
    :return:
    """
    m: Map = coerce_map(m=m, interpret_none_as_empty=True)
    preimage: Formula = coerce_formula(phi=preimage)
    # Reduce the map to assure the preimage is no longer an element of its domain.
    m: Map = reduce_map(m=m, preimage=preimage)
    extended_domain: tuple[Formula, ...] = (*m.domain, preimage)
    extended_codomain: tuple[Formula, ...] = (*m.codomain, image)
    m: Map = Map(d=extended_domain, c=extended_codomain)
    return m


def get_image_from_map(m: FlexibleMap, preimage: FlexibleFormula) -> Formula:
    """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
    if is_in_map_domain(phi=preimage, m=m):
        index_position: int = get_index_of_first_equivalent_element_in_enumeration(x=preimage, e=m.domain)
        return m.codomain[index_position]
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_028, msg='Map domain does not contain this element')


class Map(Formula):
    """A map is a formula m(t0(k0, k1, ..., kn), t1(l0, l1, ..., ln)) where:
     - m is a node with the map connective.
     - t0 is an enumeration named the keys' enumeration.
     - t1 is a tuple named the values tuple.
     - the cardinality of t0 is equal to the cardinality of 1.

     The empty-map is the map m(t0(), t1()).

     See also:
      - :py:function:`pu.as1.coerce_map`
      - :py:function:`pu.as1.get_image_from_map`
      - :py:function:`pu.as1.is_in_map_domain`
      - :py:function:`pu.as1.is_well_formed_map`

    """
    DOMAIN_INDEX: int = 0
    CODOMAIN_INDEX: int = 1

    @staticmethod
    def _data_validation_2(d: FlexibleEnumeration = None, c: FlexibleTupl = None) -> tuple[Enumeration, Tupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param d:
        :param c:
        :return:
        """
        d: Enumeration = coerce_enumeration(
            e=d, strip_duplicates=True, interpret_none_as_empty=True, canonic_conversion=True)
        c: Tupl = coerce_tuple(t=c, interpret_none_as_empty=True, canonic_conversion=True)
        if len(d) != len(c):
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_027, msg='Map: |keys| != |values|')
        return d, c

    def __new__(cls, d: FlexibleEnumeration = None, c: FlexibleTupl = None):
        """Creates a well-formed-map of python-type Map.

        :param d: An enumeration denoted as the domain of the map.
        :param c: An enumeration denoted as the codomain of the map.
        """
        d, c = Map._data_validation_2(d=d, c=c)
        o: tuple = super().__new__(cls, con=map_connective, t=(d, c,))
        return o

    def __init__(self, d: FlexibleEnumeration = None, c: FlexibleTupl = None):
        """Creates a well-formed-map of python-type Map.

        :param d: An enumeration denoted as the domain of the map.
        :param c: An enumeration denoted as the codomain of the map.
        """
        d, c = Map._data_validation_2(d=d, c=c)
        super().__init__(con=map_connective, t=(d, c,))

    @property
    def codomain(self) -> Tupl:
        """A tuple of formulas denoted as the codomain of the map.

        The codomain of a map is the enumeration of possible outputs of the get_image_from_map function.
        """
        return coerce_tuple(t=self[Map.CODOMAIN_INDEX])

    @property
    def domain(self) -> Enumeration:
        """An enumeration of formulas denoted as the domain of the map.

        The domain of a map is the enumeration of possible inputs of the get_image_from_map function.
        """
        return coerce_enumeration(e=self[Map.DOMAIN_INDEX])


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

    @staticmethod
    def _data_validation_2(e: FlexibleEnumeration = None,
                           strip_duplicates: bool = False) -> tuple[Connective, tuple]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param e:
        :param strip_duplicates:
        :return:
        """
        global enumeration_connective
        con: Connective = enumeration_connective
        if e is None:
            e = tuple()
        e_unique_only = strip_duplicate_formulas_in_python_tuple(t=e)
        if strip_duplicates:
            e = e_unique_only
        if len(e) != len(e_unique_only):
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_029,
                msg='Enumeration declaration failure. '
                    'The number of unique elements in `e` is not equal to the number of elements in `e`,'
                    'but parameter `strip_duplicates = False`.',
                len_e=len(e),
                len_e_unique_only=len(e_unique_only),
                e=e,
                e_unique_only=e_unique_only,
                strip_duplicates=strip_duplicates)
        return con, e

    def __new__(cls, e: FlexibleEnumeration = None,
                strip_duplicates: bool = False, **kwargs):
        c, e = Enumeration._data_validation_2(e=e, strip_duplicates=strip_duplicates)
        o: tuple = super().__new__(cls, con=c, t=e, **kwargs)
        return o

    def __init__(self, e: FlexibleEnumeration = None,
                 strip_duplicates: bool = False, **kwargs):
        c, e = Enumeration._data_validation_2(e=e, strip_duplicates=strip_duplicates)
        super().__init__(con=c, t=e, **kwargs)


FlexibleEnumeration = typing.Optional[typing.Union[Enumeration, typing.Iterable[FlexibleFormula]]]
"""FlexibleEnumeration is a flexible python type that may be safely coerced into an Enumeration."""


class EmptyEnumeration(Enumeration):
    """An empty-enumeration is an enumeration that has no element.
    """

    def __new__(cls):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        return super().__new__(cls=cls, e=None)

    def __init__(self):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        super().__init__(e=None)


class SingletonEnumeration(Enumeration):
    """A singleton-enumeration is an enumeration that has exactly one element.
    """

    def __new__(cls, element: FlexibleFormula):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        element: Formula = coerce_formula(phi=element)
        return super().__new__(cls=cls, e=(element,))

    def __init__(self, element: FlexibleFormula):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        element: Formula = coerce_formula(phi=element)
        super().__init__(e=element)


class Transformation(Formula, abc.ABC):
    """A transformation is a method by which new formulas may be created.

    The following transformations are supported:
     - transformation-by-variable-substitution (cf. NaturalTransformation python-class)
     - algorithmic-transformation (cf. AlgorithmicTransformation python-class)

     # TODO: Consider renaming to functor, or theory-morphism. Not sure which one is more accurate.

    """
    VARIABLES_INDEX: int = 1
    DECLARATIONS_INDEX: int = 2
    INPUT_SHAPES_INDEX: int = 3
    OUTPUT_SHAPE_INDEX: int = 0

    @staticmethod
    def _data_validation_2(
            con: Connective,
            o: FlexibleFormula,
            v: FlexibleEnumeration | None = None,
            d: FlexibleEnumeration | None = None,
            i: FlexibleTupl | None = None) -> tuple[
        Connective, Formula, Enumeration, Enumeration, Tupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param con:
        :param o: A formula denoted as the output-shape.
        :param v:
        :param d:
        :param i: A tuple of formulas denotes as the input-shapes.
        :return:
        """
        con: Connective = coerce_connective(con=con)
        o: Formula = coerce_formula(phi=o)
        v: Enumeration = coerce_enumeration(e=v, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        d: Enumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        i: Tupl = coerce_tuple(t=i, interpret_none_as_empty=True, canonic_conversion=True)
        return con, o, v, d, i

    def __new__(cls, con: Connective, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                d: FlexibleEnumeration | None = None,
                i: FlexibleTupl | None = None):
        """

        :param con:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        con, o, v, d, i = Transformation._data_validation_2(con=con, o=o, v=v, d=d, i=i)
        o: tuple = super().__new__(cls, con=transformation_by_variable_substitution_connective,
                                   t=(o, v, d, i,))
        return o

    def __init__(self, con: Connective, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                 d: FlexibleEnumeration | None = None,
                 i: FlexibleTupl | None = None):
        """

        :param con:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        con, o, v, d, i = Transformation._data_validation_2(con=con, o=o, v=v, d=d, i=i)
        super().__init__(con=transformation_by_variable_substitution_connective, t=(o, v, d, i,))

    def __call__(self, i: FlexibleTupl | None = None, i2: FlexibleTupl | None = None) -> Formula:
        """A shortcut for self.apply_transformation()

        :param i: A tuple of formulas denoted as the input arguments.
        :param i2: A tuple of formulas denoted as the complementary input arguments.
        :return:
        """
        return self.apply_transformation(i=i, i2=i2)

    @abc.abstractmethod
    def apply_transformation(self, i: FlexibleTupl | None = None,
                             i2: FlexibleTupl | None = None) -> Formula:
        """

        :param i: A tuple of formulas denoted as the input arguments.
        :param i2: A tuple of formulas denoted as the complementary input arguments.
        :return: A formula denoted as the output value.
        """
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_058,
                                  msg='Abstract python method is not implemented.',
                                  object=self, object_type=type(self),
                                  arguments=i)

    @property
    def output_shape(self) -> Formula:
        """The shape of the output returned by the transformation.

        The output-shape is expressed as an arbitrary formula that may contain variables as sub-formulas.

        :return:
        """
        return self[Transformation.OUTPUT_SHAPE_INDEX]

    @property
    def output_declarations(self) -> Enumeration:
        """A list of variables that are not present in the input-shapes,
        and that correspond to newly declared objects in the transformation output."""
        return self[Transformation.DECLARATIONS_INDEX]

    @abc.abstractmethod
    def is_compatible_with(self, t: FlexibleFormula) -> bool:
        """A computing low-cost method tha informs a calling process whether trying to use this transformation
        is worthwhile in trying to yield formula `t`.
        
        The idea here is to make an early check on the compatibility of the transformation with a certain 
        target formula `t`, before engaging in a brute-force attempt to derive a certain statement.

        :param t: A formula denoted as the target.
        :return:
        """
        raise u1.ApplicativeError(msg='abstract method')

    @property
    def input_shapes(self) -> Tupl:
        """A tuple of formulas that provide the shape of arguments (aka input values) expected by the transformation.
        Shapes are expressed as arbitrary formulas that may contain variables (cf. variables property).
        The transformation formula thus declares that it expect to receive as input values a tuple of formulas
        that are formula-equivalent-with-variables with those shapes."""
        return self[Transformation.INPUT_SHAPES_INDEX]

    @property
    def variables(self) -> Enumeration:
        """Variables used to express the shapes of arguments and the conclusion."""
        return self[Transformation.VARIABLES_INDEX]


class TransformationByVariableSubstitution(Transformation, ABC):
    """A transformation-by-variable-substitution, is a map from the class of formulas to itself.

    Syntactically, a transformation-by-variable-substitution is a formula :math:`f(o, V, D, I)` where:
     - :math:`f` is the transformation-by-variable-substitution connective,
     - :math:`o` is a formula denoted as the output-shape.
     - :math:`V` is an enumeration whose children are simple-objects called the variables.
     - :math:`D` is an enumeration whose children are simple-objects called the new-object-declarations.
     - :math:`I` is a tuple of formulas denoted as the input-shapes.
     - The intersection :math:`V ∩ D` is empty.

    Algorithm:
    The following algorithm is applied when a transformation-by-variable-substitution is "called":
     - Input argument: P_input (an enumeration of formulas that are formula-equivalent-with-variables to
       P, given variables V.
     - Procedure:
        1) Map variables in P with their corresponding sub-formulas in P_input, denoted variable_values.
        2) Substitute variables in c with their variable_values from that map.
        3) For every new object declaration, create a new connective with a new symbol.
        4) Substitute the connectives of new object declarations in c with their newly created connectives.

    Note 1: If a transformation-by-variable-substitution contains new-object-declarations, then it is non-deterministic,
        i.e.: every time it is called with the same input arguments, it creates a new unique formula.
        To the contrary, if a transformation-by-variable-substitution contains no new-object-declarations, then it is deterministic,
        i.e.: every time it is called with the same input arguments, it creates identical formulas.

    Note 2: When new-object-declarations are used, the transformation-by-variable-substitution declares new objects in the theory.
        In fact, this is the only possibility for new objects to be created / declared.

    Note 3: When new-object-declarations are used, note that it is not the sub-formulas that are replaced,
        but the connectives. This makes it possible to design transformation-by-variable-substitution that output new non

    Note 4: Transformations are the building blocks of inference-rules. Ses inference-rules for more details.

    Note 5: The transformation-by-variable-substitution in an inference rule is very similar to an intuitionistic sequent (cf. Mancosu
    et al., 2021, p. 170), i.e.: "In intuitionistic-sequent, there may be at most one formula to the right of ⇒ .", with
    some distinctive properties:
        - a transformation-by-variable-substitution comprises an explicit and finite set of variables,
          while an intuitionistic-sequent uses only formula variables.
        - the order of the premises in a transformation-by-variable-substitution does not matter a priori because it is an enumeration,
          while the order of the formulas in the antecedent of an intuitionistic-sequent matter a priori,
          even though this constraint is immediately relieved by the interchange structural rule.
    """

    @staticmethod
    def _data_validation_3(o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                           d: FlexibleEnumeration | None = None,
                           i: FlexibleTupl | None = None) -> tuple[Connective, Formula, Enumeration, Enumeration, Tupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :return:
        """
        con: Connective = transformation_by_variable_substitution_connective
        o: Formula = coerce_formula(phi=o)
        v: Enumeration = coerce_enumeration(e=v, interpret_none_as_empty=True)
        d: Enumeration = coerce_enumeration(e=d, interpret_none_as_empty=True)
        i: Tupl = coerce_tuple(t=i, interpret_none_as_empty=True, canonic_conversion=True)
        return con, o, v, d, i

    def __new__(cls, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                d: FlexibleEnumeration | None = None,
                i: FlexibleTupl | None = None):
        """

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        c2, o, v, d, i = TransformationByVariableSubstitution._data_validation_3(o=o, v=v, d=d, i=i)
        o: tuple = super().__new__(cls, con=c2, o=o, v=v, d=d, i=i)
        return o

    def __init__(self, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                 d: FlexibleEnumeration | None = None,
                 i: FlexibleTupl | None = None):
        """

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        c2, o, v, d, i = TransformationByVariableSubstitution._data_validation_3(o=o, v=v, d=d, i=i)
        super().__init__(con=c2, o=o, v=v, d=d, i=i)

    def __call__(self, i: FlexibleTupl | None = None, i2: FlexibleTupl | None = None) -> Formula:
        """A shortcut for self.apply_transformation()

        :param i: A tuple of formulas denoted as the input-values.
        :param i2: OBSOLETE: A complementary tuple of formulas.
        :return:
        """
        return self.apply_transformation(i=i, i2=i2)

    def apply_transformation(self, i: FlexibleTupl | None = None,
                             i2: FlexibleTupl | None = None) -> Formula:
        """

        :param i: A tuple of formulas denoted as the input-values.
        :param i2: OBSOLETE: A complementary tuple of formulas.
        :return:
        """
        i = coerce_tuple(t=i, interpret_none_as_empty=True)
        i2 = coerce_tuple(t=i2,
                          interpret_none_as_empty=True)  # This argument is not used by transformation-by-variable-substitution.
        # step 1: confirm every argument is compatible with its premises,
        # and seize the opportunity to retrieve the mapped variable values.
        success, variables_map = is_formula_equivalent_with_variables_2(phi=i, psi=self.input_shapes,
                                                                        variables=self.variables,
                                                                        variables_fixed_values=None)
        if not success:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_030,
                                      msg='Applying a transformation-by-variable-substitution with incorrect premises.',
                                      target_formula=i, transformation_premises=self.input_shapes,
                                      transformation_variables=self.variables, transformation=self)

        # step 2:
        outcome: Formula = replace_formulas(phi=self.output_shape, m=variables_map)

        # step 3: new objects declarations.
        declarations_map: Map = Map()
        for declaration in self.output_declarations:
            con: Connective = Connective()
            simple_formula: Formula = Formula(con=con)
            # TODO: Find a way to initialize the new_connective formula_typesetter.
            # TODO: Find a way to initialize the new_connective arity.
            declarations_map: Map = append_pair_to_map(m=declarations_map, preimage=declaration, image=simple_formula)

        # step 4: substitute new-object-declarations in the conclusion
        outcome: Formula = replace_connectives(phi=outcome, m=declarations_map)

        return outcome

    def is_compatible_with(self, t: FlexibleFormula) -> bool:
        """Performs low-cost checks and returns True if target formula `t` is compatible with the output of the
        transformation. This is useful to avoid expensive brute-force to find some derivation in a theory,
        when it is clear from the beginning that the underlying transformation.

        :param t:
        :return:
        """
        is_candidate, _ = is_formula_equivalent_with_variables_2(phi=self.output_shape, psi=t, variables=self.variables)
        return is_candidate


FlexibleTransformationByVariableSubstitution = typing.Optional[typing.Union[TransformationByVariableSubstitution]]


def coerce_transformation(f: FlexibleTransformation) -> Transformation:
    """Coerces lose argument `f` to a transformation, strongly python-typed as Transformation,
    or raises an error with code E-AS1-060 if this fails."""
    f: Formula = coerce_formula(phi=f)
    if isinstance(f, Transformation):
        return f
    elif is_well_formed_transformation_by_variable_substitution(t=f):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        # TODO: Move this logic to coerce_natural_transformation
        return TransformationByVariableSubstitution(o=f[TransformationByVariableSubstitution.OUTPUT_SHAPE_INDEX],
                                                    v=f[TransformationByVariableSubstitution.VARIABLES_INDEX],
                                                    d=f[TransformationByVariableSubstitution.DECLARATIONS_INDEX],
                                                    i=f[TransformationByVariableSubstitution.INPUT_SHAPES_INDEX])
    elif is_well_formed_transformation_by_external_algorithm(t=f):
        # phi is a well-formed algorithm,
        # it can be safely re-instantiated as an Algorithm and returned.
        # TODO: Move this logic to coerce_algorithmic_transformation
        return TransformationByExternalAlgorithm(algo=f.external_algorithm,
                                                 check=what_the_hell,  # correct this
                                                 o=f[TransformationByVariableSubstitution.OUTPUT_SHAPE_INDEX],
                                                 v=f[TransformationByVariableSubstitution.VARIABLES_INDEX],
                                                 d=f[TransformationByVariableSubstitution.DECLARATIONS_INDEX],
                                                 i=f[TransformationByVariableSubstitution.INPUT_SHAPES_INDEX])
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_060,
            msg='`t` could not be coerced to a transformation.',
            m=f)


def coerce_transformation_by_variable_substitution(t: FlexibleFormula) -> TransformationByVariableSubstitution:
    """Coerces lose argument `t` to a transformation, strongly python-typed as Transformation,
    or raises an error with code E-AS1-031 if this fails."""
    t: Formula = coerce_formula(phi=t)
    if isinstance(t, TransformationByVariableSubstitution):
        return t
    elif isinstance(t, Formula) and is_well_formed_transformation_by_variable_substitution(t=t):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        return TransformationByVariableSubstitution(o=t[TransformationByVariableSubstitution.OUTPUT_SHAPE_INDEX],
                                                    v=t[TransformationByVariableSubstitution.VARIABLES_INDEX],
                                                    d=t[TransformationByVariableSubstitution.DECLARATIONS_INDEX],
                                                    i=t[TransformationByVariableSubstitution.INPUT_SHAPES_INDEX])
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_031,
            msg='`t` could not be coerced to a transformation-by-variable-substitution.',
            t=t)


def coerce_external_algorithm(f: object) -> typing.Callable:
    """Coerces lose argument `f` to an external-algorithm, i.e. a python-function,
    or raises an error with code E-AS1-056 if this fails."""
    if isinstance(f, typing.Callable):
        return f
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_056, coerced_type=typing.Callable,
                                  external_algorithm_type=type(f),
                                  external_algorithm=f)


class TransformationByExternalAlgorithm(Transformation):
    """A well-formed algorithmic-transformation is a derivation that justified the derivation of further theorems in
    a theory, should bew impose conditions ex premises???
    by executing an algorithm that is external to the theory.
    The algorithm generates a new formula.

    Distinctively from premises, we should pass arguments to the algorithm."""

    _last_index = 0

    @staticmethod
    def _data_validation_3(
            algo: typing.Callable, check: typing.Callable, o: FlexibleFormula,
            v: FlexibleEnumeration | None = None,
            d: FlexibleEnumeration | None = None,
            i: FlexibleTupl | None = None
    ) -> tuple[Connective, typing.Callable, typing.Callable, Formula, Enumeration, Enumeration, Tupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param algo:
        :param check:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :return:
        """
        global _connectives
        con: Connective = algorithm_connective
        # TODO: Check `a` is callable nad has correct signature.
        algo: typing.Callable = coerce_external_algorithm(f=algo)
        # TODO: Check `i` is callable nad has correct signature.
        o: Formula = coerce_formula(phi=o)
        v: Enumeration = coerce_enumeration(e=v, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        d: Enumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, canonic_conversion=True,
                                            strip_duplicates=True)
        i: Tupl = coerce_tuple(t=i, interpret_none_as_empty=True, canonic_conversion=True)
        return con, algo, check, o, v, d, i

    def __new__(cls, algo: typing.Callable, check: typing.Callable, o: FlexibleFormula,
                v: FlexibleEnumeration | None = None,
                d: FlexibleEnumeration | None = None,
                i: FlexibleTupl | None = None):
        """

        :param algo: An external algorithm.
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        con, algo, check, o, v, d, i = TransformationByExternalAlgorithm._data_validation_3(algo=algo, check=check, o=o,
                                                                                            v=v, d=d,
                                                                                            i=i)
        o: tuple = super().__new__(cls, con=con, o=o, v=v, d=d, i=i)
        return o

    def __init__(self,
                 algo: typing.Callable,
                 check: typing.Callable | None,
                 o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                 d: FlexibleEnumeration | None = None,
                 i: FlexibleTupl | None = None):
        """

        :param algo:
        :param check:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        c2, algo, check, o, v, d, i = TransformationByExternalAlgorithm._data_validation_3(algo=algo, check=check, o=o,
                                                                                           v=v, d=d,
                                                                                           i=i)
        self._external_algorithm: typing.Callable = algo
        self._is_derivation_candidate: typing.Callable | None = check
        super().__init__(con=c2, o=o, v=v, d=d, i=i)

        # Default typesetting configuration
        if pl1.REF_TS not in self.ts.keys():
            TransformationByExternalAlgorithm._last_index = TransformationByExternalAlgorithm._last_index + 1
            self.ts[pl1.REF_TS] = pl1.NaturalIndexedSymbolTypesetter(body_ts=pl1.symbols.g_uppercase_serif_italic,
                                                                     index=TransformationByExternalAlgorithm._last_index)
        if pl1.DECLARATION_TS not in self.ts.keys():
            self.ts[pl1.DECLARATION_TS] = typesetters.declaration(
                conventional_class='transformation-by-external-algorithm')

        u1.log_info(self.typeset_as_string(theory=self, ts_key=pl1.DECLARATION_TS))

    def __call__(self, i: FlexibleTupl | None = None, i2: FlexibleTupl | None = None) -> Formula:
        """A shortcut for self.apply_transformation()"""
        return self.apply_transformation(i=i, i2=i2)

    def apply_transformation(self, i: FlexibleTupl | None = None,
                             i2: FlexibleTupl | None = None, m: FlexibleMap | None = None) -> Formula:
        """

        :param i: A tuple of premise arguments, whose order matches the order of the transformation premises.
        :param i2: A tuple of complementary arguments.
        :return:
        """
        i = coerce_tuple(t=i, interpret_none_as_empty=True)
        i2 = coerce_tuple(t=i2, interpret_none_as_empty=True)
        # step 1: confirm every argument is compatible with its premises,
        # and seize the opportunity to retrieve the mapped variable values.
        # supported extreme case: there are no premises.
        success, variables_map = is_formula_equivalent_with_variables_2(phi=i, psi=self.input_shapes,
                                                                        variables=self.variables,
                                                                        variables_fixed_values=None)
        if not success:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_050,
                                      msg='Transformation failure. '
                                          'Premises `p` are incompatible with transformation `t`.',
                                      p=i,
                                      t=self)

        # call the external-algorithm
        outcome: Formula = self.external_algorithm(p=i, a=i2)

        return outcome

    @property
    def external_algorithm(self) -> typing.Callable:
        return self._external_algorithm

    @property
    def output_shape(self) -> Formula:
        return self[TransformationByExternalAlgorithm.OUTPUT_SHAPE_INDEX]

    @property
    def output_declarations(self) -> Enumeration:
        return self[TransformationByExternalAlgorithm.DECLARATIONS_INDEX]

    def is_compatible_with(self, t: FlexibleFormula) -> bool:
        """Performs low-cost checks and returns True if target formula `t` is compatible with the output of the
        transformation. This is useful to avoid expensive brute-force to find some derivation in a theory,
        when it is clear from the beginning that the underlying transformation

        :param t:
        :return:
        """
        if self._is_derivation_candidate is None:
            # TODO: This is perhaps an obsolete property, perhaps we may only use the conclussion property.
            #   For the time being i make it nullable and we will see this later.
            return True
        else:
            return self._is_derivation_candidate(t=t)

    @property
    def input_shapes(self) -> Tupl:
        return self[TransformationByExternalAlgorithm.INPUT_SHAPES_INDEX]

    @property
    def variables(self) -> Enumeration:
        return self[TransformationByExternalAlgorithm.VARIABLES_INDEX]


FlexibleTransformationByExternalAlgorithm = typing.Optional[
    typing.Union[Connective, Formula, TransformationByExternalAlgorithm]]


def coerce_transformation_by_external_algorithm(
        t: FlexibleTransformationByExternalAlgorithm) -> TransformationByExternalAlgorithm:
    """Coerces loose argument `a` to an algorithm, strongly typed as Algorithm,
    or raises an error with code E-AS1-055 if this fails."""
    if isinstance(t, TransformationByExternalAlgorithm):
        return t
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_055, coerced_type=TransformationByExternalAlgorithm,
                                  algorithm_type=type(t),
                                  algorithm=t)


def coerce_connective(con: Connective) -> Connective:
    if isinstance(con, Connective):
        return con
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_059,
            msg='`con` could not be coerced to a connective.',
            c=con, c_type=type(con))


def coerce_hypothesis(h: FlexibleFormula) -> Hypothesis:
    """Coerces formula `h` into a well-formed hypothesis, or raises an error if it fails.

    :param h: A formula that is presumably a well-formed hypothesis.
    :return: A well-formed hypothesis.
    :raises ApplicativeError: with code AS1-083 if coercion fails.
    """
    if isinstance(h, Hypothesis):
        return h
    elif is_well_formed_hypothesis(h=h):
        b: Theory = coerce_theory(t=h[Hypothesis.BASE_THEORY_INDEX], interpret_none_as_empty=True,
                                  canonical_conversion=True)
        a: Formula = coerce_formula(phi=h[Hypothesis.ASSUMPTION_INDEX])
        return Hypothesis(b=b, a=a)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_083,
            msg='`h` cannot be coerced to a well-formed hypothesis.',
            h=h)


def coerce_inference(i: FlexibleFormula) -> Inference:
    """Coerces formula `i` into a well-formed inference, or raises an error if it fails.

    :param i: A formula that is presumably a well-formed inference.
    :return: A well-formed inference.
    :raises ApplicativeError: with code AS1-032 if coercion fails.
    """
    if isinstance(i, Inference):
        return i
    elif is_well_formed_inference(i=i):
        i2: InferenceRule = coerce_inference_rule(i=i[Inference.INFERENCE_RULE_INDEX])
        p: Tupl = coerce_tuple(t=i[Inference.PREMISES_INDEX], interpret_none_as_empty=True)
        a: Tupl = coerce_tuple(t=i[Inference.ARGUMENTS_INDEX], interpret_none_as_empty=True)
        return Inference(i=i2, p=p, a=a)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_032,
            msg='`i` cannot be coerced to a well-formed inference.',
            i=i)


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


def is_well_formed_tupl(t: FlexibleFormula, interpret_none_as_empty: bool = False,
                        raise_error_if_false: bool = False) -> bool:
    """Returns True if phi is a well-formed tuple, False otherwise.

    Note: by definition, all formulas are also tuples. Hence, return True if phi converts smoothly to a well-formed
    formula.

    :param raise_error_if_false:
    :param t:
    :param interpret_none_as_empty:
    :return: bool
    """
    if interpret_none_as_empty and t is None:
        return True
    t: Formula = coerce_formula(phi=t)
    if t.connective is not tupl_connective:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_066,
                msg='`t` is not a well-formed tupl.',
                t=t,
                interpret_none_as_empty=interpret_none_as_empty,
                raise_error_if_false=raise_error_if_false
            )
        return False
    return True


def is_well_formed_hypothesis(h: FlexibleHypothesis, raise_error_if_false: bool = False) -> bool:
    """Returns `True` if and only if `h` is a well-formed hypothesis, `False` otherwise.

    TODO: Check that assumption is a proposition instead of just checking it is a formula.

    :param h: A formula that may or may not be a well-formed hypothesis.
    :param raise_error_if_false: If the argument is `True`, the function raises an AS1-082 error instead of returning
        `False`.
    :return: bool.
    """
    h = coerce_formula(phi=h)
    if (h.connective is not hypothesis_connective or
            not h.arity == 2 or
            not is_well_formed_theory(t=h[Hypothesis.BASE_THEORY_INDEX]) or
            not is_well_formed_formula(phi=h[Hypothesis.ASSUMPTION_INDEX])):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_082,
                msg='`h` is not a well-formed hypothesis.',
                h=h
            )
        return False
    else:
        return True


def is_well_formed_inference(i: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns `True` if and only if `i` is a well-formed inference, `False` otherwise.

    :param i: A formula that may or may not be a well-formed inference.
    :param raise_error_if_false: If the argument is `True`, the function raises an AS1-081 error instead of returning
        `False`.
    :return: bool.
    """
    i = coerce_formula(phi=i)
    if (i.connective is not inference_connective or
            not i.arity == 3 or
            not is_well_formed_inference_rule(i=i[Inference.INFERENCE_RULE_INDEX]) or
            not is_well_formed_tupl(t=i[Inference.PREMISES_INDEX]) or
            not is_well_formed_tupl(t=i[Inference.ARGUMENTS_INDEX])):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_081,
                msg='`i` is not a well-formed inference.',
                i=i
            )
        return False
    else:
        return True


def is_well_formed_map(m: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns True if and only if `m` is a well-formed-map, False otherwise, i.e. it is ill-formed.

    :param m: A formula, possibly a well-formed map.
    :param raise_error_if_false: If True, raises an AS1-061 error when `m` is not a well-formed map.
    :return: bool.
    """
    m = coerce_formula(phi=m)
    if (m.connective is not map_connective or
            not m.arity == 2 or
            not is_well_formed_enumeration(e=m[Map.DOMAIN_INDEX]) or
            not is_well_formed_tupl(t=m[Map.CODOMAIN_INDEX])):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_061,
                msg='`m` is not a well-formed-map.',
                m=m
            )
        return False
    else:
        return True


def is_well_formed_transformation_by_variable_substitution(t: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed transformation, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if (t.connective is not transformation_by_variable_substitution_connective or
            t.arity != 4 or
            not is_well_formed_formula(phi=t.term_0) or
            not is_well_formed_enumeration(e=t.term_1) or
            not is_well_formed_enumeration(e=t.term_2) or
            not is_well_formed_tupl(t=t.term_3)):
        return False
    else:
        # TODO: Check that variables are only simple-objects (or not???)
        # TODO: Check that declarations are only simple-objects (or not???)
        return True


def is_well_formed_enumeration(e: FlexibleFormula) -> bool:
    """Return True if phi is a well-formed enumeration, False otherwise.

    :param e: A formula.
    :return: bool.
    """
    global enumeration_connective
    if e is None:
        # This is debatable.
        # Implicit conversion of None to the empty enumeration.
        return True
    else:
        e = coerce_formula(phi=e)
        if e.connective is not enumeration_connective:
            return False
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
    elif (i.connective is derivation_connective and
          i.arity == 2 and
          is_well_formed_transformation(t=i.term_0) and
          i.term_1.connective is inference_rule_connective):
        return True
    else:
        return False


def is_well_formed_transformation(t: FlexibleFormula) -> bool:
    """Return True if and only if `t` is a well-formed transformation, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if isinstance(t, Transformation):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif is_well_formed_transformation_by_variable_substitution(t=t):
        return True
    elif is_well_formed_transformation_by_external_algorithm(t=t):
        return True
    else:
        return False


def is_well_formed_transformation_by_external_algorithm(t: FlexibleFormula) -> bool:
    """Return True if and only if phi is a well-formed algorithm, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if isinstance(t, TransformationByExternalAlgorithm):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif (t.arity == 0 and
          t.connective is algorithm_connective and
          hasattr(t, 'external_algorithm')):
        return True
    else:
        return False


def is_valid_proposition_in_theory_1(p: FlexibleFormula, t: FlexibleTheory | None = None,
                                     d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                                     strip_duplicates: bool = True,
                                     interpret_none_as_empty: bool = True,
                                     canonic_conversion: bool = True,
                                     max_derivations: int | None = None) -> bool:
    """Returns `True` if and only if proposition `p` is valid in theory `t`, `False` otherwise.

    Alternatively, check validity of `p` in an enumeration of derivations `d`.

    A formula :math:`\\phi` is a valid-statement with regard to a theory :math:`t`, if and only if:
     - :math:`\\phi` is the valid-statement of an axiom in :math:`t`,
     - or :math:`\\phi` is the valid-statement of a theorem in :math:`t`.

    :param p:
    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Verifies the validity of `p` only through the first `max_derivations` derivations
        in canonical order, or all derivations if `None`.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    p: Formula = coerce_formula(phi=p)
    if t is not None:
        t: Theory = coerce_theory(t=t, interpret_none_as_empty=False)
    else:
        d: Enumeration = coerce_enumeration(e=d, strip_duplicates=True, interpret_none_as_empty=True,
                                            canonic_conversion=True)
    return any(is_formula_equivalent(phi=p, psi=valid_statement) for valid_statement in
               iterate_theory_propositions(
                   t=t,
                   d=d,
                   strip_duplicates=strip_duplicates,
                   interpret_none_as_empty=interpret_none_as_empty,
                   canonic_conversion=canonic_conversion,
                   max_derivations=max_derivations))
    # t.iterate_valid_statements())


def is_valid_proposition_in_theory_2(p: FlexibleFormula, t: FlexibleTheory) -> tuple[bool, int | None]:
    """Given a theory `t` and a proposition `p`, return a pair ("b", `i`) such that:
     - "b" is True if `p` is a valid proposition in theory `t`, False otherwise,
     - `i` is the derivation-index of the first occurrence of `p` in a derivation in `t` if "b" is True,
        None otherwise.

    This function is very similar to is_valid_proposition_in_theory_1 except that it returns
    the index of the first occurrence of a derivation that matches p. This information is typically
    required in function would_be_valid_derivation_enumeration_in_theory to check whether
    some propositions are successors or predecessors to some other propositions and verify
    derivation validity.

    Definition:
    A formula p is a valid-proposition with regard to a theory `t`, if and only if:
     - `p` is the valid-proposition of an axiom in `t`,
     - or `p` is the valid-proposition of a theorem in `t`.
    """

    p: Formula = coerce_formula(phi=p)
    t: Theory = coerce_theory(t=t)
    for d, i in zip(iterate_theory_derivations(t=t), range(len(t))):
        if is_formula_equivalent(phi=p, psi=d.valid_statement):
            return True, i
    return False, None


def iterate_formula_terms(phi: FlexibleFormula, max_terms: int | None = None
                          ) -> typing.Generator[Formula, None, None]:
    """Iterates the terms of a formula in canonical order.

    :param phi: A formula.
    :param max_terms: Yields only math:`max_terms` elements, or all terms if None.
    :return:
    """
    phi: Formula = coerce_formula(phi=phi)
    yield from itertools.islice(phi, max_terms)


def iterate_tuple_elements(phi: FlexibleTupl, max_elements: int | None = None
                           ) -> typing.Generator[Formula, None, None]:
    """Iterates the elements of a tuple in canonical order.

    :param phi: A formula.
    :param max_elements: Yields only math:`max_elements` elements, or all elements if None.
    :return:
    """
    phi = coerce_tuple(t=phi)
    yield from iterate_formula_terms(phi=phi, max_terms=max_elements)


def iterate_enumeration_elements(e: FlexibleEnumeration, max_elements: int | None = None,
                                 interpret_none_as_empty: bool | None = None, strip_duplicates: bool | None = None,
                                 canonic_conversion: bool | None = None
                                 ) -> typing.Generator[Formula, None, None]:
    """Iterates the elements of an enumeration in canonical order.

    :param e:
    :param max_elements: Yields only math:`max_elements` elements, or all elements if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `e` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `e` to enumeration. Raise an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `e` to enumeration.
    :return:
    """
    e: Enumeration = coerce_enumeration(e=e, interpret_none_as_empty=interpret_none_as_empty,
                                        strip_duplicates=strip_duplicates, canonic_conversion=canonic_conversion)
    yield from iterate_formula_terms(phi=e, max_terms=max_elements)


def are_valid_statements_in_theory(s: FlexibleTupl, t: FlexibleTheory) -> bool:
    """Returns True if every formula phi in enumeration s is a valid-statement in theory t, False otherwise.
    """
    s: Tupl = coerce_tuple(t=s, interpret_none_as_empty=True)
    t: Theory = coerce_theory(t=t)
    return all(is_valid_proposition_in_theory_1(p=phi, t=t) for phi in iterate_tuple_elements(s))


def iterate_permutations_of_enumeration_elements_with_fixed_size(e: FlexibleEnumeration, n: int) -> \
        typing.Generator[Enumeration, None, None]:
    """Iterates all distinct tuples (order matters) of exactly n elements in enumeration e.

    :param e: An enumeration.
    :param n: The fixed size of the tuples to be iterated.
    :return:
    """
    e: Enumeration = coerce_enumeration_OBSOLETE(e=e)
    # e: Enumeration = coerce_enumeration(e=e, strip_duplicates=True, interpret_none_as_empty=True,
    #                                    canonic_conversion=True)
    if n > e.arity:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_033, msg='n > |e|')
    if n < 0:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_034, msg='n < 0')
    if n == 0:
        # nothing will be yield from the function.
        # note that itertools.permutations would yield one empty tuple.
        return
    else:
        generator = itertools.permutations(iterate_enumeration_elements(e=e), n)
        for python_tuple in generator:
            permutation: Enumeration = Enumeration(e=python_tuple)
            yield permutation
        return


def iterate_theory_derivations(t: FlexibleTheory[FlexibleDerivation] | None = None,
                               d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                               strip_duplicates: bool = True,
                               interpret_none_as_empty: bool = True,
                               canonic_conversion: bool = True,
                               max_derivations: int | None = None) -> \
        typing.Generator[Formula, None, None]:
    """Iterates through derivations of a theory `t` in canonical order.

    Alternatively, iterates through an enumeration of derivations `d` in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Yields only math:`max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    if t is not None:
        coerce_theory(t=t)
        d: Enumeration = t.derivations
    else:
        d: Enumeration = coerce_enumeration(e=d, strip_duplicates=strip_duplicates,
                                            interpret_none_as_empty=interpret_none_as_empty,
                                            canonic_conversion=canonic_conversion)
    for d2 in iterate_enumeration_elements(e=d, max_elements=max_derivations):
        d2: Derivation = coerce_derivation(d=d2)
        yield d2
    return


def iterate_theory_axioms(t: FlexibleTheory | None = None,
                          d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                          strip_duplicates: bool = True,
                          interpret_none_as_empty: bool = True,
                          canonic_conversion: bool = True,
                          max_derivations: int | None = None
                          ) -> typing.Generator[Axiom, None, None]:
    """Iterates through axioms in derivations of a theory `t`, in canonical order.

    Alternatively, iterates through axioms of an enumeration of derivations `d`, in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Considers only `max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_derivations(t=t,
                                         d=d,
                                         max_derivations=max_derivations,
                                         interpret_none_as_empty=interpret_none_as_empty,
                                         strip_duplicates=strip_duplicates,
                                         canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: Axiom = coerce_axiom(a=d2)
            yield a


def iterate_theory_theorems(t: FlexibleTheory | None = None,
                            d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                            strip_duplicates: bool = True,
                            interpret_none_as_empty: bool = True,
                            canonic_conversion: bool = True,
                            max_derivations: int | None = None
                            ) -> typing.Generator[Theorem, None, None]:
    """Iterates through theorems in derivations of a theory `t`, in canonical order.

    Alternatively, iterates through theorems of an enumeration of derivations `d`, in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Considers only `max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_derivations(t=t,
                                         d=d,
                                         max_derivations=max_derivations,
                                         interpret_none_as_empty=interpret_none_as_empty,
                                         strip_duplicates=strip_duplicates,
                                         canonic_conversion=canonic_conversion):
        if is_well_formed_theorem(t=d2):
            t: Theorem = coerce_theorem(t=d2)
            yield t


def iterate_theory_inference_rules(t: FlexibleTheory | None = None,
                                   d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                                   strip_duplicates: bool = True,
                                   interpret_none_as_empty: bool = True,
                                   canonic_conversion: bool = True,
                                   max_derivations: int | None = None
                                   ) -> typing.Generator[InferenceRule, None, None]:
    """Iterates through inference-rules in derivations of a theory `t` in canonical order.

    Alternatively, iterates through inference-rules of an enumeration of derivations `d` in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Considers only `max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_derivations(t=t,
                                         d=d,
                                         max_derivations=max_derivations,
                                         interpret_none_as_empty=interpret_none_as_empty,
                                         strip_duplicates=strip_duplicates,
                                         canonic_conversion=canonic_conversion):
        if is_well_formed_inference_rule(i=d2):
            i: InferenceRule = coerce_inference_rule(i=d2)
            yield i


def iterate_theory_valid_statements(t: FlexibleTheory | None = None,
                                    d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                                    strip_duplicates: bool = True,
                                    interpret_none_as_empty: bool = True,
                                    canonic_conversion: bool = True,
                                    max_derivations: int | None = None
                                    ) -> typing.Generator[Formula, None, None]:
    """Iterates through valid-statements in derivations of a theory `t` in canonical order.

    Alternatively, iterates through propositions of an enumeration of derivations `d` in canonical order.

    Definition: theory valid-statements
    The valid-statements of a theory are the propositions of its axioms and theorems and its inference-rules.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Considers only `max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_derivations(t=t,
                                         d=d,
                                         max_derivations=max_derivations,
                                         interpret_none_as_empty=interpret_none_as_empty,
                                         strip_duplicates=strip_duplicates,
                                         canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: Axiom = coerce_axiom(a=d2)
            s: Formula = a.valid_statement
            yield s
        elif is_well_formed_theorem(t=d2):
            m: Theorem = coerce_theorem(t=d2)
            s: Formula = m.valid_statement
            yield s
        elif is_well_formed_inference_rule(i=d2):
            i: InferenceRule = coerce_inference_rule(i=d2)
            s: Formula = i.valid_statement
            yield s


def iterate_theory_propositions(t: FlexibleTheory | None = None,
                                d: FlexibleEnumeration[FlexibleDerivation] | None = None,
                                strip_duplicates: bool = True,
                                interpret_none_as_empty: bool = True,
                                canonic_conversion: bool = True,
                                max_derivations: int | None = None
                                ) -> typing.Generator[Formula, None, None]:
    """Iterates through propositions in derivations of a theory `t` in canonical order.

    Alternatively, iterates through propositions of an enumeration of derivations `d` in canonical order.

    Definition: theory propositions
    The valid-statements of axioms and theorems in a theory.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if `t` is provided.
    :param max_derivations: Considers only `max_derivations` derivations, or all derivations if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_derivations(t=t,
                                         d=d,
                                         max_derivations=max_derivations,
                                         interpret_none_as_empty=interpret_none_as_empty,
                                         strip_duplicates=strip_duplicates,
                                         canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: Axiom = coerce_axiom(a=d2)
            p: Formula = a.valid_statement
            yield p
        elif is_well_formed_theorem(t=d2):
            m: Theorem = coerce_theorem(t=d2)
            p: Formula = m.valid_statement
            yield p


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
    s: Tupl = coerce_tuple(t=s, interpret_none_as_empty=True)
    t: Theory = coerce_theory(t=t)
    variables: Enumeration = coerce_enumeration(e=variables, interpret_none_as_empty=True, strip_duplicates=True)
    variables_values: Map = coerce_map(m=variables_values, interpret_none_as_empty=True)

    # list the free variables.
    # these are the variables that are in "variables" that are not in the domain of "variables_values".
    free_variables: Enumeration = Enumeration()
    for x in iterate_enumeration_elements(e=variables):
        if not is_in_map_domain(phi=x, m=variables_values):
            free_variables: Enumeration = Enumeration(e=(*free_variables, x,))

    if debug:
        u1.log_info(f'are_valid_statements_in_theory_with_variables: free-variables:{free_variables}')

    permutation_size: int = free_variables.arity

    if permutation_size == 0:
        # there are no free variables.
        # but there may be some or no variables with assigned values.
        # it follows that 1) there will be no permutations,
        # and 2) are_valid_statements_in_theory() is equivalent.
        s_with_variable_substitution: Formula = replace_formulas(phi=s, m=variables_values)
        s_with_variable_substitution: Tupl = coerce_tuple(t=s_with_variable_substitution)
        valid: bool = are_valid_statements_in_theory(s=s_with_variable_substitution, t=t)
        if valid:
            return valid, s_with_variable_substitution
        else:
            return valid, None
    else:
        valid_statements = iterate_theory_propositions(t=t)
        for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                        n=permutation_size):
            variable_substitution: Map = Map(d=free_variables, c=permutation)
            s_with_variable_substitution: Formula = replace_formulas(phi=s, m=variable_substitution)
            s_with_variable_substitution: Tupl = coerce_tuple(t=s_with_variable_substitution)
            s_with_permutation: Tupl = Tupl(e=(*s_with_variable_substitution,))
            if are_valid_statements_in_theory(s=s_with_permutation, t=t):
                return True, s_with_permutation
        return False, None


def is_proposition_with_free_variables_in_theory(phi: FlexibleFormula, t: FlexibleTheory,
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
    global axiom_connective
    a = coerce_formula(phi=a)
    if a.arity != 2:
        return False
    if a.connective is not derivation_connective:
        return False
    if not is_well_formed_formula(phi=a.term_0):
        return False
    if a.term_1.arity != 0:
        return False
    if a.term_1.connective != axiom_connective:
        return False
    # All tests were successful.
    return True


def is_well_formed_theorem(t: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Return True if and only if phi is a well-formed theorem, False otherwise.

    :param raise_error_if_false:
    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if isinstance(t, Theorem):
        # the Theorem python-type assures the well-formedness of the object.
        return True
    if (t.connective is not derivation_connective or
            not t.arity == 2 or
            not is_well_formed_formula(phi=t.term_0) or
            not is_well_formed_inference(i=t.term_1)):
        if raise_error_if_false:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_035, t=t)
        return False
    else:
        # TODO: Factorize the check in Theorem.__new__ or __init__,
        #   that takes into account new-object-declarations.
        i: Inference = coerce_inference(i=t.term_1)
        recomputed_outcome: Formula = i.inference_rule.transformation(i.premises)
        if not is_formula_equivalent(phi=t.term_0, psi=recomputed_outcome):
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            if raise_error_if_false:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_035, phi=t, psi_expected=t.term_0,
                                          psi_inferred=recomputed_outcome,
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


def would_be_valid_derivations_in_theory(v: FlexibleTheory, u: FlexibleEnumeration,
                                         raise_error_if_false: bool = False
                                         ) -> tuple[bool, Enumeration | None, Enumeration | None]:
    """Given an enumeration of presumably verified derivations "v" (e.g.: the derivation sequence of a theory `t`),
    and an enumeration of unverified derivations "u" (e.g.: whose elements are not (yet) effective
    theorems of `t`), returns True if a theory would be well-formed if it was composed of
    derivations "u" appended to derivations "v", or False if it would not.

    This function is useful to test whether some derivations will pass well-formedness validation before
    attempting to effectively derive it.

    :param v: An enumeration of presumably verified derivations.
    :param u: An enumeration of unverified derivations.
    :param raise_error_if_false:
    :return: A triple `(b, v′, u′)` where:
     `b` is `True` if all derivations in `u` would be valid, `False` otherwise,
     `v′` = `v` with duplicates stripped out if `b` is `True`, `None` otherwise,
     `u′` = `(u \\ v)` with duplicates stripped out if `b` is `True`, `None` otherwise.
    """
    v: Enumeration = coerce_enumeration(e=v, strip_duplicates=True, interpret_none_as_empty=True,
                                        canonic_conversion=True)
    u: Enumeration = coerce_enumeration(e=u, strip_duplicates=True, interpret_none_as_empty=True,
                                        canonic_conversion=True)

    # Consider only derivations that are not elements of the verified enumeration.
    # In effect, a derivation sequence must contain unique derivations under enumeration-equivalence.
    u: Enumeration = difference_enumeration(phi=u, psi=v, strip_duplicates=True, interpret_none_as_empty=True,
                                            canonic_conversion=True)

    # Create a complete enumeration "c" composed of derivations "u" appended to derivations "v",
    # getting rid of duplicates if any in the process.
    c: Enumeration = union_enumeration(phi=v, psi=u, strip_duplicates=True)

    # Put aside the index from which the proofs of derivations have not been verified.
    verification_threshold: int = len(v)

    # Coerce all enumeration elements to axioms, inference-rules, and theorems.
    # TODO: Implement a dedicated function coerce_enumeration_of_derivations().
    coerced_elements: list = [coerce_derivation(d=d) for d in iterate_enumeration_elements(e=c)]
    c: Enumeration = Enumeration(e=coerced_elements)

    # Iterate through all index positions of derivations for which the proofs must be verified.
    for index in range(verification_threshold, len(c)):

        # Retrieve the derivation whose proof must be verified.
        d: Derivation = c[index]

        # Retrieve the proposition or statement announced by the derivation.
        p: Formula = d.valid_statement

        if is_well_formed_axiom(a=d):
            # This is an axiom.
            # By definition, the presence of an axiom in a theory is valid.
            pass
        elif is_well_formed_inference_rule(i=d):
            # This is an inference-rule.
            # By definition, the presence of an inference-rule in a theory is valid.
            pass
        elif is_well_formed_theorem(t=d):
            # This is a theorem.
            # Check that this theorem is well-formed with regard to the target theory,
            # i.e. it is a valid derivation with regard to predecessor derivations.
            m: Theorem = coerce_theorem(t=d)
            i: Inference = m.inference
            ir: InferenceRule = m.inference.inference_rule
            # Check that the inference-rule is a valid predecessor in the derivation.
            if not any(is_formula_equivalent(phi=ir, psi=ir2) for ir2 in
                       iterate_theory_inference_rules(d=c, max_derivations=index + 1)):
                if raise_error_if_false:
                    raise u1.ApplicativeError(
                        code=c1.ERROR_CODE_AS1_068,
                        msg='Inference-rule `ir` is not a valid predecessor (with index strictly less than "index").'
                            ' This forbids the derivation of proposition `p` in step `d` in the derivation sequence.',
                        p=p, ir=ir, index=index, d=d, c=c, v=v, u=u)
                return False, None, None
            # Check that all premises are valid predecessor propositions in the derivation.
            for q in i.premises:
                # Check that this premise is a valid predecessor proposition in the derivation.
                if not is_valid_proposition_in_theory_1(p=q, t=None, d=c, max_derivations=index):
                    if raise_error_if_false:
                        raise u1.ApplicativeError(
                            msg='Derivation `d` claims to derive `p`.'
                                ' `q` is a premise necessary to derive `p`.'
                                ' But `q` is not found as a valid predecessor of `p` in the derivation sequence `c`.'
                                ' It follows that derivation `d` is not well formed.'
                                ' `index` shows the position of `d` in `c`.'
                                ' `v` enumerates the presumably verified derivations in the derivation sequence.'
                                ' `u` enumerates the unverified derivations in the derivation sequence.',
                            code=c1.ERROR_CODE_AS1_036,
                            p=p, q=q, index=index, d=d, c=c, v=v, u=u)
                    return False, None, None
            # Check that the transformation of the inference-rule effectively yields the announced proposition.
            f: Transformation = i.inference_rule.transformation
            if len(f.output_declarations) > 0:
                # But wait a minute...
                # If the transformation declares/creates new objects, the inference-rule is non-deterministic.
                # For this particular case, we must map the original objects created by the first derivation,
                # with the expected conclusion of the inference-rule.
                map1_test, map1 = is_formula_equivalent_with_variables_2(phi=p, psi=f.output_shape,
                                                                         variables=f.output_declarations)
                if not map1_test:
                    if raise_error_if_false:
                        # c2 = t2.conclusion
                        # d2 = t2.declarations
                        raise u1.ApplicativeError(
                            msg='Derivation `d` claims that `p` is valid in the derivation sequence `c`.'
                                'The inference-rule `ir` has conclusion `c2` with new object declarations `d2`.'
                                'But this conclusion is not formula-equivalent-with-variables with `p`.',
                            code=c1.ERROR_CODE_AS1_074, map1_test=map1_test, map1=map1,
                            p=p, index=index, t2=f, ir=ir, i=i, d=d, c=c, v=v, u=u)
                    return False, None, None

                map1_inverse = inverse_map(m=map1)
                p_inverse = replace_formulas(phi=p, m=map1_inverse)

                # The following test is probably superfluous,
                # as the precedent test covers the compatibility of the conclusion.
                inverse_test = is_formula_equivalent(phi=p_inverse, psi=f.output_shape)
                if not inverse_test:
                    if raise_error_if_false:
                        raise u1.ApplicativeError(
                            msg='Derivation `d` claims that `p` is valid in the derivation sequence `c`.'
                                'The inference-rule `ir` has conclusion `c2` with new object declarations `d2`.'
                                'But this conclusion is not formula-equivalent-with-variables with `p`.',
                            code=c1.ERROR_CODE_AS1_075, p_inverse=p_inverse, map1_inverse=map1_inverse,
                            map1_test=map1_test, map1=map1,
                            p=p, index=index, t2=f, ir=ir, i=i, d=d, c=c, v=v, u=u)
                    return False, None, None
                pass
            else:
                # The simpler case is when the inference-rule does not create new objects.
                # No remapping is necessary and the original conclusion can simply be compared
                # with the new conclusion.
                p_prime = f.apply_transformation(i=i.premises, i2=i.arguments)
                if not is_formula_equivalent(phi=p, psi=p_prime):
                    if raise_error_if_false:
                        raise u1.ApplicativeError(
                            msg='Inference-rule `ir` does not yield the expected proposition `p`,'
                                ' but yields "p_prime".'
                                ' This forbids the derivation of `p` in step `d` in the derivation sequence.'
                                ' Inference `i` contains the arguments (premises and the complementary arguments).',
                            code=c1.ERROR_CODE_AS1_036,
                            p=p, p_prime=p_prime, index=index, t2=f, ir=ir, i=i, d=d, c=c, v=v, u=u)
                    return False, None, None
            # All tests have been successfully completed, we now have the assurance
            # that derivation `d` would be valid if appended to theory `t`.
            pass
        else:
            # Incorrect form.
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    msg='Expected derivation `d` is not of a proper form (e.g. axiom, inference-rule or theorem).'
                        ' This forbids the derivation of proposition `p` in step `d` in the derivation'
                        ' sequence.',
                    code=c1.ERROR_CODE_AS1_071,
                    p=p, d=d, index=index, c=c, v=v, u=u)
            return False, None, None
        # Derivation `d` is valid.
        pass
    # All unverified derivations have been verified.
    pass
    return True, v, u


def is_well_formed_theory(t: FlexibleFormula, raise_event_if_false: bool = False) -> bool:
    """Return True if phi is a well-formed theory, False otherwise.

    :param t: A formula.
    :param raise_event_if_false:
    :return: bool.
    """
    t = coerce_formula(phi=t)

    if isinstance(t, Theory):
        # By design, the Theory class assures the well-formedness of a theory.
        # cf. the _data_validation_ method in the Theory class.
        return True

    con: Connective = t.connective
    if con is not theory_connective:
        # TODO: Remove the 1==2 condition above to re-implement a check of strict connectives constraints.
        #   But then we must properly manage python inheritance (Axiomatization --> Theory --> Enumeration).
        if raise_event_if_false:
            raise u1.ApplicativeError(
                msg='The connective "c" of theory `t` is not the "theory-formula" connective. '
                    'It follows that `t` is not a well-formed-theory.',
                con=con,
                con_id=id(con),
                theory_formula=theory_connective,
                theory_formula_id=id(theory_connective),
                t=t)
        return False

    # Check that the terms of the formula constitute an enumeration of derivations,
    # and that derivations in this sequence of derivations is valid.
    v: Enumeration = Enumeration(e=None)  # Assume no pre-verified derivations.
    u: Enumeration = transform_formula_to_enumeration(phi=t, strip_duplicates=False)
    would_be_valid, _, _ = would_be_valid_derivations_in_theory(v=v, u=u)
    return would_be_valid


def is_well_formed_axiomatization(a: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns True if and only if `a` is a well-formed axiomatization, False otherwise, i.e. it is ill-formed.

    :param a: A formula, possibly a well-formed axiomatization.
    :param raise_error_if_false: If True, raises an error when `a` is not a well-formed
        axiomatization.
    :raises ApplicativeError: with error code AS1-064 when `a` is not a well-formed axiomatization and
        `raise_error_if_false` = True.
    :return: bool.
    """
    global axiomatization_connective
    a = coerce_formula(phi=a)
    if (a.connective is not axiomatization_connective or
            any(not is_well_formed_axiom(a=x) and not is_well_formed_inference_rule(i=x)
                for x in iterate_formula_terms(phi=a))):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_064,
                msg='`a` is not a well-formed axiomatization.',
                a=a
            )
        return False
    return True


def coerce_derivation(d: FlexibleFormula) -> Derivation:
    """

    Validate that p is a well-formed theorem and returns it properly typed as Proof, or raise exception e123.

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
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_039,
            msg=f'Argument `d` of python-type `t` could not be coerced to a derivation of python-type '
                f'Derivation. The string representation of `d` is given in `s`.',
            d=d,
            t=type(d),
            s=u1.force_str(o=d))


def coerce_axiom(a: FlexibleFormula) -> Axiom:
    """Coerces formula `a` into a well-formed axiom, or raises an error if it fails.

    :param a: A formula that is presumably a well-formed axiom.
    :return: A well-formed axiom.
    :raises ApplicativeError: with code AS1-040 if coercion fails.
    """
    if isinstance(a, Axiom):
        return a
    elif isinstance(a, Formula) and is_well_formed_axiom(a=a):
        proved_formula: Formula = a.term_0
        return Axiom(s=proved_formula)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_040,
            msg='`a` cannot be coerced to a well-formed axiom.',
            a=a)


def coerce_inference_rule(i: FlexibleInferenceRule) -> InferenceRule:
    """Coerces formula `i` into a well-formed inference-rule, or raises an error if it fails.

    :param i: A formula that is presumably a well-formed inference-rule.
    :return: A well-formed inference-rule.
    :raises ApplicativeError: with code AS1-041 if coercion fails.
    """
    if isinstance(i, InferenceRule):
        return i
    elif isinstance(i, Formula) and is_well_formed_inference_rule(i=i):
        f: Transformation = coerce_transformation(f=i.term_0)
        return InferenceRule(f=f)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_041,
            msg='`i` cannot be coerced to a well-formed inference-rule.',
            i=i)


def coerce_theorem(t: FlexibleFormula) -> Theorem:
    """Coerces formula `t` into a well-formed theorem, or raises an error if it fails.

    :param t: A formula that is presumably a well-formed theorem.
    :return: A well-formed theorem.
    :raises ApplicativeError: with code AS1-042 if coercion fails.
    """
    if isinstance(t, Theorem):
        return t
    elif isinstance(t, Formula) and is_well_formed_theorem(t=t):
        proved_formula: Formula = coerce_formula(phi=t.term_0)
        inference: Inference = coerce_inference(i=t.term_1)
        return Theorem(s=proved_formula, i=inference)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_042,
            msg='`t` cannot be coerced to a well-formed theorem.',
            t=t)


def coerce_theory(t: FlexibleTheory, interpret_none_as_empty: bool = False,
                  canonical_conversion: bool = False) -> Theory:
    """Coerces formula `t` into a well-formed theory, or raises an error if it fails.

    :param t: A formula that is presumably a well-formed theory.
    :param canonical_conversion: If necessary, apply canonical conversations to transform `t` into a well-formed theory.
    :param interpret_none_as_empty: If `t` is `None`, interpret it as the empty theory.
    :return: A well-formed theory.
    :raises ApplicativeError: with code AS1-043 if coercion fails.
    """
    if isinstance(t, Theory):
        return t
    elif interpret_none_as_empty and t is None:
        return Theory(t=None, d=None, d2=None)
    elif is_well_formed_theory(t=t):
        t: Formula = coerce_formula(phi=t)
        return Theory(t=None, d=(*t,), d2=None)
    elif canonical_conversion and is_well_formed_axiomatization(a=t):
        return transform_axiomatization_to_theory(a=t)
    elif canonical_conversion and is_well_formed_hypothesis(h=t):
        return transform_hypothesis_to_theory(h=t)
    elif canonical_conversion and is_well_formed_enumeration(e=t):
        return transform_enumeration_to_theory(e=t)
    elif canonical_conversion and is_well_formed_tupl(t=t):
        return transform_tuple_to_theory(t=t)
    elif isinstance(t, typing.Generator) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(t=None, d=tuple(element for element in t), d2=None)
    elif isinstance(t, typing.Iterable) and not isinstance(t, Formula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return Theory(t=None, d=t, d2=None)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_043,
            msg='`t` cannot be coerced to a well-formed theory.',
            t=t,
            interpret_none_as_empty=interpret_none_as_empty,
            canonical_conversion=canonical_conversion)


def coerce_axiomatization(a: FlexibleFormula, interpret_none_as_empty: bool = False) -> Axiomatization:
    """Validate that phi is a well-formed axiomatization and returns it properly python-typed as Axiomatization,
    or raise error AS1-044.

    :param a:
    :param interpret_none_as_empty:
    :return:
    """
    if isinstance(a, Axiomatization):
        return a
    elif a is None and interpret_none_as_empty:
        return Axiomatization(a=None, d=None)
    elif is_well_formed_axiomatization(a=a):
        return Axiomatization(d=a)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_044,
            msg=f'Argument `a` could not be coerced to an axiomatization.',
            a=a,
            interpret_none_as_empty=interpret_none_as_empty)


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

    Intuitively, a derivation is a justification for the existence of a valid-statement in a theory.

    There are three mutually exclusive categories of derivations:
     - derivation by axiom postulation,
     - derivation by inference-rule inclusion,
     - derivation by theorem proving.

    See their respective definitions for the local and global definitions of proper-justification.
    """
    VALID_STATEMENT_INDEX: int = 0
    JUSTIFICATION_INDEX: int = 1

    @staticmethod
    def _data_validation_2(s: FlexibleFormula, j: FlexibleFormula) -> tuple[Connective, Formula, Formula]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param s:
        :param j:
        :return:
        """
        con: Connective = derivation_connective
        s = coerce_formula(phi=s)
        j = coerce_formula(phi=j)
        return con, s, j

    def __new__(cls, s: FlexibleFormula, j: FlexibleFormula,
                **kwargs):
        c, s, j = Derivation._data_validation_2(s=s,
                                                j=j)
        o: tuple = super().__new__(cls, con=c, t=(s, j,), **kwargs)
        return o

    def __init__(self, s: FlexibleFormula, j: FlexibleFormula,
                 **kwargs):
        """

        :param s: A formula that is a valid-statement in the theory.
        :param j: A formula that is a justification for the validity of the valid-statement.
        :param kwargs:
        """
        c, s, j = Derivation._data_validation_2(s=s,
                                                j=j)
        super().__init__(con=c, t=(s, j,), **kwargs)

    @property
    def valid_statement(self) -> Formula:
        """Return the formula claimed as valid by the theorem.

        This is equivalent to phi.term_0.

        :return: A formula.
        """
        return self[Derivation.VALID_STATEMENT_INDEX]

    @property
    def justification(self) -> Formula:
        return self[Derivation.JUSTIFICATION_INDEX]


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

    TODO: migrate axioms to predicates of the form axiom(p).
    """

    @staticmethod
    def _data_validation_3(s: FlexibleFormula = None) -> tuple[Connective, Formula, Formula]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param s:
        :return:
        """
        global axiom_connective
        con: Connective = axiom_connective
        s: Formula = coerce_formula(phi=s)
        justification: Formula = Formula(con=con)
        return con, s, justification

    def __new__(cls, s: FlexibleFormula = None, **kwargs):
        c, s, justification = Axiom._data_validation_3(s=s)
        o: tuple = super().__new__(cls, s=s, j=justification, **kwargs)
        return o

    def __init__(self, s: FlexibleFormula, **kwargs):
        c, s, justification = Axiom._data_validation_3(s=s)
        super().__init__(s=s, j=justification, **kwargs)


FlexibleAxiom = typing.Union[Axiom, Formula]


class InferenceRule(Derivation):
    """A well-formed inference-rule is an authorization for the usage of a transformation or algorithm,
    to derive further theorems in a theory under certain conditions called premises.

    Two inference-rule methods are implemented:
     - inference-rules-based-on-transformation:
     - inference-rules-based-on-algorithm

    Syntactic definition:
    A formula is a well-formed inference-rule if and only if it is of the form:
        (x follows-from inference-rule)
    Where:
        - x is either a well-formed transformation, or an algorithm.
        - "inference-rule" is the inference-rule urelement.
        - "follows-from" is the follows-from binary connective.

    Semantic definition:
    An inference-rule is the statement that a transformation is a valid inference-rule in a theory,
    i.e.: all formulas derived from that inference-rule are valid in the theory.

    Note: if an inference-rule has no premises, it is equivalent to an axiom.

    """
    TRANSFORMATION_INDEX: int = Derivation.VALID_STATEMENT_INDEX

    @staticmethod
    def _data_validation_3(f: FlexibleTransformation = None) -> tuple[Connective, Transformation, Formula]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param f:
        :return:
        """
        global _connectives
        con: Connective = inference_rule_connective
        f: Transformation = coerce_transformation(f=f)
        j: Formula = Formula(con=con)
        return con, f, j

    def __new__(cls, f: FlexibleTransformation = None, **kwargs):
        c, f, j = InferenceRule._data_validation_3(f=f)
        o: tuple = super().__new__(cls, s=f, j=j, **kwargs)
        return o

    def __init__(self, f: FlexibleTransformation, **kwargs):
        c, f, j = InferenceRule._data_validation_3(f=f)
        super().__init__(s=f, j=j, **kwargs)

    @property
    def transformation(self) -> Transformation:
        return self[InferenceRule.TRANSFORMATION_INDEX]


FlexibleInferenceRule = typing.Union[InferenceRule, Formula]
FlexibleTransformation = typing.Union[
    Transformation, TransformationByExternalAlgorithm, TransformationByVariableSubstitution, Formula]

with let_x_be_a_variable(formula_ts='P') as phi, let_x_be_a_variable(formula_ts='Q') as psi:
    modus_ponens_inference_rule: InferenceRule = InferenceRule(
        f=let_x_be_a_transformation_by_variable_substitution(
            p=(
                is_a_proposition_connective(phi),
                is_a_proposition_connective(psi),
                phi | implies_connective | psi,
                phi),
            c=psi,
            v=(phi, psi,)),
        ref_ts=pl1.Monospace(text='MP'))
    """The modus-ponens inference-rule.

    Abbreviation: MP

# Modus ponens inference rule:
#   phi --> psi
#   phi
#   ___________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference    

    Premises:
     1. phi | is_a | proposition,
     2. psi | is_a | proposition,
     3. phi | implies | psi,
     4. phi

    Conclusion: psi

    Variables: phi, psi
    """


class Inference(Formula):
    """An inference is the description of a usage of an inference-rule. Intuitively, it can be understood as an instance
    of the arguments passed to an inference-rule.

    Syntactic definition:
    An inference is a formula of the form:
        inference(i, P, A)
    Where:
        - inference is the inference connective,
        - `i` is an inference-rule.
        - P is a tuple of formulas denoted as the premises, that must be valid in the theory being considered,
          in order for the inference to be valid.
        - (for algorithmic-transformations) A is a tuple of arbitrary formulas denoted as the supplementary arguments.

    Semantic definition:
    An inference is a formal description of one usage of an inference-rule."""
    INFERENCE_RULE_INDEX: int = 0
    PREMISES_INDEX: int = 1
    ARGUMENTS_INDEX: int = 2

    @staticmethod
    def _data_validation_2(
            i: FlexibleInferenceRule,
            p: FlexibleTupl | None = None,
            a: FlexibleTupl | None = None) -> tuple[Connective, InferenceRule, Tupl, Tupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param i:
        :param p:
        :param a:
        :return:
        """
        con: Connective = inference_connective
        i: InferenceRule = coerce_inference_rule(i=i)
        p: Tupl = coerce_tuple(t=p, interpret_none_as_empty=True)
        a: Tupl = coerce_tuple(t=a, interpret_none_as_empty=True)

        # Check the consistency of the shape of the premises and complementary arguments,
        # with the expected input-shapes of the inference-rule transformation.
        i2 = append_tuple_to_tuple(t1=p, t2=a)
        ok, _ = is_formula_equivalent_with_variables_2(phi=i2, psi=i.transformation.input_shapes,
                                                       variables=i.transformation.variables)
        if not ok:
            pass
            # TODO : Raise an error once migration is completed.

        return con, i, p, a

    def __new__(cls, i: FlexibleInferenceRule, p: FlexibleTupl | None = None, a: FlexibleTupl | None = None):
        """

        :param i: An inference-rule.
        :param p: A tuple of formulas denoted as the premises.
        :param a: A tuple of formulas denoted as the supplementary arguments.
        """
        c, i, p, a = Inference._data_validation_2(i=i, p=p, a=a)
        o: tuple = super().__new__(cls, con=c, t=(i, p, a))
        return o

    def __init__(self, i: FlexibleInferenceRule, p: FlexibleTupl | None = None, a: FlexibleTupl | None = None):
        """Initializes a new inference.

        :param i: An inference-rule.
        :param p: A tuple of formulas denoted as the premises, that must be valid in the theory under consideration.
        :param a: A tuple of formulas denoted as the supplementary arguments, that may or may not be propositions,
                  and that may or may not be valid in the theory under consideration.
        """
        c, i, p, a = Inference._data_validation_2(i=i, p=p, a=a)
        super().__init__(con=c, t=(i, p, a,))

    @property
    def arguments(self) -> Tupl:
        """A tuple of supplementary arguments to be passed to the transformation as input parameters. These may or
        may not be propositions, and may or may not be valid in the theory under consideration."""
        return self[Inference.ARGUMENTS_INDEX]

    @property
    def inference_rule(self) -> InferenceRule:
        """The inference-rule of the inference."""
        return self[Inference.INFERENCE_RULE_INDEX]

    @property
    def premises(self) -> Tupl:
        """The premises of the inference. All premises in the inference must be valid in the theory under
        consideration."""
        return self[Inference.PREMISES_INDEX]


FlexibleInference = typing.Optional[typing.Union[Inference]]


def inverse_map(m: FlexibleMap) -> Map:
    """If a map is bijective, returns the inverse map."""
    m: Map = coerce_map(m=m, interpret_none_as_empty=True)
    domain = transform_formula_to_enumeration(phi=m.codomain, strip_duplicates=True)
    codomain = transform_formula_to_tuple(phi=m.domain)
    if domain.arity != codomain.arity:
        assert u1.ApplicativeError(
            msg='Map `m` cannot be inverted because it is not bijective.',
            new_domain_arity=domain.arity,
            new_codomain_arity=codomain.arity,
            new_domain=domain,
            new_codomain=codomain,
            original_map=m)
    m2: Map = Map(d=domain, c=codomain)
    return m2


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
    INFERENCE_INDEX: int = Derivation.JUSTIFICATION_INDEX

    @staticmethod
    def _data_validation_3(s: FlexibleFormula, i: FlexibleInference) -> tuple[Connective, Formula, Inference]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param s: A proposition denoted as the theorem valid-statement.
        :param i: An inference.
        :return:
        """
        global _connectives
        con: Connective = theorem_connective  # TO BE IMPLEMENTED AS A PREDICATE INSTEAD OF IS-A
        s: Formula = coerce_formula(phi=s)
        i: Inference = coerce_inference(i=i)

        # check the validity of the theorem
        try:
            algorithm_output: Formula = i.inference_rule.transformation.apply_transformation(i=i.premises,
                                                                                             i2=i.arguments)
        except u1.ApplicativeError as err:
            raise u1.ApplicativeError(
                msg='Theorem initialization error. '
                    'An error was raised when the transformation `f` '
                    'of the inference-rule `ir` was applied to check the validity of the theorem. ',
                f=i.inference_rule.transformation,
                ir=i.inference_rule,
                s=s,
                i=i)

        if len(i.inference_rule.transformation.output_declarations) == 0:
            # This transformation is deterministic because it comprises no new-object-declarations.
            try:
                is_formula_equivalent(phi=s, psi=algorithm_output, raise_error_if_false=True)
            except u1.ApplicativeError as error:
                # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
                # raise an exception to prevent the creation of this ill-formed theorem-by-inference.
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_045,
                    msg='`s` is not formula-equivalent to `algorithm_output`.',
                    s=s,
                    algorithm_output=algorithm_output,
                    inference=i,
                    source_error=error
                )
        else:
            # If there are new-object-declarations, f_of_p is not directly comparable with valid_statements.
            # This is because transformations with new-object-declarations are non-deterministic.
            # In order to check that valid_statement is consistent with the inference-rule, we can
            # compare both formulas with the inference-rule conclusion and with regards to new-object-declaration
            # variables.
            success_1, m1 = is_formula_equivalent_with_variables_2(
                phi=s,
                psi=i.inference_rule.transformation.output_shape,
                variables=i.inference_rule.transformation.output_declarations)
            if not success_1:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_085,
                    msg='Theorem initialization failure. '
                        'The valid-statement `s` is not consistent with the conclusion of the inference-rule `i`, '
                        'considering new object declarations.',
                    s=s,
                    i_conclusion=i.inference_rule.transformation.output_shape,
                    i_declarations=i.inference_rule.transformation.output_declarations,
                    success_1=success_1)
            # We can reverse the map and re-test formula-equivalence-with-variables.
            m1_reversed = inverse_map(m=m1)
            success_2, _ = is_formula_equivalent_with_variables_2(phi=s,
                                                                  psi=i.inference_rule.transformation.output_shape,
                                                                  variables=m1.domain)
            pass
            valid_statement_reversed: Formula = replace_formulas(phi=s, m=m1_reversed)
            if not is_formula_equivalent(phi=valid_statement_reversed,
                                         psi=i.inference_rule.transformation.output_shape):
                raise u1.ApplicativeError(
                    msg='Reversing the valid-statement does not yield the inference-rule conclusion.',
                    valid_statement_reversed=valid_statement_reversed,
                    expected_conclusion=i.inference_rule.transformation.output_shape)

        return con, s, i

    def __new__(cls, s: FlexibleFormula, i: FlexibleInference):
        c, s, i = Theorem._data_validation_3(s=s, i=i)
        o: tuple = super().__new__(cls, s=s, j=i)
        return o

    def __init__(self, s: FlexibleFormula, i: FlexibleInference):
        c, s, i = Theorem._data_validation_3(s=s, i=i)
        # complete object initialization to assure that we have a well-formed formula with connective, etc.
        super().__init__(s=s, j=i)

    @property
    def inference(self) -> Inference:
        """The inference of the theorem."""
        return self[Theorem.INFERENCE_INDEX]


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


class Theory(Formula):
    """A theory is a justified enumeration of axioms, inference-rules, and theorems.

    Syntactic definition:
    A well-formed theory is an enumeration such that:
     - all element phi of the enumeration is a well-formed theorem,
     - all premises of all theorem-by-inferences are predecessors of their parent theorem-by-inference.

    TODO: Consider the following data-model change: a derivation is only an axiom or an inference-rule. In
        effect, stating that in inference-rule is a derivation seems to be a bit of a semantic stretch.

    """
    _last_index: int = 0

    @staticmethod
    def _data_validation_2(con: Connective, t: FlexibleTheory | None = None, d: FlexibleEnumeration = None
                           ) -> tuple[Connective, Enumeration]:
        """

        :param t:
        :param d:
        :return:
        """
        global _connectives
        con: Connective = theory_connective
        if t is not None:
            t: Theory = coerce_theory(t=t, interpret_none_as_empty=False, canonical_conversion=True)
        d: Enumeration = coerce_enumeration(e=d, strip_duplicates=True, canonic_conversion=True,
                                            interpret_none_as_empty=True)
        is_valid, v, u = would_be_valid_derivations_in_theory(v=t, u=d, raise_error_if_false=True)
        d = union_enumeration(phi=v, psi=u, strip_duplicates=True)
        return con, d

    def __new__(cls, con: Connective | None = None,
                t: FlexibleTheory | None = None, d: FlexibleEnumeration = None, **kwargs):
        """

        :param con:
        :param t: A theory that is being extended by the new theory. If None, the empty theory is assumed.
        :param d: An enumeration of complementary derivations for the new theory.
        :param kwargs:
        """
        c2, d2 = Theory._data_validation_2(con=con, t=t, d=d)
        o: tuple = super().__new__(cls, con=c2, t=d2, **kwargs)
        return o

    def __init__(self, con: Connective | None = None,
                 t: FlexibleTheory | None = None, d: FlexibleEnumeration = None, **kwargs):
        """Declares a new theory t′ such that t′ = t ∪ d, where:
         - t is a theory (or the empty theory if the argument is not provided),
         - d is an enumeration of derivations (or the empty enumeration if the argument is not provided).

        :param con:
        :param t: A theory to be extended by the new theory.
        :param d: An enumerations of derivations.
        :param kwargs:
        """
        c2, d2 = Theory._data_validation_2(con=con, t=t, d=d)
        super().__init__(con=c2, t=d2, **kwargs)
        self._heuristics: set[Heuristic, ...] | set[{}] = set()
        if t is not None:
            # Copies the heuristics and any other decoration from the base theory
            copy_theory_decorations(target=self, decorations=(t,))

        # Default typesetting configuration
        if pl1.REF_TS not in self.ts.keys():
            Theory._last_index = Theory._last_index + 1
            self.ts[pl1.REF_TS] = pl1.NaturalIndexedSymbolTypesetter(body_ts=pl1.symbols.t_uppercase_script,
                                                                     index=Theory._last_index)
        if pl1.DECLARATION_TS not in self.ts.keys():
            self.ts[pl1.DECLARATION_TS] = typesetters.declaration(conventional_class='theory')

        if t is None:
            # This is not an extended theory, this is a new theory.
            # Output its declaration.
            u1.log_info(self.typeset_as_string(theory=self, ts_key=pl1.DECLARATION_TS))

    @property
    def axioms(self) -> Enumeration:
        """Return an enumeration of all axioms in the theory.

        Note: order is preserved."""
        return Enumeration(e=tuple(self.iterate_axioms()))

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
        e: Enumeration = Enumeration(e=python_tuple)
        return e

    @property
    def inference_rules(self) -> Enumeration:
        """Return an enumeration of all inference-rules in the theory, preserving order, filtering out axioms and
        theorems."""
        return Enumeration(e=tuple(self.iterate_inference_rules()))

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
        return Enumeration(e=tuple(self.iterate_derivations()))

    @property
    def theorems(self) -> Enumeration:
        """Return an enumeration of all theorems in the theory, preserving order, filtering out axioms and
        inference-rules."""
        return Enumeration(e=tuple(self.iterate_theorems()))


def transform_axiomatization_to_theory(a: FlexibleAxiomatization) -> Theory:
    """Canonical function that converts an axiomatization `a` to a theory.

    An axiomatization is a theory whose derivations are limited to axioms and inference-rules.
    This function provides the canonical conversion method from axiomatizations to theories,
    by returning a new theory `t` such that all the derivations in `t` are derivations of `a`,
    preserving canonical order.

    :param a: An axiomatization.
    :return: A theory.
    """
    a: Axiomatization = coerce_axiomatization(a=a)
    t: Theory = Theory(d=(*a,))
    return t


def transform_hypothesis_to_theory(h: FlexibleHypothesis) -> Theory:
    """Canonical function that converts a hypothesis `h` to a theory.

    A hypothesis is a pair (b, a) where:
     - `b` is a theory denoted as the base-theory,
     - `a` is a proposition denoted as the assumption.

    The canonical conversion of hypothesis into theory consists in
    considering the assumption as an axiom.

    :param h: A hypothesis.
    :return: A theory.
    """
    h: Hypothesis = coerce_hypothesis(h=h)
    b: Theory = h.base_theory
    a: Formula = h.assumption
    t: Theory = Theory(t=b, d=(a,))
    return t


def transform_theory_to_axiomatization(t: FlexibleTheory, interpret_none_as_empty: bool = True,
                                       canonical_conversion: bool = True) -> Axiomatization:
    """Canonical function that converts a theory `t` to an axiomatization.

    An axiomatization is a theory whose derivations are limited to axioms and inference-rules.
    This function provides the canonical conversion method from theories to axiomatizations,
    by returning a new axiomatization `a` such that all the axioms and inference-rules in `t`
    become derivations of `a`, preserving canonical order.

    It follows that all theorems in `t` are discarded.

    :param t: A theory.
    :param interpret_none_as_empty: If `t` is None, interpret it as the empty-theory.
    :param canonical_conversion: If necessary, apply canonic-conversion to coerce `t` to a theory.
    :return: An axiomatization.
    """
    t: Theory = coerce_theory(t=t, interpret_none_as_empty=interpret_none_as_empty,
                              canonical_conversion=canonical_conversion)
    e: Enumeration = Enumeration(e=None)
    for d in iterate_theory_derivations(t=t):
        if is_well_formed_axiom(a=d):
            e = append_element_to_enumeration(e=e, x=d)
        if is_well_formed_inference_rule(i=d):
            e = append_element_to_enumeration(e=e, x=d)
    a: Axiomatization = Axiomatization(a=None, d=(*e,))
    return a


def is_extension_of(t2: FlexibleTheory, t1: FlexibleTheory, interpret_none_as_empty: bool = True,
                    canonical_conversion: bool = True, raise_error_if_false: bool = False):
    """Given two theories or axiomatizations `t1` and `t2`, returns `True` if and only if `t2` is an extension of `t1`,
    `False` otherwise.

    Definition: theory-extension
    ----------------------------
    A theory or axiomatization :math:`T_2` is an extension of a theory or axiomatization :math:`T_1` if and only if:
         - every axiom and inference-rule in :math:`T_1` is present in :math:`T_2`.

    Notation
    --------
    :math:`T_1 \\subseteq T_2`

    :param t1: A theory or axiomatization.
    :param t2: A theory or axiomatization.
    :param interpret_none_as_empty: If `t1` or `t2` is None, interpret it as the empty-theory.
    :param canonical_conversion:
    :param raise_error_if_false:
    :return: An axiomatization.
    """
    t1: Theory = coerce_theory(t=t1, interpret_none_as_empty=interpret_none_as_empty,
                               canonical_conversion=canonical_conversion)
    t2: Theory = coerce_theory(t=t2, interpret_none_as_empty=interpret_none_as_empty,
                               canonical_conversion=canonical_conversion)

    a1: Axiomatization = transform_theory_to_axiomatization(t=t1)
    a2: Axiomatization = transform_theory_to_axiomatization(t=t2)

    e1: Enumeration = transform_axiomatization_to_enumeration(a=a1)
    e2: Enumeration = transform_axiomatization_to_enumeration(a=a2)

    ok: bool = is_sub_enumeration(s=e1, e=e2)

    if not ok and raise_error_if_false:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_081,
            msg='Theory or axiomatization `t2` is not an extension of theory or axiomatization `t2`.',
            ok=ok,
            t1=t1,
            t2=t2,
            a1=a1,
            a2=a2
        )
    return ok


def is_axiomatization_equivalent(t1: FlexibleTheory, t2: FlexibleTheory, interpret_none_as_empty: bool = True,
                                 canonical_conversion: bool = True, raise_error_if_false: bool = False) -> bool:
    """Returns `True` if `t1` is axiomatization-equivalent with `t2`, denoted :math:`t_1 \\sim_{a} t_2`.

    Definition: axiomatization-equivalence:
    Two theories or axiomatizations :math:`t_1` and :math:`t_2` are :math:`\\text{axiomatization-equivalent}`
    if and only if for every axiom or inference-rule :math:`x` in :math:`t_1`, :math:`x \\in t_2`,
    and reciprocally for every axiom or inference-rule :math:`x` in :math:`t_2`, :math:`x \\in t_1`.

    :param t1: A theory or axiomatization.
    :param t2: A theory or axiomatization.
    :param interpret_none_as_empty: If `t1` or `t2` is None, interpret it as the empty-theory.
    :param canonical_conversion:
    :param raise_error_if_false:
    :return: An axiomatization.
    """
    t1: Theory = coerce_theory(t=t1, interpret_none_as_empty=interpret_none_as_empty,
                               canonical_conversion=canonical_conversion)
    t2: Theory = coerce_theory(t=t2, interpret_none_as_empty=interpret_none_as_empty,
                               canonical_conversion=canonical_conversion)

    a1: Axiomatization = transform_theory_to_axiomatization(t=t1)
    a2: Axiomatization = transform_theory_to_axiomatization(t=t2)

    e1: Enumeration = transform_axiomatization_to_enumeration(a=a1)
    e2: Enumeration = transform_axiomatization_to_enumeration(a=a2)

    ok: bool = is_enumeration_equivalent(phi=e1, psi=e2)

    if not ok and raise_error_if_false:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_077,
            msg='`t1` is not axiomatization-equivalent with `t2`.',
            ok=ok,
            t1=t1,
            t2=t2,
            a1=a1,
            a2=a2
        )
    return ok


def transform_enumeration_to_theory(e: FlexibleEnumeration) -> Theory:
    """Canonical function that converts an enumeration "e" to a theory,
    providing that all elements "x" of "e" are well-formed derivations.

    :param e: An enumeration.
    :return: A theory.
    """
    e: Enumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    t: Theory = Theory(d=e)
    return t


def transform_formula_to_tuple(phi: FlexibleFormula) -> Tupl:
    """Canonical transformation of formulas to tuples.

    Every formula is a tuple if we don't consider its connective.
    The canonical transformation returns a tuple if `phi` is a well-formed tupl,
    otherwise it returns a new tupl such that the elements of the tuple
    are the terms of the formula, preserving order.

    :param phi: A formula.
    :return: A theory.
    """
    phi: Formula = coerce_formula(phi=phi)
    if is_well_formed_tupl(t=phi):
        phi: Tupl = coerce_tuple(t=phi)
        return phi
    else:
        phi: Tupl = Tupl(e=iterate_formula_terms(phi=phi))
        return phi


def transform_tuple_to_theory(t: FlexibleTupl) -> Theory:
    """Canonical function that converts a tuple `t` to a theory,
    providing that all elements "x" of `t` are well-formed derivations.

    :param t: A tupl.
    :return: A theory.
    """
    t: Tupl = coerce_tuple(t=t)
    e: Enumeration = coerce_enumeration(e=t, strip_duplicates=True, canonic_conversion=True,
                                        interpret_none_as_empty=True)
    t2: Theory = transform_enumeration_to_theory(e=e)
    return t2


def transform_axiomatization_to_enumeration(a: FlexibleAxiomatization) -> Enumeration:
    """Canonical function that converts an axiomatization `a` to an enumeration.

    An axiomatization is fundamentally an enumeration of derivations, limited to axioms and inference-rules.
    This function provides the canonical conversion method from axiomatizations to enumeration,
    by returning a new enumeration "e" such that all the derivations in `a` are elements of "e",
    preserving order.

    Invertibility: yes
    Bijectivity: yes

    :param a: An axiomatization.
    :return: An enumeration.
    """
    a: Axiomatization = coerce_axiomatization(a=a)
    e: Enumeration = Enumeration(e=(*a,))
    return e


def transform_formula_to_enumeration(phi: FlexibleFormula, strip_duplicates: bool = False) -> Enumeration:
    """Canonical transformation from formula to enumeration.

    If the terms of a formula are unique, returns an enumeration whose
    elements are the terms of formula, preserving order.

    If the terms of a formula are not unique and strip_duplicates, returns an enumeration whose
    elements are the terms of formula, preserving order, removing duplicates by keeping
    only the first occurrence of every term.

    If the terms of a formula are not unique and not strip_duplicates, raise an error.

    :param phi: A formula.
    :param strip_duplicates:
    :return: An enumeration.
    """
    phi: Formula = coerce_formula(phi=phi)
    if isinstance(phi, Enumeration):
        return phi
    else:
        return Enumeration(e=iterate_formula_terms(phi=phi), strip_duplicates=strip_duplicates)


def transform_theory_to_enumeration(t: FlexibleTheory) -> Enumeration:
    """Canonical function that converts a theory `t` to an enumeration.

    A theory is fundamentally an enumeration of derivations.
    This function provides the canonical conversion method from theory to enumeration,
    by returning a new enumeration "e" such that all the derivations in `t` are elements of "e",
    preserving order.

    :param t: A theory.
    :return: An enumeration.
    """
    return transform_formula_to_enumeration(phi=t)


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
            # Copies all typesetting methods
            target.ts.update(decorative_theory.ts | target.ts)  # Give priority to the existing


class Axiomatization(Formula):
    """An axiomatization is a theory that is only composed of axioms,
    and/or inference-rules.

    Syntactic definition:
    A well-formed axiomatization is an enumeration such that:
     - all element phi of the enumeration is a well-formed axiom or an inference-rule.

    """
    _last_index: int = 0

    @staticmethod
    def _data_validation_2(a: FlexibleAxiomatization | None = None,
                           d: FlexibleEnumeration = None) -> tuple[Connective, Enumeration]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param a:
        :param d:
        :return:
        """
        global axiomatization_connective
        d: Enumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, strip_duplicates=True)
        if a is not None:
            a: Axiomatization = coerce_axiomatization(a=a)
            # Duplicate derivations are not allowed in axiomatizations, so strip duplicates during merge.
            # The first occurrence is maintained, and the second occurrence is stripped.
            d: Enumeration = Enumeration(e=(*a, *d), strip_duplicates=True)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_derivations: Enumeration = Enumeration(e=None)
        for x in iterate_enumeration_elements(e=d):
            if is_well_formed_inference_rule(i=x):
                # This is an inference-rule.
                inference_rule: InferenceRule = coerce_inference_rule(i=x)
                coerced_derivations: Enumeration = append_element_to_enumeration(
                    e=coerced_derivations, x=inference_rule)
            elif is_well_formed_axiom(a=x):
                # This is an axiom.
                axiom: Axiom = coerce_axiom(a=x)
                coerced_derivations: Enumeration = append_element_to_enumeration(
                    e=coerced_derivations, x=axiom)
            else:
                # Incorrect form.
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_062,
                                          msg=f'Cannot append derivation `d` to axiomatization `a`, '
                                              f'because `d` is not in proper form '
                                              f'(e.g.: axiom, inference-rule).',
                                          d=d,
                                          a=a
                                          )
        return axiomatization_connective, coerced_derivations

    def __new__(cls, a: FlexibleAxiomatization | None = None, d: FlexibleEnumeration = None):
        c, t = Axiomatization._data_validation_2(a=a, d=d)
        o: tuple = super().__new__(cls, con=c, t=t)
        return o

    def __init__(self, a: Axiomatization | None = None, d: FlexibleEnumeration = None):
        """Declares a new axiomatization.

        :param a: A base axiomatization. If `None`, the empty axiomatization is assumed as a base.
        :param d: An enumeration of supplementary axioms and/or inference rules to be appended to the base
            axiomatization.
        """
        c, t = Axiomatization._data_validation_2(a=a, d=d)
        super().__init__(con=c, t=t)
        self._heuristics: set[Heuristic, ...] | set[{}] = set()
        if a is not None:
            # Copies the heuristics and any other decoration from the base theory
            copy_theory_decorations(target=self, decorations=(a,))
        if pl1.REF_TS not in self.ts.keys():
            Theory._last_index = Axiomatization._last_index + 1
            self.ts[pl1.REF_TS] = pl1.NaturalIndexedSymbolTypesetter(body_ts=pl1.symbols.t_uppercase_script,
                                                                     index=Axiomatization._last_index)
        if pl1.DECLARATION_TS not in self.ts.keys():
            self.ts[pl1.DECLARATION_TS] = typesetters.declaration(conventional_class='axiomatization')

        if t is None:
            # This is not an extended theory, this is a new theory.
            # Output its declaration.
            u1.log_info(self.typeset_as_string(theory=self, ts_key=pl1.DECLARATION_TS))

    @property
    def heuristics(self) -> set[Heuristic, ...] | set[{}]:
        """A python-set of heuristics.

        Heuristics are not formally part of an axiomatization. They are decorative objects used to facilitate proof
        derivations.
        """
        return self._heuristics


FlexibleAxiomatization = typing.Optional[
    typing.Union[Axiomatization, typing.Iterable[typing.Union[Axiom, InferenceRule]]]]
"""A flexible python type for which coercion into type Axiomatization is supported.

Note that a flexible type is not an assurance of well-formedness. Coercion assures well-formedness
and raises an error if the object is ill-formed."""

FlexibleTheory = typing.Optional[
    typing.Union[Axiomatization, Theory, typing.Iterable[FlexibleDerivation]]]
"""A flexible python type for which coercion into type Theory is supported.

Note that a flexible type is not an assurance of well-formedness. Coercion assures well-formedness
and raises an error if the object is ill-formed."""

FlexibleDecorations = typing.Optional[typing.Union[typing.Tuple[FlexibleTheory, ...], typing.Tuple[()]]]


def is_recursively_included_in(s: FlexibleFormula, f: FlexibleFormula) -> bool:
    """Returns `True` if and only if formula `s` is recursively included in formula `f`, `False` otherwise.

    Symbol: ⊆⁺ (Unicode), :math:`\\subseteq^{+}` (LaTeX)

    Definition: recursive inclusion (of formulas)
    A formula :math:`s` is a recursive-sub-formula of a formula :math:`f` if and only if:
    - :math:`s ~_{f} f`,
    - or :math:`s ~_{f} g` where :math:`g` is a term of :math:`f`,
    - or :math:`s ~_{f} h` where :math:`h` is a term of a recursive-sub-formula of :math:`f`.

    Synonym: to be in the transitive closure of a formula with respect to the formula-equivalence relation.

    :param s: A formula, that may be a subformula of f.
    :param f: A formula, that may be the superformula of s.
    :return: True if and only if formula subformula is a sub-formula of formula formula, False otherwise.
    :rtype: bool
    """
    s: Formula = coerce_formula(phi=s)
    f: Formula = coerce_formula(phi=f)
    if is_formula_equivalent(phi=s, psi=f):
        return True
    for term in f:
        if is_recursively_included_in(s=s, f=term):
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
        eb: Enumeration = Enumeration(e=None)
    if not is_element_of_enumeration(x=phi, e=eb) and is_leaf_formula(phi=phi):
        eb = append_element_to_enumeration(x=phi, e=eb)
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


def append_to_theory(*args, t: FlexibleTheory) -> Theory:
    """Extend theory t by appending to it whatever is passed in *args.

    :param args:
    :param t:
    :return:
    """
    t: Theory = coerce_theory(t=t, canonical_conversion=True, interpret_none_as_empty=True)
    if args is None:
        return t
    else:
        for argument in args:
            if is_well_formed_axiomatization(a=argument):
                # If the argument is an axiomatization,
                # all the derivations (axioms and inference-rules) from the axiomatization
                # are appended to the theory.
                extension_a: Axiomatization = coerce_axiomatization(a=argument)
                t: Theory = Theory(t=t, d=(*extension_a,))
            elif is_well_formed_theory(t=argument):
                # If the argument is an axiomatization,
                # all the derivations (axioms, inference-rules, theorems) from the axiomatization
                # are appended to the theory.
                extension_t: Theory = coerce_theory(t=argument)
                t: Theory = Theory(t=t, d=(*extension_t,))
                copy_theory_decorations(target=t, decorations=(extension_t,))
            elif is_well_formed_axiom(a=argument):
                extension_a: Axiom = coerce_axiom(a=argument)
                if not is_axiom_of(a=extension_a, t=t):
                    t: Theory = Theory(t=t, d=(extension_a,))
            elif is_well_formed_inference_rule(i=argument):
                extension_i: InferenceRule = coerce_inference_rule(i=argument)
                if not is_inference_rule_of(i=extension_i, t=t):
                    t: Theory = Theory(t=t, d=(extension_i,))
            elif is_well_formed_inference(i=argument):
                extension_i: InferenceRule = coerce_inference_rule(i=argument)
                if not is_inference_rule_of(i=extension_i, t=t):
                    t: Theory = Theory(t=t, d=(extension_i,))
            elif is_well_formed_theorem(t=argument):
                extension_m: Theorem = coerce_theorem(t=argument)
                if not is_theorem_of(m=extension_m, t=t):
                    t: Theory = Theory(t=t, d=(extension_m,))
            else:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_049,
                                          msg=f'Invalid argument: ({type(argument)}) {argument}.')
        return t


def append_derivation_to_axiomatization(d: FlexibleDerivation, a: FlexibleAxiomatization) -> Axiomatization:
    """Extend axiomatization `a` with derivation `d`.

    :param d:
    :param a:
    :return:
    """
    d: Derivation = coerce_derivation(d=d)
    a: Axiomatization = coerce_axiomatization(a=a)
    if is_well_formed_axiom(a=d):
        extension_a: Axiom = coerce_axiom(a=d)
        if not is_axiom_of(a=extension_a, t=a):
            a: Axiomatization = Axiomatization(a=a, d=(extension_a,))
    elif is_well_formed_inference_rule(i=d):
        extension_i: InferenceRule = coerce_inference_rule(i=d)
        if not is_inference_rule_of(i=extension_i, t=a):
            a: Axiomatization = Axiomatization(a=a, d=(extension_i,))
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_062,
                                  msg=f'Cannot append derivation `d` to axiomatization `a`, '
                                      f'because `d` is not in proper form '
                                      f'(e.g.: axiom, inference-rule).',
                                  d=d,
                                  a=a
                                  )
    return a


def append_args_to_axiomatization(*args, a: FlexibleAxiomatization) -> Axiomatization:
    """Extend theory t by appending to it whatever is passed in *args.

    :param args:
    :param a:
    :return:
    """
    a: Axiomatization = coerce_axiomatization(a=a)
    if args is None:
        return a
    else:
        for d in args:
            a = append_derivation_to_axiomatization(d=d, a=a)
        return a


class AutoDerivationFailure(Exception):
    """Auto-derivation was required but failed to succeed."""

    def __init__(self, msg: str, **kwargs):
        super().__init__(msg)
        self.kwargs = kwargs


def derive_1(t: FlexibleTheory, c: FlexibleFormula, p: FlexibleTupl,
             i: FlexibleInferenceRule, a: FlexibleTupl | None = None,
             raise_error_if_false: bool = True) -> typing.Tuple[Theory, bool, Theorem | None]:
    """Given a theory `t`, derives a new theory `t′` that extends `t` with a new theorem `c`
    derived by applying inference-rule `i`.

    :param t: A theory.
    :param c: A proposition denoted as the conjecture.
    :param p: A tuple of propositions denoted as the premises.
    :param i: An inference-rule.
    :param a: (For algorithmic-transformations) A tuple of formulas denoted as the supplementary-arguments to be
        transmitted as input arguments to the external-algorithm.
    :param raise_error_if_false:
    :return: A python-tuple `(t′, b, m)` where `t′` is the theory `t` with the new theorem if derived successfully,
        `b` is `True` if the derivation was successful, `False` otherwise, and `m` is the new derivation.
    """
    # parameters validation
    t: Theory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    c: Formula = coerce_formula(phi=c)
    p: Tupl = coerce_tuple(t=p, interpret_none_as_empty=True, canonic_conversion=True)
    i: InferenceRule = coerce_inference_rule(i=i)
    a: Tupl = coerce_tuple(t=a, interpret_none_as_empty=True, canonic_conversion=True)

    if not is_inference_rule_of(i=i, t=t):
        # The inference_rule is not in the theory,
        # it follows that it is impossible to derive the conjecture from that inference_rule in this theory.
        if raise_error_if_false:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_067,
                                      msg=f'Derivation fails because inference-rule `i` is not valid in theory `t`.',
                                      i=i,
                                      t=t)
        else:
            return t, False, None

    for q in p:
        # The validity of the premises is checked during theory initialization,
        # but re-checking it here "in advance" helps provide more context in the exception that is being raised.
        if not is_valid_proposition_in_theory_1(p=q, t=t):
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_051,
                    msg=f'Conjecture `c` cannot be derived from inference-rule `i` because '
                        f'premise `q` is not a valid-statement in theory `t`. '
                        f'The was complete list of premises is provided as `p`.',
                    c=c,
                    q=q,
                    i=i,
                    p=p,
                    t=t)
            else:
                return t, False, None

    # TODO: consider using would_be_valid_derivations_in_theory(v=t,u=) to avoid code duplication.
    #   or implement complete check with ext algo arguments, object creation, etc.

    # Configure the inference that derives the theorem.
    inference: Inference = Inference(p=p, a=a, i=i)

    # Prepare the new theorem.
    try:
        # TODO: This is inelegant. When we use an external-algorithm,
        #   I was not able to find a simple solution to catch errors.
        #   Some evolution of the data model is probably needed here.
        theorem: Theorem = Theorem(s=c, i=inference)
    except u1.ApplicativeError as error:
        # If the initialization of the theorem fails,
        # it means that the theorem is not valid.
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='Derivation failure. '
                    'The initialization of the theorem failed, meaning that it is invalid. '
                    'The inference is composed of the premises `p`, the arguments `a`, '
                    'the inference-rule `i`.',
                p=p,
                a=a,
                i=i,
                t=t
            )
        else:
            return t, False, None

    # Extends the theory with the new theorem.
    # The validity of the derivation will be checked again during theory initialization.
    t: Theory = append_to_theory(theorem, t=t)
    # t: Theory = Theory(t=t, d=(theorem,), decorations=(t,))

    u1.log_info(theorem.typeset_as_string(theory=t))

    return t, True, theorem


def is_in_map_domain(phi: FlexibleFormula, m: FlexibleMap) -> bool:
    """Return True if phi is a formula in the domain of map m, False otherwise."""
    phi = coerce_formula(phi=phi)
    m = coerce_map(m=m, interpret_none_as_empty=True)
    return is_element_of_enumeration(x=phi, e=m.domain)


def derive_0(t: FlexibleTheory, c: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """An algorithm that attempts to automatically prove a conjecture in a theory.

    The `derive_0` algorithm "proves the obvious":
    1). Check if the conjecture is already a valid statement in the theory.

    Note: the tuple returned by the function comprises theory t as its first element. This is not necessary because
    a new theory is not derived by auto_derive_0, but it provides consistency with the return values of the other
    auto_derive functions.

    :param t: A theory.
    :param c: A proposition, denoted as the conjecture.
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    t = coerce_theory(t=t, canonical_conversion=True, interpret_none_as_empty=True)
    c = coerce_formula(phi=c)
    if debug:
        u1.log_debug(f'derive_0: start. conjecture:{c}.')
    if is_valid_proposition_in_theory_1(p=c, t=t):  # this first check is superfluous
        # loop through derivations
        for derivation in t.iterate_derivations():
            if is_formula_equivalent(phi=c, psi=derivation.valid_statement):
                # the valid-statement of this derivation matches phi,
                # the auto_derive is successful.
                # if debug:
                # u1.log_info(f'auto_derive_0 successful: {derivation}')
                return t, True, derivation
    # all derivations have been tested and none matched phi,
    # it follows that the auto_derive failed.
    return t, False, None


def derive_2(t: FlexibleTheory, c: FlexibleFormula, i: FlexibleInferenceRule,
             raise_error_if_false: bool = True,
             debug: bool = False) -> \
        typing.Tuple[Theory, bool, typing.Optional[Derivation]]:
    """Derives a new theory `t′` that extends `t` with a new theorem based on conjecture `c` using inference-rule `i`.

    Note: in contrast, derive_1 requires the explicit list of premises. derive_2 is more convenient to use because it
     automatically finds a set of premises among the valid-statements in theory t, such that conjecture c can be
     derived.

    :param t: a theory.
    :param c: the conjecture to be proven.
    :param i: the inference-rule from which the conjecture can be derived.
    :param raise_error_if_false: raise an error if the derivation fails.
    :param debug:
    :return: A python-tuple (t′, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[Theory, bool, typing.Optional[Derivation]]
    """
    t = coerce_theory(t=t)
    c = coerce_formula(phi=c)
    i = coerce_inference_rule(i=i)
    if debug:
        u1.log_debug(f'derive_2: Derivation started. conjecture:{c}. inference_rule:{i}.')

    if not is_inference_rule_of(i=i, t=t):
        # The inference_rule is not in the theory,
        # it follows that it is impossible to derive the conjecture from that inference_rule in this theory.
        u1.log_debug(
            f'derive_2: The derivation failed because the inference-rule is not contained in the theory. '
            f'conjecture:{c}. inference_rule:{i}. ')
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_078,
                msg='Inference-rule `i` is not an element of theory `t`. '
                    'It follows that proposition `c` cannot be inferred in `t` using `i`.',
                c=c, i=i, t=t,
            )
        return t, False, None

    # First try the less expansive auto_derive_0 algorithm
    t, successful, derivation, = derive_0(t=t, c=c, debug=debug)
    if successful:
        return t, successful, derivation

    # In order to list what would be the required premises to yield the conjecture,
    # the inference-rule must be "reverse-engineered".

    # By comparing the inference-rule conclusion and the conjecture,
    # we can retrieve some known variable values.
    # Function is_formula_equivalent_with_variables_2 returns this map directly.
    conclusion_is_compatible_with_conjecture, known_variable_values = is_formula_equivalent_with_variables_2(
        phi=c,
        psi=i.transformation.output_shape,
        variables=i.transformation.variables,
        variables_fixed_values=None)
    if conclusion_is_compatible_with_conjecture:
        # The conclusion of the inference-rule is compatible with the conjecture.
        # It is thus worth pursuing the attempt.

        # By contrast, the unknown variable values can be listed.
        unknown_variable_values: Enumeration = Enumeration()
        for x in i.transformation.variables:
            if not is_element_of_enumeration(x=x, e=known_variable_values.domain):
                unknown_variable_values = Enumeration(e=(*unknown_variable_values, x,))

        # Using substitution for the known_variable_values,
        # a more accurate set of premises can be computed, denoted necessary_premises.
        necessary_premises: Tupl = Tupl(
            e=replace_formulas(phi=i.transformation.input_shapes, m=known_variable_values))

        # Find a set of valid_statements in theory t, such that they match the necessary_premises.
        success, effective_premises = are_valid_statements_in_theory_with_variables(
            s=necessary_premises, t=t, variables=i.transformation.variables,
            variables_values=known_variable_values)

        if success:
            # All required premises are present in theory t, the conjecture can be proven.
            t, ok, derivation = derive_1(t=t, c=c, p=effective_premises,
                                         i=i, raise_error_if_false=True)
            return t, True, derivation
        else:
            # The required premises are not present in theory t, report failure.
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_079,
                    msg='Some premise required by inference-rule `i` are not valid propositions in theory `t`. '
                        'It follows that proposition `c` cannot be inferred in `t` using `i`.',
                    necessary_premises=necessary_premises,
                    c=c, i=i, known_variable_values=known_variable_values, t=t
                )
            return t, False, None
    else:
        # The conclusion of the inference_rule is not compatible with the conjecture.
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_080,
                msg='The candidate proposition `c` is not compatible with the conclusion of inference-rule `i`. '
                    'It follows that proposition `c` cannot be inferred in `t` using `i`.',
                c=c, i=i, known_variable_values=known_variable_values, t=t
            )
        return t, False, None


def auto_derive_with_heuristics(t: FlexibleTheory, conjecture: FlexibleFormula) -> \
        typing.Tuple[Theory, bool]:
    """Attempt to derive automatically a conjecture using the heuristics attached to the theory.

    :param t:
    :param conjecture:
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
        t, success, d = derive_2(t=t, c=conjecture, i=inference_rule, raise_error_if_false=False)
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
    conjectures: Tupl = coerce_tuple(t=conjectures, interpret_none_as_empty=True)
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
    conjecture_exclusion_list: Enumeration = coerce_enumeration(e=conjecture_exclusion_list,
                                                                interpret_none_as_empty=True)
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
    conjecture_exclusion_list = Enumeration(e=(*conjecture_exclusion_list, conjecture,))

    max_recursion = max_recursion - 1
    if max_recursion < 1:
        # We reached the max_recursion threshold, it follows that auto_derive failed.
        if debug:
            u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{conjecture}.')
        return t, False, None, conjecture_exclusion_list

    # Loop through all theory inference-rules to find those that could potentially prove the conjecture.
    # These are the inference-rules whose conclusions are formula-equivalent-with-variables to the conjecture.
    for inference_rule in t.iterate_inference_rules():
        is_equivalent, m = is_formula_equivalent_with_variables_2(phi=conjecture,
                                                                  psi=inference_rule.transformation.output_shape,
                                                                  variables=inference_rule.transformation.variables)
        if is_equivalent:
            # This inference-rule is compatible with the conjecture.

            # To list what would be the required premises to derive the conjecture,
            # the inference_rule must be "reverse-engineered".

            # first determine what are the necessary variable values in the transformation.
            # to do this, we have a trick, we can call is_formula_equivalent_with_variables and pass it
            # an empty map-builder:
            output, m, = is_formula_equivalent_with_variables_2(phi=conjecture,
                                                                psi=inference_rule.transformation.output_shape,
                                                                variables=inference_rule.transformation.variables,
                                                                variables_fixed_values=None)

            # then we list the variables for which we don't have an assigned value,
            # called the free-variables.
            free_variables: Enumeration = Enumeration()
            for x in inference_rule.transformation.variables:
                if not is_element_of_enumeration(x=x, e=m.domain):
                    free_variables = Enumeration(e=(*free_variables, x,))
            # u1.log_info(f'\t\t free-variables: {free_variables}')

            # now that we know what are the necessary variable values, we can determine what
            # are the necessary premises by substituting the variable values.
            necessary_premises: Tupl = Tupl(e=None)
            for original_premise in inference_rule.transformation.input_shapes:
                # we must find a set of premises in the theory
                # with free-variables.
                # I see two possible strategies:
                # 1) elaborate a new single proposition with the conjunction P1 and P2 and ... and Pn with all premises
                #    and then try to find that proposition in the theory, taking into account variables.
                # 2) develop an algorithm that given a set of premises returns true if they are all valid,
                #    and then extend this algorithm to support variables.
                # to avoid the burden of all these conjunctions in the theory, I start with the second approach.
                necessary_premise: Formula = replace_formulas(phi=original_premise, m=m)
                necessary_premises: Tupl = Tupl(e=(*necessary_premises, necessary_premise,))

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
                effective_premises: Tupl = Tupl(e=effective_premises)
                for premise_target_statement in effective_premises:
                    if not is_element_of_enumeration(x=premise_target_statement,
                                                     e=conjecture_exclusion_list):
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
                    t, ok, derivation = derive_1(t=t, c=conjecture,
                                                 p=effective_premises,
                                                 i=inference_rule,
                                                 raise_error_if_false=True)
                    if debug:
                        u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{conjecture}.')
                    return t, True, derivation, conjecture_exclusion_list
            else:
                valid_statements = iterate_theory_propositions(t=t)
                for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                                n=permutation_size):
                    permutation_success: bool = True
                    variable_substitution: Map = Map(d=free_variables, c=permutation)
                    effective_premises: Formula = replace_formulas(phi=necessary_premises, m=variable_substitution)
                    effective_premises: Tupl = Tupl(e=(*effective_premises, permutation,))
                    for premise_target_statement in effective_premises:
                        if not is_element_of_enumeration(x=premise_target_statement,
                                                         e=conjecture_exclusion_list):
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
                        t, ok, derivation = derive_1(t=t, c=conjecture,
                                                     p=effective_premises,
                                                     i=inference_rule,
                                                     raise_error_if_false=True)
                        if debug:
                            u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{conjecture}.')
                        return t, True, derivation, conjecture_exclusion_list
    if debug:
        u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{conjecture}.')
    return t, False, None, conjecture_exclusion_list


# HYPOTHESIS


class Hypothesis(Formula):
    """A hypothesis is....

    Syntactic definition:
    A hypothesis is a formula of the form:
        :math:`\\text{hypothesis}(t, a, ...)`
    Where:
        - :math:`b` is a theory, denoted as the base theory.
        - :math:`a` is a formula, denoted as the assumption, assumed to be true in :math:`t`.
    """
    BASE_THEORY_INDEX: int = 0
    ASSUMPTION_INDEX: int = 1

    @staticmethod
    def _data_validation_2(
            b: FlexibleTheory,
            a: FlexibleFormula) -> tuple[Connective, Theory, Formula]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param b: A theory denoted as the base theory.
        :param a: A formula denoted as the assumption.
        :return:
        """
        con: Connective = get_connectives().hypothesis_connective
        b: Theory = coerce_theory(t=b)
        a: Formula = coerce_formula(phi=a)
        return con, b, a

    def __new__(cls, b: FlexibleTheory, a: FlexibleFormula):
        """

        :param b: A theory denoted as the base theory.
        :param a: A formula denoted as the assumption.
        """
        con, b, a = Hypothesis._data_validation_2(b=b, a=a)
        o: tuple = super().__new__(cls, con=con, t=(b, a,))
        return o

    def __init__(self, b: FlexibleTheory, a: FlexibleFormula):
        """

        :param b: A theory denoted as the base theory.
        :param a: A formula denoted as the assumption.
        """
        con, b, a = Hypothesis._data_validation_2(b=b, a=a)
        super().__init__(con=con, t=(b, a,))

    @property
    def assumption(self) -> Formula:
        """A proposition assumed to be true, denoted as the assumption of the hypothesis."""
        return self[Hypothesis.ASSUMPTION_INDEX]

    @property
    def base_theory(self) -> Theory:
        """The base theory of the hypothesis."""
        return self[Hypothesis.BASE_THEORY_INDEX]


FlexibleHypothesis = typing.Optional[typing.Union[Hypothesis]]


# PRESENTATION LAYER


class ClassicalFormulaTypesetter(pl1.Typesetter):
    def __init__(self, connective_ts: pl1.Typesetter):
        super().__init__()
        connective_ts = pl1.coerce_typesetter(ts=connective_ts)
        self._connective_typesetter: pl1.Typesetter = connective_ts

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
        # is_sub_formula: bool = kwargs.get('is_sub_formula', False)
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
    def __init__(self, connective_ts: pl1.FlexibleTypesetter):
        super().__init__()
        connective_ts = pl1.coerce_typesetter(ts=connective_ts)
        self._connective_typesetter: pl1.Typesetter = connective_ts

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


class UnaryPostfixTypesetter(pl1.Typesetter):
    def __init__(self, connective_ts: pl1.FlexibleTypesetter):
        super().__init__()
        connective_ts = pl1.coerce_typesetter(ts=connective_ts)
        self._connective_typesetter: pl1.Typesetter = connective_ts

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
        if is_sub_formula:
            yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class TransformationByVariableSubstitutionTypesetter(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleTransformationByVariableSubstitution, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: TransformationByVariableSubstitution = coerce_transformation_by_variable_substitution(t=phi)

        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True
        if is_sub_formula:
            yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        yield from phi.input_shapes.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from pl1.symbols.rightwards_arrow.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from phi.output_shape.typeset_from_generator(**kwargs)
        if len(phi.variables) > 0:
            yield ' with variables '
            yield from phi.variables.typeset_from_generator(**kwargs)
        if len(phi.output_declarations) > 0:
            if len(phi.variables) > 0:
                yield ' and'
            yield ' declarations '
            yield from phi.output_declarations.typeset_from_generator(**kwargs)

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
        # is_sub_formula: bool = kwargs.get('is_sub_formula', False)
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
    """A typesetter for the map connective.

    Sample output:
     - an empty map: {}
     - a non-empty map: {x ↦ a, y ↦ b, z ↦ c}
     """

    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Map = coerce_map(m=phi, interpret_none_as_empty=True)
        # is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True

        yield from pl1.symbols.open_curly_brace.typeset_from_generator(**kwargs)
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
        yield from pl1.symbols.close_curly_brace.typeset_from_generator(**kwargs)


class IsAPredicateTypesetter(pl1.Typesetter):
    """A typesetter for "(some object) is a (some class)" predicate connectives.

    Sample output:
     - ⌜`phi`⌝ is an `class-name-starting-with-a-vowel`
     - ⌜`phi`⌝ is a `class-name-not-starting-with-a-vowel`
     """

    def __init__(self, conventional_class: str):
        super().__init__()
        self._conventional_class = conventional_class

    @property
    def conventional_class(self) -> str:
        return self._conventional_class

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        # is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True

        yield from pl1.symbols.open_corner_quote.typeset_from_generator(**kwargs)
        yield from phi[0].typeset_from_generator(**kwargs)
        yield from pl1.symbols.close_corner_quote.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield 'is'
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        if re.match(r'[aeiouAEIOU]', self.conventional_class[0]):
            yield 'an'
        else:
            yield 'a'
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from self.conventional_class


class DeclarationTypesetter(pl1.Typesetter):
    def __init__(self, conventional_class: str | None):
        self._conventional_class = conventional_class
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Formula = coerce_formula(phi=phi)
        yield 'Let '
        yield from phi.typeset_from_generator(ts_key=pl1.REF_TS, **kwargs)
        if self._conventional_class is not None:
            yield f' be a '
            yield self._conventional_class
        yield '.'


def get_theory_inference_rule_from_natural_transformation_rule(t: FlexibleTheory,
                                                               r: FlexibleTransformationByVariableSubstitution) -> \
        tuple[bool, InferenceRule | None]:
    """Given a theory `t` and a transformation-rule "r", return the first occurrence of an inference-rule in `t` such
    that its transformation-rule is formula-equivalent to "r".

    :param t: A theory.
    :param r: A transformation-rule.
    :return: A python-tuple (True, i) where `i` is the inference-rule if `i` is found in `t`, (False, None) otherwise.
    """
    t: Theory = coerce_theory(t=t)
    r: TransformationByVariableSubstitution = coerce_transformation_by_variable_substitution(t=r)
    for i in iterate_theory_inference_rules(t=t):
        i: InferenceRule
        if is_formula_equivalent(phi=r, psi=i.transformation):
            return True, i
    return False, None


def get_theory_derivation_from_valid_statement(t: FlexibleTheory, s: FlexibleFormula) -> \
        tuple[bool, Formula | None]:
    """Given a theory `t` and a valid-statement `s` in `t`, return the first occurrence of a derivation in `t` such
    that its valid-statement is formula-equivalent to `s`.

    :param t: A theory.
    :param s: A formula that is a valid statement in `t`.
    :return: A python-tuple (True, d) where `d` is the derivation if `s` is found in `t` valid-statements,
    (False, None) otherwise.
    """
    t: Theory = coerce_theory(t=t)
    s: Formula = coerce_formula(phi=s)
    for d in iterate_theory_derivations(t=t):
        d: Derivation
        if is_formula_equivalent(phi=s, psi=d.valid_statement):
            return True, d
    return False, None


def typeset_formula_reference(phi: FlexibleFormula, t: FlexibleTheory | None, **kwargs):
    """Typeset a formula's reference if it exists.

    :param phi:
    :param t:
    :return:
    """
    phi = coerce_formula(phi=phi)
    if t is not None:
        t = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    if pl1.REF_TS in phi.ts:
        # This formula has a typesetting reference, e.g. "PL01".
        yield from pl1.symbols.open_square_bracket.typeset_from_generator(**kwargs)
        if t is not None:
            yield from t.typeset_from_generator(ts_key=pl1.REF_TS, **kwargs)
            yield '.'
        yield from phi.ts.get(pl1.REF_TS).typeset_from_generator(**kwargs)
        yield from pl1.symbols.close_square_bracket.typeset_from_generator(**kwargs)
    elif t is not None and is_well_formed_derivation(d=phi) and is_term_of_formula(x=phi, phi=t):
        # phi is a derivation in a theory.
        # we can use the 1-based index of the formula in the theory.
        i: int = get_index_of_first_equivalent_term_in_formula(term=phi, formula=t)
        yield from pl1.symbols.open_square_bracket.typeset_from_generator(**kwargs)
        if t is not None:
            yield from t.typeset_from_generator(ts_key=pl1.REF_TS, **kwargs)
            yield '.'
        yield i + 1
        yield from pl1.symbols.close_square_bracket.typeset_from_generator(**kwargs)
    elif t is not None and is_valid_proposition_in_theory_1(p=phi, t=t):
        # phi is a valid-statement in a theory.
        # we can use the 1-based index of the formula in the theory.
        success, d = get_theory_derivation_from_valid_statement(t=t, s=phi)
        i: int = get_index_of_first_equivalent_term_in_formula(term=d, formula=t)
        yield from pl1.symbols.open_square_bracket.typeset_from_generator(**kwargs)
        if t is not None:
            yield from t.typeset_from_generator(ts_key=pl1.REF_TS, **kwargs)
            yield '.'
        yield i + 1
        yield from pl1.symbols.close_square_bracket.typeset_from_generator(**kwargs)
    else:
        # we don't have any context, our only choice is to typeset the original formula explicitly.
        yield from phi.typeset_from_generator(**kwargs)


class DerivationTypesetter(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleDerivation, theory: typing.Optional[FlexibleTheory] = None,
                               **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: Derivation = coerce_derivation(d=phi)
        if theory is None:
            yield '\t'
            yield from phi.valid_statement.typeset_from_generator(**kwargs)
            if is_well_formed_axiom(a=phi):
                # phi: Axiom = coerce_axiom(a=phi)
                yield '\t\t| Axiom.'
            elif is_well_formed_inference_rule(i=phi):
                # phi: InferenceRule = coerce_inference_rule(i=phi)
                yield '\t\t| Inference rule.'
            elif is_well_formed_inference(i=phi):
                # phi: InferenceRule = coerce_inference_rule(i=phi)
                yield '\t\t| Inference rule.'
            elif is_well_formed_theorem(t=phi):
                phi: Theorem = coerce_theorem(t=phi)
                inference: Inference = phi.inference
                inference_rule: InferenceRule = inference.inference_rule
                yield f'\t\t| Follows from [{inference_rule}] given '
                first: bool = True
                for premise in phi.inference.premises:
                    if not first:
                        yield ', '
                    yield f'[{premise}]'
                    first = False
                yield '.'
            else:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_052, msg=f'Unsupported derivation "{phi}" in the '
                                                                          f'theory.', phi=phi, theory=theory)
        else:
            # Theory parameter was provided, we have more context and premises can reference the derivation's number.
            yield '\t'
            yield from typeset_formula_reference(phi=phi, t=theory)
            yield f'\t'
            yield from phi.valid_statement.typeset_from_generator(**kwargs)
            if is_well_formed_axiom(a=phi):
                # phi: Axiom = coerce_axiom(a=phi)
                yield '\t\t| Axiom.'
            elif is_well_formed_inference_rule(i=phi):
                # phi: InferenceRule = coerce_inference_rule(i=phi)
                yield '\t\t| Inference rule.'
            elif is_well_formed_inference(i=phi):
                # phi: InferenceRule = coerce_inference_rule(i=phi)
                yield '\t\t| Inference rule.'
            elif is_well_formed_theorem(t=phi):
                phi: Theorem = coerce_theorem(t=phi)
                inference: Inference = phi.inference
                inference_rule: InferenceRule = inference.inference_rule
                yield f'\t\t| Follows from '
                yield from typeset_formula_reference(phi=inference_rule, t=theory, **kwargs)
                yield f' given '
                first: bool = True
                for premise in phi.inference.premises:
                    # success, derivation = get_theory_derivation_from_valid_statement(t=theory, s=premise)
                    derivation: Derivation
                    # i: int = 1 + get_index_of_first_equivalent_term_in_formula(term=derivation, formula=theory)
                    if not first:
                        yield ', '
                    yield from typeset_formula_reference(phi=premise, t=theory, **kwargs)
                    # yield f'[{i}]'
                    first = False
                yield '.'
            else:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_054,
                    msg=f'Unsupported derivation `phi` in the theory.',
                    phi=phi, theory=theory)


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
        return ClassicalFormulaTypesetter(connective_ts=connective_typesetter)

    def declaration(self, conventional_class: str | None) -> DeclarationTypesetter:
        return DeclarationTypesetter(conventional_class=conventional_class)

    def is_a_predicate(self, conventional_class: str | None) -> IsAPredicateTypesetter:
        return IsAPredicateTypesetter(conventional_class=conventional_class)

    def text(self, text: str) -> pl1.TextTypesetter:
        return pl1.typesetters.text(text=text)

    def indexed_symbol(self, symbol: pl1.Symbol, index: int) -> pl1.NaturalIndexedSymbolTypesetter:
        return pl1.typesetters.indexed_symbol(symbol=symbol, index=index)

    def infix_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> InfixFormulaTypesetter:
        return InfixFormulaTypesetter(connective_ts=connective_typesetter)

    def unary_postfix_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> UnaryPostfixTypesetter:
        return UnaryPostfixTypesetter(connective_ts=connective_typesetter)

    def map(self) -> MapTypesetter:
        return MapTypesetter()

    def transformation_by_variable_substitution(self) -> TransformationByVariableSubstitutionTypesetter:
        return TransformationByVariableSubstitutionTypesetter()

    def derivation(self) -> DerivationTypesetter:
        return DerivationTypesetter()


typesetters = Typesetters()
"""OBSOLETE: replace by declaring typesetters as module global variables.
"""
