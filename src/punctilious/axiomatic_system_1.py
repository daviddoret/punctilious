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
        return WellFormedFormula(con=self, t=args)

    def __str__(self):
        return f'{id(self)}-connective'

    def __repr__(self):
        return f'{id(self)}-connective'

    def __or__(self, other):
        # This method will be called for "self | other"
        return InfixPartialRightHandFormula(con=self, term_1=other)

    def __ror__(self, other):
        # This method will be called for "other | self"
        return InfixPartialLeftHandFormula(con=self, term_0=other)

    @property
    def formula_ts(self) -> pl1.Typesetter:
        return self._formula_typesetter

    @formula_ts.setter
    def formula_ts(self, formula_typesetter: pl1.Typesetter):
        self._formula_typesetter = formula_typesetter

    def to_formula(self) -> WellFormedFormula:
        return WellFormedFormula(con=self)

    @property
    def ts(self) -> dict[str, pl1.Typesetter]:
        """A dictionary of typesetters that may output representations of this object, or linked objects."""
        return self._ts


class ConnectiveLinkedWithAlgorithm(Connective):
    """A connective-linked-with-algorithm is a connective that is used as a link to the universe of external-algorithms.

    It comprises a complementary `algorithm` property.

    Transformations that use an external algorithm references the external algorithm using this connective.

    TODO: The external-algorithm is external to the theory. In order to emulate unicity,
        consider taking a hash of the algorithm and using a central index to assure unicity
        and non duplication of external algorithms, thus allowing a natural usage of
        formula-equivalence for formulas containing these connectives.

    """

    def __init__(self, a: typing.Callable, formula_ts: pl1.FlexibleTypesetter | None = None,
                 **kwargs):
        self._algorithm = a
        super().__init__(formula_ts=formula_ts, **kwargs)

    @property
    def algorithm(self) -> typing.Callable:
        """The external-algorithm referenced by this connective."""
        return self._algorithm


class WellFormedFormula(tuple):
    """A well-formed formula.

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
        con, t = WellFormedFormula._data_validation(con=con, t=t)
        if len(t) == 0:
            return super().__new__(cls)
        elif len(t) > 0:
            return super().__new__(cls, t)

    def __init__(self, con: Connective, t: FlexibleTupl = None, **kwargs):
        con, t = WellFormedFormula._data_validation(con=con, t=t)
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

    def __iter__(self):
        """Iterates the terms of the well-formed formula in canonical order.

        :return:
        """
        yield from super().__iter__()

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    def __or__(self, other):

        # This method will be called for "self | other"
        if isinstance(other, Connective):
            return InfixPartialLeftHandFormula(con=other, term_0=self)

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
    def term_0(self) -> WellFormedFormula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 1:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_003, c=self.connective)
        return self[0]

    @property
    def term_1(self) -> WellFormedFormula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 2:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_004, c=self.connective)
        return self[1]

    @property
    def term_2(self) -> WellFormedFormula:
        """
        TODO: Extend the data model and reserve this method to sub-classes that have an n-th element. It should be
        possible to use the __new__ method to properly type formulas based on their arity.
        :return:
        """
        if len(self) < 3:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_005, c=self.connective)
        return self[2]

    @property
    def term_3(self) -> WellFormedFormula:
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

    def iterate_formula_terms(self, max_terms: int | None = None
                              ) -> typing.Generator[WellFormedFormula, None, None]:
        """Iterates the terms of the well-formed formula in canonical order.

        :param max_terms: Yields all terms if ``None`` (default), or yields only the ``max_terms`` first elements,
        :return:
        """
        yield from iterate_formula_terms(phi=self, max_terms=max_terms)

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


class WellFormedProposition(WellFormedFormula):
    """A well-formed proposition.

    Global definition:
    A well-formed formula :math:`P` is a well-formed proposition.

    Local definition (with regard to a theory t):
    A well-formed formula :math:`P` is a well-formed proposition with regard to a theory :math:`T` if and only if:
     - :math:`P` is a globally well-formed proposition,
     - :math:`T \\vdash \\text{is-proposition}\\left( P \\right)`.

    Note:
    Whether a formula is a proposition is entirely dependent on the theory.
    """
    pass


class WellFormedTheoreticalContext(WellFormedFormula, ABC):
    """A well-formed theoretical context is a formula that is either a well-formed axiomatization, theory,
    or hypothesis. One of its defining property is to have an axiomatic base.

    .. _well_formed_theoretical_context:

    Subclasses
    ^^^^^^^^^^^^^^^^^^^^
     - :class:`WellFormedAxiomatization`
     - :class:`WellFormedTheory`
     - :class:`WellFormedHypothesis`

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed theoretical context if and only if:
      - it is a well-formed axiomatization,
      - or it is a well-formed theory,
      - or it is a well-formed hypothesis.

    Notes
    ^^^^^^^^^^^^^^^^^^^^

    Note 1
    ~~~~~~~~~~~~~~~~~~
    WellFormedTheoreticalContext is implemented as an abstract class.

    To do list
    ^^^^^^^^^^^^^^^^^^^^
    - TODO: Add TheoryExtension as a new class, defined as the extension of a theoretical context.
        do we want to distinguish TheoryDerivation as well?

    """

    @staticmethod
    def _data_validation(con: Connective, t: FlexibleTupl = None) -> tuple[Connective, tuple]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param con:
        :param t:
        :return:
        """
        # Data validation is left to 1) the non-abstract derived class, and 2) the parent Formula class.
        # This method is only maintained for the sake of consistency.
        # TODO: coerce t to tupl
        # TODO: check that all tuple elements are either axioms, theorems, or inference rules.
        return con, t

    def __new__(cls, con: Connective, t: FlexibleTupl = None, **kwargs):
        con, t = WellFormedFormula._data_validation(con=con, t=t)
        o = super().__new__(cls, con=con, t=t, **kwargs)
        return o

    def __init__(self, con: Connective, t: FlexibleTupl = None, **kwargs):
        con, t = WellFormedFormula._data_validation(con=con, t=t)
        super().__init__(con=con, t=t, **kwargs)
        self._heuristics: set[Heuristic, ...] | set[{}] = set()

    def count_components(self, recurse_extensions: bool = True,
                         strip_duplicates: bool = False,
                         max_components: bool | int = None) -> int:
        """Returns the number of components in the theoretical context.

        Definition: canonical theory length
        The canonical length of a theory is the number of components it contains,
        recursively taking into account extensions.

        Definition: raw theory length
        The raw length of a theory is the number of components it contains,
        not taking into account extensions.

        :return: The number of components in the theoretical context.
        """
        return count_theory_components(t=self, recurse_extensions=recurse_extensions, strip_duplicates=strip_duplicates,
                                       max_components=max_components)

    @abc.abstractmethod
    def extend_with_component(self, c: FlexibleComponent, return_theory_if_necessary: bool = True,
                              **kwargs) -> WellFormedTheoreticalContext:
        """

        :param c:
        :param return_theory_if_necessary: If ``self`` is an axiomatization and ``c`` is either a theorem,
            or an extension that contains (recursively) a theorem,
            returns a theory (instead of an axiomatization),
            raise an error otherwise.
        :param kwargs:
        :return:
        """
        raise u1.ApplicativeError(msg='Abstract method.')

    @property
    def axioms(self) -> WellFormedEnumeration:
        """Return an enumeration of all axioms in the theory.
        Note: order is preserved."""
        return WellFormedEnumeration(e=tuple(self.iterate_axioms()))

    @property
    def heuristics(self) -> set[Heuristic, ...] | set[{}]:
        """A python-set of heuristics.

        Heuristics are not formally part of a theory. They are decorative objects used to facilitate proof derivations.
        """
        return self._heuristics

    @property
    def valid_statements(self) -> WellFormedEnumeration:
        """Return an enumeration of all axiom and theorem valid-statements in the theory, preserving order.
        """
        python_tuple: tuple = tuple(self.iterate_valid_statements())
        e: WellFormedEnumeration = WellFormedEnumeration(e=python_tuple)
        return e

    @property
    def inference_rules(self) -> WellFormedEnumeration:
        """Return an enumeration of all inference-rules in the theory, preserving order, filtering out axioms and
        theorems.
        """
        return WellFormedEnumeration(e=tuple(self.iterate_inference_rules()))

    def iterate_axioms(self) -> typing.Iterator[WellFormedAxiom]:
        """Iterates over all axioms in the theory, preserving order, filtering out inference-rules and theorems.
        """
        yield from iterate_theory_axioms(t=self)

    def iterate_valid_statements(self) -> typing.Iterator[WellFormedFormula]:
        """Iterates over all axiom and theorem valid-statements in the theory, preserving order.
        """
        yield from iterate_theory_valid_statements(t=self)

    def iterate_inference_rules(self) -> typing.Iterator[WellFormedInferenceRule]:
        """Iterates over all inference-rules in the theory, preserving order, filtering out axioms and theorems.
        """
        yield from iterate_theory_inference_rules(t=self)

    def iterate_theorems(self) -> typing.Iterator[WellFormedTheorem]:
        """Iterates over all theorems in the theory, preserving order, filtering out axioms and inference-rules.
        """
        yield from iterate_theory_theorems(t=self)

    def iterate_components(self) -> typing.Iterator[WellFormedTheoryComponent]:
        """Iterates over all derivations, preserving order
        """
        yield from iterate_theory_components(t=self)

    @property
    def components(self) -> WellFormedEnumeration:
        """Return an enumeration of all derivations in the theory, preserving order.

                TODO: MOVE TO THEORETICAL CONTEXT???
        """
        return WellFormedEnumeration(e=tuple(self.iterate_components()))

    @property
    def theorems(self) -> WellFormedEnumeration:
        """Return an enumeration of all theorems in the theory, preserving order, filtering out axioms and
        inference-rules.

                TODO: MOVE TO THEORETICAL CONTEXT???
        """
        return WellFormedEnumeration(e=tuple(self.iterate_theorems()))


def yield_string_from_typesetter(x, **kwargs):
    # TODO: ?????
    if isinstance(x, str):
        yield x
    elif isinstance(x, pl1.Typesetter):
        for y in x.typeset_from_generator(**kwargs):
            yield_string_from_typesetter(x=y, **kwargs)


def coerce_formula(phi: FlexibleFormula) -> WellFormedFormula:
    if isinstance(phi, WellFormedFormula):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula()
    elif isinstance(phi, typing.Generator) and not isinstance(phi, WellFormedFormula):
        # Implicit conversion of generators to tuple formulas.
        return WellFormedTupl(e=(element for element in phi))
    elif isinstance(phi, typing.Iterable) and not isinstance(phi, WellFormedFormula):
        # Implicit conversion of iterators to tuple formulas.
        return WellFormedTupl(e=phi)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_006,
            msg=f'Formula coercion failure. Argument `phi` could not be coerced to a formula. ',
            phi=phi)


def coerce_proposition(p: FlexibleProposition,
                       t: FlexibleTheoreticalContext | None = None) -> WellFormedProposition:
    """Coerces ``p`` to a well-formed proposition.

    :param p: A presumably well-formed proposition.
    :param t: (Conditional) If ``None``, ``p``is coerced to a globally well-formed proposition.
        Otherwise, ``p``is coerced to a locally well-formed proposition with regard to ``t``.
    :return: A well-formed proposition.
    """
    p: WellFormedFormula = coerce_formula(phi=p)
    if isinstance(p, WellFormedProposition):
        if t is not None:
            # Check local well-formedness.
            is_well_formed_proposition(p=p, t=t, raise_error_if_false=True)
        return p
    elif is_well_formed_proposition(p=p, t=t):
        return WellFormedProposition(con=p.connective, t=(*p,))
    else:
        raise u1.ApplicativeError(
            msg='Coercion failure. `p` cannot be coerced to a well-formed proposition.',
            p=p,
            t=t
        )


def coerce_variable(x: FlexibleFormula) -> WellFormedFormula:
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
                                interpret_none_as_empty: bool = True) -> WellFormedEnumeration:
    """Coerce elements to an enumeration.
    If elements is None, coerce it to an empty enumeration."""
    if strip_duplicates:
        # this should not be necessary, because duplicate stripping
        # takes place in Enumeration __init__. but there must be some kind of implicit conversion
        # too early in the process which leads to an error being raised.
        e = strip_duplicate_formulas_in_python_tuple(t=e)
    if isinstance(e, WellFormedEnumeration):
        return e
    elif isinstance(e, WellFormedFormula) and is_well_formed_enumeration(e=e):
        # phi is a well-formed enumeration,
        # it can be safely re-instantiated as an Enumeration and returned.
        return WellFormedEnumeration(e=e, strip_duplicates=strip_duplicates)
    elif interpret_none_as_empty and e is None:
        return WellFormedEnumeration(e=None, strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Generator) and not isinstance(e, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedEnumeration(e=tuple(element for element in e), strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Iterable) and not isinstance(e, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedEnumeration(e=e, strip_duplicates=strip_duplicates)
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_008, coerced_type=WellFormedEnumeration, phi_type=type(e),
                                  phi=e)


def coerce_enumeration(e: FlexibleEnumeration, strip_duplicates: bool = False,
                       interpret_none_as_empty: bool = False,
                       canonic_conversion: bool = False) -> WellFormedEnumeration:
    """Coerce "e" to an enumeration.
    """
    if isinstance(e, WellFormedEnumeration):
        return e
    elif interpret_none_as_empty and e is None:
        return WellFormedEnumeration(e=None)
    elif is_well_formed_enumeration(e=e):
        # phi is a well-formed enumeration,
        # it can be safely re-instantiated as an Enumeration and returned.
        return WellFormedEnumeration(e=(*e,))
    elif canonic_conversion and is_well_formed_formula(phi=e):
        return transform_formula_to_enumeration(phi=e, strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Generator) and not isinstance(e, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedEnumeration(e=tuple(element for element in e), strip_duplicates=strip_duplicates)
    elif isinstance(e, typing.Iterable) and not isinstance(e, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedEnumeration(e=e, strip_duplicates=strip_duplicates)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_008,
            msg='"e" cannot be coerced to an enumeration.',
            e=e,
            interpret_none_as_empty=interpret_none_as_empty,
            canonic_conversion=canonic_conversion,
            strip_duplicates=strip_duplicates)


def coerce_tuple(s: FlexibleTupl, interpret_none_as_empty: bool = False,
                 canonic_conversion: bool = False) -> WellFormedTupl:
    """Coerces ``s``to a well-formed tuple.

    :param s: A presumably well-formed tuple.
    :param interpret_none_as_empty:
    :param canonic_conversion:
    :return: A well-formed tuple.
    """
    if isinstance(s, WellFormedTupl):
        return s
    elif is_well_formed_tupl(t=s, interpret_none_as_empty=interpret_none_as_empty):
        return WellFormedTupl(e=s)
    elif interpret_none_as_empty and s is None:
        return WellFormedTupl(e=None)
    elif canonic_conversion and is_well_formed_formula(phi=s):
        # Every formula can be transformed to a tuple using canonical transformation.
        return transform_formula_to_tuple(phi=s)
    elif isinstance(s, typing.Generator) and not isinstance(s, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedTupl(e=tuple(x for x in s))
    elif isinstance(s, typing.Iterable) and not isinstance(s, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedTupl(e=s)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_065,
            msg='No solution found to coerce ``t`` to tupl.',
            t=s,
            interpret_none_as_empty=interpret_none_as_empty)


def coerce_tuple_of_proposition(s: FlexibleTupl[FlexibleProposition],
                                t: FlexibleTheoreticalContext | None = None,
                                interpret_none_as_empty: bool = False,
                                canonic_conversion: bool = False) -> WellFormedTupl[WellFormedProposition]:
    """Coerces ``s`` to a well-formed tuple of well-formed propositions.

    :param s: A presumably well-formed tuple.
    :param t: (Conditional) If ``None``, propositions are coerced to globally well-formed propositions.
        Otherwise, propositions ares coerced to locally well-formed propositions with regard to ``t``.
    :param interpret_none_as_empty:
    :param canonic_conversion:
    :return: A well-formed tuple of propositions.
    """
    s: WellFormedTupl = coerce_tuple(s=s, interpret_none_as_empty=interpret_none_as_empty,
                                     canonic_conversion=canonic_conversion)
    if all(is_well_formed_proposition(p=p, t=t) for p in iterate_tuple_elements(phi=s)):
        return s
    else:
        return WellFormedTupl(e=(coerce_proposition(p=p, t=t) for p in iterate_tuple_elements(phi=s)))


def coerce_enumeration_of_variables(e: FlexibleEnumeration) -> WellFormedEnumeration:
    e = coerce_enumeration(e=e, interpret_none_as_empty=True)
    e2 = WellFormedEnumeration()
    for element in e:
        element = coerce_variable(x=element)
        e2 = WellFormedEnumeration(e=(*e2, element,))
    return e2


def union_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                      interpret_none_as_empty: bool = True, canonic_conversion: bool = True) -> WellFormedEnumeration:
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
    phi: WellFormedEnumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    psi: WellFormedEnumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    e: WellFormedEnumeration = WellFormedEnumeration(e=(*phi, *psi,), strip_duplicates=strip_duplicates)
    return e


def intersection_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                             interpret_none_as_empty: bool = True,
                             canonic_conversion: bool = True) -> WellFormedEnumeration:
    """Given two enumerations phi, and psi, the intersection-enumeration operator, noted phi ∩-enumeration psi,
    returns a new enumeration omega such that:
    - all elements of the resulting enumeration are elements of phi and of psi.
    Order is preserved, that is:
    - the elements from phi keep their original relative order

    Under enumeration-equivalence, the intersection-enumeration operator is:
     - Idempotent: (phi ∩-enumeration phi) ~enumeration phi.
     - Symmetric: (phi ∩-enumeration psi) ~enumeration (psi ∩-enumeration phi).
    """
    phi: WellFormedEnumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    psi: WellFormedEnumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    common_elements: list = [x for x in iterate_enumeration_elements(e=phi) if is_element_of_enumeration(x=x, e=psi)]
    e: WellFormedEnumeration = WellFormedEnumeration(e=common_elements, strip_duplicates=strip_duplicates)
    return e


def difference_enumeration(phi: FlexibleEnumeration, psi: FlexibleEnumeration, strip_duplicates: bool = True,
                           interpret_none_as_empty: bool = True,
                           canonic_conversion: bool = True) -> WellFormedEnumeration:
    """Given two enumerations phi, and psi, the difference-enumeration operator, noted phi ∖-enumeration psi,
    returns a new enumeration omega such that:
    - all elements of the resulting enumeration are elements of phi but not psi.
    Order is preserved, that is:
    - the elements from phi keep their original relative order
    """
    phi: WellFormedEnumeration = coerce_enumeration(e=phi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    psi: WellFormedEnumeration = coerce_enumeration(e=psi, interpret_none_as_empty=interpret_none_as_empty,
                                                    strip_duplicates=strip_duplicates,
                                                    canonic_conversion=canonic_conversion)
    different_elements: list = [x for x in iterate_enumeration_elements(e=phi) if
                                not is_element_of_enumeration(x=x, e=psi)]
    e: WellFormedEnumeration = WellFormedEnumeration(e=different_elements, strip_duplicates=strip_duplicates)
    return e


def union_theory(phi: FlexibleTheory, psi: FlexibleTheory) -> WellFormedTheory:
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
    phi: WellFormedTheory = coerce_theory(t=phi)
    psi: WellFormedTheory = coerce_theory(t=psi)
    t2: WellFormedTheory = WellFormedTheory(d=(*phi, *psi,))
    return t2


def coerce_map(m: FlexibleMap, interpret_none_as_empty: bool = False) -> WellFormedMap:
    if isinstance(m, WellFormedMap):
        return m
    elif interpret_none_as_empty and m is None:
        # implicit conversion of None to the empty map.
        return WellFormedMap(d=None, c=None)
    elif is_well_formed_map(m=m):
        # `m` is improperly python-typed, but it is a well-formed map.
        return WellFormedMap(d=m[WellFormedMap.DOMAIN_INDEX], c=m[WellFormedMap.CODOMAIN_INDEX])
    elif isinstance(m, dict):
        # implicit conversion of python dict to Map.
        domain: WellFormedEnumeration = coerce_enumeration(e=m.keys())
        codomain: WellFormedTupl = coerce_tuple(s=m.values())
        return WellFormedMap(d=domain, c=codomain)
    else:
        # no coercion solution found.
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_009,
            msg='Argument `m` could not be coerced to a map.',
            coerced_type=WellFormedMap, m_type=type(m), m=m)


FlexibleFormula = typing.Optional[typing.Union[Connective, WellFormedFormula]]
"""A flexible python type that may be coerced into :class:`WellFormedFormula`."""

FlexibleProposition = typing.Optional[typing.Union[FlexibleFormula, WellFormedProposition]]
"""A flexible python type that may be coerced into :class:`WellFormedProposition`."""


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


class WellFormedSimpleObject(WellFormedFormula):
    """A well-formed simple object is a formula of the form ⌜ :math:`\\boldsymbol{O}\\left( \\right)` ⌝ where
    :math:`\\boldsymbol{O}` is a (nullary) connective.

    Definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`\\phi` is a well-formed axiom if and only if:
     - its arity is equal to 0.

    Typesetting
    ~~~~~~~~~~~~~~~
    - :math:`\\boldsymbol{O}\\left( \\right)`
    - :math:`\\boldsymbol{O}` (abbreviated form)
    """

    @staticmethod
    def _data_validation_3(con: Connective = None) -> Connective:
        return con

    def __new__(cls, c: NullaryConnective):
        con = WellFormedSimpleObject._data_validation(con=c)
        o: tuple
        o = super().__new__(cls, con=c, t=None)
        return o

    def __init__(self, c: NullaryConnective):
        super().__init__(con=c, t=None)


class UnaryConnective(FixedArityConnective):

    def __init__(self, formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None):
        super().__init__(fixed_arity_constraint=1, formula_ts=formula_ts)


class PartialFormula:
    pass


class InfixPartialLeftHandFormula(PartialFormula, pl1.Typesetter):
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and gluing all this together with the InfixPartialFormula class.
    """

    def __init__(self, con: Connective, term_0: FlexibleFormula):
        self._connective = con
        self._term_0 = term_0
        pass

    def __or__(self, term_1: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        return WellFormedFormula(con=self._connective, t=(self.term_0, term_1,))

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    @property
    def connective(self) -> Connective:
        return self._connective

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield f'({self.term_0} {self.connective} ???)'

    @property
    def term_0(self) -> Connective:
        return self._term_0


class InfixPartialRightHandFormula(PartialFormula, pl1.Typesetter):
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and gluing all this together with the InfixPartialFormula class.
    """

    def __init__(self, con: Connective, term_1: FlexibleFormula):
        self._connective = con
        self._term_1 = term_1
        pass

    def __ror__(self, term_0: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        # This method will be called for "other | self"
        return WellFormedFormula(con=self._connective, t=(term_0, self.term_1,))

    def __repr__(self):
        return self.typeset_as_string()

    def __str__(self):
        return self.typeset_as_string()

    @property
    def connective(self) -> Connective:
        return self._connective

    def typeset_from_generator(self, **kwargs) -> (
            typing.Generator)[str, None, None]:
        yield f'(??? {self.connective} {self.term_1})'

    @property
    def term_1(self) -> Connective:
        return self._term_1


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
    x: WellFormedFormula = coerce_formula(phi=x)
    phi: WellFormedFormula = coerce_formula(phi=phi)
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
    x: WellFormedFormula = coerce_formula(phi=x)
    e: WellFormedEnumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    return is_term_of_formula(x=x, phi=e)


def is_axiom_of(a: FlexibleAxiom, t: FlexibleTheoreticalContext, max_components: int | None = None) -> bool:
    """Returns ``True`` if ``a`` is an axiom in theoretical context ``t``, ``False`` otherwise.

    :param a: An axiom.
    :param t: A theoretical context.
    :param max_components: If `None`, considers all derivations in ``t``. If an integer, considers only that number
        of derivations in ``t`` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: ``True`` if ``a`` is an axiom ``t``, ``False`` otherwise.
    """
    a: WellFormedAxiom = coerce_axiom(a=a)
    t: WellFormedTheory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    return any(
        is_formula_equivalent(phi=a, psi=a2) for a2 in iterate_theory_axioms(t=t, max_components=max_components))


def is_inference_rule_of(
        i: FlexibleInferenceRule,
        t: FlexibleTheoreticalContext | None = None,
        d: FlexibleEnumeration[FlexibleComponent] | None = None,
        max_components: int | None = None):
    """Returns ``True`` if `i` is an inference-rule in axiomatization or theory ``t``, ``False`` otherwise.

    If ``d`` is passed instead of ``t``, an enumeration of theory components is considered. This is useful
    to check the validity of a sequence of components without raising an error.

    :param i: An inference-rule.
    :param t: A theoretical context.
    :param d: An enumeration.
    :param max_components: If `None`, considers all derivations in ``t``. If an integer, considers only that number
        of derivations in ``t`` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: ``True`` if ``a`` is an inference-rule ``t``, ``False`` otherwise.
    """
    i: WellFormedInferenceRule = coerce_inference_rule(i=i)
    if t is not None and d is not None:
        raise u1.ApplicativeError(msg='Parameters `t` and `d` are mutually exclusive.', t=t, d=d)
    return any(is_formula_equivalent(phi=i, psi=ir2) for ir2 in
               iterate_theory_inference_rules(t=t, d=d, max_components=max_components,
                                              recurse_extensions=True))


def is_theorem_of(m: FlexibleTheorem, t: FlexibleTheory, max_components: int | None = None):
    """Returns ``True`` if `m` is a theorem in theory ``t``, ``False`` otherwise.

    :param m: A theorem.
    :param t: A theory.
    :param max_components: If `None`, considers all derivations in ``t``. If an integer, considers only that number
        of derivations in ``t`` following canonical order. This is particularly useful when analysing the consistency
        of a theory, or dependencies between derivations.
    :return: ``True`` if `m` is a theorem in ``t``, ``False`` otherwise.
    """
    m: WellFormedTheorem = coerce_theorem(m=m)
    t: WellFormedTheory = coerce_theory(t=t, interpret_none_as_empty=True, canonical_conversion=True)
    return any(is_formula_equivalent(phi=m, psi=thrm2) for thrm2 in
               iterate_theory_theorems(t=t, max_components=max_components))


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
    x: WellFormedFormula = coerce_formula(phi=x)
    e: WellFormedEnumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    return get_index_of_first_equivalent_term_in_formula(term=x, formula=e)


def get_index_of_first_equivalent_element_in_tuple(x: FlexibleFormula, t: FlexibleTupl) -> int:
    """If formula "x" is a term of tuple ``t``, return the o-based index of the first occurrence of the term "x"
    in ``t``.

    :param x: A formula.
    :param t: A tuple.
    :return: The 0-based index of "x" in ``t``.
    """
    x: WellFormedFormula = coerce_formula(phi=x)
    t: WellFormedTupl = coerce_tuple(s=t, interpret_none_as_empty=True)
    return get_index_of_first_equivalent_term_in_formula(term=x, formula=t)


class TernaryConnective(FixedArityConnective):

    def __init__(self,
                 formula_ts: typing.Optional[pl1.Typesetter] = None):
        super().__init__(fixed_arity_constraint=3, formula_ts=formula_ts)


class QuaternaryConnective(FixedArityConnective):

    def __init__(self,
                 formula_ts: typing.Optional[pl1.Typesetter] = None):
        super().__init__(fixed_arity_constraint=4, formula_ts=formula_ts)


class WellFormedVariable(WellFormedSimpleObject):
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
        phi: WellFormedFormula = coerce_formula(phi=phi)
        if phi.arity != 0:
            return False
        return True

    def __new__(cls, c: NullaryConnective):
        o: tuple
        o = super().__new__(cls, c=c)
        return o

    def __init__(self, c: NullaryConnective):
        super().__init__(c=c)

    def __enter__(self) -> WellFormedVariable:
        return self

    def __exit__(self, exc_type: typing.Optional[type], exc: typing.Optional[BaseException],
                 exc_tb: typing.Any) -> None:
        return


class MetaVariable(WellFormedSimpleObject):
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


def let_x_be_a_variable(formula_ts: str | pl1.FlexibleTypesetter | None) -> (
        typing.Union)[WellFormedVariable, typing.Generator[WellFormedVariable, typing.Any, None]]:
    """Declares a new well-formed variable.

    See :class:`WellFormedVariable` for detailed information on well-formed variables.

    :param formula_ts: A name for the variable.
    :return: A well-formed variable.
    """
    if isinstance(formula_ts, str):
        formula_ts = pl1.SerifItalic(text=formula_ts)
    return WellFormedVariable(c=NullaryConnective(formula_ts=formula_ts))


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


def let_x_be_a_simple_object(formula_ts: typing.Optional[pl1.FlexibleTypesetter] = None) -> WellFormedSimpleObject:
    """A helper function to declare one or multiple simple-objects.

    :param formula_ts: A string (or an iterable of strings) default representation for the simple-object(s).
    :return: A simple-object (if rep is a string), or a python-tuple of simple-objects (if rep is an iterable).
    """
    return WellFormedSimpleObject(c=NullaryConnective(formula_ts=formula_ts))


def let_x_be_some_simple_objects(
        reps: tuple[pl1.FlexibleTypesetter, ...]) -> typing.Generator[WellFormedSimpleObject, typing.Any, None]:
    """A helper function to declare some simple-objects.

    :param reps: An iterable of strings or typesetters, denoted as the default representation of the simple-objects.
    :return: A python-tuple of simple-objects.
    """
    return (let_x_be_a_simple_object(formula_ts=rep) for rep in reps)


def let_x_be_some_variables(
        reps: tuple[pl1.FlexibleTypesetter, ...]) -> typing.Generator[WellFormedVariable, typing.Any, None]:
    """A helper function to declare some variables.

    :param reps: An iterable of typesetters or strings, denoted as the default representations of the variables.
    :return: A python-tuple of variables.
    """
    return (let_x_be_a_variable(formula_ts=rep) for rep in reps)


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
                               ) -> tuple[WellFormedTheoreticalContext, WellFormedInferenceRule]:
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
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, interpret_none_as_empty=True)
    # Signature #1: provide the inference-rule
    if i is not None:
        i: WellFormedInferenceRule = coerce_inference_rule(i=i)
    # Signature #2: provide the transformation upon which the inference-rule can be built
    elif f is not None:
        f: ABCTransformation = coerce_transformation(f=f)
        i: WellFormedInferenceRule = WellFormedInferenceRule(f=f)
    # Signature #3: provide the arguments upon which the transformation can be built upon which ...
    elif c is not None:
        c: WellFormedFormula = coerce_formula(phi=c)
        v: WellFormedEnumeration = coerce_enumeration(e=v, interpret_none_as_empty=True, canonic_conversion=True,
                                                      strip_duplicates=True)
        d: WellFormedEnumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, canonic_conversion=True,
                                                      strip_duplicates=True)
        p: WellFormedTupl = coerce_tuple(s=p, interpret_none_as_empty=True, canonic_conversion=True)
        # if a is None:
        # Signature 3: This is a transformation-by-variable-transformation:
        f: WellFormedTransformationByVariableSubstitution = WellFormedTransformationByVariableSubstitution(o=c, v=v,
                                                                                                           d=d, i=p)
        i: WellFormedInferenceRule = WellFormedInferenceRule(f=f)
        # else:
        #    # Signature 4: This is an algorithmic transformation:
        #    f: TransformationByExternalAlgorithm = TransformationByExternalAlgorithm(algo=a, check=i2, o=c, v=v,
        #                                                                             d=d, i=p)
        #    i: InferenceRule = InferenceRule(f=f)
    else:
        raise u1.ApplicativeError(msg='Inference rule declaration error. Inconsistent arguments.', i=i, f=f, c=c, v=v,
                                  d=d, p=p, a=a, t=t)
    i = coerce_inference_rule(i=i)
    t = t.extend_with_component(c=i)
    u1.log_info(i.typeset_as_string(theory=t))
    return t, i


def let_x_be_an_axiom(t: FlexibleTheoreticalContext | None = None, s: typing.Optional[FlexibleFormula] = None,
                      a: typing.Optional[FlexibleAxiom] = None, **kwargs) -> (
        WellFormedTheoreticalContext, WellFormedAxiom):
    """Given a theoretical context ``t``, returns a new theoretical context ``t'`` such that it extends ``t`` with axiom ``a``.

    :param t: An axiomatization or a theory. If None, the empty axiom-collection is implicitly used.
    :param s: The statement claimed by the new axiom. Either the claim or axiom parameter
    must be provided, and not both.
    :param a: An existing axiom. Either the claim or axiom parameter must be provided,
    and not both.
    :return: a pair (t, a) where t is an extension of the input theory, with a new axiom claiming the
    input statement, and ``a`` is the new axiom.
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, interpret_none_as_empty=True)

    if s is not None and a is not None:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_016,
            msg='Both `s` and ``a`` are not None. It is mandatory to provide only one of these two arguments.',
            s=s,
            a=a,
            t=t)
    elif s is None and a is None:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_017,
            msg='Both `s` and ``a`` are None. It is mandatory to provide one of these two arguments.')
    elif s is not None:
        a: WellFormedAxiom = WellFormedAxiom(p=s, **kwargs)
    coerce_axiom(a=a)
    t = t.extend_with_component(c=a)
    u1.log_info(a.typeset_as_string(theory=t))
    return t, a


def let_x_be_an_extension(t: FlexibleTheoreticalContext | None = None, e: FlexibleTheoreticalContext | None = None,
                          **kwargs) -> (
        WellFormedTheoreticalContext, WellFormedExtension):
    """Given a theoretical context ``t``, returns a new theoretical context ``t'`` such that it extends ``t``
    with theoretical context ``e``.

    :param t: A theoretical context. If None, the empty axiomatization is implicitly used.
    :param e: A theoretical context. If None, the empty axiomatization is implicitly used.
    :return: a pair ``(t', e)`` where ``t2`` is the extended theoretical context ``t'``,
        and ``e`` is the extension.
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, interpret_none_as_empty=True)
    e: WellFormedTheoreticalContext = coerce_theoretical_context(t=e, interpret_none_as_empty=True)
    e: WellFormedExtension = WellFormedExtension(t=e)
    t_prime: WellFormedTheoreticalContext = extend_with_component(t=t, c=e)
    return t_prime, e


def let_x_be_a_theory(
        t: FlexibleTheory | None = None,
        d: FlexibleEnumeration | None = None,
        **kwargs) -> WellFormedTheory:
    """Declares a new theory ``t``.

    :param t:
    :param d: an enumeration of derivations to initialize T. If None, the empty theory is implicitly assumed.
    :return: A python-tuple (m, t).
    """
    t: WellFormedTheory = WellFormedTheory(t=t, d=d, **kwargs)

    return t


def let_x_be_an_axiomatization(
        a: FlexibleAxiomatization | None = None,
        d: FlexibleEnumeration | None = None,
        **kwargs) -> WellFormedAxiomatization:
    """Declares a new well-formed axiomatization.

    :param a:
    :param d: an enumeration of derivations to initialize the axiomatization. If None, the empty theory is implicitly assumed.
    :return: An axiomatization.
    """
    a: WellFormedAxiomatization = WellFormedAxiomatization(a=a, d=d, **kwargs)

    return a


def let_x_be_a_meta_theory(m: FlexibleTheory | None = None,
                           d: FlexibleEnumeration | None = None,
                           **kwargs) -> WellFormedTheory:
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
    m: WellFormedTheory = WellFormedTheory(t=m, d=d, **kwargs)

    # TODO: Load automatically mt1

    return m


def let_x_be_a_sub_theory_of_y(m: FlexibleTheory, t: FlexibleTheory) -> tuple[WellFormedTheory, WellFormedTheory]:
    """

    :param t:
    :param m:
    :return:
    """
    m = coerce_theory(t=t)
    t = coerce_theory(t=t)
    # Move this to mt1 and redevelop it to use derivation from mt1 inference-rule.
    m, a = let_x_be_an_axiom(t=m, s=connective_for_is_well_formed_theoretical_context(t))
    return m, t


def let_x_be_a_collection_of_axioms(axioms: FlexibleEnumeration):
    return WellFormedAxiomatization(d=axioms)


def let_x_be_a_transformation_by_variable_substitution(o: FlexibleFormula,
                                                       v: FlexibleEnumeration | None = None,
                                                       d: FlexibleEnumeration | None = None,
                                                       i: FlexibleTupl | None = None,
                                                       a: FlexibleConnectiveLinkedToAlgorithm | None = None
                                                       ):
    """

    :param a: (Conditional) A connective-linked-to-algorithm denoted as the external algorithm reference. Only
    applicable to transformations that require an external validation algorithm.
    :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
    :param d: An enumeration of variables used to reference new object declarations in the output-shape.
    :param i: A tuple of formulas denoted as the input-shapes.
    :param o: A formula denoted as the output-shape.
    :return:
    """
    return WellFormedTransformationByVariableSubstitution(o=o, v=v, d=d, i=i, a=a)


# Declare fundamental connectives.
connective_for_algorithm_formula = NullaryConnective(formula_ts='algorithm')
"""The connective that signals external algorithm formulas.

TODO: Check if connective_for_algorithm_formula is still in use.

"""
connective_for_axiom_formula = let_x_be_a_unary_connective(formula_ts='axiom')
connective_for_axiomatization_formula = let_x_be_a_free_arity_connective(formula_ts='axiomatization')
connective_for_theory_component = let_x_be_a_binary_connective(formula_ts='derivation')
connective_for_enumeration = let_x_be_a_free_arity_connective(formula_ts='enumeration')
connective_for_extension = let_x_be_a_free_arity_connective(formula_ts='extension')
connective_for_hypothesis = let_x_be_a_free_arity_connective(formula_ts='hypothesis')
connective_for_logical_implication = let_x_be_a_binary_connective(formula_ts='implies')
connective_for_inference = let_x_be_a_ternary_connective(formula_ts='inference')
connective_for_inference_rule = let_x_be_a_unary_connective(formula_ts='inference-rule')
connective_for_is_a_propositional_variable = UnaryConnective(formula_ts='is-a-propositional-variable')
connective_for_is_a_valid_proposition = BinaryConnective(formula_ts='is-a-valid-proposition-in')
connective_for_is_inconsistent = UnaryConnective(formula_ts='is-inconsistent')
"""The connective that signals the :math:`is-inconsistent` predicate.

Sample formula: :math:`\\text{is-inconsistent}\\left(\\phi\\right)`
"""
connective_for_is_well_formed_formula = let_x_be_a_unary_connective(formula_ts='is-well-formed-formula')
connective_for_is_well_formed_inference_rule = let_x_be_a_unary_connective(formula_ts='is-well-formed-inference-rule')
connective_for_is_well_formed_proposition = UnaryConnective(formula_ts='is-well-formed-proposition')
connective_for_is_well_formed_theoretical_context = let_x_be_a_unary_connective(
    formula_ts='is-well-formed-theoretical-context')
connective_for_is_well_formed_transformation = let_x_be_a_unary_connective(formula_ts='is-well-formed-transformation')
connective_for_logical_conjunction = let_x_be_a_binary_connective(formula_ts='∧')
connective_for_logical_negation = let_x_be_a_unary_connective(formula_ts='¬')
connective_for_logical_disjunction = let_x_be_a_binary_connective(formula_ts='∨')
connective_for_map = let_x_be_a_binary_connective(formula_ts='map')
connective_for_proves = let_x_be_a_binary_connective(formula_ts='⊢')
connective_for_theorem = let_x_be_a_free_arity_connective(formula_ts='theorem')
connective_for_theory = let_x_be_a_free_arity_connective(formula_ts='theory-formula')
"""The connective that signals a :math:`theory` formula.

Sample formulas: :math:`\\text{tuple}\\left(d_1, d_2, \\ldots\\right)` where :math:`d_n` is a derivation.
"""
connective_for_tupl = let_x_be_a_free_arity_connective(formula_ts='tuple')
"""The connective that signals a :math:`tupl` formula.

Sample formulas: :math:`\\text{tuple}\\left(\\phi, \\psi\\right)`, abbreviated as :math:`\\left(\\phi, \\psi\\right)`.
"""
transformation_by_variable_substitution_connective: FreeArityConnective = let_x_be_a_free_arity_connective(
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
    """Returns ``True`` if :math:`\\phi \\sim_c \\; \\psi`, ``False`` otherwise.

    Definition:
    Two formulas :math:`\\phi` and :math:`\\psi` are :math:`\\text{connective-equivalent}`, noted
    :math:`\\phi \\sim_c \\; \\psi`, if and only if they have equal root connectives.

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
    phi: WellFormedFormula = coerce_formula(phi=phi)
    psi: WellFormedFormula = coerce_formula(phi=psi)
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
        typing.Tuple)[bool, typing.Optional[WellFormedMap]]:
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

    TODO: REVIEW THIS DEFINITION TO EMBED THE DYNAMIC REPLACEMENT OF VARIABLES IN PSI.

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
    variables_fixed_values: WellFormedMap = coerce_map(m=variables_fixed_values, interpret_none_as_empty=True)
    phi: WellFormedFormula = coerce_formula(phi=phi)
    psi: WellFormedFormula = coerce_formula(phi=psi)
    variables: WellFormedEnumeration = coerce_enumeration(e=variables, interpret_none_as_empty=True)

    if any(is_recursively_included_in(f=phi, s=x) for x in iterate_enumeration_elements(e=variables)):
        # If any variable x in the enumeration of variables is a sub-formula of phi,
        # dynamically create new variables and substitute the variables in the template psi with the new ones.
        # In effect, by the definition of a transformation and the definition of formula-equivalence-with-variables,
        # the scope of the variables are strictly limited to the "template" formula, here psi.
        # This avoids any conflict with the possible presence of the template variables in phi.
        # In meta-theory, making derivations on inference-rules for examples,
        # such as with the is-well-formed-inference-rule(i) predicate,
        # there are situations where it is impossible to avoid the presence of such variables in phi.
        variables_2: WellFormedEnumeration = WellFormedEnumeration()
        variables_substitution: WellFormedMap = WellFormedMap()
        for x in iterate_enumeration_elements(e=variables):
            x_substitute: WellFormedVariable = let_x_be_a_variable(
                formula_ts=x.connective.formula_ts.typeset_as_string() + '′')  # TODO: Make "add prime" a function.
            variables_2 = append_element_to_enumeration(e=variables_2, x=x_substitute)
            variables_substitution = append_pair_to_map(m=variables_substitution, preimage=x, image=x_substitute)
        variables = variables_2
        psi: WellFormedFormula = substitute_formulas(phi=psi, m=variables_substitution)

    # check that all variables are atomic formulas
    for x in variables:
        x: WellFormedFormula = coerce_formula(phi=x)
        if x.arity != 0:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_020,
                                      msg=f'the arity of variable "{x}" in variables is not equal to 0.')
        if is_recursively_included_in(f=phi, s=x):
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_021,
                msg=f'Variable `x` is a sub-formula of `phi`.',
                x=x,
                phi=phi,
                psi=psi,
                variables=variables,
                variables_fixed_values=variables_fixed_values)
    # check that all variables in the map are atomic formulas and are correctly listed in variables
    for x in variables_fixed_values.domain:
        x: WellFormedFormula = coerce_formula(phi=x)
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
            psi_value: WellFormedFormula = get_image_from_map(m=variables_fixed_values, preimage=psi)
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
            psi_value: WellFormedFormula = phi
            # extend the map of fixed values
            variables_fixed_values: WellFormedMap = WellFormedMap(d=(*variables_fixed_values.domain, psi,),
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
    """Returns ``True`` if enumeration `s` is a sub-enumeration of enumeration `e`, ``False`` otherwise.

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
    e = coerce_enumeration(e=e, strip_duplicates=strip_duplicates, interpret_none_as_empty=interpret_none_as_empty,
                           canonic_conversion=canonic_conversion)
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
    phi: WellFormedFormula = coerce_enumeration(e=phi, interpret_none_as_empty=True)
    psi: WellFormedFormula = coerce_enumeration(e=psi, interpret_none_as_empty=True)

    test_1 = all(any(is_formula_equivalent(phi=phi_prime, psi=psi_prime) for psi_prime in psi) for phi_prime in phi)
    test_2 = all(any(is_formula_equivalent(phi=psi_prime, psi=phi_prime) for phi_prime in phi) for psi_prime in psi)

    return test_1 and test_2


def substitute_formulas(phi: FlexibleFormula, m: FlexibleMap) -> WellFormedFormula:
    """Performs a top-down, left-to-right substitution of formulas in formula phi.



    References:
        - Rautenberg, Wolfgang. A Concise Introduction to Mathematical Logic - Textbook - 2nd Edition. Springer, 2006.
            see p. 47 on substitutions.

    """
    phi: WellFormedFormula = coerce_formula(phi=phi)
    m: WellFormedMap = coerce_map(m=m, interpret_none_as_empty=True)
    if is_in_map_domain(phi=phi, m=m):
        # phi must be replaced at its root.
        # the replacement algorithm stops right there (i.e.: no more recursion).
        assigned_value: WellFormedFormula = get_image_from_map(m=m, preimage=phi)
        return assigned_value
    else:
        # build the replaced formula.
        fb: WellFormedFormula = WellFormedFormula(con=phi.connective)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = substitute_formulas(phi=term, m=m)
            fb: WellFormedFormula = append_term_to_formula(f=fb, t=term_substitute)
        return fb


def substitute_connectives(phi: FlexibleFormula, m: FlexibleMap) -> WellFormedFormula:
    """Given a formula phi, return a new formula psi structurally equivalent to phi,
    where all connectives are substituted according to the map m.

    :param phi:
    :param m: A map of connectives, where connectives are represented as atomic formulas (c).
    :return:
    """
    phi: WellFormedFormula = coerce_formula(phi=phi)
    m: WellFormedMap = coerce_map(m=m, interpret_none_as_empty=True)
    # TODO: Check that the map domain and codomain are composed of simple objects.
    con: Connective = phi.connective
    c_formula: WellFormedFormula = WellFormedFormula(con=con)
    if is_in_map_domain(phi=c_formula, m=m):
        preimage: WellFormedFormula = WellFormedFormula(con=con)
        image: WellFormedFormula = get_image_from_map(m=m, preimage=preimage)
        con: Connective = image.connective
    # Build the new formula psi with the new connective,
    # and by calling replace_connectives recursively on all terms.
    psi: WellFormedFormula = WellFormedFormula(con=con, t=(substitute_connectives(phi=term, m=m) for term in phi))
    return psi


class WellFormedTupl(WellFormedFormula):
    """A well-formed tuple is a well-formed formula of the form ⌜ :math:`\\text{tuple}\\left( \\boldsymbol{\\phi_1},
    \\boldsymbol{\\phi_2}, \\cdots, \\boldsymbol{\\phi_n} \\right)` ⌝ where :math:`\\boldsymbol{\\phi_i}`
    is a well-formed formula.

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed axiom if and only if:
     - it is a well-formed formula,
     - its root connective is the tuples-formula connective.

    Typesetting
    ^^^^^^^^^^^^^^^^^^^^

    Classical
    ~~~~~~~~~~~~~~~~~~~~
    :math:`\\text{tuple}\\left( \\boldsymbol{\\phi_1},\\boldsymbol{\\phi_2},\\cdots, \\boldsymbol{\\phi_n} \\right)`

    Abbreviated
    ~~~~~~~~~~~~~~~~~~~~
    :math:`\\left( \\boldsymbol{\\phi_1},\\boldsymbol{\\phi_2}, \\cdots, \\boldsymbol{\\phi_n} \\right)`

    Notes
    ^^^^^^^^^^^^^^^^^^^^

    Note 1
    ~~~~~~~~~~~~~~~~~~~~
    The formula terms of tuples are called elements.

    Note 2
    ~~~~~~~~~~~~~~~~~~~~
    The empty-tuple is the tuple with no term, i.e.: :math:`\\left( \\right)`.

    Note 3
    ~~~~~~~~~~~~~~~~~~~~
    The rationale for a dedicated class is semantic. When considering tuples, we do not take into account the
    root connective of the formula, but only its terms.

    Note 4
    ~~~~~~~~~~~~~~~~~~~~
    In Python, the word ``tuple`` is a reserved keyword. For this reason, the word ``tupl`` without the ``e``
    is used instead.
    """

    @staticmethod
    def _data_validation_2(e: FlexibleTupl) -> tuple[Connective, FlexibleTupl]:
        con: Connective = connective_for_tupl
        # TODO: To avoid an infinite loop, we cannot coerce `e` as a tuple here.
        #   As a future improvement, implement here a complementary check on `e`.
        return con, e

    def __new__(cls, e: FlexibleTupl = None):
        """Creates a new instance of :class:`WellFormedTupl`.

        :param e:
        """
        con, e = WellFormedTupl._data_validation_2(e=e)
        o: tuple = super().__new__(cls, con=con, t=e)
        return o

    def __init__(self, e: FlexibleTupl = None):
        """Initializes a new instance of :class:`WellFormedTupl`.

        :param e: The elements of the tupl.
        """
        con, e = WellFormedTupl._data_validation_2(e=e)
        super().__init__(con=connective_for_tupl, t=e)

    def get_index_of_first_equivalent_element(self, phi: WellFormedFormula) -> typing.Optional[int]:
        """Returns the o-based index of the first occurrence of a formula psi in the tuple such that psi ~formula phi.

        TODO: Move this to a base function and remove the method.

        :param phi: A formula.
        :return:
        """
        return self.get_index_of_first_equivalent_term(phi=phi)

    def has_element(self, phi: WellFormedFormula) -> bool:
        """Return True if the tuple has phi as one of its elements.

        TODO: Remove this method and substitute a first-level has_element function.
        """
        return is_term_of_formula(x=phi, phi=self)


FlexibleTupl = typing.Optional[typing.Union[WellFormedTupl, typing.Iterable[FlexibleFormula], tuple, None]]
"""FlexibleTupl is a flexible python type that may be safely coerced into a Tupl."""

FlexibleConnectiveLinkedToAlgorithm = ConnectiveLinkedWithAlgorithm
"""FlexibleConnectiveLinkedToAlgorithm is a flexible python type that may be safely coerced into a 
ConnectiveLinkedToAlgorithm."""


def reduce_map(m: FlexibleFormula, preimage: FlexibleFormula) -> WellFormedMap:
    """Return a new map such that the preimage is no longer an element of its domain."""
    m: WellFormedMap = coerce_map(m=m, interpret_none_as_empty=True)
    preimage: WellFormedFormula = coerce_formula(phi=preimage)
    if is_element_of_enumeration(x=preimage, e=m.domain):
        index: int = get_index_of_first_equivalent_term_in_formula(term=preimage, formula=m.domain)
        reduced_domain: tuple[WellFormedFormula, ...] = (*m.domain[0:index], *m.domain[index + 1:])
        reduced_codomain: tuple[WellFormedFormula, ...] = (*m.codomain[0:index], *m.codomain[index + 1:])
        reduced_map: WellFormedMap = WellFormedMap(d=reduced_domain, c=reduced_codomain)
        return reduced_map
    else:
        return m


def append_element_to_enumeration(e: FlexibleEnumeration, x: FlexibleFormula) -> WellFormedEnumeration:
    """Return a new enumeration e′ such that:
     - all elements of e are elements of e′,
     - x is an element of e′.

    Note: if "x" is an element of "e", then: e ~ e′.

    Definition (extend an enumeration "e" with an element "x"):
    Cf. the definition of enumeration.
    If "x" is an element of "e", return "e".
    If "x" is not an element of "e", and `s` is the sequence of terms in "e", return "(s, e)".
    """
    e: WellFormedEnumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    x: WellFormedFormula = coerce_formula(phi=x)
    if is_element_of_enumeration(x=x, e=e):
        # "x" is an element of "e":
        return e
    else:
        # "x" is not an element of "e":
        extended_enumeration: WellFormedEnumeration = WellFormedEnumeration(e=(*e, x,))
        return extended_enumeration


def append_element_to_tuple(t: FlexibleTupl, x: FlexibleFormula) -> WellFormedTupl:
    """Return a new extended punctilious-tuple such that element is a new element appended to its existing elements.
    """
    t: WellFormedTupl = coerce_tuple(s=t, interpret_none_as_empty=True)
    x: WellFormedFormula = coerce_formula(phi=x)
    extended_tupl: WellFormedTupl = WellFormedTupl(e=(*t, x,))
    return extended_tupl


def append_tuple_to_tuple(t1: FlexibleTupl, t2: FlexibleTupl) -> WellFormedTupl:
    """Return a new tuple which appends all the elements of `t2` to `t1`.
    """
    t1: WellFormedTupl = coerce_tuple(s=t1, interpret_none_as_empty=True, canonic_conversion=True)
    t2: WellFormedTupl = coerce_tuple(s=t2, interpret_none_as_empty=True, canonic_conversion=True)
    t3: WellFormedTupl = WellFormedTupl(e=(*t1, *t2,))
    return t3


def append_term_to_formula(f: FlexibleFormula, t: FlexibleFormula) -> WellFormedFormula:
    """Return a new extended formula such that term is a new term appended to its existing terms.
    """
    f: WellFormedFormula = coerce_formula(phi=f)
    t: WellFormedFormula = coerce_formula(phi=t)
    extended_formula: WellFormedFormula = WellFormedFormula(t=(*f, t,), con=f.connective)
    return extended_formula


def append_pair_to_map(m: FlexibleMap, preimage: FlexibleFormula, image: FlexibleFormula) -> WellFormedMap:
    """Return a new map m2 with a new (preimage, image) pair.
    If the preimage is already defined in m, replace it.

    :param m:
    :param preimage:
    :param image:
    :return:
    """
    m: WellFormedMap = coerce_map(m=m, interpret_none_as_empty=True)
    preimage: WellFormedFormula = coerce_formula(phi=preimage)
    # Reduce the map to assure the preimage is no longer an element of its domain.
    m: WellFormedMap = reduce_map(m=m, preimage=preimage)
    extended_domain: tuple[WellFormedFormula, ...] = (*m.domain, preimage)
    extended_codomain: tuple[WellFormedFormula, ...] = (*m.codomain, image)
    m: WellFormedMap = WellFormedMap(d=extended_domain, c=extended_codomain)
    return m


def get_image_from_map(m: FlexibleMap, preimage: FlexibleFormula) -> WellFormedFormula:
    """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
    if is_in_map_domain(phi=preimage, m=m):
        index_position: int = get_index_of_first_equivalent_element_in_enumeration(x=preimage, e=m.domain)
        return m.codomain[index_position]
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_028, msg='Map domain does not contain this element')


class WellFormedMap(WellFormedFormula):
    """A map is a formula m(t0(k0, k1, ..., kn), t1(l0, l1, ..., ln)) where:
     - m is a node with the map connective.
     - t0 is an enumeration named the keys' enumeration.
     - t1 is a tuple named the values tuple.
     - the cardinality of t0 is equal to the cardinality of 1.

    Syntax:
    :math:`\\text{map}\\left( \\{ i_1, i_2, \\cdots, i_n \\}, \\left( o_1, o_2, \\cdots, o_m \\right) \\right)`

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
    def _data_validation_2(d: FlexibleEnumeration = None, c: FlexibleTupl = None) -> tuple[
        WellFormedEnumeration, WellFormedTupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param d:
        :param c:
        :return:
        """
        d: WellFormedEnumeration = coerce_enumeration(
            e=d, strip_duplicates=True, interpret_none_as_empty=True, canonic_conversion=True)
        c: WellFormedTupl = coerce_tuple(s=c, interpret_none_as_empty=True, canonic_conversion=True)
        if len(d) != len(c):
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_027, msg='Map: |keys| != |values|')
        return d, c

    def __new__(cls, d: FlexibleEnumeration = None, c: FlexibleTupl = None):
        """Creates a well-formed-map of python-type Map.

        :param d: An enumeration denoted as the domain of the map.
        :param c: An enumeration denoted as the codomain of the map.
        """
        d, c = WellFormedMap._data_validation_2(d=d, c=c)
        o: tuple = super().__new__(cls, con=connective_for_map, t=(d, c,))
        return o

    def __init__(self, d: FlexibleEnumeration = None, c: FlexibleTupl = None):
        """Creates a well-formed-map of python-type Map.

        :param d: An enumeration denoted as the domain of the map.
        :param c: An enumeration denoted as the codomain of the map.
        """
        d, c = WellFormedMap._data_validation_2(d=d, c=c)
        super().__init__(con=connective_for_map, t=(d, c,))

    @property
    def codomain(self) -> WellFormedTupl:
        """A tuple of formulas denoted as the codomain of the map.

        The codomain of a map is the enumeration of possible outputs of the get_image_from_map function.
        """
        return coerce_tuple(s=self[WellFormedMap.CODOMAIN_INDEX])

    @property
    def domain(self) -> WellFormedEnumeration:
        """An enumeration of formulas denoted as the domain of the map.

        The domain of a map is the enumeration of possible inputs of the get_image_from_map function.
        """
        return coerce_enumeration(e=self[WellFormedMap.DOMAIN_INDEX])


FlexibleMap = typing.Optional[typing.Union[WellFormedMap, typing.Dict[WellFormedFormula, WellFormedFormula]]]
"""FlexibleMap is a flexible python type that may be safely coerced into a Map."""


def strip_duplicate_formulas_in_python_tuple(t: tuple[WellFormedFormula, ...]) -> tuple[WellFormedFormula, ...]:
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


class WellFormedEnumeration(WellFormedFormula):
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
        global connective_for_enumeration
        con: Connective = connective_for_enumeration
        if e is None:
            e = tuple()
        else:
            e = tuple(element for element in e)
        # e = coerce_tuple(t=e, interpret_none_as_empty=True)
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
        c, e = WellFormedEnumeration._data_validation_2(e=e, strip_duplicates=strip_duplicates)
        o: tuple = super().__new__(cls, con=c, t=e, **kwargs)
        return o

    def __init__(self, e: FlexibleEnumeration = None,
                 strip_duplicates: bool = False, **kwargs):
        c, e = WellFormedEnumeration._data_validation_2(e=e, strip_duplicates=strip_duplicates)
        super().__init__(con=c, t=e, **kwargs)


FlexibleEnumeration = typing.Optional[typing.Union[WellFormedEnumeration, typing.Iterable[FlexibleFormula]]]
"""FlexibleEnumeration is a flexible python type that may be safely coerced into an Enumeration."""


class EmptyEnumeration(WellFormedEnumeration):
    """An empty-enumeration is an enumeration that has no element.
    """

    def __new__(cls):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        return super().__new__(cls=cls, e=None)

    def __init__(self):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        super().__init__(e=None)


class SingletonEnumeration(WellFormedEnumeration):
    """A singleton-enumeration is an enumeration that has exactly one element.
    """

    def __new__(cls, element: FlexibleFormula):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        element: WellFormedFormula = coerce_formula(phi=element)
        return super().__new__(cls=cls, e=(element,))

    def __init__(self, element: FlexibleFormula):
        # re-use the enumeration-builder __init__ to assure elements are unique and order is preserved.
        element: WellFormedFormula = coerce_formula(phi=element)
        super().__init__(e=element)


class ABCTransformation(WellFormedFormula, abc.ABC):
    """Abstract class.

    TODO: Consider renaming transformation to functor, or theory-morphism. Not sure which one is more accurate.
    TODO: Consider removing this abstract class, not sure we need other transformations than variable substitution.

    A transformation is a method by which new formulas may be created.

    The following transformations are supported:
     - transformation-by-variable-substitution (cf. NaturalTransformation python-class)
     - algorithmic-transformation (cf. AlgorithmicTransformation python-class)


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
            i: FlexibleTupl | None = None,
            a: FlexibleConnectiveLinkedToAlgorithm | None = None) -> tuple[
        Connective, WellFormedFormula, WellFormedEnumeration, WellFormedEnumeration, WellFormedTupl, ConnectiveLinkedWithAlgorithm | None]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param con:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :return:
        """
        con: Connective = coerce_connective(con=con)
        o: WellFormedFormula = coerce_formula(phi=o)
        v: WellFormedEnumeration = coerce_enumeration(e=v, interpret_none_as_empty=True, canonic_conversion=True,
                                                      strip_duplicates=True)
        d: WellFormedEnumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, canonic_conversion=True,
                                                      strip_duplicates=True)
        i: WellFormedTupl = coerce_tuple(s=i, interpret_none_as_empty=True, canonic_conversion=True)
        # TODO: Coerce argument ``a`` as well
        return con, o, v, d, i, a

    def __new__(cls,
                con: Connective,
                o: FlexibleFormula,
                v: FlexibleEnumeration | None = None,
                d: FlexibleEnumeration | None = None,
                i: FlexibleTupl | None = None,
                a: FlexibleConnectiveLinkedToAlgorithm | None = None):
        """

        :param con:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        con, o, v, d, i, a = ABCTransformation._data_validation_2(con=con, o=o, v=v, d=d, i=i, a=a)
        if a is None:
            o: tuple = super().__new__(cls, con=transformation_by_variable_substitution_connective,
                                       t=(o, v, d, i,))
        else:
            o: tuple = super().__new__(cls, con=transformation_by_variable_substitution_connective,
                                       t=(o, v, d, i, a,))
        return o

    def __init__(self, con: Connective,
                 o: FlexibleFormula,
                 v: FlexibleEnumeration | None = None,
                 d: FlexibleEnumeration | None = None,
                 i: FlexibleTupl | None = None,
                 a: FlexibleConnectiveLinkedToAlgorithm | None = None):
        """

        :param con:
        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        """
        con, o, v, d, i, a = ABCTransformation._data_validation_2(con=con, o=o, v=v, d=d, i=i, a=a)
        if a is None:
            super().__init__(con=transformation_by_variable_substitution_connective, o=o, v=v, d=d, i=i)
        else:
            super().__init__(con=transformation_by_variable_substitution_connective, o=o, v=v, d=d, i=i, a=a)

    def __call__(self, i: FlexibleTupl | None = None) -> WellFormedFormula:
        """A shortcut for self.apply_transformation()

        :param i: A tuple of formulas denoted as the input arguments.
        :return:
        """
        return self.apply_transformation(i=i)

    @abc.abstractmethod
    def apply_transformation(self, i: FlexibleTupl | None = None) -> WellFormedFormula:
        """

        :param i: A tuple of formulas denoted as the input values, or input arguments.
        :return: A formula denoted as the output value.
        """
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_058,
                                  msg='Transformation failure. Abstract python method is not implemented.',
                                  object=self,
                                  i=i)

    @property
    def output_shape(self) -> WellFormedFormula:
        """The shape of the output returned by the transformation.

        The output-shape is expressed as an arbitrary formula that may contain variables as sub-formulas.

        :return:
        """
        return self[ABCTransformation.OUTPUT_SHAPE_INDEX]

    @property
    def output_declarations(self) -> WellFormedEnumeration:
        """A list of variables that are not present in the input-shapes,
        and that correspond to newly declared objects in the transformation output."""
        return self[ABCTransformation.DECLARATIONS_INDEX]

    @abc.abstractmethod
    def is_compatible_with(self, t: FlexibleFormula) -> bool:
        """A computing low-cost method tha informs a calling process whether trying to use this transformation
        is worthwhile in trying to yield formula ``t``.
        
        The idea here is to make an early check on the compatibility of the transformation with a certain 
        target formula ``t``, before engaging in a brute-force attempt to derive a certain statement.

        :param t: A formula denoted as the target.
        :return:
        """
        raise u1.ApplicativeError(msg='abstract method')

    @property
    def input_shapes(self) -> WellFormedTupl:
        """A tuple of formulas that provide the shape of arguments (aka input values) expected by the transformation.
        Shapes are expressed as arbitrary formulas that may contain variables (cf. variables property).
        The transformation formula thus declares that it expect to receive as input values a tuple of formulas
        that are formula-equivalent-with-variables with those shapes."""
        return self[ABCTransformation.INPUT_SHAPES_INDEX]

    @property
    def variables(self) -> WellFormedEnumeration:
        """Variables used to express the shapes of arguments and the conclusion."""
        return self[ABCTransformation.VARIABLES_INDEX]


class WellFormedTransformationByVariableSubstitution(ABCTransformation, ABC):
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

    DATA_VALIDATION_ALGORITHM_INDEX: int = 4

    @staticmethod
    def _data_validation_3(
            o: FlexibleFormula,
            v: FlexibleEnumeration | None = None,
            d: FlexibleEnumeration | None = None,
            i: FlexibleTupl | None = None,
            a: FlexibleConnectiveLinkedToAlgorithm = None
    ) -> tuple[
        Connective, WellFormedFormula, WellFormedEnumeration, WellFormedEnumeration, WellFormedTupl, ConnectiveLinkedWithAlgorithm | None]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :param a: (Conditional) A formula referencing an external algorithm used to validate input-values.
        :return:
        """
        con: Connective = transformation_by_variable_substitution_connective
        o: WellFormedFormula = coerce_formula(phi=o)
        v: WellFormedEnumeration = coerce_enumeration(e=v, interpret_none_as_empty=True)
        d: WellFormedEnumeration = coerce_enumeration(e=d, interpret_none_as_empty=True)
        i: WellFormedTupl = coerce_tuple(s=i, interpret_none_as_empty=True, canonic_conversion=True)
        if a is not None:
            pass
            # TODO: Implement the coerce_connective_linked_with_algorithm function
            # d: ConnectiveLinkedWithAlgorithm = coerce_connective_linked_with_algorithm(c=d)
        return con, o, v, d, i, a

    def __new__(cls, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                d: FlexibleEnumeration | None = None,
                i: FlexibleTupl | None = None, a: FlexibleConnectiveLinkedToAlgorithm | None = None):
        """

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :param a: (Conditional) A formula referencing an external algorithm used to validate input-values.
        """
        con, o, v, d, i, a = WellFormedTransformationByVariableSubstitution._data_validation_3(o=o, v=v, d=d, i=i, a=a)
        o: WellFormedFormula  # Why is this type not properly detected by the PyCharm IDE?
        if a is None:
            o: tuple = super().__new__(cls, con=con, o=o, v=v, d=d, i=i)
        else:
            o: tuple = super().__new__(cls, con=con, o=o, v=v, d=d, i=i, a=a)
        return o

    def __init__(self, o: FlexibleFormula, v: FlexibleEnumeration | None = None,
                 d: FlexibleEnumeration | None = None,
                 i: FlexibleTupl | None = None, a: FlexibleConnectiveLinkedToAlgorithm | None = None):
        """

        :param v: An enumeration of variables that may be used in the input-shapes and output-shape.
        :param d: An enumeration of variables used to reference new object declarations in the output-shape.
        :param i: A tuple of formulas denoted as the input-shapes.
        :param o: A formula denoted as the output-shape.
        :param a: (Conditional) A formula referencing an external algorithm used to validate input-values.
        """
        c2, o, v, d, i, a = WellFormedTransformationByVariableSubstitution._data_validation_3(o=o, v=v, d=d, i=i, a=a)
        if a is None:
            super().__init__(con=c2, o=o, v=v, d=d, i=i)
        else:
            super().__init__(con=c2, o=o, v=v, d=d, i=i, a=a)

    def __call__(self, i: FlexibleTupl | None = None) -> WellFormedFormula:
        """A shortcut for self.apply_transformation()

        :param i: A tuple of formulas denoted as the input-values.
        :return:
        """
        return self.apply_transformation(i=i)

    def apply_transformation(self, i: FlexibleTupl | None = None) -> WellFormedFormula:
        """

        :param i: A tuple of formulas denoted as the input-values.
        :return:
        """
        i = coerce_tuple(s=i, interpret_none_as_empty=True)

        # step 0: re-declares all variables dynamically.
        # this is necessary to prevent issues in meta-theories,
        # where the variable is a sub-formula of the input.
        # ex: is-well-formed-inference-rule(i).
        variables = WellFormedEnumeration()
        variables_substitution = WellFormedMap()
        for v in iterate_enumeration_elements(e=self.variables):
            v2 = let_x_be_a_variable(formula_ts=v.connective.formula_ts)
            variables = append_element_to_enumeration(e=variables, x=v2)
            variables_substitution = append_pair_to_map(m=variables_substitution, preimage=v, image=v2)
        for d in iterate_enumeration_elements(e=self.output_declarations):
            if not is_element_of_enumeration(x=d, e=variables):
                d2 = let_x_be_a_variable(formula_ts=d.connective.formula_ts)
                variables = append_element_to_enumeration(e=variables, x=d2)
                variables_substitution = append_pair_to_map(m=variables_substitution, preimage=d, image=d2)
        input_shapes = substitute_formulas(phi=self.input_shapes, m=variables_substitution)
        output_shape = substitute_formulas(phi=self.output_shape, m=variables_substitution)
        output_declarations = substitute_formulas(phi=self.output_declarations, m=variables_substitution)

        # step 1: confirm every argument is compatible with its premises,
        # and seize the opportunity to retrieve the mapped variable values.
        success, variables_values = is_formula_equivalent_with_variables_2(phi=i, psi=input_shapes,
                                                                           variables=variables,
                                                                           variables_fixed_values=None)
        if not success:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_030,
                msg='Transformation failure. '
                    'The input-values `i` are incompatible with the input-shapes `s`, '
                    'of transformation `f` considering variables `v`.',
                i=i, s=input_shapes,
                v=variables, f=self)

        # Step 1b: If an external-algorithm validation is configured on this transformation,
        # call it to check the validity of the input values.
        if self.validation_algorithm is not None:
            try:
                ok, output_value = self.validation_algorithm(i=i, raise_error_if_false=True)
            except u1.ApplicativeError as err:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_086,
                                          msg='Transformation failure. '
                                              'The tuple of input-values `i` is incompatible with '
                                              'the validation-algorithm `a`, '
                                              'of transformation `f`. '
                                              'The tuple of input-shapes `i2` '
                                              'and the tuple of variables `v` are provided for information.',
                                          i=i,
                                          a=self.validation_algorithm,
                                          i2=input_shapes,
                                          v=variables,
                                          f=self)

        # step 2:
        outcome: WellFormedFormula = substitute_formulas(phi=output_shape, m=variables_values)

        # step 3: new objects declarations.
        declarations_map: WellFormedMap = WellFormedMap()
        for declaration in output_declarations:
            con: Connective = Connective()
            simple_formula: WellFormedFormula = WellFormedFormula(con=con)
            # TODO: Find a way to initialize the new_connective formula_typesetter.
            # TODO: Find a way to initialize the new_connective arity.
            declarations_map: WellFormedMap = append_pair_to_map(m=declarations_map, preimage=declaration,
                                                                 image=simple_formula)

        # step 4: substitute new-object-declarations in the conclusion
        outcome: WellFormedFormula = substitute_connectives(phi=outcome, m=declarations_map)

        return outcome

    def is_compatible_with(self, t: FlexibleFormula) -> bool:
        """Performs low-cost checks and returns True if target formula ``t`` is compatible with the output of the
        transformation. This is useful to avoid expensive brute-force to find some derivation in a theory,
        when it is clear from the beginning that the underlying transformation.

        :param t:
        :return:
        """
        is_candidate, _ = is_formula_equivalent_with_variables_2(phi=self.output_shape, psi=t, variables=self.variables)
        return is_candidate

    @property
    def validation_algorithm(self) -> typing.Callable[
                                          [FlexibleTupl, bool], typing.Tuple[
                                              bool, typing.Optional[WellFormedFormula]]] | None:
        """(Conditional). A transformation-by-variable-substitution may have a validation-algorithm.

        A validation-algorithm is a python-function that receives the input-values as input arguments
        and return ``True`` if these input-values are valid, and ``False``otherwise.

        :return:
        """
        if self.arity == 5:
            phi: WellFormedFormula = self[
                WellFormedTransformationByVariableSubstitution.DATA_VALIDATION_ALGORITHM_INDEX]
            con: Connective = phi.connective
            if isinstance(con, ConnectiveLinkedWithAlgorithm):
                con: ConnectiveLinkedWithAlgorithm = con
                algo = con.algorithm
                return algo
            else:
                raise u1.ApplicativeError(
                    msg='Connective is not of ConnectiveLinkedWithAlgorithm type.',
                    phi=phi,
                    con=con,
                    self=self)
        else:
            return None


FlexibleTransformationByVariableSubstitution = typing.Optional[
    typing.Union[WellFormedTransformationByVariableSubstitution]]


def coerce_transformation(f: FlexibleTransformation) -> ABCTransformation:
    """Coerces lose argument `f` to a transformation, strongly python-typed as Transformation,
    or raises an error with code E-AS1-060 if this fails."""
    f: WellFormedFormula = coerce_formula(phi=f)
    if isinstance(f, ABCTransformation):
        return f
    elif is_well_formed_transformation_by_variable_substitution(t=f):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        # TODO: Move this logic to coerce_natural_transformation
        return WellFormedTransformationByVariableSubstitution(
            o=f[WellFormedTransformationByVariableSubstitution.OUTPUT_SHAPE_INDEX],
            v=f[WellFormedTransformationByVariableSubstitution.VARIABLES_INDEX],
            d=f[WellFormedTransformationByVariableSubstitution.DECLARATIONS_INDEX],
            i=f[WellFormedTransformationByVariableSubstitution.INPUT_SHAPES_INDEX])
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_060,
            msg='`t` could not be coerced to a transformation.',
            m=f)


def coerce_transformation_by_variable_substitution(
        t: FlexibleFormula) -> WellFormedTransformationByVariableSubstitution:
    """Coerces lose argument ``t`` to a transformation, strongly python-typed as Transformation,
    or raises an error with code E-AS1-031 if this fails."""
    t: WellFormedFormula = coerce_formula(phi=t)
    if isinstance(t, WellFormedTransformationByVariableSubstitution):
        return t
    elif isinstance(t, WellFormedFormula) and is_well_formed_transformation_by_variable_substitution(t=t):
        # phi is a well-formed transformation,
        # it can be safely re-instantiated as a Transformation and returned.
        return WellFormedTransformationByVariableSubstitution(
            o=t[WellFormedTransformationByVariableSubstitution.OUTPUT_SHAPE_INDEX],
            v=t[WellFormedTransformationByVariableSubstitution.VARIABLES_INDEX],
            d=t[WellFormedTransformationByVariableSubstitution.DECLARATIONS_INDEX],
            i=t[WellFormedTransformationByVariableSubstitution.INPUT_SHAPES_INDEX])
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


def coerce_connective(con: Connective) -> Connective:
    if isinstance(con, Connective):
        return con
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_059,
            msg='`con` could not be coerced to a connective.',
            c=con, c_type=type(con))


def coerce_hypothesis(h: FlexibleFormula) -> WellFormedHypothesis:
    """Coerces formula ``h`` into a well-formed hypothesis, or raises an error if it fails.

    :param h: A formula that is presumably a well-formed hypothesis.
    :return: A well-formed hypothesis.
    :raises ApplicativeError: with code AS1-083 if coercion fails.
    """
    if isinstance(h, WellFormedHypothesis):
        return h
    elif is_well_formed_hypothesis(h=h):
        b: WellFormedExtension = coerce_extension(e=h[WellFormedHypothesis.BASE_THEORY_INDEX])
        a: WellFormedAxiom = coerce_axiom(a=h[WellFormedHypothesis.ASSUMPTION_INDEX])
        return WellFormedHypothesis(b=b, a=a)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_083,
            msg='`h` cannot be coerced to a well-formed hypothesis.',
            h=h)


def coerce_simple_object(o: FlexibleSimpleObject) -> WellFormedSimpleObject:
    """Coerces formula `o` into a well-formed simple-object, or raises an error if it fails.

    :param o: A formula that is presumably a well-formed simple-object.
    :return: A well-formed simple-object.
    :raises ApplicativeError: with code AS1-087 if coercion fails.
    """
    o: WellFormedFormula = coerce_formula(phi=o)
    if isinstance(o, WellFormedSimpleObject):
        return o
    elif is_well_formed_simple_object(o=o):
        con: Connective = o.connective
        return WellFormedSimpleObject(c=con)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_087,
            msg='`o` cannot be coerced to a well-formed simple-object.',
            o=o)


def coerce_inference(i: FlexibleFormula) -> WellFormedInference:
    """Coerces formula `i` into a well-formed inference, or raises an error if it fails.

    :param i: A formula that is presumably a well-formed inference.
    :return: A well-formed inference.
    :raises ApplicativeError: with code AS1-032 if coercion fails.
    """
    if isinstance(i, WellFormedInference):
        return i
    elif is_well_formed_inference(i=i):
        i2: WellFormedInferenceRule = coerce_inference_rule(i=i[WellFormedInference.INFERENCE_RULE_INDEX])
        p: WellFormedTupl = coerce_tuple(s=i[WellFormedInference.PREMISES_INDEX], interpret_none_as_empty=True)
        a: WellFormedTupl = coerce_tuple(s=i[WellFormedInference.ARGUMENTS_INDEX], interpret_none_as_empty=True)
        return WellFormedInference(i=i2, p=p, a=a)
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


def is_well_formed_proposition(p: FlexibleFormula, t: FlexibleTheoreticalContext | None = None,
                               raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if it is proven that ``p`` is a well-formed proposition, ``False`` otherwise.

    Note 1: *Being a proposition* is a property that is relative to a theoretical context. In effect, some formula
    may be recognized as a proposition in some theoretical context and not in others. For example, a logic
    may be defined with negation and implication as its sole operators. In that logic, :math:`P \\lor Q` is not
    a recognized proposition. But in a different logic where disjunction is defined, the same formula is a
    proposition. It follows that the property of being a proposition is a local definition with regard to
    some theoretical context.

    Note 2: To positively answer the question: "is :math:`P` a well-formed proposition with regard to
    theoretical context :math:`T` ?", it is necessary that
    :math:`T \\; \\vdash \\; \\left( \\text{is-well-formed-proposition}(P) \\right)`. It follows that this
    function may return ``False`` if :math:`\\text{is-well-formed-proposition}(P)` is not proven (yet) in
    :math:`T`, even though it may be possible to prove it with complementary derivations.

    Global definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`P` is a well-formed proposition if and only if:
     - :math:`P` is a well-formed formula.

    Local definition
    ~~~~~~~~~~~~~~~~~
    A formula :math:`P` is a well-formed proposition with regard to some theoretical context :math:`T` if and only if:
     - :math:`P` is globally a well-formed proposition.
     - :math:`T \\; \\vdash \\; \\left( \\text{is-well-formed-proposition}(P) \\right)`

    TODO: We may wish to add a conditional parameter ``auto_derive`` but then we should return a tuple (b, T).
        Reconsider this.

    :param p: A formula.
    :param t: (conditional) A theoretical context.
    :return: ``True`` if ``p`` is a well-formed proposition, ``False`` otherwise. The global definition is used it
    ``t`` is ``None``, the local definition with regard to ``t`` is used instead.
    """
    global connective_for_is_well_formed_proposition

    # Global definition
    # Condition #1: P is a well-formed formula.
    p: WellFormedFormula = coerce_formula(phi=p)

    if t is not None:
        # Local definition
        t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
        # Condition #2: T ⊢ is-a-proposition(P).
        p_is_a_proposition: WellFormedFormula = connective_for_is_well_formed_proposition(p)
        ok = is_valid_proposition_so_far_1(p=p_is_a_proposition, t=t)
        if not ok:
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    msg='Locally ill-formed proposition. `p` is not demonstrated as valid in n`t`.',
                    p=p, t=t, raise_error_if_false=raise_error_if_false
                )
            return False

    # All necessary conditions are fulfilled.
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
    t: WellFormedFormula = coerce_formula(phi=t)
    if t.connective is not connective_for_tupl:
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


def is_well_formed_hypothesis(
        h: FlexibleHypothesis,
        t: FlexibleTheoreticalContext | None = None,
        raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if and only if ``h`` is a well-formed hypothesis, ``False`` otherwise.

    TODO: Check that assumption is a proposition instead of just checking it is a formula.

    :param t:
    :param h: A formula that may or may not be a well-formed hypothesis.
    :param raise_error_if_false: If the argument is ``True``, the function raises an AS1-082 error instead of returning
        ``False``.
    :return: bool.
    """
    h: WellFormedFormula = coerce_formula(phi=h)
    if isinstance(h, WellFormedHypothesis):
        if t is not None:
            # Check local well-formedness.
            ok: bool = is_axiomatization_equivalent(t1=t, t2=h.base_theory, raise_error_if_false=False)
            if not ok:
                if raise_error_if_false:
                    raise u1.ApplicativeError(
                        msg='Locally ill-formed hypothesis. `h` is a globally well-formed hypothesis but it is not locally '
                            'well-formed with regard to `t`, because its base theory is not axiomatically equivalent to '
                            '`t`.',
                        h=h,
                        t=t,
                        raise_error_if_false=raise_error_if_false)
                else:
                    return False
        return True
    elif (h.connective is not connective_for_hypothesis or
          not h.arity >= 2 or
          not is_well_formed_extension(e=h[WellFormedHypothesis.BASE_THEORY_INDEX], t=t) or
          not is_well_formed_axiom(a=h[WellFormedHypothesis.ASSUMPTION_INDEX])):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_082,
                msg='Globally ill-formed hypothesis. `h` is not a globally well-formed hypothesis.',
                h=h, t=t, raise_error_if_false=raise_error_if_false
            )
        else:
            return False
    else:
        if t is not None:
            # Use recursion to check local well-formedness.
            h: WellFormedHypothesis = coerce_hypothesis(h=h)
            return is_well_formed_hypothesis(h=h, t=t, raise_error_if_false=raise_error_if_false)
        return True


def is_well_formed_inference(i: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if and only if `i` is a well-formed inference, ``False`` otherwise.

    :param i: A formula that may or may not be a well-formed inference.
    :param raise_error_if_false: If the argument is ``True``, the function raises an AS1-081 error instead of returning
        ``False``.
    :return: bool.
    """
    i = coerce_formula(phi=i)
    if (i.connective is not connective_for_inference or
            not i.arity == 3 or
            not is_well_formed_inference_rule(i=i[WellFormedInference.INFERENCE_RULE_INDEX]) or
            not is_well_formed_tupl(t=i[WellFormedInference.PREMISES_INDEX]) or
            not is_well_formed_tupl(t=i[WellFormedInference.ARGUMENTS_INDEX])):
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
    if (m.connective is not connective_for_map or
            not m.arity == 2 or
            not is_well_formed_enumeration(e=m[WellFormedMap.DOMAIN_INDEX]) or
            not is_well_formed_tupl(t=m[WellFormedMap.CODOMAIN_INDEX])):
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
    global connective_for_enumeration
    if e is None:
        # This is debatable.
        # Implicit conversion of None to the empty enumeration.
        return True
    else:
        e = coerce_formula(phi=e)
        if e.connective is not connective_for_enumeration:
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
    if isinstance(i, WellFormedInferenceRule):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif (i.connective is connective_for_inference_rule and
          i.arity == 1 and
          is_well_formed_transformation(t=i.term_0)
    ):
        return True
    else:
        return False


def is_well_formed_transformation(t: FlexibleFormula) -> bool:
    """Return True if and only if ``t`` is a well-formed transformation, False otherwise.

    :param t: A formula.
    :return: bool.
    """
    t = coerce_formula(phi=t)
    if isinstance(t, ABCTransformation):
        # Shortcut: the class assures the well-formedness of the formula.
        return True
    elif is_well_formed_transformation_by_variable_substitution(t=t):
        return True
    else:
        return False


def is_valid_proposition_so_far_1(p: FlexibleFormula, t: FlexibleTheoreticalContext | None = None,
                                  d: FlexibleEnumeration[FlexibleComponent] | None = None,
                                  strip_duplicates: bool = True,
                                  interpret_none_as_empty: bool = True,
                                  canonic_conversion: bool = True,
                                  max_components: int | None = None) -> bool:
    """Returns ``True`` if and only if proposition `p` is valid in theory ``t``,
    according to ``t`` known derivations, ``False`` otherwise.

    Alternatively, check validity of `p` in an enumeration of derivations `d`.

    Note: the expression "so far" is meant to stress that more derivations may be inferred from ``t``,
    and it is a priori unknown whether such derivations would or would not prove `p`.

    A formula :math:`\\phi` is a valid-statement with regard to a theory :math:`t`, if and only if:
     - :math:`\\phi` is the valid-statement of an axiom in :math:`t`,
     - or :math:`\\phi` is the valid-statement of a theorem in :math:`t`.

    :param p:
    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Verifies the validity of `p` only through the first `max_components` derivations
        in canonical order, or all derivations if `None`.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    p: WellFormedFormula = coerce_formula(phi=p)
    if t is not None:
        t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, interpret_none_as_empty=False)
    else:
        d: WellFormedEnumeration = coerce_enumeration(e=d, strip_duplicates=True, interpret_none_as_empty=True,
                                                      canonic_conversion=True)
    return any(is_formula_equivalent(phi=p, psi=valid_statement) for valid_statement in
               iterate_theory_propositions(
                   t=t,
                   d=d,
                   recurse_extensions=True,
                   strip_duplicates=strip_duplicates,
                   interpret_none_as_empty=interpret_none_as_empty,
                   canonic_conversion=canonic_conversion,
                   max_components=max_components))
    # t.iterate_valid_statements())


def is_valid_proposition_so_far_2(p: FlexibleFormula, t: FlexibleTheory) -> tuple[bool, int | None]:
    """Given a theory ``t`` and a proposition `p`, return a pair ("b", `i`) such that:
     - "b" is True if `p` is a valid proposition in theory ``t``, False otherwise,
     - `i` is the derivation-index of the first occurrence of `p` in a derivation in ``t`` if "b" is True,
        None otherwise.

    Note: the expression "so far" is meant to stress that more derivations may be inferred from ``t``,
    and it is a priori unknown whether such derivations would or would not prove `p`.

    This function is very similar to is_valid_proposition_in_theory_1 except that it returns
    the index of the first occurrence of a derivation that matches p. This information is typically
    required in function would_be_valid_derivation_enumeration_in_theory to check whether
    some propositions are successors or predecessors to some other propositions and verify
    derivation validity.

    Definition:
    A formula p is a valid-proposition with regard to a theory ``t``, if and only if:
     - `p` is the valid-proposition of an axiom in ``t``,
     - or `p` is the valid-proposition of a theorem in ``t``.
    """

    p: WellFormedFormula = coerce_formula(phi=p)
    t: WellFormedTheory = coerce_theory(t=t)
    for d, i in zip(iterate_theory_components(t=t), range(count_theory_components(t=t))):
        if is_formula_equivalent(phi=p, psi=d.valid_statement):
            return True, i
    return False, None


def iterate_formula_terms(phi: FlexibleFormula, max_terms: int | None = None
                          ) -> typing.Generator[WellFormedFormula, None, None]:
    """Iterates the terms of a well-formed formula in canonical order.

    :param phi: A well-formed formula.
    :param max_terms: Yields all terms if ``None`` (default), or yields only the ``max_terms`` first elements,
    :return:
    """
    phi: WellFormedFormula = coerce_formula(phi=phi)
    yield from itertools.islice(phi, max_terms)


def iterate_tuple_elements(phi: FlexibleTupl, max_elements: int | None = None
                           ) -> typing.Generator[WellFormedFormula, None, None]:
    """Iterates the elements of a tuple in canonical order.

    :param phi: A formula.
    :param max_elements: Yields only math:`max_elements` elements, or all elements if None.
    :return:
    """
    phi = coerce_tuple(s=phi)
    yield from iterate_formula_terms(phi=phi, max_terms=max_elements)


def iterate_enumeration_elements(e: FlexibleEnumeration, max_elements: int | None = None,
                                 interpret_none_as_empty: bool | None = None, strip_duplicates: bool | None = None,
                                 canonic_conversion: bool | None = None
                                 ) -> typing.Generator[WellFormedFormula, None, None]:
    """Iterates the elements of an enumeration in canonical order.

    :param e:
    :param max_elements: Yields only math:`max_elements` elements, or all elements if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `e` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `e` to enumeration. Raise an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `e` to enumeration.
    :return:
    """
    e: WellFormedEnumeration = coerce_enumeration(e=e, interpret_none_as_empty=interpret_none_as_empty,
                                                  strip_duplicates=strip_duplicates,
                                                  canonic_conversion=canonic_conversion)
    yield from iterate_formula_terms(phi=e, max_terms=max_elements)


def are_valid_statements_in_theory(s: FlexibleTupl, t: FlexibleTheoreticalContext,
                                   raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if every formula ``phi`` in enumeration ``s`` is a valid-statement in theoretical context ``t``,
    ``False`` otherwise.

    :param s: A tuple of (possibly valid) statements.
    :param t: A theoretical context.
    :param raise_error_if_false:
    :return: ``True`` if every formula ``phi`` in enumeration ``s`` is a valid-statement in theory ``t``, ``False``
    otherwise.
    """
    s: WellFormedTupl = coerce_tuple(s=s, interpret_none_as_empty=True)
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    for phi in iterate_tuple_elements(phi=s):
        if not is_valid_proposition_so_far_1(p=phi, t=t):
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    msg='Statements validity check failure. Statement `s` is not a valid statement in `t`.',
                    s=s,
                    t=t,
                    raise_error_if_false=raise_error_if_false
                )
            else:
                return False
    return True


def iterate_permutations_of_enumeration_elements_with_fixed_size(e: FlexibleEnumeration, n: int) -> \
        typing.Generator[WellFormedEnumeration, None, None]:
    """Iterates all distinct tuples (order matters) of exactly n elements in enumeration e.

    :param e: An enumeration.
    :param n: The fixed size of the tuples to be iterated.
    :return:
    """
    e: WellFormedEnumeration = coerce_enumeration_OBSOLETE(e=e)
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
            permutation: WellFormedEnumeration = WellFormedEnumeration(e=python_tuple)
            yield permutation
        return


def iterate_theory_components(t: FlexibleTheory[FlexibleComponent] | None = None,
                              d: FlexibleEnumeration[FlexibleComponent] | None = None,
                              recurse_extensions: bool = True,
                              strip_duplicates: bool = True,
                              interpret_none_as_empty: bool = True,
                              canonic_conversion: bool = True,
                              max_components: int | None = None) -> \
        typing.Generator[WellFormedFormula, None, None]:
    """Iterates the components of a theoretical context ``t`` in canonical order.

    Alternatively, iterates through an enumeration of derivations `d` in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param recurse_extensions: If ``True``, yields the components of the extension, yields the extension formula itself
        otherwise.
    :param max_components: Yields only math:``max_components`` components, or all components if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    if t is not None:
        t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
        d: WellFormedEnumeration = transform_theoretical_context_to_enumeration(t=t)
    else:
        d: WellFormedEnumeration = coerce_enumeration(e=d, strip_duplicates=strip_duplicates,
                                                      interpret_none_as_empty=interpret_none_as_empty,
                                                      canonic_conversion=canonic_conversion)
    if max_components is None:
        # Yield all components without any index limit.
        for d2 in iterate_enumeration_elements(e=d):
            d2: WellFormedTheoryComponent = coerce_theory_component(d=d2)
            if recurse_extensions and is_well_formed_extension(e=d2):
                e: WellFormedExtension = coerce_extension(e=d2)
                t2: WellFormedTheoreticalContext = e.theoretical_context
                yield from iterate_theory_components(
                    t=t2, recurse_extensions=recurse_extensions,
                    strip_duplicates=strip_duplicates, interpret_none_as_empty=interpret_none_as_empty,
                    canonic_conversion=canonic_conversion,
                    max_components=None)
            else:
                yield d2
        return
    else:
        # Yield all components up to some index limit.
        i: int = 0
        for c in iterate_theory_components(
                t=t, d=d,
                strip_duplicates=strip_duplicates,
                interpret_none_as_empty=interpret_none_as_empty,
                max_components=None):
            i = i + 1
            if i > max_components:
                return
            else:
                yield c
        return


def count_theory_components(t: FlexibleTheory[FlexibleComponent] | None = None,
                            d: FlexibleEnumeration[FlexibleComponent] | None = None,
                            recurse_extensions: bool = True,
                            strip_duplicates: bool = True,
                            interpret_none_as_empty: bool = True,
                            max_components: int | None = None) -> int:
    """Count the components of a theoretical context ``t``, taking into account extensions.
    Alternatively, count the components of an enumeration ``d``.

    :param t:
    :param d:
    :param recurse_extensions:
    :param strip_duplicates:
    :param interpret_none_as_empty:
    :param max_components:
    :return:
    """
    if t is not None and d is not None:
        raise u1.ApplicativeError(msg='Parameters `t` and `d` are mutually exclusive.',
                                  t=t,
                                  d=d)
    ci: int = 0  # the component index
    for c in iterate_theory_components(t=t, d=d, recurse_extensions=recurse_extensions,
                                       strip_duplicates=strip_duplicates,
                                       interpret_none_as_empty=interpret_none_as_empty,
                                       max_components=max_components):
        ci = ci + 1
    return ci


def iterate_theory_axioms(t: FlexibleTheory | None = None,
                          d: FlexibleEnumeration[FlexibleComponent] | None = None,
                          recurse_extensions: bool = True,
                          strip_duplicates: bool = True,
                          interpret_none_as_empty: bool = True,
                          canonic_conversion: bool = True,
                          max_components: int | None = None
                          ) -> typing.Generator[WellFormedAxiom, None, None]:
    """Iterates through the axioms of a theoretical context ``t``, in canonical order.

    Alternatively, iterates through axioms of an enumeration of theory components `d`, in canonical order.

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Considers only ``max_components`` components, or all components if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_components(t=t,
                                        d=d,
                                        recurse_extensions=recurse_extensions,
                                        max_components=max_components,
                                        interpret_none_as_empty=interpret_none_as_empty,
                                        strip_duplicates=strip_duplicates,
                                        canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: WellFormedAxiom = coerce_axiom(a=d2)
            yield a


def iterate_theory_theorems(t: FlexibleTheoreticalContext | None = None,
                            d: FlexibleEnumeration[FlexibleComponent] | None = None,
                            recurse_extensions: bool = True,
                            strip_duplicates: bool = True,
                            interpret_none_as_empty: bool = True,
                            canonic_conversion: bool = True,
                            max_components: int | None = None
                            ) -> typing.Generator[WellFormedTheorem, None, None]:
    """Iterates through the theorems of a theoretical context ``t``, in canonical order.

    Alternatively, iterates through theorems of an enumeration of derivations `d`, in canonical order.

    :param t: A theoretical context.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Considers only ``max_components`` components, or all components if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_components(t=t,
                                        d=d,
                                        recurse_extensions=recurse_extensions,
                                        max_components=max_components,
                                        interpret_none_as_empty=interpret_none_as_empty,
                                        strip_duplicates=strip_duplicates,
                                        canonic_conversion=canonic_conversion):
        if is_well_formed_theorem(m=d2):
            t: WellFormedTheorem = coerce_theorem(m=d2)
            yield t


def iterate_theory_inference_rules(t: FlexibleTheory | None = None,
                                   d: FlexibleEnumeration[FlexibleComponent] | None = None,
                                   recurse_extensions: bool = True,
                                   strip_duplicates: bool = True,
                                   interpret_none_as_empty: bool = True,
                                   canonic_conversion: bool = True,
                                   max_components: int | None = None
                                   ) -> typing.Generator[WellFormedInferenceRule, None, None]:
    """Iterates through the inference-rules of theoretical context ``t`` in canonical order.

    Alternatively, iterates through inference-rules of an enumeration of derivations `d` in canonical order.

    :param t: A theoretical context.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Considers only ``max_components`` components, or all components if None.
    :param recurse_extensions:
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for c in iterate_theory_components(t=t,
                                       d=d,
                                       recurse_extensions=recurse_extensions,
                                       max_components=max_components,
                                       interpret_none_as_empty=interpret_none_as_empty,
                                       strip_duplicates=strip_duplicates,
                                       canonic_conversion=canonic_conversion):
        if is_well_formed_inference_rule(i=c):
            i: WellFormedInferenceRule = coerce_inference_rule(i=c)
            yield i


def iterate_theory_valid_statements(t: FlexibleTheory | None = None,
                                    d: FlexibleEnumeration[FlexibleComponent] | None = None,
                                    recurse_extensions: bool = True,
                                    strip_duplicates: bool = True,
                                    interpret_none_as_empty: bool = True,
                                    canonic_conversion: bool = True,
                                    max_components: int | None = None
                                    ) -> typing.Generator[WellFormedFormula, None, None]:
    """Iterates through the valid-statements of a theoretical context ``t`` in canonical order.

    Alternatively, iterates through propositions of an enumeration of derivations `d` in canonical order.

    Definition: theory valid-statements
    The valid-statements of a theory are the propositions of its axioms and theorems and its inference-rules.

    :param t: A theoretical context.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Considers only ``max_components`` components, or all components if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_components(t=t,
                                        d=d,
                                        recurse_extensions=recurse_extensions,
                                        max_components=max_components,
                                        interpret_none_as_empty=interpret_none_as_empty,
                                        strip_duplicates=strip_duplicates,
                                        canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: WellFormedAxiom = coerce_axiom(a=d2)
            s: WellFormedFormula = a.valid_statement
            yield s
        elif is_well_formed_theorem(m=d2):
            m: WellFormedTheorem = coerce_theorem(m=d2)
            s: WellFormedFormula = m.valid_statement
            yield s
        elif is_well_formed_inference_rule(i=d2):
            i: WellFormedInferenceRule = coerce_inference_rule(i=d2)
            s: WellFormedFormula = i.valid_statement
            yield s


def iterate_theory_propositions(t: FlexibleTheory | None = None,
                                d: FlexibleEnumeration[FlexibleComponent] | None = None,
                                recurse_extensions: bool = True,
                                strip_duplicates: bool = True,
                                interpret_none_as_empty: bool = True,
                                canonic_conversion: bool = True,
                                max_components: int | None = None
                                ) -> typing.Generator[WellFormedFormula, None, None]:
    """Iterates through propositions in derivations of a theory ``t`` in canonical order.

    Alternatively, iterates through propositions of an enumeration of derivations `d` in canonical order.

    Definition: theory propositions
    The valid-statements of axioms and theorems in a theory.

    TODO: Is this a synonym for iterate_theory_valid_statements? Check this...

    :param t: A theory.
    :param d: An enumeration of derivations. Ignored if ``t`` is provided.
    :param max_components: Considers only ``max_components`` components, or all components if None.
    :param canonic_conversion: Uses canonic conversion if needed when coercing `d` to enumeration.
    :param strip_duplicates: Strip duplicates when coercing `d` to enumeration. Raises an error otherwise.
    :param interpret_none_as_empty: Interpret None as the empty enumeration when coercing `d` to enumeration.
    :return:
    """
    for d2 in iterate_theory_components(t=t,
                                        d=d,
                                        recurse_extensions=recurse_extensions,
                                        max_components=max_components,
                                        interpret_none_as_empty=interpret_none_as_empty,
                                        strip_duplicates=strip_duplicates,
                                        canonic_conversion=canonic_conversion):
        if is_well_formed_axiom(a=d2):
            a: WellFormedAxiom = coerce_axiom(a=d2)
            p: WellFormedFormula = a.valid_statement
            yield p
        elif is_well_formed_theorem(m=d2):
            m: WellFormedTheorem = coerce_theorem(m=d2)
            p: WellFormedFormula = m.valid_statement
            yield p


def are_valid_statements_in_theory_with_variables(
        s: FlexibleTupl, t: FlexibleTheoreticalContext,
        variables: FlexibleEnumeration,
        variables_values: FlexibleMap, debug: bool = False) \
        -> tuple[bool, typing.Optional[WellFormedTupl]]:
    """Return True if every formula phi in tuple s is a valid-statement in theory t,
    considering some variables, and some variable values.
    If a variable in variables has not an assigned value, then it is a free variable.
    Return False otherwise.

    Performance warning: this may be a very expansive algorithm, because multiple
    recursive iterations may be required to find a solution.

    TODO: retrieve and return the final map of variable values as well? is this really needed?

    """
    s: WellFormedTupl = coerce_tuple(s=s, interpret_none_as_empty=True)
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    variables: WellFormedEnumeration = coerce_enumeration(e=variables, interpret_none_as_empty=True,
                                                          strip_duplicates=True)
    variables_values: WellFormedMap = coerce_map(m=variables_values, interpret_none_as_empty=True)

    # list the free variables.
    # these are the variables that are in "variables" that are not in the domain of "variables_values".
    free_variables: WellFormedEnumeration = WellFormedEnumeration()
    for x in iterate_enumeration_elements(e=variables):
        if not is_in_map_domain(phi=x, m=variables_values):
            free_variables: WellFormedEnumeration = WellFormedEnumeration(e=(*free_variables, x,))

    if debug:
        u1.log_info(f'are_valid_statements_in_theory_with_variables: free-variables:{free_variables}')

    permutation_size: int = free_variables.arity

    if permutation_size == 0:
        # there are no free variables.
        # but there may be some or no variables with assigned values.
        # it follows that 1) there will be no permutations,
        # and 2) are_valid_statements_in_theory() is equivalent.
        s_with_variable_substitution: WellFormedFormula = substitute_formulas(phi=s, m=variables_values)
        s_with_variable_substitution: WellFormedTupl = coerce_tuple(s=s_with_variable_substitution)
        valid: bool = are_valid_statements_in_theory(s=s_with_variable_substitution, t=t)
        if valid:
            return valid, s_with_variable_substitution
        else:
            return valid, None
    else:
        valid_statements = iterate_theory_propositions(t=t)
        for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                        n=permutation_size):
            variable_substitution: WellFormedMap = WellFormedMap(d=free_variables, c=permutation)
            s_with_variable_substitution: WellFormedFormula = substitute_formulas(phi=s, m=variable_substitution)
            s_with_variable_substitution: WellFormedTupl = coerce_tuple(s=s_with_variable_substitution)
            s_with_permutation: WellFormedTupl = WellFormedTupl(e=(*s_with_variable_substitution,))
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
    phi: WellFormedFormula = coerce_formula(phi=phi)
    t: WellFormedTheory = coerce_theory(t=t)
    free_variables: WellFormedEnumeration = coerce_enumeration_of_variables(e=free_variables)
    for valid_statement in t.iterate_valid_statements():
        output, _, = is_formula_equivalent_with_variables_2(phi=valid_statement, psi=phi, variables=free_variables)
        if output:
            return True
    return False


def is_well_formed_axiom(a: FlexibleFormula, t: FlexibleTheoreticalContext | None = None) -> bool:
    """Returns ``True`` if ``a`` is a well-formed axiom, ``False`` otherwise.

    If ``t`` is ``None``, uses the global definition of well-formed axiom.
    If ``t`` is not ``None``, uses the local definition of well-formed axiom with regards to theoretical-context ``t``.


    :param a: A formula.
    :param t: A theoretical context.
    :return: ``True`` if ``a`` is a well-formed axiom, ``False`` otherwise.
    """
    global connective_for_axiom_formula
    a: WellFormedFormula = coerce_formula(phi=a)
    if t is not None:
        t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    if a.arity != 1:
        return False
    if a.connective is not connective_for_axiom_formula:
        return False
    # Check that the axiom proposition is well-formed, with regard to `t` if `t` is not `None`.
    # If `t` is not `None`, `is_well_formed_proposition` checks the validity of `is-a-proposition(p)` in `t`.
    if not is_well_formed_proposition(p=a[WellFormedAxiom.PROPOSITION_INDEX], t=t):
        return False
    # All tests were successful.
    return True


def is_well_formed_extension(e: FlexibleExtension,
                             t: FlexibleTheoreticalContext | None = None,
                             raise_error_if_false: bool = False) -> bool:
    """Return ``True`` if and only if ``e`` is a well-formed theory extension, ``True`` otherwise.

    #   which assures that the resulting theory is well-formed.s

    :param e: A formula that may be a well-formed extension.
    :param raise_error_if_false:
    :return: bool.
    """

    # TODO: Implement parameter t, in order to test the local definition of extension.
    #   For the time being, t is not implemented.

    e = coerce_formula(phi=e)
    if isinstance(e, WellFormedExtension):
        # the Theorem python-type assures the well-formedness of the object.
        return True
    elif (e.connective is not connective_for_extension or
          not e.arity == 1 or
          not is_well_formed_theoretical_context(t=e.term_0)):
        if raise_error_if_false:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_092, e=e)
        return False
    else:
        return True


def is_well_formed_theorem(m: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Return True if and only if phi is a well-formed theorem, False otherwise.

    :param raise_error_if_false:
    :param m: A formula.
    :return: bool.
    """
    global connective_for_theorem

    m = coerce_formula(phi=m)
    if isinstance(m, WellFormedTheorem):
        # the Theorem python-type assures the well-formedness of the object.
        return True
    if (m.connective is not connective_for_theorem or
            not m.arity == 2 or
            not is_well_formed_proposition(p=m.term_0, t=None) or
            not is_well_formed_inference(i=m.term_1)):
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_035,
                msg='Ill-formed object. `m` is not a well-formed theorem.',
                m=m)
        return False
    else:
        # TODO: Factorize the check in Theorem.__new__ or __init__,
        #   that takes into account new-object-declarations.
        p: WellFormedProposition = coerce_proposition(p=m[WellFormedTheorem.PROPOSITION_INDEX])
        i: WellFormedInference = coerce_inference(i=m[WellFormedTheorem.INFERENCE_INDEX])
        p2: WellFormedFormula = i.inference_rule.transformation(i.premises)
        p2: WellFormedProposition = coerce_proposition(p=p2)
        if not is_formula_equivalent(phi=p, psi=p2):
            # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_035,
                    msg='Ill-formed object. '
                        'Object `m` is not a well-formed theorem because it claims `p`, '
                        'but inference `i` yields `p2`.',
                    m=m, p=p,
                    p2=p2,
                    i=i)
            return False
        return True


def is_well_formed_derivation(d: FlexibleFormula) -> bool:
    """Return ``True`` if ``d`` is a well-formed theorem, ``False`` otherwise.

    :param d: A formula.
    :return: bool.
    """
    d: WellFormedFormula = coerce_formula(phi=d)
    if is_well_formed_theorem(m=d):
        return True
    elif is_well_formed_inference_rule(i=d):
        return True
    elif is_well_formed_axiom(a=d):
        return True
    else:
        return False


def is_well_formed_axiomatic_base(t: FlexibleTheoreticalContext, raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if ``t`` is a well-formed axiomatic base, ``False`` otherwise.

    Intuitive definition
    ^^^^^^^^^^^^^^^^^^^^
    An axiomatic base is a theoretical context that is only composed of inference-rule and or axioms.

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed axiomatic base if and only if:
     - it is a well-formed theoretical context,
     - all component :math:`d` in :math:`\\phi`:
       - is a well-formed inference-rule,
       - or is a well-formed axiom.

    :param t: A theoretical context.
    :param raise_error_if_false:
    :return: bool.
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    for c in iterate_theory_components(t=t):
        if not is_well_formed_axiomatic_base_component(d=c):
            return False
    return True


def is_well_formed_axiomatic_base_component(d: FlexibleFormula) -> bool:
    """Returns ``True`` if ``d`` is a well-formed axiomatic base component, ``False`` otherwise.

    Intuitive definition
    ^^^^^^^^^^^^^^^^^^^^
    An axiomatic base component is a proper component for the definition of axiomatic bases. It can be either an
    inference rule, or an axiom.

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed axiomatic base component if and only if:
     - it is a well-formed inference-rule,
     - or it is a well-formed axiom,
     - or it is an extension and all component :math:`c` in :math:`\\phi` is a well-formed
        axiomatic base component.

    :param d: A formula.
    :return: ``True`` if ``d`` is a well-formed axiomatic base component, ``False`` otherwise.
    """
    d: WellFormedFormula = coerce_formula(phi=d)
    if is_well_formed_theorem(m=d):
        # Theorems are derivations, they cannot be components of an axiomatic base.
        return False
    elif is_well_formed_inference_rule(i=d):
        return True
    elif is_well_formed_axiom(a=d):
        return True
    elif is_well_formed_extension(e=d):
        e: WellFormedExtension = coerce_extension(e=d)
        for c in iterate_theory_components(t=e.theoretical_context):
            if not is_well_formed_axiomatic_base_component(d=c):
                # If any component of the extension is (recursively)
                # not a well-formed axiomatic base component, it follows that
                # the extension itself is not a well-formed axiomatic base component.
                return False
        return True
    else:
        return False


def is_well_formed_theoretical_context(t: FlexibleTheoreticalContext) -> bool:
    """Returns ``True`` if ``t`` is a well-formed theoretical context, ``False`` otherwise.

    See :class:`WellFormedTheoreticalContext` for the definition of theoretical context.

    :param t: A theoretical context.
    :return: ``True`` if ``t`` is a well-formed theoretical context, ``False`` otherwise..
    """
    t: WellFormedFormula = coerce_formula(phi=t)
    if is_well_formed_theory(t=t):
        return True
    elif is_well_formed_axiomatization(a=t):
        return True
    elif is_well_formed_hypothesis(h=t):
        return True
    else:
        return False


def would_be_valid_components_in_theory(v: FlexibleTheory, u: FlexibleEnumeration,
                                        raise_error_if_false: bool = False
                                        ) -> tuple[bool, WellFormedEnumeration | None, WellFormedEnumeration | None]:
    """Given an enumeration of presumably verified derivations "v" (e.g.: the derivation sequence of a theory ``t``),
    and an enumeration of unverified derivations "u" (e.g.: whose elements are not (yet) effective
    theorems of ``t``), returns True if a theory would be well-formed if it was composed of
    derivations "u" appended to derivations "v", or False if it would not.

    This function is useful to test whether some derivations will pass well-formedness validation before
    attempting to effectively derive it.

    :param v: An enumeration of presumably verified derivations.
    :param u: An enumeration of unverified derivations.
    :param raise_error_if_false:
    :return: A triple `(b, v′, u′)` where:
     `b` is ``True`` if all derivations in `u` would be valid, ``False`` otherwise,
     `v′` = `v` with duplicates stripped out if `b` is ``True``, ``None`` otherwise,
     `u′` = `(u \\ v)` with duplicates stripped out if `b` is ``True``, ``None`` otherwise.
    """
    v: WellFormedEnumeration = coerce_enumeration(e=v, strip_duplicates=True, interpret_none_as_empty=True,
                                                  canonic_conversion=True)
    u: WellFormedEnumeration = coerce_enumeration(e=u, strip_duplicates=True, interpret_none_as_empty=True,
                                                  canonic_conversion=True)

    # Consider only derivations that are not elements of the verified enumeration.
    # In effect, a derivation sequence must contain unique derivations under enumeration-equivalence.
    u: WellFormedEnumeration = difference_enumeration(phi=u, psi=v, strip_duplicates=True, interpret_none_as_empty=True,
                                                      canonic_conversion=True)

    # Create a complete enumeration "c" composed of derivations "u" appended to derivations "v",
    # getting rid of duplicates in the process.
    c: WellFormedEnumeration = union_enumeration(phi=v, psi=u, strip_duplicates=True)

    # Put aside the index from which the proofs of derivations have not been verified.
    verification_threshold: int = len(v)

    # Coerce all enumeration elements to axioms, inference-rules, and theorems.
    # TODO: Implement a dedicated function coerce_enumeration_of_derivations().
    coerced_elements: list = [coerce_theory_component(d=d) for d in iterate_enumeration_elements(e=c)]
    c: WellFormedEnumeration = WellFormedEnumeration(e=coerced_elements)

    # Iterate through all index positions of derivations for which the proofs must be verified.
    for index in range(verification_threshold, len(c)):

        # Retrieve the derivation whose proof must be verified.
        d: WellFormedTheoryComponent = c[index]

        # Retrieve the proposition or statement announced by the derivation.
        p: WellFormedFormula = d.valid_statement

        if is_well_formed_axiom(a=d):
            # This is an axiom.
            # By definition, the presence of an axiom in a theory is valid.
            pass
        elif is_well_formed_inference_rule(i=d):
            # This is an inference-rule.
            # By definition, the presence of an inference-rule in a theory is valid.
            pass
        elif is_well_formed_extension(e=d):
            # This is a theory extension.
            # We must recursively check the validity of the extension components in the parent theory.
            # An alternative approach would be to specify recurse_extensions=True in the parent loop,
            # but this is less preferable because the extensions would not be explicitly
            # verified with the same approach as the other classes of components.
            # put aside the components that have been verified so far.
            verified_so_far: WellFormedEnumeration = WellFormedEnumeration(e=(*v, *u[0:index]))
            d: WellFormedExtension = coerce_extension(e=d)
            t2: WellFormedTheoreticalContext = d.theoretical_context
            if not would_be_valid_components_in_theory(v=verified_so_far,
                                                       u=iterate_theory_components(t=t2, recurse_extensions=False)):
                if raise_error_if_false:
                    raise u1.ApplicativeError(
                        code=c1.ERROR_CODE_AS1_094,
                        msg='Some component of theory `t2` in extension `d` would not be valid in `v`.',
                        p=p, t2=t2, index=index, d=d, c=c, v=v, u=u)
                return False, None, None
        elif is_well_formed_theorem(m=d):
            # This is a theorem.
            # Check that this theorem is well-formed with regard to the target theory,
            # i.e. it is a valid derivation with regard to predecessor derivations.
            m: WellFormedTheorem = coerce_theorem(m=d)
            i: WellFormedInference = m.inference
            ir: WellFormedInferenceRule = m.inference.inference_rule
            verified_so_far: WellFormedEnumeration = WellFormedEnumeration(e=(*v, *u[0:index]))
            # Check that the inference-rule is a valid predecessor in the derivation.
            if not is_inference_rule_of(i=ir, d=verified_so_far):
                # if not any(is_formula_equivalent(phi=ir, psi=ir2) for ir2 in
                #           iterate_theory_inference_rules(
                #               d=c,
                #               max_components=index + 1,  # BUG IS HERE
                #               recurse_extensions=True)):
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
                if not is_valid_proposition_so_far_1(p=q, t=None, d=verified_so_far):
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
            f: ABCTransformation = i.inference_rule.transformation
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
                p_inverse = substitute_formulas(phi=p, m=map1_inverse)

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
                i3: WellFormedTupl = append_tuple_to_tuple(t1=i.premises, t2=i.arguments)
                p_prime: WellFormedFormula = f.apply_transformation(i=i3)
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
            # that derivation `d` would be valid if appended to theory ``t``.
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


def is_well_formed_theory(t: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Return True if phi is a well-formed theory, False otherwise.

    :param t: A formula.
    :param raise_error_if_false:
    :return: bool.
    """
    t = coerce_formula(phi=t)

    if isinstance(t, WellFormedTheory):
        # By design, the Theory class assures the well-formedness of a theory.
        # cf. the _data_validation_ method in the Theory class.
        return True

    con: Connective = t.connective
    if con is not connective_for_theory:
        # TODO: Remove the 1==2 condition above to re-implement a check of strict connectives constraints.
        #   But then we must properly manage python inheritance (Axiomatization --> Theory --> Enumeration).
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='The connective "c" of theory ``t`` is not the "theory-formula" connective. '
                    'It follows that ``t`` is not a well-formed-theory.',
                con=con,
                con_id=id(con),
                theory_formula=connective_for_theory,
                theory_formula_id=id(connective_for_theory),
                t=t)
        return False

    # Check that the terms of the formula constitute an enumeration of derivations,
    # and that derivations in this sequence of derivations is valid.
    v: WellFormedEnumeration = WellFormedEnumeration(e=None)  # Assume no pre-verified derivations.
    u: WellFormedEnumeration = transform_formula_to_enumeration(phi=t, strip_duplicates=False)
    would_be_valid, _, _ = would_be_valid_components_in_theory(v=v, u=u)
    return would_be_valid


def is_well_formed_axiomatization(a: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if ``a`` is a well-formed axiomatization, ``False`` otherwise.

    TODO: Because proposition is a local definition, add a conditional argument ``t`` and
        pass it to is_well_formed_axiom which then must pass it to is_well_formed_proposition.

    :param a: A formula, possibly a well-formed axiomatization.
    :param raise_error_if_false: If True, raises an error when ``a`` is not a well-formed
        axiomatization.
    :raises ApplicativeError: with error code AS1-064 when ``a`` is not a well-formed axiomatization and
        `raise_error_if_false` = True.
    :return: bool.
    """
    global connective_for_axiomatization_formula
    a = coerce_formula(phi=a)

    if isinstance(a, WellFormedAxiomatization):
        # By design, the WellFormedAxiomatization class assures the well-formedness of an axiomatization.
        # cf. the _data_validation_ method in the Theory class.
        return True
    elif (a.connective is not connective_for_axiomatization_formula or
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


def is_well_formed_simple_object(o: FlexibleFormula, raise_error_if_false: bool = False) -> bool:
    """Returns ``True`` if ``o`` is a well-formed simple-object, ``False`` otherwise.

    See :class:`WellFormedSimpleObject` for a definition of simple-object.

    :param o: A formula, possibly a well-formed simple-object.
    :param raise_error_if_false: If ``True``, raises an error when ``o`` is not a well-formed
        simple-object.
    :raises ApplicativeError: with error code AS1-088 if ``raise_error_if_false`` and ``o`` is not a
        well-formed simple-object.
    :return: ``True`` if ``o`` is a well-formed simple-object, ``False`` otherwise.
    """
    o = coerce_formula(phi=o)
    if o.arity == 0:
        return True
    else:
        if raise_error_if_false:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_088,
                msg='`o` is not a well-formed simple-objects.',
                o=o
            )
        return False


def coerce_theory_component(d: FlexibleFormula) -> WellFormedTheoryComponent:
    """

    Validate that p is a well-formed theorem and returns it properly typed as Proof, or raise exception e123.

    :param d:
    :return:
    """
    d: WellFormedFormula = coerce_formula(phi=d)
    if is_well_formed_theorem(m=d):
        return coerce_theorem(m=d)
    elif is_well_formed_inference_rule(i=d):
        return coerce_inference_rule(i=d)
    elif is_well_formed_axiom(a=d):
        return coerce_axiom(a=d)
    elif is_well_formed_extension(e=d):
        return coerce_extension(e=d)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_039,
            msg=f'Coercion failure. Argument `d` could not be coerced to a theory component.',
            d=d)


def coerce_theoretical_context(t: FlexibleTheoreticalContext,
                               interpret_none_as_empty: bool = False,
                               canonical_conversion: bool = True) -> WellFormedTheoreticalContext:
    """

    Validate that t is a well-formed theoretical context and returns it properly typed as WellFormedTheoreticalContext,
    or raise an error with code AS1-089.

    :param t: A theoretical context.
    :param interpret_none_as_empty: If ``t`` is ``None``, returns an empty theory.
    :return:
    """
    if t is None and interpret_none_as_empty:
        t: WellFormedTheory = WellFormedTheory()
        return t
    else:
        t: WellFormedFormula = coerce_formula(phi=t)
        if is_well_formed_hypothesis(h=t, raise_error_if_false=False):
            return coerce_hypothesis(h=t)
        elif is_well_formed_axiomatization(a=t, raise_error_if_false=False):
            return coerce_axiomatization(a=t)
        elif is_well_formed_theory(t=t, raise_error_if_false=False):
            return coerce_theory(t=t, canonical_conversion=canonical_conversion)
        else:
            raise u1.ApplicativeError(
                code=c1.ERROR_CODE_AS1_090,
                msg=f'Argument `t` could not be coerced to a theoretical context of python-type '
                    f'WellFormedTheoreticalContext.',
                t=t)


def coerce_axiom(a: FlexibleFormula) -> WellFormedAxiom:
    """Coerces formula ``a`` into a well-formed axiom, or raises an error if it fails.

    :param a: A formula that is presumably a well-formed axiom.
    :return: A well-formed axiom.
    :raises ApplicativeError: with code AS1-040 if coercion fails.
    """
    if isinstance(a, WellFormedAxiom):
        return a
    elif isinstance(a, WellFormedFormula) and is_well_formed_axiom(a=a):
        p: WellFormedProposition = coerce_proposition(p=a[WellFormedAxiom.PROPOSITION_INDEX])
        return WellFormedAxiom(p=p)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_040,
            msg='Coercion failure. `a` cannot be coerced to a well-formed axiom.',
            a=a)


def coerce_extension(e: FlexibleFormula) -> WellFormedExtension:
    """Coerces formula ``e`` into a well-formed extension, or raises an error if it fails.

    :param e: A formula that is presumably a well-formed extension.
    :return: A well-formed extension.
    :raises ApplicativeError: with code AS1-093 if coercion fails.
    """
    if isinstance(e, WellFormedExtension):
        return e
    elif is_well_formed_extension(e=e):
        t = e[WellFormedExtension.THEORETICAL_CONTEXT_INDEX]
        return WellFormedExtension(t=t)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_093,
            msg='`e` cannot be coerced to a well-formed extension.',
            e=e)


def coerce_inference_rule(i: FlexibleInferenceRule) -> WellFormedInferenceRule:
    """Coerces formula `i` into a well-formed inference-rule, or raises an error if it fails.

    :param i: A formula that is presumably a well-formed inference-rule.
    :return: A well-formed inference-rule.
    :raises ApplicativeError: with code AS1-041 if coercion fails.
    """
    if isinstance(i, WellFormedInferenceRule):
        return i
    elif isinstance(i, WellFormedFormula) and is_well_formed_inference_rule(i=i):
        f: ABCTransformation = coerce_transformation(f=i[WellFormedInferenceRule.TRANSFORMATION_INDEX])
        return WellFormedInferenceRule(f=f)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_041,
            msg='`i` cannot be coerced to a well-formed inference-rule.',
            i=i)


def coerce_theorem(m: FlexibleFormula) -> WellFormedTheorem:
    """Coerces formula ``m`` into a well-formed theorem, or raises an error if it fails.

    :param m: A formula that is presumably a well-formed theorem.
    :return: A well-formed theorem.
    :raises ApplicativeError: with code AS1-042 if coercion fails.
    """
    if isinstance(m, WellFormedTheorem):
        return m
    elif isinstance(m, WellFormedFormula) and is_well_formed_theorem(m=m):
        p: WellFormedProposition = coerce_proposition(p=m[WellFormedTheorem.PROPOSITION_INDEX])
        i: WellFormedInference = coerce_inference(i=m[WellFormedTheorem.INFERENCE_INDEX])
        return WellFormedTheorem(p=p, i=i)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_042,
            msg='Coercion failure. `m` cannot be coerced to a well-formed theorem.',
            m=m)


def coerce_theory(t: FlexibleTheory, interpret_none_as_empty: bool = False,
                  canonical_conversion: bool = False) -> WellFormedTheory:
    """Coerces formula ``t`` into a well-formed theory, or raises an error if it fails.

    :param t: A formula that is presumably a well-formed theory.
    :param canonical_conversion: If necessary, apply canonical conversations to transform ``t`` into a well-formed theory.
    :param interpret_none_as_empty: If ``t`` is ``None``, interpret it as the empty theory.
    :return: A well-formed theory.
    :raises ApplicativeError: with code AS1-043 if coercion fails.
    """
    if isinstance(t, WellFormedTheory):
        return t
    elif interpret_none_as_empty and t is None:
        return WellFormedTheory(t=None, d=None, d2=None)
    elif is_well_formed_theory(t=t):
        t: WellFormedFormula = coerce_formula(phi=t)
        return WellFormedTheory(t=None, d=(*t,), d2=None)
    elif canonical_conversion and is_well_formed_axiomatization(a=t):
        return transform_axiomatization_to_theory(a=t)
    elif canonical_conversion and is_well_formed_hypothesis(h=t):
        return transform_hypothesis_to_theory(h=t)
    elif canonical_conversion and is_well_formed_enumeration(e=t):
        return transform_enumeration_to_theory(e=t)
    elif canonical_conversion and is_well_formed_tupl(t=t):
        return transform_tuple_to_theory(t=t)
    elif isinstance(t, typing.Generator) and not isinstance(t, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedTheory(t=None, d=tuple(element for element in t), d2=None)
    elif isinstance(t, typing.Iterable) and not isinstance(t, WellFormedFormula):
        """A non-Formula iterable type, such as python native tuple, set, list, etc.
        We assume here that the intention was to implicitly convert this to an enumeration
        whose elements are the elements of the iterable."""
        return WellFormedTheory(t=None, d=t, d2=None)
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_043,
            msg='`t` cannot be coerced to a well-formed theory.',
            t=t,
            interpret_none_as_empty=interpret_none_as_empty,
            canonical_conversion=canonical_conversion)


def coerce_axiomatization(a: FlexibleFormula, interpret_none_as_empty: bool = False) -> WellFormedAxiomatization:
    """Validate that phi is a well-formed axiomatization and returns it properly python-typed as Axiomatization,
    or raise error AS1-044.

    :param a:
    :param interpret_none_as_empty:
    :return:
    """
    if isinstance(a, WellFormedAxiomatization):
        return a
    elif a is None and interpret_none_as_empty:
        return WellFormedAxiomatization(a=None, d=None)
    elif is_well_formed_axiomatization(a=a):
        return WellFormedAxiomatization(d=(*a,))
    else:
        raise u1.ApplicativeError(
            code=c1.ERROR_CODE_AS1_044,
            msg=f'Argument ``a`` could not be coerced to an axiomatization.',
            a=a,
            interpret_none_as_empty=interpret_none_as_empty)


class WellFormedTheoryComponent(WellFormedFormula):
    """A derivation has two definitions: a local definition with regard to a theory t, and a global definition.

    Global definition:
    A well-formed derivation s is a formula of the form:
     - phi follows-from psi,
    where:
     - phi is a formula,
     - follows-from is the derivation connector,
     - and psi is a proper-justification.

    Local definition (with regard to a theory t):
    A well-formed derivation s with regard to a theory t is a formula that is:
     - a term of theory t,
     - a well-formed (global) derivation,
     - and whose justification with regard to theory t is a proper-justification.


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
    def _data_validation_2(s: FlexibleFormula, j: FlexibleFormula, con: Connective | None = None) -> tuple[
        Connective, WellFormedFormula, WellFormedFormula]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param s:
        :param j:
        :return:
        """
        if con is None:
            con: Connective = connective_for_theory_component
        s = coerce_formula(phi=s)
        if j is not None:
            j = coerce_formula(phi=j)
        return con, s, j

    def __new__(cls, s: FlexibleFormula, j: FlexibleFormula | None = None, con: Connective | None = None,
                **kwargs):
        con, s, j = WellFormedTheoryComponent._data_validation_2(s=s,
                                                                 j=j, con=con)
        if j is not None:
            o: tuple = super().__new__(cls, con=con, t=(s, j,), **kwargs)
        else:
            o: tuple = super().__new__(cls, con=con, t=(s,), **kwargs)
        return o

    def __init__(self, s: FlexibleFormula, j: FlexibleFormula | None = None, con: Connective | None = None,
                 **kwargs):
        """

        :param s: A formula that is a valid-statement in the theory.
        :param j: A formula that is a justification for the validity of the valid-statement.
        :param kwargs:
        """
        con, s, j = WellFormedTheoryComponent._data_validation_2(s=s,
                                                                 j=j, con=con)
        if j is not None:
            super().__init__(con=con, t=(s, j,), **kwargs)
        else:
            super().__init__(con=con, t=(s,), **kwargs)

    @property
    def valid_statement(self) -> WellFormedFormula:
        """Return the formula claimed as valid by the theorem.

        This is equivalent to phi.term_0.

        :return: A formula.
        """
        return self[WellFormedTheoryComponent.VALID_STATEMENT_INDEX]

    @property
    def justification(self) -> WellFormedFormula:
        return self[WellFormedTheoryComponent.JUSTIFICATION_INDEX]


class WellFormedAxiom(WellFormedTheoryComponent):
    """A well-formed axiom is a formula of the form ⌜ :math:`\\text{axiom}\\left( \\boldsymbol{P} \\right)` ⌝ where
    :math:`\\boldsymbol{P}` is a well-formed proposition.

    Global definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`\\phi` is a well-formed axiom if and only if:
     - its root connective is the axiom-formula connective,
     - its arity is equal to 1,
     - its term is a globally well-formed proposition.

    Local definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`\\boldsymbol{\\phi}` is a well-formed axiom with regard to theoretical context :math:`T`
    if and only if:
     - it is a globally well-formed axiom,
     - its term is a locally well-formed proposition with regard to :math:`T`.

    TODO: An axiom may be viewed as an inference-rule without premises. Thus, Axiom could derive from InferenceRule.

    TODO: When an axiom is postulated in a theory, automatically infer is-a-well-formed-proposition(P)?

    TODO: QUESTION: To be locally well-formed, the proposition of an axiom must be signaled as a proposition.
        but this may require an initial axiom stating that the first is-a-proposition(is-a-proposition(...))
        is a proposition, leading to an infinite loop. In practice this is not an issue but how this plays
        out should be properly documented.

    """

    PROPOSITION_INDEX: int = 0

    @staticmethod
    def _data_validation_3(p: FlexibleProposition) -> tuple[Connective, WellFormedProposition]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param p: A proposition.
        :return:
        """
        global connective_for_axiom_formula
        con: Connective = connective_for_axiom_formula
        p: WellFormedProposition = coerce_proposition(p=p)
        return con, p

    def __new__(cls, p: FlexibleProposition, **kwargs):
        """Creates a new axiom.

        :param p: A proposition.
        :param kwargs:
        """
        con, p = WellFormedAxiom._data_validation_3(p=p)
        o: tuple = super().__new__(cls, con=con, s=p, **kwargs)
        return o

    def __init__(self, p: FlexibleProposition, **kwargs):
        """initializes a new axiom.

        :param p: A proposition.
        :param kwargs:
        :returns: A well-formed axiom.
        """
        con, p = WellFormedAxiom._data_validation_3(p=p)
        super().__init__(con=con, s=p, **kwargs)

    @property
    def proposition(self) -> WellFormedProposition:
        """The proposition postulated as true by the axiom."""
        return self[WellFormedAxiom.PROPOSITION_INDEX]


FlexibleAxiom = typing.Union[WellFormedAxiom, WellFormedFormula]


class WellFormedExtension(WellFormedTheoryComponent):
    """A well-formed extension is a formula of the form ⌜ :math:`\\text{extension}\\left( \\boldsymbol{T} \\right)` ⌝
    where :math:`\\boldsymbol{T}` is a theoretical context, signaling the extension of the parent theoretical context,
    i.e.: the theoretical context of which the extension is a component.

    Global definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`\\phi` is a well-formed axiom if and only if:
     - its root connective is the axiom-formula connective,
     - its arity is equal to 1,
     - its term is a globally well-formed proposition.

    Local definition
    ~~~~~~~~~~~~~~~~~~
    A formula :math:`\\boldsymbol{\\phi}` is a well-formed axiom in a theoretical context :math:`T` if and only if:
     - it is a well-formed axiom as per the global definition above,
     - its term is a proposition in :math:`T`.

    Question: is the extension connective necessary?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This is an open question. An alternative design would be to consider well-formed theory the formula theory(ir1,
    ir2, a1, a2, theory(a1, ir4, d5), ...) where theories can be directly embedded into parent theories as components.
        This formalism and data model seem to work perfectly as well.
        The usage of an explicit connective extension(theory(...)) may just add useless verbosity.
        This is an open question.

    """
    THEORETICAL_CONTEXT_INDEX: int = 0

    @staticmethod
    def _data_validation_3(t: WellFormedTheoreticalContext = None) -> tuple[Connective, WellFormedTheoreticalContext]:
        """Assures the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param t: A theoretical context.
        :return:
        """
        con: Connective = connective_for_extension
        t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
        return con, t

    def __new__(cls, t: WellFormedTheoreticalContext = None, **kwargs):
        """Creates a new extension.

        :param t: A theoretical context.
        :param kwargs:
        """
        con, t = WellFormedExtension._data_validation_3(t=t)
        o: tuple = super().__new__(cls, con=con, s=t, **kwargs)
        return o

    def __init__(self, t: WellFormedTheoreticalContext, **kwargs):
        """initializes a new extension.

        :param t: A theoretical context.
        :param kwargs:
        """
        con, p = WellFormedExtension._data_validation_3(t=t)
        super().__init__(con=con, s=t, **kwargs)

    @property
    def theoretical_context(self) -> WellFormedTheoreticalContext:
        """Returns the theoretical context :math`t` of the extension formula :math:`\\text{extension}(t)`.

        :return: The theoretical context :math`t` of the extension formula :math:`\\text{extension}(t)`.
        """
        return self[WellFormedExtension.THEORETICAL_CONTEXT_INDEX]


FlexibleExtension = typing.Union[WellFormedExtension, WellFormedFormula]

FlexibleSimpleObject = typing.Union[WellFormedSimpleObject, WellFormedFormula]


class WellFormedInferenceRule(WellFormedTheoryComponent):
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
    TRANSFORMATION_INDEX: int = WellFormedTheoryComponent.VALID_STATEMENT_INDEX

    @staticmethod
    def _data_validation_3(f: FlexibleTransformation = None) -> tuple[Connective, ABCTransformation]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param f: A transformation.
        :return:
        """
        con: Connective = connective_for_inference_rule
        f: ABCTransformation = coerce_transformation(f=f)
        return con, f

    def __new__(cls, f: FlexibleTransformation = None, **kwargs):
        """

        :param f: A transformation.

        :param kwargs:
        """
        con, f = WellFormedInferenceRule._data_validation_3(f=f)
        o: tuple = super().__new__(cls, con=con, s=f, **kwargs)
        return o

    def __init__(self, f: FlexibleTransformation, **kwargs):
        """

        :param f: A transformation.
        :param kwargs:
        """
        con, f = WellFormedInferenceRule._data_validation_3(f=f)
        super().__init__(con=con, s=f, **kwargs)

    @property
    def transformation(self) -> ABCTransformation:
        return self[WellFormedInferenceRule.TRANSFORMATION_INDEX]


FlexibleInferenceRule = typing.Union[WellFormedInferenceRule, WellFormedFormula]
FlexibleTransformation = typing.Union[
    ABCTransformation, WellFormedTransformationByVariableSubstitution, WellFormedFormula]

with let_x_be_a_variable(formula_ts='P') as phi, let_x_be_a_variable(formula_ts='Q') as psi:
    modus_ponens_inference_rule: WellFormedInferenceRule = WellFormedInferenceRule(
        f=let_x_be_a_transformation_by_variable_substitution(
            i=(
                connective_for_is_well_formed_proposition(phi),
                connective_for_is_well_formed_proposition(psi),
                phi | connective_for_logical_implication | psi,
                phi),
            o=psi,
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


class WellFormedInference(WellFormedFormula):
    """An inference is the description of a usage of an inference-rule. Intuitively, it can be understood as an instance
    of the arguments passed to an inference-rule.

    TODO: QUESTION: Do we keep it in the data model?

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
            p: FlexibleTupl[FlexibleProposition] | None = None,
            a: FlexibleTupl | None = None) -> tuple[
        Connective, WellFormedInferenceRule, WellFormedTupl[WellFormedProposition], WellFormedTupl]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param i:
        :param p:
        :param a:
        :return:
        """
        con: Connective = connective_for_inference
        i: WellFormedInferenceRule = coerce_inference_rule(i=i)
        p: WellFormedTupl[WellFormedProposition] = coerce_tuple_of_proposition(s=p, interpret_none_as_empty=True)
        a: WellFormedTupl = coerce_tuple(s=a, interpret_none_as_empty=True)

        # Check the consistency of the shape of the premises and complementary arguments,
        # with the expected input-shapes of the inference-rule transformation.
        i2 = append_tuple_to_tuple(t1=p, t2=a)
        ok, _ = is_formula_equivalent_with_variables_2(phi=i2, psi=i.transformation.input_shapes,
                                                       variables=i.transformation.variables)
        if not ok:
            raise u1.ApplicativeError(
                msg='Well-formed inference rule validation error. ',
                i2=i2,
                input_shapes=i.transformation.input_shapes,
                variables=i.transformation.variables
            )

        return con, i, p, a

    def __new__(cls, i: FlexibleInferenceRule, p: FlexibleTupl[FlexibleProposition] | None = None,
                a: FlexibleTupl | None = None):
        """

        :param i: An inference-rule.
        :param p: A tuple of propositions denoted as the premises.
        :param a: A tuple of formulas denoted as the supplementary arguments.
        """
        c, i, p, a = WellFormedInference._data_validation_2(i=i, p=p, a=a)
        o: tuple = super().__new__(cls, con=c, t=(i, p, a))
        return o

    def __init__(self, i: FlexibleInferenceRule, p: FlexibleTupl[FlexibleProposition] | None = None,
                 a: FlexibleTupl | None = None):
        """Initializes a new inference.

        :param i: An inference-rule.
        :param p: A tuple of formulas denoted as the premises, that must be valid in the theory under consideration.
        :param a: A tuple of formulas denoted as the supplementary arguments, that may or may not be propositions,
                  and that may or may not be valid in the theory under consideration.
        """
        c, i, p, a = WellFormedInference._data_validation_2(i=i, p=p, a=a)
        super().__init__(con=c, t=(i, p, a,))

    @property
    def arguments(self) -> WellFormedTupl:
        """A tuple of supplementary arguments to be passed to the transformation as input parameters. These may or
        may not be propositions, and may or may not be valid in the theory under consideration."""
        return self[WellFormedInference.ARGUMENTS_INDEX]

    @property
    def inference_rule(self) -> WellFormedInferenceRule:
        """The inference-rule of the inference."""
        return self[WellFormedInference.INFERENCE_RULE_INDEX]

    @property
    def premises(self) -> WellFormedTupl:
        """The premises of the inference. All premises in the inference must be valid in the theory under
        consideration."""
        return self[WellFormedInference.PREMISES_INDEX]


FlexibleInference = typing.Optional[typing.Union[WellFormedInference]]


def inverse_map(m: FlexibleMap) -> WellFormedMap:
    """If a map is bijective, returns the inverse map."""
    m: WellFormedMap = coerce_map(m=m, interpret_none_as_empty=True)
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
    m2: WellFormedMap = WellFormedMap(d=domain, c=codomain)
    return m2


class WellFormedTheorem(WellFormedTheoryComponent):
    """A well-formed theorem is a proposition that is proven by a valid inference.

    Global definition
    ~~~~~~~~~~~~~~~~~

    Local definition
    ~~~~~~~~~~~~~~~~~

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
    PROPOSITION_INDEX: int = 0
    INFERENCE_INDEX: int = WellFormedTheoryComponent.JUSTIFICATION_INDEX

    @staticmethod
    def _data_validation_3(p: FlexibleProposition, i: FlexibleInference) -> tuple[
        Connective, WellFormedProposition, WellFormedInference]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        TODO: Consider removing Inference from the data model and merging its content inside the theorem formula.
            This is just a simplification, it is not absolutely necessary.

        :param p: A proposition denoted as the theorem valid-statement.
        :param i: An inference.
        :return:
        """
        con: Connective = connective_for_theorem
        p: WellFormedProposition = coerce_proposition(p=p)
        i: WellFormedInference = coerce_inference(i=i)

        # check the validity of the theorem
        try:
            i2: WellFormedTupl = append_tuple_to_tuple(t1=i.premises, t2=i.arguments)
            algorithm_output: WellFormedFormula = i.inference_rule.transformation.apply_transformation(i=i2)
        except u1.ApplicativeError as err:
            raise u1.ApplicativeError(
                msg='Theorem initialization error. '
                    'An error was raised when the transformation `f` '
                    'of the inference-rule `ir` was applied to check the validity of the theorem. ',
                f=i.inference_rule.transformation,
                ir=i.inference_rule,
                s=p,
                i=i)

        if len(i.inference_rule.transformation.output_declarations) == 0:
            # This transformation is deterministic because it comprises no new-object-declarations.
            try:
                is_formula_equivalent(phi=p, psi=algorithm_output, raise_error_if_false=True)
            except u1.ApplicativeError as error:
                # the formula is ill-formed because f(p) yields a formula that is not ~formula to phi.
                # raise an exception to prevent the creation of this ill-formed theorem-by-inference.
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_045,
                    msg='`s` is not formula-equivalent to `algorithm_output`.',
                    s=p,
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
                phi=p,
                psi=i.inference_rule.transformation.output_shape,
                variables=i.inference_rule.transformation.output_declarations)
            if not success_1:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_085,
                    msg='Theorem initialization failure. '
                        'The valid-statement `s` is not consistent with the conclusion of the inference-rule `i`, '
                        'considering new object declarations.',
                    s=p,
                    i_conclusion=i.inference_rule.transformation.output_shape,
                    i_declarations=i.inference_rule.transformation.output_declarations,
                    success_1=success_1)
            # We can reverse the map and re-test formula-equivalence-with-variables.
            m1_reversed = inverse_map(m=m1)
            success_2, _ = is_formula_equivalent_with_variables_2(phi=p,
                                                                  psi=i.inference_rule.transformation.output_shape,
                                                                  variables=m1.domain)
            pass
            valid_statement_reversed: WellFormedFormula = substitute_formulas(phi=p, m=m1_reversed)
            if not is_formula_equivalent(phi=valid_statement_reversed,
                                         psi=i.inference_rule.transformation.output_shape):
                raise u1.ApplicativeError(
                    msg='Reversing the valid-statement does not yield the inference-rule conclusion.',
                    valid_statement_reversed=valid_statement_reversed,
                    expected_conclusion=i.inference_rule.transformation.output_shape)

        return con, p, i

    def __new__(cls, p: FlexibleProposition, i: FlexibleInference):
        con, p, i = WellFormedTheorem._data_validation_3(p=p, i=i)
        o: tuple = super().__new__(cls, con=con, s=p, j=i)
        return o

    def __init__(self, p: FlexibleProposition, i: FlexibleInference):
        con, p, i = WellFormedTheorem._data_validation_3(p=p, i=i)
        # complete object initialization to assure that we have a well-formed formula with connective, etc.
        super().__init__(con=con, s=p, j=i)

    @property
    def inference(self) -> WellFormedInference:
        """The inference justifying the proposition of the theorem."""
        return self[WellFormedTheorem.INFERENCE_INDEX]

    @property
    def proposition(self) -> WellFormedProposition:
        """The proposition proven by the theorem."""
        return self[WellFormedTheorem.PROPOSITION_INDEX]


FlexibleTheorem = typing.Union[WellFormedTheorem, WellFormedFormula]
FlexibleComponent = typing.Union[FlexibleAxiom, FlexibleTheorem, FlexibleInferenceRule, FlexibleExtension]


class Heuristic(abc.ABC):
    """A heuristic is a method that facilitates proofs. It recognizes a conjecture pattern to check if the
    conjecture is a conjecture that it is able to process, and then it applies an algorithm to attempt to automatically
    derive the conjecture.

    Heuristics can be attached to theories to simplify proofs.
    """

    @abc.abstractmethod
    def process_conjecture(self, conjecture: FlexibleFormula, t: FlexibleTheory) -> tuple[WellFormedTheory, bool,]:
        """

        :param conjecture:
        :param t:
        :return:
        """
        pass


class WellFormedTheory(WellFormedTheoreticalContext):
    """A well-formed theory is a :ref:`theoretical context<well_formed_theoretical_context>` of the form
    ⌜ :math:`\\text{theory}\\left( \\boldsymbol{d_1}, \\boldsymbol{d_2}, \\cdots, \\boldsymbol{d_n} \\right)` ⌝
    where :math:`\\boldsymbol{d_i}` is a valid derivation in that theory.

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed theory if and only if:
     - its root connective is the theory-formula connective,
     - all term :math:`\\psi` in :math:`\\phi` is:
       - either a well-formed inference rule,
       - a locally well-formed axiom with regard to :math:`\\phi`,
       - a locally well-formed theorem with regard to :math:`\\phi`,
       - or a valid extension of a theoretical context.

    Notes
    ^^^^^^^^^^^^^^^^^^^^

    Note 1
    ~~~~~~~~~~~~~~~~~~
    The empty theory is the theory that has no terms, i.e.:
    :math:`\\text{theory}\\left( \\right)`

    """

    _last_index: int = 0

    @staticmethod
    def _data_validation_2(con: Connective, t: FlexibleTheory | None = None, d: FlexibleEnumeration = None
                           ) -> tuple[Connective, WellFormedEnumeration]:
        """

        :param t:
        :param d:
        :return:
        """
        con: Connective = connective_for_theory
        if t is not None:
            t: WellFormedTheory = coerce_theory(t=t, interpret_none_as_empty=False, canonical_conversion=True)
        d: WellFormedEnumeration = coerce_enumeration(e=d, strip_duplicates=True, canonic_conversion=True,
                                                      interpret_none_as_empty=True)
        is_valid, v, u = would_be_valid_components_in_theory(v=t, u=d, raise_error_if_false=True)
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
        c2, d2 = WellFormedTheory._data_validation_2(con=con, t=t, d=d)
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
        c2, d2 = WellFormedTheory._data_validation_2(con=con, t=t, d=d)
        super().__init__(con=c2, t=d2, **kwargs)
        if t is not None:
            # Copies the heuristics and any other decoration from the base theory
            copy_theory_decorations(target=self, decorations=(t,))

        # Default typesetting configuration
        if pl1.REF_TS not in self.ts.keys():
            WellFormedTheory._last_index = WellFormedTheory._last_index + 1
            self.ts[pl1.REF_TS] = pl1.NaturalIndexedSymbolTypesetter(body_ts=pl1.symbols.t_uppercase_script,
                                                                     index=WellFormedTheory._last_index)
        if pl1.DECLARATION_TS not in self.ts.keys():
            self.ts[pl1.DECLARATION_TS] = typesetters.declaration(conventional_class='theory')

        if t is None:
            # This is not an extended theory, this is a new theory.
            # Output its declaration.
            u1.log_info(self.typeset_as_string(theory=self, ts_key=pl1.DECLARATION_TS))

    def extend_with_component(
            self, c: FlexibleComponent,
            **kwargs) -> WellFormedTheoreticalContext:
        """Given a theory ``self`` and a theory component ``c``, returns a new theory ``self′``
        that is an extension of ``self`` with ``c`` appended as its last component.

        :param c:
        :return:
        """
        c: WellFormedTheoryComponent = coerce_theory_component(d=c)
        return WellFormedTheory(t=self, d=(c,))


def transform_axiomatization_to_theory(a: FlexibleAxiomatization) -> WellFormedTheory:
    """Canonical function that converts an axiomatization ``a`` to a theory.

    An axiomatization is a theory whose derivations are limited to axioms and inference-rules.
    This function provides the canonical conversion method from axiomatizations to theories,
    by returning a new theory ``t`` such that all the derivations in ``t`` are derivations of ``a``,
    preserving canonical order.

    :param a: An axiomatization.
    :return: A theory.
    """
    a: WellFormedAxiomatization = coerce_axiomatization(a=a)
    t: WellFormedTheory = WellFormedTheory(d=(*a,))
    return t


def transform_hypothesis_to_theory(h: FlexibleHypothesis) -> WellFormedTheory:
    """Canonical function that converts a hypothesis ``h`` to a theory.

    A hypothesis is a pair (b, a) where:
     - `b` is a theory denoted as the base-theory,
     - ``a`` is a proposition denoted as the assumption.

    The canonical conversion of hypothesis into theory consists in
    considering the assumption as an axiom.

    :param h: A hypothesis.
    :return: A theory.
    """
    h: WellFormedHypothesis = coerce_hypothesis(h=h)
    b: WellFormedTheory = h.base_theory
    a: WellFormedFormula = h.assumption
    t: WellFormedTheory = WellFormedTheory(t=b, d=(a,))
    return t


def transform_theory_to_axiomatization(t: FlexibleTheory, interpret_none_as_empty: bool = True,
                                       canonical_conversion: bool = True) -> WellFormedAxiomatization:
    """Canonical function that converts a theory ``t`` to an axiomatization.

    An axiomatization is a theory whose derivations are limited to axioms and inference-rules.
    This function provides the canonical conversion method from theories to axiomatizations,
    by returning a new axiomatization ``a`` such that all the axioms and inference-rules in ``t``
    become derivations of ``a``, preserving canonical order.

    It follows that all theorems in ``t`` are discarded.

    :param t: A theory.
    :param interpret_none_as_empty: If ``t`` is None, interpret it as the empty-theory.
    :param canonical_conversion: If necessary, apply canonic-conversion to coerce ``t`` to a theory.
    :return: An axiomatization.
    """
    t: WellFormedTheory = coerce_theory(t=t, interpret_none_as_empty=interpret_none_as_empty,
                                        canonical_conversion=canonical_conversion)
    e: WellFormedEnumeration = WellFormedEnumeration(e=None)
    for c in iterate_theory_components(t=t):
        if is_well_formed_axiom(a=c):
            e = append_element_to_enumeration(e=e, x=c)
        if is_well_formed_inference_rule(i=c):
            e = append_element_to_enumeration(e=e, x=c)
    a: WellFormedAxiomatization = WellFormedAxiomatization(a=None, d=(*e,))
    return a


def is_extension_of(t2: FlexibleTheory, t1: FlexibleTheory, interpret_none_as_empty: bool = True,
                    canonical_conversion: bool = True, raise_error_if_false: bool = False):
    """Given two theories or axiomatizations `t1` and `t2`, returns ``True`` if and only if `t2` is an extension of `t1`,
    ``False`` otherwise.

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
    t1: WellFormedTheory = coerce_theory(t=t1, interpret_none_as_empty=interpret_none_as_empty,
                                         canonical_conversion=canonical_conversion)
    t2: WellFormedTheory = coerce_theory(t=t2, interpret_none_as_empty=interpret_none_as_empty,
                                         canonical_conversion=canonical_conversion)

    a1: WellFormedAxiomatization = transform_theory_to_axiomatization(t=t1)
    a2: WellFormedAxiomatization = transform_theory_to_axiomatization(t=t2)

    e1: WellFormedEnumeration = transform_axiomatization_to_enumeration(a=a1)
    e2: WellFormedEnumeration = transform_axiomatization_to_enumeration(a=a2)

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
    """Returns ``True`` if `t1` is axiomatization-equivalent with `t2`, denoted :math:`t_1 \\sim_{a} t_2`.

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
    t1: WellFormedTheory = coerce_theory(t=t1, interpret_none_as_empty=interpret_none_as_empty,
                                         canonical_conversion=canonical_conversion)
    t2: WellFormedTheory = coerce_theory(t=t2, interpret_none_as_empty=interpret_none_as_empty,
                                         canonical_conversion=canonical_conversion)

    a1: WellFormedAxiomatization = transform_theory_to_axiomatization(t=t1)
    a2: WellFormedAxiomatization = transform_theory_to_axiomatization(t=t2)

    e1: WellFormedEnumeration = transform_axiomatization_to_enumeration(a=a1)
    e2: WellFormedEnumeration = transform_axiomatization_to_enumeration(a=a2)

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


def transform_enumeration_to_theory(e: FlexibleEnumeration) -> WellFormedTheory:
    """Canonical function that converts an enumeration "e" to a theory,
    providing that all elements "x" of "e" are well-formed derivations.

    :param e: An enumeration.
    :return: A theory.
    """
    e: WellFormedEnumeration = coerce_enumeration(e=e, interpret_none_as_empty=True)
    t: WellFormedTheory = WellFormedTheory(d=e)
    return t


def transform_formula_to_tuple(phi: FlexibleFormula) -> WellFormedTupl:
    """Transforms a formula `phi` into a tupl whose terms are the terms of `phi` with order preserved.

    This is the canonical transformation of formulas to tuples.

    Note 1: Every formula is a tuple if we don't consider its connective.

    Note 2: If `phi` is a well-formed tupl, the function returns `phi`.

    :param phi: A formula.
    :return: A tupl.
    """
    phi: WellFormedFormula = coerce_formula(phi=phi)
    if is_well_formed_tupl(t=phi):
        t: WellFormedTupl = coerce_tuple(s=phi)
        return t
    else:
        t: WellFormedTupl = WellFormedTupl(e=iterate_formula_terms(phi=phi))
        return t


def transform_tuple_to_theory(t: FlexibleTupl) -> WellFormedTheory:
    """Canonical function that converts a tuple ``t`` to a theory,
    providing that all elements "x" of ``t`` are well-formed derivations.

    :param t: A tupl.
    :return: A theory.
    """
    t: WellFormedTupl = coerce_tuple(s=t)
    e: WellFormedEnumeration = coerce_enumeration(e=t, strip_duplicates=True, canonic_conversion=True,
                                                  interpret_none_as_empty=True)
    t2: WellFormedTheory = transform_enumeration_to_theory(e=e)
    return t2


def transform_axiomatization_to_enumeration(a: FlexibleAxiomatization) -> WellFormedEnumeration:
    """Canonical function that converts an axiomatization ``a`` to an enumeration.

    An axiomatization is fundamentally an enumeration of derivations, limited to axioms and inference-rules.
    This function provides the canonical conversion method from axiomatizations to enumeration,
    by returning a new enumeration "e" such that all the derivations in ``a`` are elements of "e",
    preserving order.

    Invertibility: yes
    Bijectivity: yes

    :param a: An axiomatization.
    :return: An enumeration.
    """
    a: WellFormedAxiomatization = coerce_axiomatization(a=a)
    e: WellFormedEnumeration = WellFormedEnumeration(e=(*a,))
    return e


def transform_formula_to_enumeration(phi: FlexibleFormula, strip_duplicates: bool = False) -> WellFormedEnumeration:
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
    phi: WellFormedFormula = coerce_formula(phi=phi)
    if isinstance(phi, WellFormedEnumeration):
        return phi
    else:
        return WellFormedEnumeration(e=iterate_formula_terms(phi=phi), strip_duplicates=strip_duplicates)


def transform_theoretical_context_to_enumeration(t: FlexibleTheoreticalContext) -> WellFormedEnumeration:
    """Canonical function that converts a theoretical context ``t`` to an enumeration.

    A theory is fundamentally an enumeration of derivations.
    This function provides the canonical conversion method from theory to enumeration,
    by returning a new enumeration "e" such that all the derivations in ``t`` are elements of "e",
    preserving order.

    If the theoretical context contains extensions, the extensions are not recursed but
    returned directly.

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


class WellFormedAxiomatization(WellFormedTheoreticalContext):
    """A well-formed axiomatization is a :ref:`theoretical context<well_formed_theoretical_context>` of the form
    ⌜ :math:`\\text{axiomatization}\\left( \\boldsymbol{d_1}, \\boldsymbol{d_2}, \\cdots, \\boldsymbol{d_n} \\right)` ⌝
    where :math:`\\boldsymbol{d_i}` is a derivation that is a valid constituent of an axiomatic base.

    See :function:`axiomatic_base` for a definition of axiomatic base.

    Definition
    ^^^^^^^^^^^^^^^^^^^^
    A formula :math:`\\phi` is a well-formed axiomatization if and only if:
     - its root connective is the axiomatization-formula connective,
     - all term :math:`\\psi` in :math:`\\phi` is:
       - either a well-formed inference rule,
       - a well-formed axiom,
       - or an extension of an axiomatization.

    Notes
    ^^^^^^^^^^^^^^^^^^^^

    Note 1
    ~~~~~~~~~~~~~~~~~~
    The empty axiomatization is the axiomatization that has no terms, i.e.:
    :math:`\\text{axiomatization}\\left( \\right)`

    """
    _last_index: int = 0

    @staticmethod
    def _data_validation_2(a: FlexibleAxiomatization | None = None,
                           d: FlexibleEnumeration = None) -> tuple[Connective, WellFormedEnumeration]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param a:
        :param d:
        :return:
        """
        global connective_for_axiomatization_formula
        d: WellFormedEnumeration = coerce_enumeration(e=d, interpret_none_as_empty=True, strip_duplicates=True)
        if a is not None:
            a: WellFormedAxiomatization = coerce_axiomatization(a=a)
            # Duplicate derivations are not allowed in axiomatizations, so strip duplicates during merge.
            # The first occurrence is maintained, and the second occurrence is stripped.
            d: WellFormedEnumeration = WellFormedEnumeration(e=(*a, *d), strip_duplicates=True)
        # coerce all elements of the enumeration to axioms or inference-rules.
        coerced_components: WellFormedEnumeration = WellFormedEnumeration(e=None)
        for x in iterate_enumeration_elements(e=d):
            if is_well_formed_inference_rule(i=x):
                # This is an inference-rule.
                inference_rule: WellFormedInferenceRule = coerce_inference_rule(i=x)
                coerced_components: WellFormedEnumeration = append_element_to_enumeration(
                    e=coerced_components, x=inference_rule)
            elif is_well_formed_axiom(a=x):
                # This is an axiom.
                axiom: WellFormedAxiom = coerce_axiom(a=x)
                coerced_components: WellFormedEnumeration = append_element_to_enumeration(
                    e=coerced_components, x=axiom)
            elif is_well_formed_extension(e=x):
                # This is a theory extension.
                e: WellFormedExtension = coerce_extension(e=x)
                # Check that the extension is a valid axiomatic base.
                if not is_well_formed_axiomatic_base_component(d=e):
                    raise u1.ApplicativeError(
                        msg='Well-formed axiomatization data validation failure. Extension `e` is not a valid'
                            'axiomatic base.',
                        e=e,
                        a=a,
                        d=d
                    )
                coerced_components: WellFormedEnumeration = append_element_to_enumeration(
                    e=coerced_components, x=e)
            else:
                # Incorrect form.
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_062,
                                          msg=f'Cannot append derivation `d` to axiomatization ``a``, '
                                              f'because `d` is not in proper form '
                                              f'(e.g.: axiom, inference-rule).',
                                          d=d,
                                          a=a
                                          )
        return connective_for_axiomatization_formula, coerced_components

    def __new__(cls, a: FlexibleAxiomatization | None = None, d: FlexibleEnumeration = None, **kwargs):
        c, t = WellFormedAxiomatization._data_validation_2(a=a, d=d)
        o: tuple = super().__new__(cls, con=c, t=t, **kwargs)
        return o

    def __init__(self, a: WellFormedAxiomatization | None = None, d: FlexibleEnumeration = None, **kwargs):
        """Declares a new axiomatization.

        :param a: A base axiomatization. If ``None``, the empty axiomatization is assumed as a base.
        :param d: An enumeration of supplementary axioms and/or inference rules to be appended to the base
            axiomatization.
        """
        c, t = WellFormedAxiomatization._data_validation_2(a=a, d=d)
        super().__init__(con=c, t=t, **kwargs)
        self._heuristics: set[Heuristic, ...] | set[{}] = set()
        if a is not None:
            # Copies the heuristics and any other decoration from the base theory
            copy_theory_decorations(target=self, decorations=(a,))
        if pl1.REF_TS not in self.ts.keys():
            WellFormedTheory._last_index = WellFormedAxiomatization._last_index + 1
            self.ts[pl1.REF_TS] = pl1.NaturalIndexedSymbolTypesetter(body_ts=pl1.symbols.t_uppercase_script,
                                                                     index=WellFormedAxiomatization._last_index)
        if pl1.DECLARATION_TS not in self.ts.keys():
            self.ts[pl1.DECLARATION_TS] = typesetters.declaration(conventional_class='axiomatization')

        if t is None:
            # This is not an extended theory, this is a new theory.
            # Output its declaration.
            u1.log_info(self.typeset_as_string(theory=self, ts_key=pl1.DECLARATION_TS))

    def extend_with_component(
            self, c: FlexibleComponent,
            return_theory_if_necessary: bool = True, **kwargs) -> WellFormedTheoreticalContext:
        """Given an axiomatization ``self`` and a theory component ``c``, returns a new axiomatization ``self′``
        that is an extension of ``self`` with ``c``.

        :param c:
        :param return_theory_if_necessary: If ``self`` is an axiomatization and ``c`` is either a theorem,
            or an extension that contains (recursively) a theorem,
            returns a theory (instead of an axiomatization),
            raise an error otherwise.
        :return:
        """
        c: WellFormedTheoryComponent = coerce_theory_component(d=c)
        if is_well_formed_axiomatic_base_component(d=c):
            return WellFormedAxiomatization(a=self, d=(c,))
        elif return_theory_if_necessary:
            t: WellFormedTheory = transform_axiomatization_to_theory(a=self)
            return t.extend_with_component(c=c, **kwargs)
        else:
            raise u1.ApplicativeError(
                msg='Axiomatization extension failure. Axiomatization `self` could not be extended with component `c`.',
                c=c, return_theory_if_necessary=return_theory_if_necessary,
                kwargs=kwargs, self=self
            )

    @property
    def heuristics(self) -> set[Heuristic, ...] | set[{}]:
        """A python-set of heuristics.

        Heuristics are not formally part of an axiomatization. They are decorative objects used to facilitate proof
        derivations.
        """
        return self._heuristics


FlexibleAxiomatization = typing.Optional[
    typing.Union[WellFormedAxiomatization, typing.Iterable[typing.Union[WellFormedAxiom, WellFormedInferenceRule]]]]
"""A flexible python type for which coercion into type Axiomatization is supported.

Note that a flexible type is not an assurance of well-formedness. Coercion assures well-formedness
and raises an error if the object is ill-formed."""

FlexibleTheory = typing.Optional[
    typing.Union[WellFormedAxiomatization, WellFormedTheory, typing.Iterable[FlexibleComponent]]]
"""A flexible python type for which coercion into type Theory is supported.

Note that a flexible type is not an assurance of well-formedness. Coercion assures well-formedness
and raises an error if the object is ill-formed."""

FlexibleHypothesis = FlexibleFormula
"""TODO: Develop FlexibleHypothesis
"""

FlexibleTheoreticalContext = FlexibleTheory | FlexibleAxiomatization | FlexibleHypothesis

FlexibleDecorations = typing.Optional[typing.Union[typing.Tuple[FlexibleTheory, ...], typing.Tuple[()]]]


def is_recursively_included_in(s: FlexibleFormula, f: FlexibleFormula) -> bool:
    """Returns ``True`` if and only if formula `s` is recursively included in formula `f`, ``False`` otherwise.

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
    s: WellFormedFormula = coerce_formula(phi=s)
    f: WellFormedFormula = coerce_formula(phi=f)
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


def get_leaf_formulas(phi: FlexibleFormula, eb: WellFormedEnumeration = None) -> WellFormedEnumeration:
    """Return the enumeration of leaf-formulas in phi.

    Note: if phi is a leaf-formula, return phi.

    :param phi:
    :param eb: (conditional) An enumeration-builder for recursive call.
    :return:
    """
    phi: WellFormedFormula = coerce_formula(phi=phi)
    if eb is None:
        eb: WellFormedEnumeration = WellFormedEnumeration(e=None)
    if not is_element_of_enumeration(x=phi, e=eb) and is_leaf_formula(phi=phi):
        eb = append_element_to_enumeration(x=phi, e=eb)
    else:
        for term in phi:
            # Recursively call get_leaf_formulas,
            # which complete eb with any remaining leaf formulas.
            eb = union_enumeration(phi=eb, psi=get_leaf_formulas(phi=term, eb=eb))
    return eb


def rank(phi: FlexibleFormula) -> int:
    """Return the rank of the formula `phi`.

    Intuitively, the rank of a formula is the maximal depth of sub-formulas.

        "(...) define rk φ, the rank of the formula φ, by rk π = 0 for prime formulas π
        and rk(α ∧ β) = max{rk α, rk β} +1, rk ¬α = rk ∀xα = rk α +1."
        -- :cite:`rautenberg_2006_conciseintroduction`

    :param phi: A formula.
    :return: The rank of the formula `phi`.
    """
    phi = coerce_formula(phi=phi)
    if phi.arity == 0:
        return 1
    else:
        return max(rank(phi=term) for term in phi) + 1


def extend_with_component(t: FlexibleTheoreticalContext, c: FlexibleComponent,
                          return_theory_if_necessary: bool = True,
                          **kwargs) -> WellFormedTheoreticalContext:
    """Given the theoretical context ``t``, returns a new theoretical context ``t′`` that is
    an extension of ``t`` with the component ``c``.

    :param t: A theoretical context.
    :param c: A theory component.
    :param return_theory_if_necessary: If ``self`` is an axiomatization and ``c`` is either a theorem,
        or an extension that contains (recursively) a theorem,
        returns a theory (instead of an axiomatization),
        raise an error otherwise.
    :return: A theoretical context.
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    c: WellFormedTheoryComponent = coerce_theory_component(d=c)
    return t.extend_with_component(c=c, return_theory_if_necessary=return_theory_if_necessary, **kwargs)


def append_to_theory(*args, t: FlexibleTheoreticalContext) -> WellFormedTheory:
    """Extend theoretical context ``t`` by appending to it whatever components are passed in *args.

    TODO: REDEVELOP THIS TO SUPPORT FLEXIBLE THEORETICAL CONTEXTS,
        THIS FUNCTION MUST BE REPLACED BY EXTEND_WITH_COMPONENT,
        AND WE MUST PRESERVE THE PYTHON TYPE OF THE ORIGINAL `T`
        WHENEVER POSSIBLE, E.G. APPENDING AXIOMS TO AN AXIOMATIZATION
        MUST YIELD AN AXIOMATIZATION.

    :param args:
    :param t:
    :return:
    """
    t: FlexibleTheoreticalContext = coerce_theoretical_context(t=t)
    if args is None:
        return t
    else:
        for argument in args:
            if is_well_formed_axiomatization(a=argument):
                # If the argument is an axiomatization,
                # all the derivations (axioms and inference-rules) from the axiomatization
                # are appended to the theory.
                extension_a: WellFormedAxiomatization = coerce_axiomatization(a=argument)
                t: WellFormedTheory = WellFormedTheory(t=t, d=(*extension_a,))
            elif is_well_formed_theory(t=argument):
                # If the argument is an axiomatization,
                # all the derivations (axioms, inference-rules, theorems) from the axiomatization
                # are appended to the theory.
                extension_t: WellFormedTheory = coerce_theory(t=argument)
                t: WellFormedTheory = WellFormedTheory(t=t, d=(*extension_t,))
                copy_theory_decorations(target=t, decorations=(extension_t,))
            elif is_well_formed_axiom(a=argument):
                extension_a: WellFormedAxiom = coerce_axiom(a=argument)
                if not is_axiom_of(a=extension_a, t=t):
                    t: WellFormedTheory = WellFormedTheory(t=t, d=(extension_a,))
            elif is_well_formed_inference_rule(i=argument):
                extension_i: WellFormedInferenceRule = coerce_inference_rule(i=argument)
                if not is_inference_rule_of(i=extension_i, t=t):
                    t: WellFormedTheory = WellFormedTheory(t=t, d=(extension_i,))
            elif is_well_formed_inference(i=argument):
                extension_i: WellFormedInferenceRule = coerce_inference_rule(i=argument)
                if not is_inference_rule_of(i=extension_i, t=t):
                    t: WellFormedTheory = WellFormedTheory(t=t, d=(extension_i,))
            elif is_well_formed_theorem(m=argument):
                extension_m: WellFormedTheorem = coerce_theorem(m=argument)
                if not is_theorem_of(m=extension_m, t=t):
                    t: WellFormedTheory = WellFormedTheory(t=t, d=(extension_m,))
            else:
                raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_049,
                                          msg=f'Invalid argument: ({type(argument)}) {argument}.')
        return t


def append_component_to_axiomatization(d: FlexibleComponent, a: FlexibleAxiomatization) -> WellFormedAxiomatization:
    """Extend axiomatization ``a`` with derivation `d`.

    :param d:
    :param a:
    :return:
    """
    d: WellFormedTheoryComponent = coerce_theory_component(d=d)
    a: WellFormedAxiomatization = coerce_axiomatization(a=a)
    if is_well_formed_axiom(a=d):
        extension_a: WellFormedAxiom = coerce_axiom(a=d)
        if not is_axiom_of(a=extension_a, t=a):
            a: WellFormedAxiomatization = WellFormedAxiomatization(a=a, d=(extension_a,))
    elif is_well_formed_inference_rule(i=d):
        extension_i: WellFormedInferenceRule = coerce_inference_rule(i=d)
        if not is_inference_rule_of(i=extension_i, t=a):
            a: WellFormedAxiomatization = WellFormedAxiomatization(a=a, d=(extension_i,))
    else:
        raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_062,
                                  msg=f'Cannot append derivation `d` to axiomatization ``a``, '
                                      f'because `d` is not in proper form '
                                      f'(e.g.: axiom, inference-rule).',
                                  d=d,
                                  a=a
                                  )
    return a


def append_args_to_axiomatization(*args, a: FlexibleAxiomatization) -> WellFormedAxiomatization:
    """Extend theory t by appending to it whatever is passed in *args.

    :param args:
    :param a:
    :return:
    """
    a: WellFormedAxiomatization = coerce_axiomatization(a=a)
    if args is None:
        return a
    else:
        for d in args:
            a = append_component_to_axiomatization(d=d, a=a)
        return a


class AutoDerivationFailure(Exception):
    """Auto-derivation was required but failed to succeed."""

    def __init__(self, msg: str, **kwargs):
        super().__init__(msg)
        self.kwargs = kwargs


def derive_1(t: FlexibleTheoreticalContext, c: FlexibleFormula, p: FlexibleTupl[FlexibleProposition],
             i: FlexibleInferenceRule, a: FlexibleTupl | None = None,
             raise_error_if_false: bool = True) -> typing.Tuple[
    WellFormedTheoreticalContext, bool, WellFormedTheorem | None]:
    """Given a theory ``t``, derives a new theory `t′` that extends ``t`` with a new theorem `c`
    derived by applying inference-rule `i`.

    :param t: A theory.
    :param c: A proposition denoted as the conjecture.
    :param p: A tuple of propositions denoted as the premises.
    :param i: An inference-rule.
    :param a: (For algorithmic-transformations) A tuple of formulas denoted as the supplementary-arguments to be
        transmitted as input arguments to the external-algorithm.
    :param raise_error_if_false:
    :return: A python-tuple `(t′, b, m)` where `t′` is the theory ``t`` with the new theorem if derived successfully,
        `b` is ``True`` if the derivation was successful, ``False`` otherwise, and `m` is the new derivation.
    """
    # parameters validation
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, interpret_none_as_empty=True,
                                                                 canonical_conversion=True)
    c: WellFormedFormula = coerce_formula(phi=c)
    # TODO: Question: when calling coerce_tuple_of_proposition, we do not pass t=t,
    #   and thus limit coercion to proposition global well-formedness. Otherwise,
    #   it would be necessary to have `is-proposition(p)` for every proposition `p`,
    #   leading to the impossibility to declare the first proposition. Global well-formedness
    #   is thus sufficient to allow derivation of theorems, without imposing a priori
    #   a theory of propositional syntax.
    p: WellFormedTupl = coerce_tuple_of_proposition(s=p, t=None, interpret_none_as_empty=True, canonic_conversion=True)
    i: WellFormedInferenceRule = coerce_inference_rule(i=i)
    a: WellFormedTupl = coerce_tuple(s=a, interpret_none_as_empty=True, canonic_conversion=True)

    if not is_inference_rule_of(i=i, t=t):
        # The inference_rule is not in the theory,
        # it follows that it is impossible to derive the conjecture from that inference_rule in this theory.
        if raise_error_if_false:
            raise u1.ApplicativeError(code=c1.ERROR_CODE_AS1_067,
                                      msg=f'Derivation fails because inference-rule `i` is not valid in theory ``t``.',
                                      i=i,
                                      t=t)
        else:
            return t, False, None

    for q in p:
        # The validity of the premises is checked during theory initialization,
        # but re-checking it here "in advance" helps provide more context in the exception that is being raised.
        if not is_valid_proposition_so_far_1(p=q, t=t):
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_051,
                    msg=f'Conjecture `c` cannot be derived from inference-rule `i` because '
                        f'premise `q` is not a valid-statement in theory ``t``. '
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
    try:
        i2: WellFormedInference = WellFormedInference(p=p, a=a, i=i)
    except u1.ApplicativeError as err:
        # If the initialization of the inference fails,
        # it means that the inference is not valid.
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='Derivation failure. '
                    'The initialization of the inference `inference(p, a, i)` failed and raised error `err`, '
                    'meaning that it is invalid. ',
                p=p,
                a=a,
                i=i,
                t=t,
                err=err
            )
        else:
            return t, False, None

    # Prepare the new theorem.
    try:
        # TODO: This is inelegant. When we use an external-algorithm,
        #   I was not able to find a simple solution to catch errors.
        #   Some evolution of the data model is probably needed here.
        theorem: WellFormedTheorem = WellFormedTheorem(p=c, i=i2)
    except u1.ApplicativeError as error:
        # If the initialization of the theorem fails,
        # it means that the theorem is not valid.
        if raise_error_if_false:
            raise u1.ApplicativeError(
                msg='Derivation failure. '
                    'The initialization of the theorem failed, meaning that it is invalid. '
                    'The inference is composed of the premises `p`, the arguments ``a``, '
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
    # t: WellFormedTheory = append_to_theory(theorem, t=t)
    t: WellFormedTheoreticalContext = extend_with_component(t=t, c=theorem, return_theory_if_necessary=True)
    # t: Theory = Theory(t=t, d=(theorem,), decorations=(t,))

    u1.log_info(theorem.typeset_as_string(theory=t))

    return t, True, theorem


def is_in_map_domain(phi: FlexibleFormula, m: FlexibleMap) -> bool:
    """Return True if phi is a formula in the domain of map m, False otherwise."""
    phi = coerce_formula(phi=phi)
    m = coerce_map(m=m, interpret_none_as_empty=True)
    return is_element_of_enumeration(x=phi, e=m.domain)


def derive_0(t: FlexibleTheoreticalContext, c: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[WellFormedTheoreticalContext, bool, typing.Optional[WellFormedTheoryComponent]]:
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
    :rtype: typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent]]
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t, canonical_conversion=True,
                                                                 interpret_none_as_empty=True)
    c: WellFormedFormula = coerce_formula(phi=c)
    if debug:
        u1.log_debug(f'derive_0: start. conjecture:{c}.')
    if is_valid_proposition_so_far_1(p=c, t=t):  # this first check is superfluous
        # loop through derivations
        for c2 in t.iterate_components():
            if is_formula_equivalent(phi=c, psi=c2.valid_statement):
                # the valid-statement of this derivation matches phi,
                # the auto_derive is successful.
                # if debug:
                # u1.log_info(f'auto_derive_0 successful: {derivation}')
                return t, True, c2
    # all derivations have been tested and none matched phi,
    # it follows that the auto_derive failed.
    return t, False, None


def derive_2(t: FlexibleTheoreticalContext, c: FlexibleFormula, i: FlexibleInferenceRule,
             raise_error_if_false: bool = True,
             debug: bool = False) -> \
        typing.Tuple[WellFormedTheoreticalContext, bool, typing.Optional[WellFormedTheoryComponent]]:
    """Derives a new theory `t′` that extends ``t`` with a new theorem based on conjecture `c` using inference-rule `i`.

    Note: in contrast, derive_1 requires the explicit list of premises. derive_2 is more convenient to use because it
     automatically finds a set of premises among the valid-statements in theory t, such that conjecture c can be
     derived.

    :param t: a theory.
    :param c: the conjecture to be proven.
    :param i: the inference-rule from which the conjecture can be derived.
    :param raise_error_if_false: raise an error if the derivation fails.
    :param debug:
    :return: A python-tuple (t′, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent]]
    """
    t: WellFormedTheoreticalContext = coerce_theoretical_context(t=t)
    c: WellFormedFormula = coerce_formula(phi=c)
    i: WellFormedInferenceRule = coerce_inference_rule(i=i)
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
                msg='Inference-rule `i` is not an element of theory ``t``. '
                    'It follows that proposition `c` cannot be inferred in ``t`` using `i`.',
                c=c, i=i, t=t,
            )
        return t, False, None

    # First try the less expansive auto_derive_0 algorithm
    t, successful, c2, = derive_0(t=t, c=c, debug=debug)
    if successful:
        return t, successful, c2

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
        unknown_variable_values: WellFormedEnumeration = WellFormedEnumeration()
        for x in i.transformation.variables:
            if not is_element_of_enumeration(x=x, e=known_variable_values.domain):
                unknown_variable_values = WellFormedEnumeration(e=(*unknown_variable_values, x,))

        # Using substitution for the known_variable_values,
        # a more accurate set of premises can be computed, denoted necessary_premises.
        necessary_premises: WellFormedTupl = WellFormedTupl(
            e=substitute_formulas(phi=i.transformation.input_shapes, m=known_variable_values))

        # Find a set of valid_statements in theory t, such that they match the necessary_premises.
        success, effective_premises = are_valid_statements_in_theory_with_variables(
            s=necessary_premises, t=t, variables=i.transformation.variables,
            variables_values=known_variable_values)

        if success:
            # All required premises are present in theory t, the conjecture can be proven.
            t, ok, c2 = derive_1(t=t, c=c, p=effective_premises,
                                 i=i, raise_error_if_false=True)
            return t, True, c2
        else:
            # The required premises are not present in theory t, report failure.
            if raise_error_if_false:
                raise u1.ApplicativeError(
                    code=c1.ERROR_CODE_AS1_079,
                    msg='Some premise required by inference-rule `i` are not valid propositions in theory ``t``. '
                        'It follows that proposition `c` cannot be inferred in ``t`` using `i`.',
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
                    'It follows that proposition `c` cannot be inferred in ``t`` using `i`.',
                c=c, i=i, known_variable_values=known_variable_values, t=t
            )
        return t, False, None


def auto_derive_with_heuristics(t: FlexibleTheory, conjecture: FlexibleFormula) -> \
        typing.Tuple[WellFormedTheory, bool]:
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


def auto_derive_2(t: FlexibleTheory, c: FlexibleFormula, debug: bool = False) -> \
        typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent]]:
    """An algorithm that attempts to automatically prove a conjecture in a theory.

    The auto_derive_2 algorithm "wide and shallow inference" builds on auto_derive_1 and:
    1) loop through all inference-rules in theory t, and try the auto_derive_1 algorithm.

    Note: this algorithm is still trivial as it does not rely on recursion to look for solutions.

    :param t:
    :param c:
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent]]
    """
    t = coerce_theory(t=t)
    c = coerce_formula(phi=c)
    if debug:
        u1.log_debug(f'auto_derive_2: start. conjecture:{c}.')

    # Loop through all inference_rules in theory t.
    for inference_rule in t.iterate_inference_rules():
        t, success, d = derive_2(t=t, c=c, i=inference_rule, raise_error_if_false=False)
        if success:
            # Eureka, the conjecture was proven.
            return t, success, d

    # Unfortunately, we tried to prove the conjecture from all inference_rules without success.
    return t, False, None


auto_derivation_max_formula_depth_preference = 4


def auto_derive_3(
        t: FlexibleTheory, conjectures: FlexibleTupl) -> \
        typing.Tuple[WellFormedTheory, bool]:
    """An auto-derivation algorithm that receives a tuple (basically an ordered list) of conjectures,
    and that applies auto-derivation-2 to derive these conjectures in sequence.

    :param t:
    :param conjectures:
    :return:
    """
    t: WellFormedTheory = coerce_theory(t=t)
    conjectures: WellFormedTupl = coerce_tuple(s=conjectures, interpret_none_as_empty=True)
    for conjecture in iterate_tuple_elements(phi=conjectures):
        t, success, _ = auto_derive_2(t=t, c=conjecture)
        if not success:
            return t, False
    return t, True


def auto_derive_4(
        t: FlexibleTheory, c: FlexibleFormula, max_recursion: int = 3,
        conjecture_exclusion_list: FlexibleEnumeration = None, debug: bool = False) -> \
        typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent], FlexibleEnumeration]:
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
    :param c:
    :param max_recursion:
    :param conjecture_exclusion_list:
    :param debug:
    :return: A python-tuple (t, True, derivation) if the derivation was successful, (t, False, None) otherwise.
    :rtype: typing.Tuple[WellFormedTheory, bool, typing.Optional[WellFormedTheoryComponent]]
    """
    global auto_derivation_max_formula_depth_preference
    t: WellFormedTheory = coerce_theory(t=t)
    c: WellFormedFormula = coerce_formula(phi=c)
    conjecture_exclusion_list: WellFormedEnumeration = coerce_enumeration(e=conjecture_exclusion_list,
                                                                          interpret_none_as_empty=True)
    indent: str = ' ' * (auto_derivation_max_formula_depth_preference - max_recursion + 1)
    if max_recursion == 2:
        pass
    if debug:
        u1.log_debug(f'{indent}auto_derive_3: start. conjecture:{c}.')

    # As a first step, attempt to auto_derive the conjecture with the less powerful,
    # but less expansive auto_derive_2 method:
    t, successful, c2, = auto_derive_2(t=t, c=c)
    if successful:
        if debug:
            u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{c}.')
        return t, successful, c2, None

    # To prevent infinite loops, populate an exclusion list of conjectures that are already
    # being searched in higher recursions.
    conjecture_exclusion_list = WellFormedEnumeration(e=(*conjecture_exclusion_list, c,))

    max_recursion = max_recursion - 1
    if max_recursion < 1:
        # We reached the max_recursion threshold, it follows that auto_derive failed.
        if debug:
            u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{c}.')
        return t, False, None, conjecture_exclusion_list

    # Loop through all theory inference-rules to find those that could potentially prove the conjecture.
    # These are the inference-rules whose conclusions are formula-equivalent-with-variables to the conjecture.
    for inference_rule in t.iterate_inference_rules():
        is_equivalent, m = is_formula_equivalent_with_variables_2(phi=c,
                                                                  psi=inference_rule.transformation.output_shape,
                                                                  variables=inference_rule.transformation.variables)
        if is_equivalent:
            # This inference-rule is compatible with the conjecture.

            # To list what would be the required premises to derive the conjecture,
            # the inference_rule must be "reverse-engineered".

            # first determine what are the necessary variable values in the transformation.
            # to do this, we have a trick, we can call is_formula_equivalent_with_variables and pass it
            # an empty map-builder:
            output, m, = is_formula_equivalent_with_variables_2(phi=c,
                                                                psi=inference_rule.transformation.output_shape,
                                                                variables=inference_rule.transformation.variables,
                                                                variables_fixed_values=None)

            # then we list the variables for which we don't have an assigned value,
            # called the free-variables.
            free_variables: WellFormedEnumeration = WellFormedEnumeration()
            for x in inference_rule.transformation.variables:
                if not is_element_of_enumeration(x=x, e=m.domain):
                    free_variables = WellFormedEnumeration(e=(*free_variables, x,))
            # u1.log_info(f'\t\t free-variables: {free_variables}')

            # now that we know what are the necessary variable values, we can determine what
            # are the necessary premises by substituting the variable values.
            necessary_premises: WellFormedTupl = WellFormedTupl(e=None)
            for original_premise in inference_rule.transformation.input_shapes:
                # we must find a set of premises in the theory
                # with free-variables.
                # I see two possible strategies:
                # 1) elaborate a new single proposition with the conjunction P1 and P2 and ... and Pn with all premises
                #    and then try to find that proposition in the theory, taking into account variables.
                # 2) develop an algorithm that given a set of premises returns true if they are all valid,
                #    and then extend this algorithm to support variables.
                # to avoid the burden of all these conjunctions in the theory, I start with the second approach.
                necessary_premise: WellFormedFormula = substitute_formulas(phi=original_premise, m=m)
                necessary_premises: WellFormedTupl = WellFormedTupl(e=(*necessary_premises, necessary_premise,))

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
                effective_premises: WellFormedFormula = substitute_formulas(phi=necessary_premises, m=m)
                effective_premises: WellFormedTupl = WellFormedTupl(e=effective_premises)
                for premise_target_statement in effective_premises:
                    if not is_element_of_enumeration(x=premise_target_statement,
                                                     e=conjecture_exclusion_list):
                        # recursively try to auto_derive the premise
                        t, derivation_success, _, conjecture_exclusion_list = auto_derive_4(
                            t=t,
                            c=premise_target_statement,
                            conjecture_exclusion_list=conjecture_exclusion_list,
                            max_recursion=max_recursion - 1,
                            debug=debug)
                        if not derivation_success:
                            inference_rule_success = False
                            break
                if inference_rule_success:
                    # all premises have been successfully proven.
                    t, ok, c2 = derive_1(t=t, c=c,
                                         p=effective_premises,
                                         i=inference_rule,
                                         raise_error_if_false=True)
                    if debug:
                        u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{c}.')
                    return t, True, c2, conjecture_exclusion_list
            else:
                valid_statements = iterate_theory_propositions(t=t)
                for permutation in iterate_permutations_of_enumeration_elements_with_fixed_size(e=valid_statements,
                                                                                                n=permutation_size):
                    permutation_success: bool = True
                    variable_substitution: WellFormedMap = WellFormedMap(d=free_variables, c=permutation)
                    effective_premises: WellFormedFormula = substitute_formulas(phi=necessary_premises,
                                                                                m=variable_substitution)
                    effective_premises: WellFormedTupl = WellFormedTupl(e=(*effective_premises, permutation,))
                    for premise_target_statement in effective_premises:
                        if not is_element_of_enumeration(x=premise_target_statement,
                                                         e=conjecture_exclusion_list):
                            # recursively try to auto_derive the premise
                            t, derivation_success, _, conjecture_exclusion_list = auto_derive_4(
                                t=t, c=premise_target_statement,
                                conjecture_exclusion_list=conjecture_exclusion_list,
                                max_recursion=max_recursion - 1, debug=debug)
                            if not derivation_success:
                                permutation_success = False
                                break
                    if permutation_success:
                        # all premises have been successfully proven.
                        t, ok, c2 = derive_1(t=t, c=c,
                                             p=effective_premises,
                                             i=inference_rule,
                                             raise_error_if_false=True)
                        if debug:
                            u1.log_debug(f'{indent}auto_derive_3: success. conjecture:{c}.')
                        return t, True, c2, conjecture_exclusion_list
    if debug:
        u1.log_debug(f'{indent}auto_derive_3: failure. conjecture:{c}.')
    return t, False, None, conjecture_exclusion_list


# HYPOTHESIS


class WellFormedHypothesis(WellFormedTheoreticalContext):
    """A well-formed hypothesis.

    An hypothesis is a specialization of a theoretical context.

    A well-formed formula :math:`\\phi` is a globally well-formed hypothesis if and only if:
     - its root connective is the hypothesis connective,
     - its first term is a well-formed theory extension denoted as the base theory,
     - its second term is an axiom denoted as the hypothesis assumption,
     - its subsequent terms, if any, are valid theory components.

    A well-formed formula :math:`\\phi` is a locally well-formed hypothesis with regard to a theoretical context
    𝒯 if and only if:
     - it is a globally well-formed hypothesis,
     - its base theory is axiomatically equivalent to 𝒯.

    Syntax:
    A hypothesis is a formula of the form:
        hypothesis(extension(𝓑), 𝓐, ...)
    Where:
        - 𝓑 is a theoretical context, denoted as the hypothesis base theory.
        - 𝓐 is an axiom, denoted as the assumption.
        - ... are some (if any) valid theory components.

    Note: Specializing hypothesis as a first class object in the axiomatic system data model is not
    necessary. In effect, an equivalent axiomatic system may be built with only theories and no
    hypothesis, nor axiomatization. Even theories could be stripped from the data model, considering
    only tuples whose elements are well-formed derivations. But specializing hypothesis as a first
    class object enriches the model and allows for more natural expression and simplified automations.
    """
    BASE_THEORY_INDEX: int = 0
    ASSUMPTION_INDEX: int = 1

    @staticmethod
    def _data_validation_2(
            b: FlexibleTheoreticalContext,
            a: FlexibleFormula, c: FlexibleEnumeration[FlexibleComponent] | None = None) -> tuple[
        Connective, WellFormedExtension, WellFormedAxiom, FlexibleEnumeration[FlexibleComponent] | None]:
        """Assure the well-formedness of the object before it is created. Once created, the object
        must be fully reliable and considered well-formed a priori.

        :param b: A theory denoted as the base theory.
        :param a: A formula denoted as the assumption.
        :return:
        """
        con: Connective = connective_for_hypothesis
        b: WellFormedTheoreticalContext = coerce_theoretical_context(t=b)
        b_extension: WellFormedExtension = WellFormedExtension(t=b)
        a: WellFormedFormula = coerce_formula(phi=a)
        a_axiom: WellFormedAxiom = WellFormedAxiom(p=a)
        if c is not None:
            c = coerce_enumeration(e=c, strip_duplicates=True, canonic_conversion=True)
            if c.arity == 0:
                c = None
        return con, b_extension, a_axiom, c

    def __new__(cls, b: FlexibleTheoreticalContext, a: FlexibleFormula,
                c: FlexibleEnumeration[FlexibleComponent] | None = None, **kwargs):
        """

        :param b: A theory denoted as the base theory.
        :param a: A proposition denoted as the assumption.
        :param c: (Conditional) An enumeration of complementary theory components.
        """
        con, b_extension, a_axiom, c = WellFormedHypothesis._data_validation_2(b=b, a=a, c=c)
        if c is None:
            o: tuple = super().__new__(cls, con=con, t=(b_extension, a_axiom))
        else:
            o: tuple = super().__new__(cls, con=con, t=(b_extension, a_axiom, *c))
        return o

    def __init__(self, b: FlexibleTheoreticalContext, a: FlexibleFormula,
                 c: FlexibleEnumeration[FlexibleComponent] | None = None, **kwargs):
        """

        :param b: A theory denoted as the base theory.
        :param a: A formula denoted as the assumption.
        :param c: (Conditional) An enumeration of complementary theory components.

        """
        con, b_extension, a_axiom, c = WellFormedHypothesis._data_validation_2(b=b, a=a, c=c)
        if c is None:
            super().__init__(con=con, t=(b_extension, a_axiom))
        else:
            super().__init__(con=con, t=(b_extension, a_axiom, *c))

    @property
    def assumption(self) -> WellFormedFormula:
        """A proposition assumed to be true, denoted as the assumption of the hypothesis."""
        return self[WellFormedHypothesis.ASSUMPTION_INDEX][WellFormedAxiom.VALID_STATEMENT_INDEX]

    @property
    def base_theory(self) -> WellFormedTheory:
        """The base theory of the hypothesis."""
        return self[WellFormedHypothesis.BASE_THEORY_INDEX][WellFormedExtension.THEORETICAL_CONTEXT_INDEX]

    def extend_with_component(
            self, c: FlexibleComponent,
            **kwargs) -> WellFormedTheoreticalContext:
        """Given a hypothesis ``self`` and a theory component ``c``, returns a new hypothesis ``self′``
        that is an extension of ``self`` with ``c`` appended as its last component.

        :param c:
        :return:
        """
        c: WellFormedTheoryComponent = coerce_theory_component(d=c)
        return WellFormedHypothesis(b=self.base_theory, a=self.assumption, c=(c,))


FlexibleHypothesis = typing.Optional[typing.Union[WellFormedHypothesis]]


# PRESENTATION LAYER


class TypesetterForClassicalFormula(pl1.Typesetter):
    def __init__(self, connective_ts: pl1.FlexibleTypesetter):
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
        phi: WellFormedFormula = coerce_formula(phi=phi)
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


class TypesetterForInfixFormula(pl1.Typesetter):
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
        phi: WellFormedFormula = coerce_formula(phi=phi)
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


class TypesetterForUnaryPostfix(pl1.Typesetter):
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
        phi: WellFormedFormula = coerce_formula(phi=phi)
        is_sub_formula: bool = kwargs.get('is_sub_formula', False)
        kwargs['is_sub_formula'] = True
        if is_sub_formula:
            yield from pl1.symbols.open_parenthesis.typeset_from_generator(**kwargs)
        yield from phi.term_0.typeset_from_generator(**kwargs)
        yield from pl1.symbols.space.typeset_from_generator(**kwargs)
        yield from self.connective_typesetter.typeset_from_generator(**kwargs)
        if is_sub_formula:
            yield from pl1.symbols.close_parenthesis.typeset_from_generator(**kwargs)


class TypesetterForTransformationByVariableSubstitution(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleTransformationByVariableSubstitution, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: WellFormedTransformationByVariableSubstitution = coerce_transformation_by_variable_substitution(t=phi)

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


class TypesetterForBracketedList(pl1.Typesetter):
    def __init__(self, open_bracket: pl1.Symbol, separator: pl1.Symbol, close_bracket: pl1.Symbol):
        self.open_bracket = open_bracket
        self.separator = separator
        self.close_bracket = close_bracket
        super().__init__()

    def typeset_from_generator(self, phi: WellFormedFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: WellFormedFormula = coerce_formula(phi=phi)
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


class TypesetterForMap(pl1.Typesetter):
    """A typesetter for the map connective.

    Sample output:
     - an empty map: {}
     - a non-empty map: {x ↦ a, y ↦ b, z ↦ c}
     """

    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: WellFormedMap = coerce_map(m=phi, interpret_none_as_empty=True)
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


class TypesetterForIsAPredicate(pl1.Typesetter):
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
        phi: WellFormedFormula = coerce_formula(phi=phi)
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


class TypesetterForDeclaration(pl1.Typesetter):
    def __init__(self, conventional_class: str | None):
        self._conventional_class = conventional_class
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleFormula, **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: WellFormedFormula = coerce_formula(phi=phi)
        yield 'Let '
        yield from phi.typeset_from_generator(ts_key=pl1.REF_TS, **kwargs)
        if self._conventional_class is not None:
            yield f' be a '
            yield self._conventional_class
        yield '.'


def get_theory_inference_rule_from_natural_transformation_rule(t: FlexibleTheory,
                                                               r: FlexibleTransformationByVariableSubstitution) -> \
        tuple[bool, WellFormedInferenceRule | None]:
    """Given a theory ``t`` and a transformation-rule "r", return the first occurrence of an inference-rule in ``t`` such
    that its transformation-rule is formula-equivalent to "r".

    :param t: A theory.
    :param r: A transformation-rule.
    :return: A python-tuple (True, i) where `i` is the inference-rule if `i` is found in ``t``, (False, None) otherwise.
    """
    t: WellFormedTheory = coerce_theory(t=t)
    r: WellFormedTransformationByVariableSubstitution = coerce_transformation_by_variable_substitution(t=r)
    for i in iterate_theory_inference_rules(t=t):
        i: WellFormedInferenceRule
        if is_formula_equivalent(phi=r, psi=i.transformation):
            return True, i
    return False, None


def get_theory_component_from_valid_statement(t: FlexibleTheory, s: FlexibleFormula) -> \
        tuple[bool, WellFormedFormula | None]:
    """Given a theory ``t`` and a valid-statement `s` in ``t``,
    return the first occurrence of a component in ``t`` such that its valid-statement is formula-equivalent to `s`.

    :param t: A theory.
    :param s: A formula that is a valid statement in ``t``.
    :return: A python-tuple (True, d) where `d` is the derivation if `s` is found in ``t`` valid-statements,
    (False, None) otherwise.
    """
    t: WellFormedTheory = coerce_theory(t=t)
    s: WellFormedFormula = coerce_formula(phi=s)
    for d in iterate_theory_components(t=t):
        d: WellFormedTheoryComponent
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
    elif t is not None and is_valid_proposition_so_far_1(p=phi, t=t):
        # phi is a valid-statement in a theory.
        # we can use the 1-based index of the formula in the theory.
        success, d = get_theory_component_from_valid_statement(t=t, s=phi)
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


class TypesetterForDerivation(pl1.Typesetter):
    def __init__(self):
        super().__init__()

    def typeset_from_generator(self, phi: FlexibleComponent, theory: typing.Optional[FlexibleTheory] = None,
                               **kwargs) -> (
            typing.Generator)[str, None, None]:
        phi: WellFormedTheoryComponent = coerce_theory_component(d=phi)
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
            elif is_well_formed_theorem(m=phi):
                phi: WellFormedTheorem = coerce_theorem(m=phi)
                inference: WellFormedInference = phi.inference
                inference_rule: WellFormedInferenceRule = inference.inference_rule
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
            elif is_well_formed_theorem(m=phi):
                phi: WellFormedTheorem = coerce_theorem(m=phi)
                inference: WellFormedInference = phi.inference
                inference_rule: WellFormedInferenceRule = inference.inference_rule
                yield f'\t\t| Follows from '
                yield from typeset_formula_reference(phi=inference_rule, t=theory, **kwargs)
                yield f' given '
                first: bool = True
                for premise in phi.inference.premises:
                    # success, derivation = get_theory_derivation_from_valid_statement(t=theory, s=premise)
                    derivation: WellFormedTheoryComponent
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
        return TypesetterForBracketedList(open_bracket=open_bracket, separator=separator, close_bracket=close_bracket)

    def symbol(self, symbol: pl1.Symbol) -> pl1.SymbolTypesetter:
        return pl1.typesetters.symbol(symbol=symbol)

    def classical_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> TypesetterForClassicalFormula:
        return TypesetterForClassicalFormula(connective_ts=connective_typesetter)

    def declaration(self, conventional_class: str | None) -> TypesetterForDeclaration:
        return TypesetterForDeclaration(conventional_class=conventional_class)

    def is_a_predicate(self, conventional_class: str | None) -> TypesetterForIsAPredicate:
        return TypesetterForIsAPredicate(conventional_class=conventional_class)

    def text(self, text: str) -> pl1.TextTypesetter:
        return pl1.typesetters.text(text=text)

    def indexed_symbol(self, symbol: pl1.Symbol, index: int) -> pl1.NaturalIndexedSymbolTypesetter:
        return pl1.typesetters.indexed_symbol(symbol=symbol, index=index)

    def infix_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> TypesetterForInfixFormula:
        return TypesetterForInfixFormula(connective_ts=connective_typesetter)

    def unary_postfix_formula(self, connective_typesetter: pl1.FlexibleTypesetter) -> TypesetterForUnaryPostfix:
        return TypesetterForUnaryPostfix(connective_ts=connective_typesetter)

    def map(self) -> TypesetterForMap:
        return TypesetterForMap()

    def transformation_by_variable_substitution(self) -> TypesetterForTransformationByVariableSubstitution:
        return TypesetterForTransformationByVariableSubstitution()

    def derivation(self) -> TypesetterForDerivation:
        return TypesetterForDerivation()


typesetters = Typesetters()
"""OBSOLETE: replace by declaring typesetters as module global variables.
"""
