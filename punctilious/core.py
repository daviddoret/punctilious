from __future__ import annotations
import textwrap
import warnings
from types import SimpleNamespace
import repm
import contextlib
import abc
import collections.abc
import collections


class InconsistencyWarning(UserWarning):
    pass


class Configuration:
    def __init__(self):
        self.auto_index = None
        self.echo_axiom = None
        self.echo_axiom_inclusion = None
        self.echo_default = False
        self.echo_definition = None
        self.echo_definition_inclusion = None
        self.echo_definition_direct_inference = None
        self.echo_formula = None
        self.echo_hypothesis = None
        self.echo_note = None
        self.echo_relation = None
        self.echo_simple_objct = None
        self.echo_statement = None
        self.echo_symbolic_objct = None
        self.echo_universe_of_discourse = None
        self.echo_variable = None
        self.output_index_if_max_index_equal_1 = False
        self.raise_exception_on_verification_error = True
        self.text_output_indent = 2
        self.text_output_statement_column_width = 70
        self.text_output_justification_column_width = 40
        self.text_output_total_width = 122
        self.warn_on_inconsistency = True


configuration = Configuration()


def get_config(*args, fallback_value):
    """Return the first not None value."""
    for a in args:
        if a is not None:
            return a
    return fallback_value


def unpack_formula(o: TheoreticalObjct) -> Formula:
    """Receive a theoretical-objct and unpack its formula if it is a statement that contains a formula."""
    verify(
        is_in_class(o, classes.theoretical_objct),
        'Parameter ⌜o⌝ must be an element of the theoretical-objct declarative-class.',
        o=o)
    if hasattr(o, 'valid_proposition'):
        # Unpack python objects that "contain" their formula,
        # such as FormulaStatement, DirectAxiomInference, etc.
        return o.valid_proposition
    else:
        return o


class Consistency(repm.Representation):
    """A qualification regarding the consistency of a theory."""

    def __init__(self, python_name):
        super().__init__(python_name=python_name)


class ConsistencyValues(repm.Representation):
    """The list of consistency values."""

    def __init__(self, python_name):
        super().__init__(python_name=python_name)

    proved_consistent = Consistency('proved-consistent')
    proved_inconsistent = Consistency('proved-inconsistent')
    undetermined = Consistency('undetermined')


consistency_values = ConsistencyValues('consistency-values')
"""The list of consistency values."""


class DeclarativeClass(repm.Representation):
    """The DeclarativeClass python class models a declarative-class."""

    def __init__(self, python_name, natural_language_name):
        super().__init__(python_name=python_name, natural_language_name=natural_language_name)


class DeclarativeClassList(repm.Representation):
    """A list of of well-known declarative-classes."""

    def __init__(self, python_name, natural_language_name):
        super().__init__(python_name=python_name, natural_language_name=natural_language_name)
        self.atheoretical_statement = DeclarativeClass('atheoretical_statement', 'atheoretical-statement')
        self.axiom = DeclarativeClass('axiom', 'axiom')
        self.axiom_inclusion = DeclarativeClass('axiom_inclusion', 'axiom-inclusion')
        self.definition = DeclarativeClass('definition', 'definition')
        self.definition_inclusion = DeclarativeClass('definition_inclusion', 'definition-inclusion')
        self.direct_axiom_inference = DeclarativeClass('direct_axiom_inference', 'direct-axiom-inference')
        self.direct_definition_inference = DeclarativeClass('direct_definition_inference',
                                                            'direct-definition-inference')
        self.formula = DeclarativeClass('formula', 'formula')
        self.formula_statement = DeclarativeClass('formula_statement', 'formula-statement')
        self.free_variable = DeclarativeClass('free_variable', 'free-variable')
        self.hypothesis = DeclarativeClass('hypothesis', 'hypothesis')
        self.inference_rule = DeclarativeClass('inference_rule', 'inference-rule')
        self.inference_rule_inclusion = DeclarativeClass('inference_rule_inclusion', 'inference-rule-inclusion')
        self.inferred_proposition = DeclarativeClass('inferred_proposition', 'inferred-proposition')
        self.note = DeclarativeClass('note', 'note')
        self.proposition = DeclarativeClass('proposition', 'proposition')
        self.relation = DeclarativeClass('relation', 'relation')
        self.simple_objct = DeclarativeClass('simple_objct', 'simple-objct')
        self.statement = DeclarativeClass('statement', 'statement')
        self.symbolic_objct = DeclarativeClass('symbolic_objct', 'symbolic-objct')
        self.theoretical_objct = DeclarativeClass('theoretical_objct', 'theoretical-objct')
        self.theory_elaboration = DeclarativeClass('theory', 'theory')
        self.universe_of_discourse = DeclarativeClass('universe_of_discourse', 'universe-of-discourse')
        # Shortcuts
        self.a = self.axiom
        self.dai = self.direct_axiom_inference
        self.ddi = self.direct_definition_inference
        self.f = self.formula
        self.r = self.relation
        self.t = self.theory_elaboration
        self.u = self.universe_of_discourse


"""A list of well-known declarative-classes."""
declarative_class_list = DeclarativeClassList('declarative_class_list', 'declarative-class-list')

"""A list of well-known declarative-classes. A shortcut for p.declarative_class_list."""
classes = declarative_class_list


def is_in_class(
        o: TheoreticalObjct,
        c: DeclarativeClass) -> bool:
    """Return True if o is a member of the declarative-class c, False otherwise.

    :param o: An arbitrary python object.
    :param c: A declarative-class.
    :return: (bool).
    """
    # verify(o is not None, 'o is None.', o=o, c=c)
    verify(hasattr(o, 'is_in_class'), 'o does not have attribute is_in_class.', o=o, c=c)
    verify(callable(getattr(o, 'is_in_class')), 'o.is_in_class() is not callable.', o=o, c=c)
    return o.is_in_class(c)


class FailedVerificationException(Exception):
    """Python custom exception raised whenever a verification fails if
    setting raise_exception_on_verification_failure = True."""

    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.kwargs = kwargs


class UnsupportedInferenceRuleException(Exception):
    """Python custom exception raised if an attempt is made
     to use an inference rule on a theory."""

    def __init__(self, msg, **kwargs):
        self.msg = msg
        self.kwargs = kwargs


class VerificationSeverity(repm.Representation):
    def __init__(self, python_name):
        super().__init__(python_name=python_name)


class VerificationSeverities(repm.Representation):
    def __init__(self, python_name):
        super().__init__(python_name=python_name)
        self.verbose = VerificationSeverity('verbose')
        self.information = VerificationSeverity('information')
        self.warning = VerificationSeverity('warning')
        self.error = VerificationSeverity('error')


verification_severities = VerificationSeverities('verification_severities')


def verify(
        assertion, msg,
        severity: VerificationSeverity = verification_severities.error, **kwargs):
    if not assertion:
        contextual_information = ''
        for key, value in kwargs.items():
            value_as_string = f'(str conversion failure of type {str(type(value))})'
            try:
                value_as_string = value.repr_as_fully_qualified_name()
            except:
                value_as_string = str(value)
            finally:
                pass
            contextual_information += f'\n{key}: {value_as_string}'
        report = f'{str(severity).upper()}: {msg}\nContextual information:{contextual_information}'
        repm.prnt(report)
        if severity is verification_severities.warning:
            warnings.warn(report)
        if configuration.raise_exception_on_verification_error and severity is verification_severities.error:
            raise FailedVerificationException(msg=report, **kwargs)


def set_attr(o, a, v):
    """A wrapper function for the naive setattr function.
    It set attributes on Tuple instances in a prudent manner.
    """
    assert isinstance(a, str)
    if not hasattr(o, a):
        setattr(o, a, v)
    else:
        assert getattr(o, a) is v


# import rich
# import rich.console
# import rich.markdown
# import rich.table


class Symbol:
    """A specialized string-like object to represent things algebraically in formulae.

    """

    def __init__(self, base, index):
        self.base = base
        self.index = index

    def __hash__(self):
        return hash((self.base, self.index))

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr(self, hide_index=False) -> str:
        """Return the default representation for this python obje.

        :param hide_index:
        :return:
        """
        if hide_index:
            return f'{self.base}'
        else:
            return f'{self.base}{repm.subscriptify(self.index)}'


class ObjctHeader:
    """A header to introduce some symbolic-objcts in reports.

    Features:
    - long-names have a short (reference) and long (long-name) version.
    - long-names do not have an index.
    - long-names comprise a category that must be consistent with
        the declarative class of the symbolic-objct.
    """

    def __init__(self, reference, category=None, title=None):
        category = statement_categories.missing_category if category is None else category
        verify(isinstance(category, (StatementCategory, NoteCategory)),
               'category is not of type StatementCategory or NoteCategory.',
               reference=reference, category=category, title=title)
        verify(isinstance(reference, str), 'reference is not of type str.', reference=reference, category=category,
               title=title)
        self.reference = reference
        self.category = category
        self.title = title

    def __hash__(self):
        """Note that the title attribute is not hashed,
        because title is considered purely decorative.
        """
        return hash((self.category, self.reference))

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr(self, cap: bool = False) -> str:
        """Return the default representation for this long-name.

        :param cap: Whether the representation must be capitalized (default: False).
        :return: str
        """
        return self.repr_reference(cap=cap)

    def repr_header(self, cap: bool = False) -> str:
        return f'{self.category.repr_as_natural_language(cap=cap)} {self.reference}{"" if self.title is None else " - " + self.title}'

    def repr_reference(self, cap: bool = False) -> str:
        cap = False if cap is None else cap
        return f'{self.category.repr_as_natural_language(cap=cap)} {self.reference}'


class DashedName:
    """A dashed-name to provide more semantically meaningful names to symbolic-objcts in reports than symbols.

    Features:
    - Immutable
    """

    def __init__(self, dashed_named):
        verify(isinstance(dashed_named, str), 'dashed-name is not of type str.', dashed_named=dashed_named)
        # TODO: Clean string from non-alphanumeric, digits, dash characters, etc.
        self._dashed_name = dashed_named

    def __hash__(self):
        """"""
        return hash((self._dashed_name))

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr(self) -> str:
        """Return the default representation.
        """
        return self.repr_dashed_name()

    def repr_dashed_name(self) -> str:
        """Return a dashed-name representation.
        """
        return self._dashed_name


class StatementTitleOBSOLETE:
    """Replaced by ObjctHeader."""

    def __init__(self, category, reference, title):
        self.category = category
        self.reference = reference
        self.title = title

    def __hash__(self):
        return hash((self.category, self.reference, self.title))

    def __repr__(self):
        return self.repr_ref()

    def __str__(self):
        return self.repr_ref()

    def repr_full(self, cap=False) -> str:
        category = str(self.category.natural_name.capitalize() if cap else self.category.natural_name)
        reference = str(self.reference)
        return repm.serif_bold(
            f'{category} {reference}{" - " + self.title if self.title is not None else ""}')

    def repr_ref(self, cap=False) -> str:
        return repm.serif_bold(
            f'{self.category.natural_name.capitalize() if cap else self.category.natural_name} {self.reference}')


class SymbolicObjct:
    """
    Definition
    ----------
    A symbolic-objct is a python object instance that is assigned symbolic names,
    that is linked to a theory, but that is not necessarily constitutive of the theory.
    """

    def __init__(
            self,
            symbol: (None, str, Symbol),
            universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False,
            is_universe_of_discourse: bool = False,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: bool = False):
        echo = get_config(echo, configuration.echo_symbolic_objct, configuration.echo_default, fallback_value=False)
        self._declarative_classes = frozenset()
        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        # By design, every symbolic-objct is a component of a theory,
        # unless it is itself a theory-foundation-system,
        # or it is itself a universe-of-discourse.
        assert is_universe_of_discourse or is_in_class(
            universe_of_discourse, classes.u)
        verify(
            isinstance(symbol, Symbol),
            'The symbol of a symbolic-objct must be of type Symbol.')
        self.symbol = symbol
        self.header = header  # Header validation is implemented in parent classes with proper category.
        if isinstance(dashed_name, str):
            dashed_name = DashedName(dashed_name)
        self.dashed_name = dashed_name
        self.is_theory_foundation_system = is_theory_foundation_system
        if not is_universe_of_discourse:
            self._universe_of_discourse = universe_of_discourse
            self._universe_of_discourse.cross_reference_symbolic_objct(o=self)
        else:
            self._universe_of_discourse = None
        self._declare_class_membership(classes.symbolic_objct)
        if echo:
            repm.prnt(self.repr_as_declaration())

    def __hash__(self):
        # Symbols are unique within their universe-of-discourse,
        # thus hashing can be safely based on the key: U + symbol.
        # With a special case for the universe-of-discourse itself,
        # where hash of the symbol is sufficient.
        return hash(self.symbol) if is_in_class(self, classes.u) else hash(
            (self.universe_of_discourse, self.symbol))

    def __repr__(self):
        return self.repr_as_symbol()

    def __str__(self):
        return self.repr_as_symbol()

    @property
    def declarative_classes(self) -> frozenset[DeclarativeClass]:
        """The set of declarative-classes this symbolic-objct is a member of."""
        return self._declarative_classes

    @property
    def u(self):
        """This symbolic-object''s universe of discourse. Full name: o.universe_of_discourse."""
        return self.universe_of_discourse

    @property
    def universe_of_discourse(self):
        """This symbolic-object''s universe of discourse. Shortcut: o.u"""
        return self._universe_of_discourse

    def _declare_class_membership(self, c: DeclarativeClass):
        """During construction (__init__()), add the declarative-classes this symboli-objct is being made a member of."""
        if not hasattr(self, '_declarative_classes'):
            setattr(self, '_declarative_classes', frozenset())
        self._declarative_classes = self._declarative_classes.union({c})

    @abc.abstractmethod
    def echo(self):
        raise NotImplementedError('This is an abstract method.')

    def is_declarative_class_member(self, c: DeclarativeClass) -> bool:
        """True if this symbolic-objct is a member of declarative-class 𝒞, False, otherwise."""
        if hasattr(self, '_declarative_classes'):
            return c in self._declarative_classes
        else:
            return False

    def is_in_class(self, c: DeclarativeClass) -> bool:
        """True if this symbolic-objct is a member of declarative-class 𝒞, False, otherwise.

        A shortcut for o.is_declarative_class_member(...)."""
        return self.is_declarative_class_member(c=c)

    def is_symbol_equivalent(self, o2) -> bool:
        """Returns true if this object and o2 are symbol-equivalent.

        Definition:
        -----------
        Two symbolic-objects o₁ and o₂ are symbol-equivalent if and only if:
         1. o₁ and o₂ have symbol-equivalent theories.¹
         2. o₁ and o₂ have equal symbols.²

        ¹. Theories are symbolic-objects. This recursive condition
           yields a complete path between the objects and the universe-of-discourse.
        ². Remember that every symbolic-object has a unique symbol in its parent theory.

        Note:
        -----
        The symbol-equivalence relation allows to compare any pair of symbolic-objcts, including:
         * Both theoretical and atheoretical objects.
         * Symbolic-objcts linked to distinct theories.
        """
        # A theoretical-object can only be compared with a theoretical-object
        assert isinstance(o2, SymbolicObjct)
        if self is o2:
            # If the current symbolic-objct is referencing the same
            # python object instance, by definitions the two python references
            # are referencing the same object.
            return True
        if not self.universe_of_discourse.is_symbol_equivalent(
                o2.universe_of_discourse):
            return False
        if self.symbol != o2.symbol:
            return False
        return True

    def prnt(self, expanded=False):
        repm.prnt(self.repr(expanded=expanded))

    def repr_dashed_name(self) -> str:
        """"""
        if self.dashed_name is None:
            return None
        return self.dashed_name.repr_dashed_name()

    def repr_fully_qualified_name(self) -> str:
        """"""
        fully_qualified_name = self.repr_header() if self.header is not None else self.repr_dashed_name() if self.dashed_name is not None else self.repr_as_symbol()
        fully_qualified_name += ' (' if self.header is not None or self.dashed_name is not None else ''
        fully_qualified_name += self.repr_dashed_name() + ', ' if self.header is not None and self.dashed_name is not None else ''
        fully_qualified_name += self.repr_as_symbol() + ')' if self.header is not None or self.dashed_name is not None else ''
        return fully_qualified_name

    def repr_as_declaration(self) -> str:
        return f'Let {self.repr_as_symbol()} be a symbolic-objct denoted as ⌜ {self.repr_as_symbol()} ⌝.'

    def repr_as_symbol(self) -> str:
        global configuration
        hide_index = \
            not is_in_class(self, classes.u) and \
            self.symbol.index == 1 and \
            not configuration.output_index_if_max_index_equal_1 and \
            not is_in_class(self, classes.universe_of_discourse) and \
            self.universe_of_discourse.get_symbol_max_index(self.symbol.base) == 1

        return self.symbol.repr(hide_index=hide_index)

    def repr_header(self, cap: bool = False) -> str:
        global configuration
        if self.header is None:
            # If we have no long-name for this symbolic-objct,
            # we use the (mandatory) symbol as a fallback method.
            return self.repr_as_symbol()
        return self.header.repr_header(cap=cap)

    def repr_reference(self, cap: bool = False) -> str:
        global configuration
        if self.header is None:
            # If we have no long-name for this symbolic-objct,
            # we use the (mandatory) symbol as a fallback method.
            return self.repr_as_symbol()
        return self.header.repr_reference(cap=cap)

    def repr(self, expanded=None) -> str:
        # If a long-name is available, represent the objct as a reference.
        # Otherwise, represent it as a symbol.
        return self.repr_reference()


class TheoreticalObjct(SymbolicObjct):
    """
    Definition
    ----------
    Given a theory 𝒯, a theoretical-object ℴ is an object that:
     * is constitutive of 𝒯,
     * may be referenced in 𝒯 formulae (i.e. 𝒯 may "talk about" ℴ),
     * that may be but is not necessarily a statement in 𝒯 (e.g. it may be an invalid or inconsistent formula).

    The following are supported classes of theoretical-objects:
    * axiom
    * formula
    * lemma
    * proposition
    * relation
    * simple-object
    * theorem
    * theory
    * variable
    """

    def __init__(
            self,
            symbol: (None, str, Symbol),
            universe_of_discourse: UniverseOfDiscourse,
            is_theory_foundation_system: bool = False,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: bool = False):
        # pseudo-class properties. these must be overwritten by
        # the parent constructor after calling __init__().
        # the rationale is that checking python types fails
        # miserably (e.g. because of context managers),
        # thus, implementing explicit functional-types will prove
        # more robust and allow for duck typing.
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse,
            is_theory_foundation_system=is_theory_foundation_system,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(classes.theoretical_objct)
        if echo:
            repm.prnt(self.repr_fully_qualified_name())

    def get_variable_set(self):
        """Return the set of variables contained in o (self), including o itself.

        This function recursively traverse formula components (relation + parameters)
        to compile the set of variables contained in o."""
        return self._get_variable_set()

    def _get_variable_set(self, _variable_set=None):
        _variable_set = set() if _variable_set is None else _variable_set
        if isinstance(self, Formula):
            _variable_set = _variable_set.union(
                self.relation._get_variable_set(_variable_set=_variable_set))
            for p in self.parameters:
                _variable_set = _variable_set.union(
                    p._get_variable_set(_variable_set=_variable_set))
            return _variable_set
        elif isinstance(self, FreeVariable):
            return _variable_set.union({self})
        else:
            return _variable_set

    def is_formula_equivalent_to(self, o2):
        """Returns true if this theoretical-obct and theoretical-obct o2 are formula-equivalent.

        Parameters:
        -----------
        o2 : TheoreticalObject
            The theoretical-object with which to verify formula-equivalence.

        Definition:
        -----------
        Two theoretical-obcts o1 and o₂ that are not both formulae,
        are formula-equivalent if and only if:
        Necessary conditions:
         1. o1 and o₂ are symbolic-equivalent.
        Unnecessary but valid conditions:
         2. o1 and o₂ are of the same theory class (simple-objct, relation, etc.)
         3. o1 and o₂ are constitutive of symbolic-equivalent theories.
         4. o1 and o₂ have equal defining-properties (e.g. arity for a relation).

        For the special case when o1 and o₂ are both formulae,
        cf. the overridden method Formula.is_formula_equivalent_to.

        Note:
        -----
        o1 and o₂ may be subject to identical theoretical constraints,
        that is to say they are theoretically-equivalent,
        but if they are defined with distinct symbols, they are not formula-equivalent.
        """
        return self.is_symbol_equivalent(o2)

    def is_masked_formula_similar_to(
            self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObjct),
            mask: (None, frozenset[FreeVariable]) = None) \
            -> bool:
        """Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        return True if o₁ and o₂ are masked-formula-similar, False otherwise.

        Definition
        ----------
        Given two theoretical-objects o₁ (self) and o₂,
        and a finite set of variables 𝐌,
        o₁ and o₂ are masked-formula-similar if and only if:
         1. o₁ is formula-equivalent to o₂, including the special case
            when both o₁ and o₂ are symbolic-equivalent to a variable 𝐱 in 𝐌,
         2. or the weaker condition that strictly one theoretical-object o₁ or o₂
            is symbolic-equivalent to a variable 𝐱 in 𝐌,
            and, denoting the other object the variable-observed-value,
            every variable-observed-value of 𝐱 are formula-equivalent.
         3. or, if o₁ or o₂ are both formula, their components are masked-formula-similar.

        Note
        ----
        masked-formula-similitude is not a well-defined equivalence-class.
        In effect, equivalence-classes are reflexive, symmetric, and transitive.
        An obvious counterexample: (x + 1) ~ (5 + x).
        This is why it is called similitude and not equivalence.

        Parameters
        ----------
        o2 : TheoreticalObjct
            A theoretical-object with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        """
        output, _values = self._is_masked_formula_similar_to(o2=o2, mask=mask)
        return output

    def _is_masked_formula_similar_to(
            self,
            o2: (Formula, FormulaStatement, FreeVariable, Relation, SimpleObjct, TheoreticalObjct),
            mask: (None, frozenset[FreeVariable]) = None,
            _values: (None, dict) = None) \
            -> (bool, dict):
        """A "private" version of the is_masked_formula_similar_to method,
        with the "internal" parameter _values.

        Parameters
        ----------
        o2 : TheoreticalObjct
            A theoretical-object with which to verify masked-formula-similitude.

        mask: set
            Set of FreeVariable elements. If None, the empty set is assumed.

        _values:
            Internal dict of FreeVariable values used to keep track
            of variable values consistency.
        """
        o1 = self
        # if is_in_class(o1, classes.formula_statement):
        #    # Unpack the formula-statement
        #    # to compare the formula it contains.
        #    o1 = o1.valid_proposition
        # if is_in_class(o2, classes.formula_statement):
        #    # Unpack the formula-statement
        #    # to compare the formula it contains.
        #    o2 = o2.valid_proposition
        mask = frozenset() if mask is None else mask
        _values = dict() if _values is None else _values
        if o1 is o2:
            # Trivial case.
            return True, _values
        if o1.is_formula_equivalent_to(o2):
            # Sufficient condition.
            return True, _values
        if isinstance(o1, (Formula, FormulaStatement)) and isinstance(o2, (Formula, FormulaStatement)):
            # When both o1 and o2 are formula,
            # verify that their components are masked-formula-similar.
            relation_output, _values = o1.relation._is_masked_formula_similar_to(
                o2=o2.relation, mask=mask, _values=_values)
            if not relation_output:
                return False, _values
            # Arities are necessarily equal.
            for i in range(len(o1.parameters)):
                parameter_output, _values = o1.parameters[
                    i]._is_masked_formula_similar_to(
                    o2=o2.parameters[i], mask=mask, _values=_values)
                if not parameter_output:
                    return False, _values
            return True, _values
        if o1 not in mask and o2 not in mask:
            # We know o1 and o2 are not formula-equivalent,
            # and we know they are not in the mask.
            return False, _values
        if o1 in mask:
            variable = o2
            newly_observed_value = o1
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if o2 in mask:
            variable = o1
            newly_observed_value = o2
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(
                        already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        return True, _values

    def substitute(
            self, substitution_map, target_theory, lock_variable_scope=None):
        """Given a theoretical-objct o₁ (self),
        and a substitution map 𝐌,
        return a theoretical-objct o₂
        where all components, including o₂ itself,
        have been substituted if present in 𝐌.

        Note
        ----
        The scope of variables is locked to their most-parent formula.
        In consequence, and in order to generate valid formluae,
        substition must simultaneously substite all variables with
        new variables.

        Note
        ----
        The result of substitution depends on the order
        of traversal of o₁. The substitution() method
        uses the canonical-traversal-method which is:
        top-down, left-to-right, depth-first, relation-before-parameters.

        Parameters
        ----------
        substitution_map : dict
            A dictionary of theoretical-objct pairs (o, o'),
            where o is the original theoretical-objct in o₁,
            and o' is the substitute theoretical-objct in o₂.

        """
        lock_variable_scope = True if lock_variable_scope is None else lock_variable_scope
        substitution_map = dict() if substitution_map is None else substitution_map
        assert isinstance(substitution_map, dict)
        output = None
        for key, value in substitution_map.items():
            # FreeVariable instances may be of type contextlib._GeneratorContextManager
            # when used inside a with statement.
            pass
            # assert isinstance(key, TheoreticalObjct)  ##### XXXXX
            # verify(
            #    isinstance(value, (
            #    TheoreticalObjct, contextlib._GeneratorContextManager)),
            #    'The value component of this key/value pair in this '
            #    'substitution map is not an instance of TheoreticalObjct.',
            #    key=key, value=value, value_type=type(value), self2=self)
            # A formula relation cannot be replaced by a simple-objct.
            # But a simple-object could be replaced by a formula,
            # if that formula "yields" such simple-objects.
            # TODO: Implement clever rules here to avoid ill-formed formula,
            #   or let the formula constructor do the work.
            # assert type(key) == type(value) or isinstance(
            #    value, FreeVariable) or isinstance(
            #    key, FreeVariable)
            # If these are formula, their arity must be equal
            # to prevent the creation of an ill-formed formula.
            # NO, THIS IS WRONG. TODO: Re-analyze this point.
            # assert not isinstance(key, Formula) or key.arity == value.arity

        # Because the scope of variables is locked,
        # the substituted formula must create "duplicates" of all variables.
        variables_list = self.get_variable_set()
        for x in variables_list:
            if x not in substitution_map.keys():
                # Call declare_free_variable() instead of v()
                # to explicitly manage variables scope locking.
                x2 = self.universe_of_discourse.declare_free_variable(
                    x.symbol.base)
                substitution_map[x] = x2

        # Now we may proceed with substitution.
        if self in substitution_map:
            return substitution_map[self]
        elif isinstance(self, Formula):
            # If both key / value are formulae,
            #   we must check for formula-equivalence,
            #   rather than python-object-equality.
            for k, v in substitution_map.items():
                if self.is_formula_equivalent_to(k):
                    return v

            # If the formula itself is not matched,
            # the next step consist in decomposing it
            # into its constituent parts, i.e. relation and parameters,
            # to apply the substitution operation on these.
            relation = self.relation.substitute(
                substitution_map=substitution_map, target_theory=target_theory,
                lock_variable_scope=lock_variable_scope)
            parameters = tuple(
                p.substitute(
                    substitution_map=substitution_map,
                    target_theory=target_theory, lock_variable_scope=False) for
                p in
                self.parameters)
            phi = self.universe_of_discourse.f(
                relation, *parameters, lock_variable_scope=lock_variable_scope)
            return phi
        else:
            return self

    def iterate_relations(self, include_root: bool = True):
        """Iterate through this and all the theoretical-objcts it contains recursively, providing they are relations."""
        return (
            r for r in self.iterate_theoretical_objcts_references(include_root=include_root)
            if is_in_class(r, classes.relation))

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})

    def contains_theoretical_objct(self, o: TheoreticalObjct):
        """Return True if o is in this theory's hierarchy, False otherwise."""
        return o in self.iterate_theoretical_objcts_references(include_root=True)


def substitute_xy(o, x, y):
    """Return the result of a *substitution* of x with y on o."""
    verify(isinstance(o, TheoreticalObjct), msg='o is not a TheoreticalObjct.')
    verify(isinstance(x, TheoreticalObjct), msg='x is not a TheoreticalObjct.')
    verify(isinstance(y, TheoreticalObjct), msg='y is not a TheoreticalObjct.')
    return o.substitute(substitution_map={x: y})


class FreeVariable(TheoreticalObjct):
    """


    Defining properties:
    --------------------
    The defining-properties of a free-variable are:
     * Being a free-variable
     * The scope-formula of the free-variable
     * The index-position of the free-variable in its scope-formula
    """

    class Status(repm.Representation):
        pass

    scope_initialization_status = Status('scope_initialization_status')
    closed_scope_status = Status('closed_scope_status')

    def __init__(
            self, symbol=None,
            universe_of_discourse=None, status=None, scope=None, echo=None):
        echo = get_config(echo, configuration.echo_variable, configuration.echo_default, fallback_value=False)
        status = FreeVariable.scope_initialization_status if status is None else status
        scope = frozenset() if scope is None else scope
        scope = {scope} if isinstance(scope, Formula) else scope
        verify(
            isinstance(scope, frozenset),
            'The scope of a FreeVariable must be of python type frozenset.')
        verify(
            isinstance(status, FreeVariable.Status),
            'The status of a FreeVariable must be of the FreeVariable.Status type.')
        self._status = status
        self._scope = scope
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        if symbol is None:
            base = '𝐱'
            index = universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = universe_of_discourse.index_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse, echo=False)
        self.universe_of_discourse.cross_reference_variable(x=self)
        super()._declare_class_membership(declarative_class_list.free_variable)
        if echo:
            self.echo()

    def echo(self):
        self.repr_as_declaration()

    @property
    def scope(self):
        """The scope of a free variable is the set of the formula where the variable is used.

        :return:
        """
        return self._scope

    def lock_scope(self):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(
            self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be locked if it is open.')
        # Close variable scope
        self._status = FreeVariable.closed_scope_status

    def extend_scope(self, phi):
        # Support for the with pythonic syntax
        # Start building  variable scope
        verify(
            self._status == FreeVariable.scope_initialization_status,
            'The scope of an instance of FreeVariable can only be extended if it is open.')
        # Close variable scope
        verify(
            isinstance(phi, Formula),
            'Scope extensions of FreeVariable must be of type Formula.')
        self._scope = self._scope.union({phi})

    def is_masked_formula_similar_to(self, o2, mask, _values):
        # TODO: Re-implement this
        assert isinstance(o2, TheoreticalObjct)
        if isinstance(o2, FreeVariable):
            if o2 in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if o2 in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[o2]
                    if known_value is self:
                        # the existing value matches the newly observed value.
                        # until there, masked-formula-similitude is preserved.
                        return True, _values
                    else:
                        # the existing value does not match the newly observed value.
                        # masked-formula-similitude is no longer preserved.
                        return False, _values
                else:
                    # the value is not present in the dictionary.
                    # until there, masked-formula-similitude is preserved.
                    _values[o2] = self
                    return True, _values
        if not isinstance(o2, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_equivalent_to(o2), _values

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be a free-variable in {self.universe_of_discourse.repr_as_symbol()}'


class Formula(TheoreticalObjct):
    """A formula is a theoretical-objct.
    It is also a tuple (U, r, p1, p1, p2, ..., pn)

    Definition
    ----------
    A formula 𝜑 is a tuple (◆, 𝒳) where:
     * ◆ is a relation.
     * 𝒳 is a finite tuple of parameters
       whose elements are theoretical-objects, possibly formulae.

    Defining properties:
    --------------------
    The defining-properties of a formula are:
     * Being a formula.
     * A relation r.
     * A finite tuple of parameters.

     To do list
     ----------
     - TODO: Question: supporting relation as subformula, where the subformula
        would be a function whose domain would be the class of relations,
        could be an interesting approach to extend the expressiveness of
        Punctilious as a formal language. Consider this in later developments.

    Attributes
    ----------
    relation : (Relation, FreeVariable)

    """

    function_call_representation = repm.Representation(
        python_name='function-call', sample='◆(𝐱₁, 𝐱₂ ,… ,𝐱ₙ)')
    infix_operator_representation = repm.Representation(
        python_name='infix-operator', sample='𝐱₁ ◆ 𝐱₂')
    prefix_operator_representation = repm.Representation(
        python_name='prefix-operator', sample='◆𝐱')
    postfix_operator_representation = repm.Representation(
        python_name='postfix-operator', sample='𝐱◆')

    def __init__(
            self,
            relation: (Relation, FreeVariable),
            parameters: tuple,
            universe_of_discourse: UniverseOfDiscourse,
            symbol: (None, str, Symbol) = None,
            lock_variable_scope: bool = False,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """

        :param theory:
        :param relation:
        :param parameters:
        :param symbol:
        :param arity: Mandatory if relation is a FreeVariable.
        """
        echo = get_config(echo, configuration.echo_formula, configuration.echo_default, fallback_value=False)
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        # self.formula_index = theory.crossreference_formula(self)
        if symbol is None:
            symbol_base = '𝜑'
            symbol = Symbol(
                base=symbol_base, index=universe_of_discourse.index_symbol(
                    base=symbol_base))
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple(
            [parameters])
        self.arity = len(parameters)
        verify(self.arity > 0,
               'The number of parameters in this formula is zero. 0-ary relations are currently not supported.')

        verify(
            is_in_class(relation, classes.free_variable) or
            self.relation.arity == self.arity,
            'The arity of this formula''s relation is inconsistent with the number of parameters in the formula.',
            relation=self.relation,
            parameters=parameters)
        self.parameters = parameters
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        universe_of_discourse.cross_reference_formula(self)
        verify(
            is_in_class(relation, classes.relation) or is_in_class(relation, classes.free_variable),
            'The relation of this formula is neither a relation, nor a '
            'free-variable.',
            formula=self, relation=relation)
        verify(
            relation.universe_of_discourse is self.universe_of_discourse,
            'The universe_of_discourse of the relation of this formula is '
            'distint from the formula unierse_of_disourse.',
            formula=self, relation=relation)
        self.cross_reference_variables()
        for p in parameters:
            verify(
                is_in_class(p, classes.theoretical_objct),
                'p is not a theoretical-objct.',
                slf=self, p=p)
            if is_in_class(p, classes.free_variable):
                p.extend_scope(self)
        if lock_variable_scope:
            self.lock_variable_scope()
        if echo:
            self.echo()
        super()._declare_class_membership(declarative_class_list.formula)

    def __repr__(self):
        return self.repr(expanded=True)

    def __str__(self):
        return self.repr(expanded=True)

    def crossreference_variable(self, x):
        """During construction, cross-reference a free-variable 𝓍
        with its parent formula if it is not already cross-referenced,
        and return its 0-based index in Formula.free_variables."""
        assert isinstance(x, FreeVariable)
        x.formula = self if x.formula is None else x.formula
        assert x.formula is self
        if x not in self.free_variables:
            self.free_variables = self.free_variables + tuple([x])
        return self.free_variables.index(x)

    def cross_reference_variables(self):
        # TODO: Iterate through formula filtering on variable placeholders.
        # TODO: Call cross_reference_variable on every variable placeholder.
        pass
        # assert False

    def echo(self):
        repm.prnt(self.repr_as_declaration())

    @property
    def is_proposition(self):
        """Tell if the formula is a logic-proposition.

        This property is directly inherited from the formula-is-proposition
        attribute of the formula's relation."""
        return self.relation.signal_proposition

    def is_formula_equivalent_to(self, o2: (TheoreticalObjct, Statement, Formula)) -> bool:
        """Returns true if this formula and o2 are formula-equivalent.

        Definition:
        -----------
        A formula φ and a theoretical-object o₂ are formula-equivalent if and only if:
         1. o₂ is a formula.
         2. The relations of φ and o₂ are formula-equivalent.
         3. The parameter ordered tuples of φ and o₂ are pair-wise formula-equivalent.ᵃ

        ᵃ. See the special case of variables formula-equivalence.

        Note:
        -----
        Intuitively, formula-equivalence state that two formula express the
        same thing with the same symbols.
        For instance, formula (¬(True)) and (False) are not formula-equivalent,
        because the former expresses the negation of truth (which is equal to false),
        and the latter expresses falsehood "directly". Both formulae yield
        the same value, but are formulated in a different manned.
        It follows that two formula may yield equal values and not be formula-equivalent.
        But two formula that are formula-equivalent necessarily yield the same value.
        Finally, two formula may not be symbolically-equivalent while
        being formula-equivalent. Because formulae are theoretical-objects.
        and theoretical-objects are symbolic-objcts, formulae have unique symbols.

        To do list
        ----------
        We would not need the concept of formula-equivalence if we would
        forbid the instantiation of "duplicate" formulae in theories.
        TODO: Consider the pros and cons of forbiding "duplicate" formulae in theories
            and removing formula-equivalence as a concept from Punctilious.

        """
        # if o2 is a statement, unpack its embedded formula
        o2 = o2.valid_proposition if is_in_class(o2, classes.statement) else o2
        if self is o2:
            # Trivial case.
            return True
        if not isinstance(o2, Formula):
            return False
        if not self.relation.is_formula_equivalent_to(o2.relation):
            return False
        # Arities are necessarily equal.
        for i in range(len(self.parameters)):
            if not self.parameters[i].is_formula_equivalent_to(
                    o2.parameters[i]):
                return False
        return True

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.relation not in visited:
            yield self.relation
            visited.update({self.relation})
            yield from self.relation.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)
        for parameter in set(self.parameters).difference(visited):
            yield parameter
            visited.update({parameter})
            yield from parameter.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
                                                     extension_limit: (None, Statement) = None):
        """Return a python frozenset of this formula and all theoretical_objcts it contains."""
        ol = frozenset() if ol is None else ol
        ol = ol.union({self})
        if self.relation not in ol:
            ol = ol.union(self.relation.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        for p in self.parameters:
            if p not in ol:
                ol = ol.union(p.list_theoretical_objcts_recursively_OBSOLETE(ol=ol))
        return ol

    def lock_variable_scope(self):
        """Variable scope must be locked when the formula construction
        is completed."""
        variables_list = self.get_variable_set()
        for x in variables_list:
            x.lock_scope()

    def repr(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        if expanded:
            return self.repr_as_formula(expanded=expanded)
        else:
            return super().repr(expanded=expanded)

    def repr_as_function_call(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        return f'{self.relation.repr_as_symbol()}({", ".join([p.repr(expanded=expanded) for p in self.parameters])})'

    def repr_as_infix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        assert self.relation.arity == 2
        return f'({self.parameters[0].repr(expanded=expanded)} {self.relation.repr_as_symbol()} {self.parameters[1].repr(expanded=expanded)})'

    def repr_as_postfix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        assert self.relation.arity == 1
        return f'({self.parameters[0].repr(expanded=expanded)}){self.relation.repr_as_symbol()}'

    def repr_as_prefix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        verify(
            isinstance(expanded, bool),
            'Method parameter "expanded" is not an instance of bool.',
            self=self, expanded=expanded)
        verify(
            self.relation.arity == 1,
            'Attempt to represent prefix operator, but relation arity is not equal to 1.',
            self_relation=self.relation,
            parameters=self.parameters)
        return f'{self.relation.repr_as_symbol()}({self.parameters[0].repr(expanded=expanded)})'

    def repr_as_formula(self, expanded: bool = True):
        if is_in_class(self.relation, classes.free_variable):
            # If the relation of this formula is a free-variable,
            # it has no arity, neither a representation-mode.
            # In this situation, our design-choice is to
            # fallback on the function-call representation-mode.
            # In future developments, we may choose to allow
            # the "decoration" of free-variables with arity,
            # and presentation-mode to improve readability.
            return self.repr_as_function_call(expanded=expanded)
        else:
            match self.relation.formula_rep:
                case Formula.function_call_representation:
                    return self.repr_as_function_call(expanded=expanded)
                case Formula.infix_operator_representation:
                    return self.repr_as_infix_operator(expanded=expanded)
                case Formula.prefix_operator_representation:
                    return self.repr_as_prefix_operator(expanded=expanded)
                case Formula.postfix_operator_representation:
                    return self.repr_as_postfix_operator(expanded=expanded)
        assert 1 == 2

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be the formula {self.repr_as_formula(expanded=True)} in {self.universe_of_discourse.repr_as_symbol()}.'


class RelationDeclarationFormula(Formula):
    def __init__(self, theory, relation, symbol):
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(relation, Relation)
        assert theory.contains_theoretical_objct(relation)
        formula_relation = theoretical_relations.relation_declaration
        super().__init__(
            theory=theory, relation=formula_relation,
            parameters=(theory, relation),
            python=python,
            dashed=dashed, symbol=symbol)


class SimpleObjctDeclarationFormula(Formula):
    """

    Definition
    ----------
    A simple-objct-declaration-formula 𝜑 is a binary formula of the form (◆, (𝒯, ℴ)) where:
    * ◆ is the simple-objct-declaration relation-component.
    * 𝒯 is the parent theory.
    * ℴ is a simple-objct-component.
    """

    def __init__(
            self, theory, simple_objct, python=None, dashed=None, symbol=None):
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(simple_objct, SimpleObjct)
        assert theory.contains_theoretical_objct(simple_objct)
        relation = theoretical_relations.simple_objct_declaration
        super().__init__(
            theory=theory, relation=relation, parameters=(theory, simple_objct),
            python=python,
            dashed=dashed, symbol=symbol)


class StatementCategory(repm.Representation):
    def __init__(self, python_name, symbol_base, natural_name):
        self.symbol_base = symbol_base
        self.natural_name = natural_name
        super().__init__(python_name=python_name, natural_language_name=natural_name)


class StatementCategories(repm.Representation):
    axiom = StatementCategory('axiom', 'a', 'axiom')
    axiom_inclusion = StatementCategory('axiom_inclusion', 'a', 'axiom-inclusion')
    corollary = StatementCategory('corollary', 'p', 'corollary')
    definition = StatementCategory('definition', 'd', 'definition')
    formal_definition = StatementCategory('formal_definition', 'd', 'formal definition')
    hypothesis = StatementCategory('hypothesis', 'h', 'hypothesis')
    inference_rule_inclusion = StatementCategory('inference_rule_inclusion', 'i', 'inference rule inclusion')
    inferred_proposition = ('inferred_proposition', 'i', 'inferred-proposition')
    lemma = StatementCategory('lemma', 'p', 'lemma')
    proposition = StatementCategory('proposition', 'p', 'proposition')
    theorem = StatementCategory('theorem', 'p', 'theorem')
    # Special categories
    missing_category = StatementCategory('missing_category', '�', 'missing category')


statement_categories = StatementCategories('statement_categories')


class NoteCategory(repm.Representation):
    def __init__(self, python_name, symbol_base, natural_name):
        self.symbol_base = symbol_base
        self.natural_name = natural_name
        super().__init__(python_name=python_name)


class NoteCategories(repm.Representation):
    comment = StatementCategory('comment', '𝙲', 'comment')
    note = StatementCategory('note', '𝙽', 'note')
    remark = StatementCategory('remark', '𝚁', 'remark')


note_categories = NoteCategories('note_categories')


class Statement(TheoreticalObjct):
    """

    Definition
    ----------
    Given a theory 𝒯, a statement 𝒮 is a theoretical-object that:
     * announces some truth in 𝒯.

    For 𝒯 to be valid, all statements in 𝒯 must be valid.
    For 𝒯 to be consistent, all statements in 𝒯 must be consistent.
    etc.
    """

    def __init__(
            self,
            theory: TheoryElaboration,
            category,
            symbol: (None, str, Symbol) = None,
            reference=None,
            title=None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: bool = False):
        echo = get_config(echo, configuration.echo_statement, configuration.echo_default, fallback_value=False)
        universe_of_discourse = theory.universe_of_discourse
        self.statement_index = theory.crossreference_statement(self)
        self.theory = theory
        self.category = category
        if symbol is None:
            symbol = Symbol(
                base=self.category.symbol_base, index=self.statement_index)
        reference = symbol.index if reference is None else reference
        self.title = StatementTitleOBSOLETE(
            category=category, reference=reference, title=title)
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.statement)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.repr_as_statement())

    @abc.abstractmethod
    def repr_as_statement(self):
        raise NotImplementedError('This is an abstract method.')

    def repr_as_title(self, cap=False):
        return self.title.repr_full(cap=cap)

    def repr_as_ref(self, cap=False):
        return self.title.repr_ref(cap=cap)


class Axiom(TheoreticalObjct):
    """The Axiom pythonic class models the elaboration of a _contentual_ _axiom_ in a _universe-of-discourse_.

    """

    def __init__(
            self, natural_language, u, symbol=None, auto_index=None, echo=None, header=None):
        """

        :param natural_language: The axiom's content in natural-language.
        :param u: The universe-of-discourse.
        :param symbol:
        :param echo:
        """
        auto_index = get_config(auto_index, configuration.auto_index, fallback_value=False)
        echo = get_config(echo, configuration.echo_axiom, configuration.echo_default, fallback_value=False)
        verify(is_in_class(u, classes.universe_of_discourse),
               'Parameter u is not a member of class universe-of-discourse.')
        verify(isinstance(natural_language, str),
               'Parameter natural-language is not of python-type str.')
        natural_language = natural_language.strip()
        verify(natural_language != '',
               'Parameter natural-language is an empty string (after trimming).')
        self.natural_language = natural_language
        if header is None:
            # Long-names are not a mandatory attribute,
            # it is available to improve readability in reports.
            pass
        elif isinstance(header, str):
            header = ObjctHeader(header, category=statement_categories.axiom, title=None)
        elif header.category is not statement_categories.axiom:
            header = ObjctHeader(header.reference, category=statement_categories.axiom, title=header.title)
            # warnings.warn('A new long-name was generated to force its category property to: axiom.')
        if symbol is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            base = 'a'
            index = u.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            index = u.index_symbol(base=symbol) if auto_index else None
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            universe_of_discourse=u, symbol=symbol, echo=echo, header=header)
        super()._declare_class_membership(declarative_class_list.axiom)
        u.cross_reference_axiom(self)
        if echo:
            repm.prnt(self.repr_as_statement())

    def repr_as_statement(self, output_proofs=True, wrap: bool = True):
        """Return a representation that expresses and justifies the statement."""
        algebraic_name = '' if self.header is None else f' ({self.repr_as_symbol()})'
        text = f'{repm.serif_bold(self.repr_header(cap=True))}{algebraic_name}: “{self.natural_language}”'
        if wrap:
            text = '\n'.join(textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))
        return text


class AxiomInclusion(Statement):
    """An axiom postulation (aka inclusion, endorsement) in the current theory-elaboration.
    """

    def __init__(
            self,
            a: Axiom,
            t: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Postulate (aka include, endorse) an axiom in a theory-elaboration.
        """
        self.axiom = a
        t.crossreference_axiom_inclusion(self)
        super().__init__(
            theory=t,
            category=statement_categories.axiom_inclusion,
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.axiom_inclusion)
        if echo:
            repm.prnt(self.repr_as_statement())

    def repr_as_statement(self, output_proofs=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.repr_as_title(cap=True)}: “{self.axiom.natural_language}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class InferenceRuleInclusion(Statement):
    """An inference-rule inclusion (aka allowance) in the current theory-elaboration.
    """

    def __init__(
            self,
            i: InferenceRule,
            t: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Include (aka allow) an inference-rule in a theory-elaboration.
        """
        self._inference_rule = i
        super().__init__(
            theory=t,
            category=statement_categories.inference_rule_inclusion,
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        t.crossreference_inference_rule_inclusion(self)
        super()._declare_class_membership(declarative_class_list.inference_rule_inclusion)
        if echo:
            repm.prnt(self.repr_as_statement())

    def infer_formula(self, *args, echo: (None, bool) = None):
        return self.inference_rule.infer_formula(*args, t=self.theory, echo=echo)

    def infer_statement(self, *args, echo: (None, bool) = None):
        return self.inference_rule.infer_statement(*args, t=self.theory, echo=echo)

    def verify_args(self, *args):
        return self.inference_rule.verify_args(*args, t=self.theory)

    @property
    def i(self):
        return self.inference_rule

    @property
    def inference_rule(self):
        return self._inference_rule

    def verify_compatibility(self, *args):
        return self.inference_rule.verify_args(*args, t=self.theory)

    def repr_as_statement(self, output_proofs=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'Allow inference-rule “{self.inference_rule}”.'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class Definition(TheoreticalObjct):
    """The Definition pythonic class models the elaboration of a _contentual_ _definition_ in a _universe-of-discourse_.

    """

    def __init__(
            self,
            natural_language: str,
            u: UniverseOfDiscourse,
            auto_index=None,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """

        :param natural_language: The definition's content in natural-language.
        :param u: The universe-of-discourse.
        :param symbol:
        :param echo:
        """
        auto_index = get_config(auto_index, configuration.auto_index, fallback_value=False)
        echo = get_config(echo, configuration.echo_definition, configuration.echo_default, fallback_value=False)
        natural_language = natural_language.strip()
        verify(natural_language != '',
               'Parameter natural-language is an empty string (after trimming).')
        self.natural_language = natural_language
        if header is None:
            # Long-names are not a mandatory attribute,
            # it is available to improve readability in reports.
            pass
        elif isinstance(header, str):
            header = ObjctHeader(header, category=statement_categories.definition, title=None)
        elif header.category is not statement_categories.definition:
            header = ObjctHeader(header.reference, category=statement_categories.definition, title=header.title)
            # warnings.warn('A new long-name was generated to force its category property to: definition.')
        if symbol is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            base = 'd'
            index = u.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            index = u.index_symbol(base=symbol) if auto_index else None
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            universe_of_discourse=u, symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)
        super()._declare_class_membership(declarative_class_list.definition)
        u.cross_reference_definition(self)
        if echo:
            repm.prnt(self.repr_as_statement())

    def repr_as_statement(self, output_proofs=True, wrap: bool = True):
        """Return a representation that expresses and justifies the statement."""
        algebraic_name = '' if self.header is None else f' ({self.repr_as_symbol()})'
        text = f'{repm.serif_bold(self.repr_header(cap=True))}{algebraic_name}: “{self.natural_language}”'
        if wrap:
            text = '\n'.join(textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))
        return text


class DefinitionEndorsement(Statement):
    """A definition-endorsement in the current theory-elaboration.
    """

    def __init__(
            self,
            d: Definition,
            t: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Endorsement (aka include, endorse) an definition in a theory-elaboration.
        """
        echo = get_config(echo, configuration.echo_definition_inclusion, configuration.echo_default,
                          fallback_value=False)
        self.definition = d
        t.crossreference_definition_endorsement(self)
        super().__init__(
            theory=t,
            category=statement_categories.definition,
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        super()._declare_class_membership(declarative_class_list.definition_inclusion)
        if echo:
            repm.prnt(self.repr_as_statement())

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.repr_as_title(cap=True)}: “{self.definition.natural_language}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class FormulaStatement(Statement):
    """

    Definition:
    -----------
    An formula-statement is a statement that expresses the validity of a formula in the parent theory.

    To do list
    ----------
    - TODO: Make FormulaStatement an abstract class

    """

    def __init__(
            self, theory: TheoryElaboration, valid_proposition: Formula,
            symbol: (None, Symbol) = None, category=None,
            reference=None, title=None,
            header: (None, ObjctHeader) = None, dashed_name: (None, DashedName) = None,
            echo=None):
        echo = get_config(echo, configuration.echo_statement, configuration.echo_default, fallback_value=False)
        verify(
            theory.universe_of_discourse is valid_proposition.universe_of_discourse,
            'The universe-of-discourse of this formula-statement''s theory-elaboration is '
            'inconsistent with the universe-of-discourse of the valid-proposition of that formula-statement.')
        universe_of_discourse = theory.universe_of_discourse
        # Theory statements must be logical propositions.
        verify(
            valid_proposition.is_proposition,
            'The formula of this statement is not propositional.')
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        self.valid_proposition = valid_proposition
        self.statement_index = theory.crossreference_statement(self)
        category = statement_categories.proposition if category is None else category
        super().__init__(
            theory=theory, symbol=symbol, category=category,
            reference=reference, title=title,
            header=header, dashed_name=dashed_name,
            echo=False)
        # manage theoretical-morphisms
        self.morphism_output = None
        if self.valid_proposition.relation.signal_theoretical_morphism:
            # this formula-statement is a theoretical-morphism.
            # it follows that this statement "yields" new statements in the theory.
            assert self.valid_proposition.relation.implementation is not None
            self.morphism_output = Morphism(
                theory=theory, source_statement=self)
        super()._declare_class_membership(declarative_class_list.formula_statement)
        if echo:
            self.echo()

    def __repr__(self):
        return self.repr(expanded=True)

    def __str__(self):
        return self.repr(expanded=True)

    @property
    def parameters(self):
        """The parameters of a formula-statement
        are the parameters of the valid-proposition-formula it contains."""
        return self.valid_proposition.parameters

    @property
    def relation(self):
        """The relation of a formula-statement
        is the relation of the valid-proposition-formula it contains."""
        return self.valid_proposition.relation

    def is_formula_equivalent_to(self, o2):
        """Considering this formula-statement as a formula,
        that is the valid-proposition-formula it contains,
        check if it is formula-equivalent to o2."""
        return self.valid_proposition.is_formula_equivalent_to(o2)

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.valid_proposition not in visited:
            yield self.valid_proposition
            visited.update({self.valid_proposition})
            yield from self.valid_proposition.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
                                                     extension_limit: (None, Statement) = None):
        """Return a python frozenset containing this formula-statement,
         and all theoretical_objcts it contains. If a statement-limit is provided,
         does not yield statements whose index is greater than the theoretical-objct."""
        ol = frozenset() if ol is None else ol
        if extension_limit is not None and \
                extension_limit.theory == self.theory and \
                extension_limit.statement_index >= self.statement_index:
            ol = ol.union({self})
            if self.valid_proposition not in ol:
                ol = ol.union(
                    self.valid_proposition.list_theoretical_objcts_recursively_OBSOLETE(ol=ol,
                                                                                        extension_limit=extension_limit))
        return ol

    def repr(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        if expanded:
            return self.repr_as_formula(expanded=expanded)
        else:
            return super().repr(expanded=expanded)

    def repr_as_formula(self, expanded=None):
        # return f'{self.repr_as_symbol()} ⊢ ({self.valid_proposition.repr_as_formula(expanded=expanded)})'
        return f'{self.valid_proposition.repr_as_formula(expanded=expanded)}'


class DirectAxiomInference(FormulaStatement):
    """

    Definition:
    -----------
    A direct-axiom-inference is a valid-proposition directly inferred from a free-text-axiom.

    """

    def __init__(
            self, valid_proposition: FormulaStatement, ap: AxiomInclusion, theory: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            reference=None,
            title=None, category=None, echo: bool = False):
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(ap, AxiomInclusion)
        assert isinstance(valid_proposition, Formula)
        self.axiom = ap
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            symbol=symbol, category=category,
            reference=reference, title=title, echo=echo)
        verify(theory.contains_theoretical_objct(ap), 'The ap is not in the theory hierarchy.', slf=self,
               ap=ap)
        verify(ap not in theory.statements or ap.statement_index < self.statement_index,
               'The dai is a predecessor of the ap that is stated in the same theory.', slf=self, ap=ap)
        super()._declare_class_membership(declarative_class_list.direct_axiom_inference)

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it contains recursively."""
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        if self.axiom not in visited:
            yield self.axiom
            visited.update({self.axiom})
            # axioms are leaf objects, no need to iterate it recursively.
        if self.valid_proposition not in visited:
            yield self.valid_proposition
            visited.update({self.valid_proposition})
            yield from self.valid_proposition.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    def list_theoretical_objcts_recursively_OBSOLETE(self, ol: (None, frozenset) = None,
                                                     extension_limit: (None, Statement) = None):
        print(1 / 0)  # OBSOLETE, REPLACE WITH iterate_theoretical_objcts

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language axiom")}'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {self.axiom.repr_as_ref()}.'
        return output


class Morphism(FormulaStatement):
    """

    Definition:
    -----------
    A theoretical-morphism-statement, or morphism for short, aka syntactic-operation is a valid-proposition produced by a valid-morphism-formula.

    """

    def __init__(
            self, source_statement, symbol=None, theory=None,
            category=None):
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(source_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(source_statement)
        self.source_statement = source_statement
        assert source_statement.valid_proposition.relation.signal_theoretical_morphism
        self.morphism_implementation = source_statement.valid_proposition.relation.implementation
        valid_proposition = self.morphism_implementation(
            self.source_statement.valid_proposition)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            symbol=symbol, category=category)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.repr_as_symbol(cap=True))}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        if output_proofs:
            output = output + self.repr_as_sub_statement()
        return output

    def repr_as_sub_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\t{repm.serif_bold("Derivation by theoretical-morphism / syntactic-operation")}'
        output = output + f'\n\t{self.source_statement.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.source_statement.repr_as_symbol())}.'
        output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Output of {repm.serif_bold(self.source_statement.valid_proposition.relation.repr_as_symbol())} morphism.'
        return output


class PropositionStatement:
    """
    Definition
    ----------
    A proposition-statement 𝒮 is a tuple (𝒯, n, 𝜑, 𝒫) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * 𝜑 is a valid-formula in 𝒯 of the form ⟨◆, 𝒯, 𝜓⟩ where:
        * ◆ is a theoretical-relation
        * 𝜓 is a free-formula
    * 𝒫 is a proof of 𝜑's validity in 𝒯 solely based on predecessors of 𝒮
    """

    def __init__(self, theory, position, phi, proof):
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(position, int) and position > 0
        assert isinstance(phi, Formula)
        assert theory.contains_theoretical_objct(phi)
        assert isinstance(proof, Proof)
        assert theory.contains_theoretical_objct(proof)
        self.theory = theory
        self.position = position
        self.phi = phi
        self.proof = proof


class DirectDefinitionInference(FormulaStatement):
    """

    Definition:
    A theoretical-statement that states that x = some other theoretical-object.
    When an object is defined like this, it means that for every formula
    where x is present, the same formula with the substitution of x by x' can be substituted in all theories.
    TODO: QUESTION: Should we create a base "Alias" object that is distinct from simple-objct???
    XXXXXXX
    """

    def __init__(
            self,
            p: Formula,
            d: DefinitionEndorsement,
            t: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_definition_direct_inference, configuration.echo_default,
                          fallback_value=False)
        verify(
            t.contains_theoretical_objct(d),
            'The definition-endorsement ⌜d⌝ must be contained '
            'in the hierarchy of theory-elaboration ⌜t⌝.',
            d=d, t=t)
        verify(
            p.universe_of_discourse is t.universe_of_discourse,
            'The universe-of-discourse of the valid-proposition ⌜p⌝ must be '
            'consistent with the universe-of-discourse of theory-elaboration ⌜t⌝.',
            p=p, t=t)
        verify(
            p.relation is t.universe_of_discourse.r.equality,
            'The root relation of the valid-proposition ⌜p⌝ must be '
            'the well-known equality-relation ⌜=⌝ in the universe-of-discourse.',
            p=p, p_relation=p.relation)
        self.definition = d
        super().__init__(
            theory=t, valid_proposition=p,
            symbol=symbol, category=statement_categories.formal_definition,
            header=header, dashed_name=dashed_name, echo=False)
        assert d.statement_index < self.statement_index
        super()._declare_class_membership(declarative_class_list.direct_definition_inference)
        if echo:
            repm.prnt(self.repr_as_statement())

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language definition")}'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.definition.repr_as_symbol())}.'
        return output


universe_of_discourse_symbol_indexes = dict()


def index_universe_of_discourse_symbol(base):
    """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
    such that (S, n) is a unique identifier for this UniverseOfDiscourse.

    :param base: The symbol-base.
    :return:
    """
    global universe_of_discourse_symbol_indexes
    if base not in universe_of_discourse_symbol_indexes:
        universe_of_discourse_symbol_indexes[base] = 1
    else:
        universe_of_discourse_symbol_indexes[base] += 1
    return universe_of_discourse_symbol_indexes[base]


class InferenceRuleOBSOLETE:
    """
    TODO: Complete the implementation of InferenceRule, and make ModusPonens a subclass of it.
    TODO: Make InferenceRule itself a Formula with the Sequent operator ⊢.

    Attributes:
    -----------
        premises : tuple
            A tuple of formulae.
        conclusion: Formula
            The conclusion to be derived from the premises if they are true.
    """

    def __init__(self, premises, conclusion):
        self._premises = premises
        self._conclusion = conclusion

    @staticmethod
    def infer(*args, **kwargs):
        pass


import collections.abc


class InferenceRule(TheoreticalObjct):
    """An inference-rule object.

    If an inference-rule is allowed / included in a theory-elaboration,
    it allows to take a sequences of premise statements P1, P2, P3, ...
    of certain shapes,
    and infer a new statement C."""

    def __init__(self,
                 universe_of_discourse: UniverseOfDiscourse,
                 infer_formula: collections.abc.Callable,
                 verify_args: collections.abc.Callable,
                 symbol: (None, str, Symbol) = None,
                 header: (None, str, ObjctHeader) = None,
                 dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        self._infer_formula = infer_formula
        self._verify_args = verify_args
        if symbol is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            base = 'ir'
            index = universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        super().__init__(universe_of_discourse=universe_of_discourse,
                         is_theory_foundation_system=False,
                         symbol=symbol, header=header, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.inference_rule)
        universe_of_discourse.cross_reference_inference_rule(self)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.repr_report())

    def infer_formula(self, *args, t: TheoryElaboration, echo: (None, bool) = None) -> Formula:
        """Apply this inference-rules on input statements and return the resulting statement."""
        phi = self._infer_formula(*args, t=t)
        if echo:
            repm.prnt(phi.repr_as_statement())
        return phi

    def infer_statement(self, *args, t: TheoryElaboration, echo: (None, bool) = None) -> InferredProposition:
        """Apply this inference-rules on input statements and return the resulting statement."""
        return InferredProposition(*args, i=self, t=t, echo=echo)

    def verify_args(self, *args, t: TheoryElaboration):
        """Verify the syntactical-compatibility of input statements and return True
        if they are compatible, False otherwise."""
        return self._verify_args(*args, t=t)


class AtheoreticalStatement(SymbolicObjct):
    """
    Definition
    ----------
    A theoretical-statement 𝒮 is a tuple (𝒯, n, …) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * … is any number of decorative attributes informally related to 𝒮 for human explanatory purposes
    """

    def __init__(self, theory, symbol=None, echo=None):
        assert isinstance(theory, TheoryElaboration)
        self.theory = theory
        super().__init__(symbol=symbol, echo=echo, universe_of_discourse=theory.universe_of_discourse)
        super()._declare_class_membership(classes.atheoretical_statement)


class Note(AtheoreticalStatement):
    """The Note pythonic-class models a note, comment, or remark in a theory.

    """

    def __init__(
            self, natural_language, theory, category: NoteCategory, symbol=None,
            reference=None, title=None, echo=None):
        echo = get_config(echo, configuration.echo_note, configuration.echo_default, fallback_value=False)
        verify(is_in_class(theory, classes.t), 'theory is not a member of declarative-class theory.', theory=theory,
               slf=self)
        universe_of_discourse = theory.universe_of_discourse
        category = note_categories.note if category is None else category
        self.statement_index = theory.crossreference_statement(self)
        self.theory = theory
        self.natural_language = natural_language
        self.category = category
        if symbol is None:
            symbol = Symbol(
                base=self.category.symbol_base, index=self.statement_index)
        reference = symbol.index if reference is None else reference
        self.title = StatementTitleOBSOLETE(
            category=category, reference=reference, title=title)
        super().__init__(
            symbol=symbol,
            theory=theory,
            echo=False)
        if echo:
            self.echo()
        super()._declare_class_membership(declarative_class_list.note)

    def echo(self):
        repm.prnt(self.repr_as_statement())

    def repr_as_title(self, cap=False):
        return self.title.repr_full(cap=cap)

    def repr_as_ref(self, cap=False):
        return self.title.repr_ref(cap=cap)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation of the note that may be included as a section in a report."""
        text = f'{repm.serif_bold(self.repr_as_title(cap=True))}: {self.natural_language}'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class TheoryElaboration(TheoreticalObjct):
    """The TheoryElaboration pythonic class models a [theory-elaboration](theory-elaboration).

    """

    def __init__(
            self,
            u: UniverseOfDiscourse,
            symbol: (str, Symbol) = None,
            dashed_name: (str, DashedName) = None,
            header: (str, ObjctHeader) = None,
            extended_theory: (None, TheoryElaboration) = None,
            extended_theory_limit: (None, Statement) = None,
            include_inconsistency_introduction_inference_rule: bool = False,
            stabilized: bool = False,
            echo: bool = False
    ):
        """

        :param theory: :param is_foundation_system: True if this theory is
        the foundation-system, False otherwise. :param symbol:
         :param extended_theory: :param is_an_element_of_itself:
        """
        self._consistency = consistency_values.undetermined
        self._stabilized = False
        self.axiom_inclusions = tuple()
        self.definition_inclusions = tuple()
        self._inference_rule_inclusions = InferenceRuleInclusionDict(t=self)
        self.statements = tuple()
        self._extended_theory = extended_theory
        self._extended_theory_limit = extended_theory_limit
        self._commutativity_of_equality = None
        if symbol is None:
            base = '𝑡'
            index = u.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = u.index_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            symbol=symbol,
            is_theory_foundation_system=True if extended_theory is None else False,
            universe_of_discourse=u,
            dashed_name=dashed_name,
            header=header,
            echo=False)
        verify(is_in_class(u, classes.universe_of_discourse),
               'Parameter "u" is not a member of declarative-class universe-of-discourse.', u=u)
        verify(extended_theory is None or is_in_class(extended_theory, classes.theory_elaboration),
               'Parameter "extended_theory" is neither None nor a member of declarative-class theory.', u=u)
        verify(extended_theory_limit is None or
               (extended_theory is not None and
                is_in_class(extended_theory_limit, classes.statement) and
                extended_theory_limit in extended_theory.statements),
               'Parameter "theory_extension_statement_limit" is inconsistent.',
               u=u)
        # Inference rules
        # Inconsistency introduction
        self._inconsistency_introduction_inference_rule = None
        include_inconsistency_introduction_inference_rule = False if \
            include_inconsistency_introduction_inference_rule is None else \
            include_inconsistency_introduction_inference_rule
        self._includes_inconsistency_introduction_inference_rule = False
        if include_inconsistency_introduction_inference_rule:
            self.include_inconsistency_introduction_inference_rule()
        super()._declare_class_membership(classes.theory_elaboration)
        if stabilized:
            # It is a design choice to stabilize the theory-elaboration
            # at the very end of construction (__init__()). Note that it
            # is thus possible to extend a theory and, for example,
            # add some new inference-rules by passing these instructions
            # to the constructor.
            self.stabilize()
        if echo:
            repm.prnt(self.repr_as_declaration())

    @property
    def commutativity_of_equality(self):
        """Commutativity-of-equality is a fundamental theory property that enables
        support for SoET. None if the property is not equipped on
        the theory. An instance of FormalAxiom otherwise."""
        if self._commutativity_of_equality is not None:
            return self._commutativity_of_equality
        elif self.extended_theory is not None:
            return self.extended_theory.commutativity_of_equality
        else:
            return None

    @commutativity_of_equality.setter
    def commutativity_of_equality(self, p):
        verify(
            self._commutativity_of_equality is None,
            'A theory commutativity-of-equality property can only be set once '
            'to prevent inconsistency.')
        self._commutativity_of_equality = p

    @property
    def conjunction_introduction_inference_rule(self):
        """The conjunction-introduction inference-rule if it exists in this
        theory, or this theory's foundation-system, otherwise None.
        """
        if self._conjunction_introduction_inference_rule is not None:
            return self._conjunction_introduction_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.conjunction_introduction_inference_rule
        else:
            return None

    @conjunction_introduction_inference_rule.setter
    def conjunction_introduction_inference_rule(self, ir: InferenceRuleOBSOLETE):
        verify(
            not self.stabilized,
            'This theory-elaboration is stabilized, it is no longer possible to allow new inference-rules.',
            inference_rule=ir,
            self_stabilized=self.stabilized,
            slf=self
        )
        verify(
            self._conjunction_introduction_inference_rule is not None and
            self._conjunction_introduction_inference_rule is not ir,
            'The conjunction-introduction inference-rule is already set on this theory-elaboration, '
            'it is no longer possible to modify this inference-rule.',
            inference_rule=ir,
            self_stabilized=self.stabilized,
            slf=self
        )
        self._conjunction_introduction_inference_rule = ir

    def crossreference_axiom_inclusion(self, a):
        """During construction, cross-reference an axiom
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.axioms."""
        assert isinstance(a, AxiomInclusion)
        a.theory = a.theory if hasattr(a, 'theory') else self
        assert a.theory is self
        if a not in self.axiom_inclusions:
            self.axiom_inclusions = self.axiom_inclusions + tuple(
                [a])
        return self.axiom_inclusions.index(a)

    def crossreference_definition_endorsement(self, d):
        """During construction, cross-reference an endorsement
        with its parent theory (if it is not already cross-referenced),
        and return its 0-based index in Theory.endorsements."""
        assert isinstance(d, DefinitionEndorsement)
        d.theory = d.theory if hasattr(d, 'theory') else self
        assert d.theory is self
        if d not in self.definition_inclusions:
            self.definition_inclusions = self.definition_inclusions + tuple(
                [d])
        return self.definition_inclusions.index(d)

    def crossreference_inference_rule_inclusion(self, i: InferenceRuleInclusion):
        """During construction, cross-reference an inference-rule
        with its parent theory-elaboration (if it is not already cross-referenced)."""
        i.theory = i.theory if hasattr(i, 'theory') else self
        assert i.theory is self
        if i not in self.inference_rule_inclusions:
            self.inference_rule_inclusions[i] = i
            return True
        else:
            return False

    def crossreference_statement(self, s):
        """During construction, cross-reference a statement 𝒮
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.statements."""
        assert isinstance(s, (Statement, Note))
        s.theory = s.theory if hasattr(s, 'theory') else self
        assert s.theory is self
        if s not in self.statements:
            self.statements = self.statements + tuple([s])
        return self.statements.index(s)

    # def declare_formula(self, relation, *parameters, **kwargs):
    #    """Declare a new :term:`formula` in this theory.
    #
    #    This method is a shortcut for Formula(theory=t, ...).
    #
    #    A formula is *declared* in a theory, and not *stated*, because it is not a statement,
    #    i.e. it is not necessarily true in this theory.
    #    """
    #    return Formula(
    #        relation=relation, parameters=parameters, theory=self, **kwargs)

    def elaborate_direct_axiom_inference(
            self,
            valid_proposition,
            ap,
            symbol=None, reference=None, title=None, echo: (None, bool) = None) \
            -> DirectAxiomInference:
        """Elaborate a new direct-axiom-inference in the theory. Shortcut for FormalAxiom(theory=t, ...)"""
        return DirectAxiomInference(
            valid_proposition=valid_proposition, ap=ap, symbol=symbol,
            theory=self, reference=reference, title=title, echo=echo)

    def elaborate_direct_definition_inference(
            self, p: Formula, d: DefinitionEndorsement,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Elaborate a formal-definition in this theory.

        Shortcut for FormalDefinition(theory=t, ...)"""
        return DirectDefinitionInference(
            p=p, d=d,
            t=self, symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    @property
    def extended_theory(self) -> (None, TheoryElaboration):
        """None if this is a root theory, the theory that this theory extends otherwise."""
        return self._extended_theory

    @property
    def extended_theory_limit(self) -> (None, Statement):
        """If this is a limited extended-theory, the inclusive statement-limit of the inclusion."""
        return self._extended_theory_limit

    @property
    def inconsistency_introduction_inference_rule(self):
        """The inconsistency-introduction inference-rule if it exists in this
        theory, or this theory's foundation-system, otherwise None.
        """
        if self._inconsistency_introduction_inference_rule is not None:
            return self._inconsistency_introduction_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.inconsistency_introduction_inference_rule
        else:
            return None

    @inconsistency_introduction_inference_rule.setter
    def inconsistency_introduction_inference_rule(self, ir: InferenceRuleOBSOLETE):
        verify(
            self._inconsistency_introduction_inference_rule is None,
            'The inconsistency-introduction inference-rule property of a theory can only be '
            'set once to prevent instability.')
        self._inconsistency_introduction_inference_rule = ir

    def infer_by_biconditional_introduction(
            self, conditional_phi, conditional_psi, symbol=None, category=None,
            reference=None, title=None, echo=None):
        """Infer a new statement in this theory by applying the
        biconditional-introduction inference-rule.

        :param conditional_phi:
        :param conditional_psi:
        :param symbol:
        :param category:
        :param reference:
        :param title:
        :return:
        """
        if not self.biconditional_introduction_inference_rule_is_included:
            raise UnsupportedInferenceRuleException(
                'The biconditional-introduction inference-rule is not contained '
                'in this theory.',
                theory=self, conditional_phi=conditional_phi,
                conditional_psi=conditional_psi)
        else:
            return self.biconditional_introduction_inference_rule.infer(
                theory=self, conditional_phi=conditional_phi,
                conditional_psi=conditional_psi,
                symbol=symbol, category=category,
                reference=reference, title=title, echo=echo)

    def infer_by_conjunction_introduction(
            self, conjunct_p, conjunct_q, symbol=None, category=None,
            reference=None, title=None) -> ConjunctionIntroductionStatement:
        """Infer a new statement in this theory by applying the
        conjunction-introduction inference-rule.

        :param conjunct_p:
        :param conjunct_q:
        :param symbol:
        :param category:
        :param reference:
        :param title:
        :return:
        """
        if self.conjunction_introduction_inference_rule is None:
            raise UnsupportedInferenceRuleException(
                'The conjunction-introduction inference-rule is not contained '
                'in this theory-elaboration.',
                theory_elaboration=self, conjunct_p=conjunct_p, conjunct_q=conjunct_q)
        else:
            return self.conjunction_introduction_inference_rule.infer(
                theory=self, conjunct_p=conjunct_p, conjunct_q=conjunct_q,
                symbol=symbol, category=category,
                reference=reference, title=title)

    def infer_by_double_negation_introduction(
            self, p, symbol=None, category=None,
            reference=None, title=None):
        """Infer a new statement in this theory by applying the
        double-negation-introduction inference-rule.

        :param p:
        :param symbol:
        :param category:
        :param reference:
        :param title:
        :return:
        """
        if not self.double_negation_introduction_inference_rule_is_included:
            raise UnsupportedInferenceRuleException(
                'The double-negation-introduction inference-rule is not contained '
                'in this theory.',
                theory=self, p=p)
        else:
            return self.double_negation_introduction_inference_rule.infer(
                theory=self, p=p,
                symbol=symbol, category=category,
                reference=reference, title=title)

    def infer_by_inconsistency_introduction(
            self, p, not_p, symbol=None, category=None,
            reference=None, title=None):
        """Infer a new statement in this theory by applying the
        inconsistency-introduction inference-rule.

        :param conjunct_p:
        :param conjunct_q:
        :param symbol:
        :param category:
        :param reference:
        :param title:
        :return:
        """
        if not self.inconsistency_introduction_inference_rule_is_included:
            raise UnsupportedInferenceRuleException(
                'The inconsistency-introduction inference-rule is not contained '
                'in this theory.',
                theory=self, p=p, not_p=not_p)
        else:
            return self.inconsistency_introduction_inference_rule.infer(
                theory=self, p=p, not_p=not_p,
                symbol=symbol, category=category,
                reference=reference, title=title)

    def infer_by_modus_ponens(
            self, conditional, antecedent, symbol=None, category=None,
            reference=None, title=None):
        """Infer a statement by applying the modus-ponens (
        MP) inference-rule.

        Let 𝒯 be the theory under consideration.
        Let 𝝋 ⟹ 𝝍 be an implication-statement in 𝒯,
        called the conditional.
        Let 𝝋 be a statement in 𝒯,
        called the antecedent.
        It follows that 𝝍 is valid in 𝒯.
        """
        if self.modus_ponens_inference_rule is None:
            raise UnsupportedInferenceRuleException(
                'The modus-ponens inference-rule is not contained in this '
                'theory',
                theory=self, conditional=conditional, antecedent=antecedent)
        else:
            return self.modus_ponens_inference_rule.infer(
                theory=self, conditional=conditional, antecedent=antecedent,
                symbol=symbol, category=category,
                reference=reference, title=title)

    @property
    def i(self):
        """Return the dictionary of inference-rule-inclusions contained in this theory-elaboration."""
        return self.inference_rule_inclusions

    @property
    def inference_rule_inclusions(self):
        """Return the dictionary of inference-rule-inclusions contained in this theory-elaboration."""
        return self._inference_rule_inclusions

    def iterate_theoretical_objcts_references(self, include_root: bool = True, visited: (None, set) = None):
        """Iterate through this and all the theoretical-objcts it references recursively.

        Theoretical-objcts may contain references to multiple and diverse other theoretical-objcts. Do not confuse this iteration of all references with iterations of objects in the theory-chain.
        """
        visited = set() if visited is None else visited
        if include_root and self not in visited:
            yield self
            visited.update({self})
        for statement in set(self.statements).difference(visited):
            yield statement
            visited.update({statement})
            yield from statement.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)
        if self.extended_theory is not None and self.extended_theory not in visited:
            # Iterate the extended-theory.
            if self.extended_theory_limit is not None:
                # The extended-theory is limited
                # i.e. this theory branched out before the end of the elaboration.
                # Thus, we must exclude statements that are posterior to the limit.
                # To do this, we simply black-list them
                # by including them in the visited set.
                black_list = (
                    statement
                    for statement in set(self.extended_theory.statements)
                    if statement.statement_index > self.extended_theory_limit.statement_index)
                visited.update(black_list)
            yield self.extended_theory
            visited.update({self.extended_theory})
            yield from self.extended_theory.iterate_theoretical_objcts_references(
                include_root=False, visited=visited)

    @property
    def modus_ponens_inference_rule(self):
        """Some theories may contain the modus-ponens inference-rule.

        This property may only be set once to assure the stability of the
        theory."""
        if self._modus_ponens_inference_rule is not None:
            return self._modus_ponens_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.modus_ponens_inference_rule
        else:
            return None

    @modus_ponens_inference_rule.setter
    def modus_ponens_inference_rule(self, ir: InferenceRuleOBSOLETE):
        verify(
            self._modus_ponens_inference_rule is None,
            'The modus-ponens inference-rule property of a theory can only be '
            'set once to prevent instability.')
        self._modus_ponens_inference_rule = ir

    def postulate_axiom(
            self, a: Axiom, symbol: (None, str, Symbol) = None, header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        """Postulate an axiom in this theory-elaboration (self)."""
        return AxiomInclusion(
            a=a, t=self, symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def include_definition(
            self, d: Definition, symbol: (None, str, Symbol) = None, header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        """Include (aka endorse) a definition in this theory-elaboration (self)."""
        return DefinitionEndorsement(
            d=d, t=self, symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def endorse_definition(
            self, d: Definition, symbol: (None, str, Symbol) = None, header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None, echo: (None, bool) = None):
        """Endorse (aka include) a definition in this theory-elaboration (self)."""
        return self.include_definition(
            d=d, symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def infer_by_substitution_of_equal_terms(
            self, original_expression, equality_statement, symbol=None,
            category=None, reference=None, title=None):
        """Infer a statement by applying the substitution-of-equal-terms (
        SoET) inference-rule.

        Let
        """
        return SubstitutionOfEqualTerms(
            original_expression=original_expression,
            equality_statement=equality_statement, symbol=symbol,
            category=category, theory=self, reference=reference, title=title)

    # @property
    # def equality(self):
    #     """(None, Relation) Equality is a fundamental theory property that enables
    #     support for SoET. None if the property is not equipped on
    #     the theory. An instance of Relation otherwise."""
    #     if self._equality is not None:
    #         return self._equality
    #     elif self.extended_theory is not None:
    #         return self.extended_theory.equality
    #     else:
    #         return None
    #
    # @equality.setter
    # def equality(self, r):
    #     verify(
    #         self._equality is None,
    #         'A theory equality property can only be set once to prevent '
    #         'inconsistency.')
    #     verify(
    #         isinstance(r, Relation),
    #         'The equality property must be a relation.')
    #     self._equality = r

    def dai(
            self,
            valid_proposition,
            ap,
            symbol=None, reference=None, title=None,
            echo: (None, bool) = None) \
            -> DirectAxiomInference:
        """Elaborate a new direct-axiom-inference in the theory. Shortcut for
        Theory.elaborate_direct_axiom_inference(...)."""
        return self.elaborate_direct_axiom_inference(
            valid_proposition=valid_proposition, ap=ap, symbol=symbol,
            reference=reference, title=title, echo=echo)

    def ddi(
            self, p: Formula, d: DefinitionEndorsement,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Elaborate a formal-definition in this theory.

        Shortcut for FormalDefinition(theory=t, ...)"""
        return self.elaborate_direct_definition_inference(
            p=p, d=d,
            symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def iterate_statements_in_theory_chain(self):
        """Iterate through the (proven or sound) statements in the current theory-chain."""
        for t in self.iterate_theory_chain():
            for s in t.statements:
                yield s

    def iterate_theory_chain(self, visited: (None, set) = None):
        """Iterate over the theory-chain of this theory.


        The sequence is: this theory, this theory's extended-theory, the extended-theory's extended-theory, etc. until the root-theory is processes.

        Note:
        -----
        The theory-chain set is distinct from theory-dependency set.
        The theory-chain informs of the parent theories whose statements are considered valid in the current theory.
        Distinctively, theories may be referenced by meta-theorizing, or in hypothesis, or possibly other use cases.
        """
        visited = set() if visited is None else visited
        t = self
        while t is not None:
            yield t
            visited.update({t})
            if t.extended_theory is not None and t.extended_theory not in visited:
                t = t.extended_theory
            else:
                t = None

    def iterate_valid_propositions_in_theory_chain(self):
        """Iterate through the valid-propositions in the current theory-chain."""
        visited = set()
        for s in self.iterate_statements_in_theory_chain():
            if is_in_class(s, classes.formula_statement) and s.valid_proposition not in visited:
                yield s.valid_proposition
                visited.update({s.valid_proposition})

    def ii(
            self, p, not_p, symbol=None, category=None,
            reference=None, title=None):
        """Infer a new statement in this theory by applying the
        inconsistency-introduction inference-rule."""
        return self.infer_by_inconsistency_introduction(
            p=p, not_p=not_p,
            symbol=symbol,
            category=category, reference=reference, title=title)

    def include_inconsistency_introduction_inference_rule(self):
        """Include the inconsistency-introduction inference-rule in this
        theory."""
        verify(
            not self.inconsistency_introduction_inference_rule_is_included,
            'The inconsistency-introduction inference-rule is already included in this theory.')
        # TODO: Justify the inclusion of the inference-rule in the theory
        #   with adequate statements (axioms?).
        self._inconsistency_introduction_inference_rule = InconsistencyIntroductionInferenceRuleOBSOLETE
        self._includes_inconsistency_introduction_inference_rule = True

    @property
    def consistency(self) -> Consistency:
        """The currently proven consistency status of this theory.

        Possible values are:
        - proved-consistent,
        - proved-inconsistent,
        - undetermined."""
        return self._consistency

    @property
    def inconsistency_introduction_inference_rule_is_included(self):
        """True if the inconsistency-introduction inference-rule is included in this theory, False otherwise."""
        if self._includes_inconsistency_introduction_inference_rule is not None:
            return self._includes_inconsistency_introduction_inference_rule
        elif self.extended_theory is not None:
            return self.extended_theory.inconsistency_introduction_inference_rule_is_included
        else:
            return None

    def d(self, natural_language, symbol=None, reference=None, title=None):
        """Elaborate a new definition with natural-language. Shortcut function for
        t.elaborate_definition(...)."""
        return self.endorse_definition(
            natural_language=natural_language, symbol=symbol,
            reference=reference, title=title)

    def pose_hypothesis(
            self,
            hypothetical_proposition: Formula, symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None, dashed_name: (None, str, DashedName) = None,
            echo: bool = False) -> Hypothesis:
        """Pose a new hypothesis in the current theory."""
        return Hypothesis(
            t=self, hypothetical_formula=hypothetical_proposition,
            symbol=symbol, header=header, dashed_name=dashed_name,
            echo=echo)

    def repr_theory_report(self, output_proofs=True):
        """Return a representation that expresses and justifies the theory."""
        output = f'\n{repm.serif_bold(self.repr_as_symbol())}'
        output += f'\n{repm.serif_bold("Consistency:")} {str(self.consistency)}'
        output += f'\n{repm.serif_bold("Stabilized:")} {str(self.stabilized)}'
        output += f'\n{repm.serif_bold("Extended theory:")} {"N/A" if self.extended_theory is None else self.extended_theory.repr_fully_qualified_name()}'
        output += f'\n\n{repm.serif_bold("Simple-objct declarations:")}'
        # TODO: Limit the listed objects to those that are referenced by the theory,
        #   instead of outputting all objects in the universe-of-discourse.
        output = output + '\n' + '\n'.join(
            o.repr_as_declaration() for o in
            self.universe_of_discourse.simple_objcts.values())
        # Relation declarations
        relations = self.iterate_relations()
        arities = frozenset(r.arity for r in relations)
        for a in arities:
            output += repm.serif_bold(f'\n\n{repr_arity_as_text(a).capitalize()} relations:')
            for r_long_name in frozenset(r.repr_fully_qualified_name() for r in relations if r.arity == a):
                output += '\n ⁃ ' + r_long_name
        # output += f'\n\n{repm.serif_bold("Relation declarations:")}'
        # output = output + '\n' + '\n'.join(
        #    r.repr_as_declaration() for r in
        #    self.universe_of_discourse.relations.values())
        output += f'\n\n{repm.serif_bold("Theory elaboration:")}'
        output = output + '\n\n' + '\n\n'.join(
            s.repr_as_statement(output_proofs=output_proofs) for s in
            self.statements)
        return str(output)

    def soet(
            self, original_expression, equality_statement, symbol=None,
            category=None, reference=None, title=None):
        """Elaborate a new modus-ponens statement in the theory. Shortcut for
        ModusPonens(theory=t, ...)"""
        return self.infer_by_substitution_of_equal_terms(
            original_expression=original_expression,
            equality_statement=equality_statement, symbol=symbol,
            category=category, reference=reference, title=title)

    def prnt(self, output_proofs=True):
        repm.prnt(self.repr_theory_report(output_proofs=output_proofs))

    def prove_inconsistent(self, ii):
        verify(isinstance(ii, InconsistencyIntroductionStatement),
               'The ii statement is not of type InconsistencyIntroductionStatement.', ii=ii, theory=self)
        verify(ii in self.statements,
               'The ii statement is not a statement of this theory.', ii=ii, theory=self)
        self._consistency = consistency_values.proved_inconsistent

    def export_to_text(self, file_path, output_proofs=True):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.repr_theory_report(output_proofs=output_proofs))
        text_file.close()

    @property
    def stabilized(self):
        """Return the stabilized property of this theory-elaboration.
        """
        return self._stabilized

    def stabilize(self):
        verify(not self._stabilized,
               'This theory-elaboration is already stabilized.', severity=verification_severities.warning)
        self._stabilized = True

    def take_note(self, natural_language, symbol=None, reference=None,
                  title=None, echo=None, category=None):
        """Take a note in this theory.

        Shortcut for u.take_note(theory=t, ...)"""
        return self.universe_of_discourse.take_note(
            t=self,
            natural_language=natural_language, symbol=symbol,
            reference=reference, title=title, echo=echo, category=category)

    @property
    def theoretical_objcts(self):
        list = set()
        for s in self.statements:
            list.add(s)
            if is_in_class(s, classes.formula):
                list.add()


class Hypothesis(Statement):
    def __init__(
            self, t: TheoryElaboration, hypothetical_formula: Formula, symbol: (None, Symbol) = None,
            header: (None, ObjctHeader) = None, dashed_name: (None, DashedName) = None,
            echo: bool = False):
        category = statement_categories.hypothesis
        # TODO: Check that all components of the hypothetical-proposition
        #  are elements of the source theory-branch.
        verify(
            hypothetical_formula.is_proposition,
            'The hypothetical-formula is not a proposition.',
            hypothetical_formula=hypothetical_formula,
            slf=self)
        if symbol is None:
            # If no symbol is passed as a parameter,
            # automated assignment of symbol is assumed.
            base = 'ℎ'
            index = t.universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        super().__init__(
            theory=t, category=category, symbol=symbol,
            header=header, dashed_name=dashed_name, echo=False)
        super()._declare_class_membership(declarative_class_list.hypothesis)
        self.hypothetical_proposition_formula = hypothetical_formula
        self.hypothetical_t = t.universe_of_discourse.t(
            extended_theory=t,
            extended_theory_limit=self
        )
        self.hypothetical_axiom = self.universe_of_discourse._inference_rule(
            f'Assume {hypothetical_formula.repr_as_formula()} is true.')
        self.hypothetical_axiom_postulate = self.hypothetical_t.postulate_axiom(
            self.hypothetical_axiom)
        self.proposition = self.hypothetical_t.dai(valid_proposition=hypothetical_formula,
                                                   ap=self.hypothetical_axiom_postulate)


class Proof:
    """TODO: Define the proof class"""

    def __init__(self):
        self.is_valid = True  # TODO: Develop the is_valid attribute


class Relation(TheoreticalObjct):
    """
    Definition
    ----------
    A relation ◆ is a theoretical-object for formula.
    It assigns the following meaning to its composite formula 𝜑:
    𝜑 establishes a relation between its parameters.
    A relation ◆ has a fixed arity.

    Defining properties
    -------------------
     - Arity
     - Symbol

    Attributes
    ----------
    signal_proposition : bool
        True if the relation instance signals that formulae based on this relation are logical-propositions,
        i.e. the relation is a function whose domain is the set of truth values {True, False}.
        False otherwise.
        When True, the formula may be used as a theory-statement.

    signal_theoretical_morphism : bool
        True if the relation instance signals that formulae based on this relation are theoretical-morphisms.

    implementation : bool
        If the relation has an implementation, a reference to the python function.
    """

    def __init__(
            self, arity: int, symbol: (None, str, Symbol) = None, formula_rep=None,
            signal_proposition=None, signal_theoretical_morphism=None,
            implementation=None, universe_of_discourse=None, dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_relation, configuration.echo_default,
                          fallback_value=False)
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        signal_proposition = False if signal_proposition is None else signal_proposition
        signal_theoretical_morphism = False if signal_theoretical_morphism is None else signal_theoretical_morphism
        assert isinstance(signal_proposition, bool)
        assert isinstance(signal_theoretical_morphism, bool)
        self.formula_rep = Formula.function_call_representation if formula_rep is None else formula_rep
        self.signal_proposition = signal_proposition
        self.signal_theoretical_morphism = signal_theoretical_morphism
        self.implementation = implementation
        if symbol is None:
            base = '◆'
            index = universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = universe_of_discourse.index_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity
        super().__init__(
            universe_of_discourse=universe_of_discourse, symbol=symbol, dashed_name=dashed_name,
            echo=False)
        self.universe_of_discourse.cross_reference_relation(r=self)
        super()._declare_class_membership(classes.relation)
        if echo:
            self.echo()

    # def repr(self, expanded=None):
    #    return self.repr_as_symbol()

    def echo(self):
        repm.prnt(self.repr_as_declaration())

    def repr_as_declaration(self):
        output = f'Let {self.repr_fully_qualified_name()} be a {repr_arity_as_text(self.arity)} relation in {self.u.repr_as_symbol()}'
        output = output + f' (notation convention: {self.formula_rep} syntax).'
        return output


def repr_arity_as_text(n):
    match n:
        case 1:
            return 'unary'
        case 2:
            return 'binary'
        case 3:
            return 'ternary'
        case _:
            return f'{n}-ary'


class SimpleObjct(TheoreticalObjct):
    """
    Definition
    ----------
    A simple-objct-component ℴ is a theoretical-object that has no special attribute,
    and whose sole function is to provide the meaning of being itself.
    """

    def __init__(
            self, universe_of_discourse: UniverseOfDiscourse,
            symbol: (None, str, Symbol) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_simple_objct, configuration.echo_default,
                          fallback_value=False)
        if symbol is None:
            base = 'ℴ'
            index = universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        if isinstance(symbol, str):
            symbol = symbol.strip()
            verify(symbol != '', 'The symbol is an empy string.', symbol=symbol)
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = universe_of_discourse.index_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            universe_of_discourse=universe_of_discourse, symbol=symbol,
            dashed_name=dashed_name, echo=False)
        self.universe_of_discourse.cross_reference_simple_objct(o=self)
        if echo:
            self.echo()

    def echo(self):
        repm.prnt(self.repr_as_declaration())

    def is_masked_formula_similar_to(self, o2, mask, _values):
        assert isinstance(o2, TheoreticalObjct)
        if isinstance(o2, FreeVariable):
            if o2 in mask:
                # o2 is a variable, and it is present in the mask.
                # first, we must check if it is already in the dictionary of values.
                if o2 in _values:
                    # the value is already present in the dictionary.
                    known_value = _values[o2]
                    if known_value is self:
                        # the existing value matches the newly observed value.
                        # until there, masked-formula-similitude is preserved.
                        return True, _values
                    else:
                        # the existing value does not match the newly observed value.
                        # masked-formula-similitude is no longer preserved.
                        return False, _values
                else:
                    # the value is not present in the dictionary.
                    # until there, masked-formula-similitude is preserved.
                    _values[o2] = self
                    return True, _values
        if not isinstance(o2, SimpleObjct):
            # o1 (self) is a simple-objct, and o2 is something else.
            # in consequence, masked-formula-similitude is no longer preserved.
            return False, _values
        # o2 is not a variable.
        return self.is_formula_equivalent_to(o2), _values

    def repr_as_declaration(self):
        output = f'Let {self.repr_fully_qualified_name()} be a simple-objct in {self.u.repr_as_symbol()}.'
        return output


class SubstitutionOfEqualTerms(FormulaStatement):
    """
    TODO: Develop SubstitutionOfEqualTerms

    Definition:
    -----------
    A substitution-of-equal-terms is a valid rule-of-inference propositional-logic argument that,
    given a proposition (phi)
    given a proposition (x = y)
    infers the proposition (subst(phi, x, y))
    """

    symbol_base = '𝚂𝙾𝙴𝚃'

    def __init__(
            self, original_expression, equality_statement, symbol=None,
            category=None, theory=None, reference=None, title=None):
        category = statement_categories.proposition if category is None else category
        # Check p_implies_q consistency
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(original_expression, FormulaStatement)
        assert theory.contains_theoretical_objct(original_expression)
        assert isinstance(equality_statement, FormulaStatement)
        assert theory.contains_theoretical_objct(equality_statement)
        assert equality_statement.valid_proposition.relation is theory.universe_of_discourse.r.equality
        left_term = equality_statement.valid_proposition.parameters[0]
        right_term = equality_statement.valid_proposition.parameters[1]
        self.original_expression = original_expression
        self.equality_statement = equality_statement
        substitution_map = {left_term: right_term}
        valid_proposition = original_expression.valid_proposition.substitute(
            substitution_map=substitution_map, target_theory=theory,
            lock_variable_scope=True)
        # Note: valid_proposition will be formula-equivalent to self,
        #   if there are no occurrences of left_term in original_expression.
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category,
            symbol=symbol, reference=reference, title=title)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Substitution of equal terms")}'
            output = output + f'\n\t{self.original_expression.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.original_expression.repr_as_ref())}.'
            output = output + f'\n\t{self.equality_statement.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.equality_statement.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class TheoreticalRelation(Relation):
    """
    Definition:
    A theoretical-relation ◆ is a relation that express theoretical-statements.

    Note:
    Simply put, theoretical-relations is a list of pre-defined relations
    that makes it possible to elaborate theories.

    """

    def __init__(self, theory, arity, symbol):
        super().__init__(theory=theory, arity=arity, symbol=symbol)


class Tuple(tuple):
    """Tuple subclasses the native tuple class.
    The resulting supports setattr, getattr, hasattr,
    which are convenient to create friendly programmatic shortcuts."""
    pass


class RelationDict(collections.UserDict):
    """A dictionary that exposes well-known relations as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._biconditional = None
        self._conjunction = None
        self._disjunction = None
        self._equality = None
        self._inconsistent = None
        self._inequality = None
        self._implication = None
        self._negation = None

    def declare(self, arity: int, symbol: (None, str, Symbol) = None, formula_rep=None,
                signal_proposition=None,
                signal_theoretical_morphism=None,
                implementation=None, dashed_name: (None, str, DashedName) = None,
                echo: (None, bool) = None):
        """Declare a new relation in this universe-of-discourse.
        """
        return Relation(
            arity=arity,
            symbol=symbol, dashed_name=dashed_name,
            formula_rep=formula_rep,
            signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation,
            universe_of_discourse=self.u,
            echo=echo)

    @property
    def biconditional(self):
        """The well-known biconditional relation.

        Abridged property: u.r.iif

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._biconditional is None:
            self._biconditional = self.declare(
                2, '⟺', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='biconditional')
        return self._biconditional

    @property
    def conjunction(self):
        """The well-known conjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._conjunction is None:
            self._conjunction = self.declare(
                2, '∧', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='conjunction')
        return self._conjunction

    @property
    def disjunction(self):
        """The well-known disjunction relation.

        Abridged property: u.r.land

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._disjunction is None:
            self._disjunction = self.declare(
                2, '∨', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='disjunction')
        return self._disjunction

    @property
    def eq(self):
        """The well-known equality relation.

        Unabridged property: u.r.equality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.equality

    @property
    def equality(self):
        """The well-known equality relation.

        Abridged property: u.r.eq

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._equality is None:
            self._equality = self.declare(
                2, '=', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='equality')
        return self._equality

    @property
    def inc(self):
        """The well-known (theory-)inconsistent relation.

        Unabridged property: u.r.inconsistent

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inconsistent

    @property
    def implication(self):
        """The well-known implication relation.

        Abridged property: u.r.implies

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._implication is None:
            self._implication = self.declare(
                2, '⟹', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='implication')
        return self._implication

    @property
    def implies(self):
        """The well-known implication relation.

        Unabridged property: u.r.implication

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.implication

    @property
    def inconsistent(self):
        """The well-known (theory-)inconsistent relation.

        Abridged property: u.r.inc

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inconsistent is None:
            self._inconsistent = self.declare(
                1, 'Inc', Formula.prefix_operator_representation,
                signal_proposition=True, dashed_name='inconsistent')
        return self._inconsistent

    @property
    def inequality(self):
        """The well-known inequality relation.

        Abridged property: u.r.neq

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._inequality is None:
            self._inequality = self.declare(
                2, '≠', Formula.infix_operator_representation,
                signal_proposition=True, dashed_name='inequality')
        return self._inequality

    @property
    def land(self):
        """The well-known conjunction relation.

        Unabridged property: u.r.conjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.conjunction

    @property
    def lnot(self):
        """The well-known negation relation.

        Abridged property: u.r.negation

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.negation

    @property
    def lor(self):
        """The well-known disjunction relation.

        Unabridged property: u.r.disjunction

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.disjunction

    @property
    def negation(self):
        """The well-known negation relation.

        Abridged property: u.r.lnot

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        if self._negation is None:
            self._negation = self.declare(
                1, '¬', Formula.prefix_operator_representation,
                signal_proposition=True, dashed_name='negation')
        return self._negation

    @property
    def neq(self):
        """The well-known inequality relation.

        Unabridged property: u.r.inequality

        If it does not exist in the universe-of-discourse,
        declares it automatically.
        """
        return self.inequality


class InferenceRuleDict(collections.UserDict):
    """A dictionary that exposes well-known objects as properties.

    """

    def __init__(self, u: UniverseOfDiscourse):
        self.u = u
        super().__init__()
        # Well-known objects
        self._absorption = None
        self._biconditional_elimination_left = None
        self._biconditional_elimination_right = None
        self._biconditional_introduction = None
        self._conjunction_elimination_left = None
        self._conjunction_elimination_right = None
        self._conjunction_introduction = None
        self._disjunction_elimination = None  # TODO: IMPLEMENT disjunction_elimination
        self._disjunction_introduction = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._modus_ponens = None

    @property
    def absorb(self) -> InferenceRule:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.absorption

    @property
    def absorption(self) -> InferenceRule:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for absorption
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            phi = unpack_formula(args[0])
            p = unpack_formula(phi.parameters[0])
            q = unpack_formula(phi.parameters[1])
            psi = t.u.f(t.u.r.implication, p, t.u.f(t.u.r.conjunction, p, q))
            return psi

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.implication,
                'The relation of formula ⌜phi⌝ must be an implication.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._absorption is None:
            self._absorption = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('absorb', index=None),
                dashed_name=DashedName('absorption'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._absorption

    @property
    def bi(self) -> InferenceRule:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_introduction

    @property
    def bel(self) -> InferenceRule:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_elimination_left

    @property
    def ber(self) -> InferenceRule:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_elimination_right

    @property
    def biconditional_elimination_left(self) -> InferenceRule:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for bel
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            phi = unpack_formula(args[0])
            # phi is a formula of the form P ⟺ Q
            # unpack the embedded formulae
            p = unpack_formula(phi.parameters[0])
            q = unpack_formula(phi.parameters[1])
            psi = t.u.f(t.u.r.implication, p, q)
            return psi

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.biconditional,
                'The relation of formula ⌜phi⌝ must be a biconditional.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('bel', index=None),
                dashed_name=DashedName('biconditional-elimination-left'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> InferenceRule:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for ber
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            phi = unpack_formula(args[0])
            # phi is a formula of the form P ⟺ Q
            # unpack the embedded formulae
            p = unpack_formula(phi.parameters[0])
            q = unpack_formula(phi.parameters[1])
            psi = t.u.f(t.u.r.implication, q, p)
            return psi

        def verify_compatibility(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            phi = args[0]
            verify(
                t.contains_theoretical_objct(phi),
                'Statement ⌜phi⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                phi=phi, t=t, slf=self)
            phi = unpack_formula(phi)
            verify(
                phi.relation is t.u.r.biconditional,
                'The relation of formula ⌜phi⌝ must be a biconditional.',
                phi_relation=phi.relation, phi=phi, t=t, slf=self)
            return True

        if self._biconditional_elimination_right is None:
            self._biconditional_elimination_right = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('ber', index=None),
                dashed_name=DashedName('biconditional-elimination-right'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._biconditional_elimination_right

    @property
    def biconditional_introduction(self) -> InferenceRule:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for bi
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])
            return t.u.f(t.u.r.biconditional, p, q)

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p_implies_q = args[0]
            verify(
                t.contains_theoretical_objct(p_implies_q),
                'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p_implies_q=p_implies_q, t=t, slf=self)
            p_implies_q = unpack_formula(p_implies_q)
            verify(
                p_implies_q.relation is t.u.r.implication,
                'The relation of formula ⌜p_implies_q⌝ must be an implication.',
                p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
            q_implies_p = args[1]
            verify(
                t.contains_theoretical_objct(q_implies_p),
                'Statement ⌜q_implies_p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                q_implies_p=q_implies_p, t=t, slf=self)
            q_implies_p = unpack_formula(q_implies_p)
            verify(
                q_implies_p.relation is t.u.r.implication,
                'The relation of formula ⌜q_implies_p⌝ must be an implication.',
                q_implies_p_relation=p_implies_q.relation, q_implies_p=q_implies_p, t=t, slf=self)
            return True

        if self._biconditional_introduction is None:
            self._biconditional_introduction = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('bi', index=None),
                dashed_name=DashedName('biconditional-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._biconditional_introduction

    @property
    def conjunction_elimination_left(self) -> InferenceRule:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Abridged property: u.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for cel
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(p.parameters[0])
            return q

        def verify_compatibility(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.conjunction,
                'The relation of formula ⌜p⌝ must be a conjunction.',
                p_relation=p.relation, p=p, t=t, slf=self)
            return True

        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('cel', index=None),
                dashed_name=DashedName('conjunction-elimination-left'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRule:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Abridged property: u.i.cer()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for cer
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            r = unpack_formula(p.parameters[1])
            return r

        def verify_compatibility(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.conjunction,
                'The relation of formula ⌜p⌝ must be a conjunction.',
                p_relation=p.relation, p=p, t=t, slf=self)
            return True

        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('cer', index=None),
                dashed_name=DashedName('conjunction-elimination-right'),
                infer_formula=infer_formula,
                verify_args=verify_compatibility)
        return self._conjunction_elimination_right

    @property
    def conjunction_introduction(self) -> InferenceRule:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Abridged property: u.i.ci

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for CI
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])
            return t.u.f(t.u.r.land, p, q)

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p=p, t=t, slf=self)
            p = unpack_formula(p)
            q = args[1]
            verify(
                t.contains_theoretical_objct(q),
                'Statement ⌜q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                q=q, t=t, slf=self)
            q = unpack_formula(q)
            return True

        if self._conjunction_introduction is None:
            self._conjunction_introduction = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('ci', index=None),
                dashed_name=DashedName('conjunction-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._conjunction_introduction

    @property
    def di(self) -> InferenceRule:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Unabridged property: u.i.disjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.disjunction_introduction

    @property
    def disjunction_introduction(self) -> InferenceRule:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Abridged property: u.i.di

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for di
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(args[1])  # Note: q may be a formula, because q may be false.
            return t.u.f(t.u.r.disjunction, p, q)

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args: A statement P, and a propositional-formula Q
            :param t:
            :return: The statement (P ∨ Q)
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p=p, t=t, slf=self)
            p = unpack_formula(p)
            # Q may be a formula (i.e. it is not necessarily a statement),
            # because Q may be any propositional formula (i.e it may be false).
            q = unpack_formula(args[1])
            verify(
                q.is_proposition,
                'Statement ⌜q⌝ must be a logical-proposition formula (and not necessarily a statement).',
                q_is_proposition=q.is_proposition, q=q, p=p, t=t, slf=self)
            return True

        if self._disjunction_introduction is None:
            self._disjunction_introduction = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('di', index=None),
                dashed_name=DashedName('disjunction-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._disjunction_introduction

    @property
    def double_negation_elimination(self) -> InferenceRule:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Abridged property: u.i.dne

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for dne
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            q = unpack_formula(p.parameters[0])
            r = unpack_formula(q.parameters[0])
            return r

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            p = unpack_formula(p)
            verify(
                p.relation is t.u.r.lnot,
                'The relation of formula ⌜p⌝ must be a negation.',
                p_relation=p.relation, p=p, t=t, slf=self)
            q = unpack_formula(p.parameters[0])
            verify(
                q.relation is t.u.r.lnot,
                'The relation of formula ⌜q⌝ must be a negation.',
                q_relation=q.relation, q=q, p=p, t=t, slf=self)
            return True

        if self._double_negation_elimination is None:
            self._double_negation_elimination = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('dne', index=None),
                dashed_name=DashedName('double-negation-elimination'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> InferenceRule:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Abridged property: u.i.dni

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.

        TODO: Implement free-variables support for dni
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args:
            :param t:
            :return:
            """
            p = unpack_formula(args[0])
            return t.u.f(t.u.r.lnot, t.u.f(t.u.r.lnot, p))

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args:
            :param t:
            :return:
            """
            verify(
                len(args) == 1,
                'Exactly 1 item is expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p = args[0]
            verify(
                t.contains_theoretical_objct(p),
                'Statement ⌜p⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                args=args, t=t, slf=self)
            return True

        if self._double_negation_introduction is None:
            self._double_negation_introduction = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('dni', index=None),
                dashed_name=DashedName('double-negation-introduction'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._double_negation_introduction

    @property
    def cel(self) -> InferenceRule:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_left

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_elimination_left

    @property
    def cer(self) -> InferenceRule:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_right

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_elimination_right

    @property
    def ci(self) -> InferenceRule:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_introduction

    @property
    def dne(self) -> InferenceRule:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Original method: universe_of_discourse.inference_rules.double_negation_elimination

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.double_negation_elimination

    @property
    def dni(self) -> InferenceRule:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Original method: universe_of_discourse.inference_rules.double_negation_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.double_negation_introduction

    @property
    def modus_ponens(self) -> InferenceRule:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P' ⊢ Q'.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """

        def infer_formula(*args, t: TheoryElaboration) -> Formula:
            """

            :param args: A statement (P ⟹ Q), and a statement P
            :param t:
            :return: A formula Q
            """
            p_implies_q = unpack_formula(args[0])
            p = unpack_formula(p_implies_q.parameters[0])
            q = unpack_formula(p_implies_q.parameters[1])
            # The antecedant ⌜p⌝ of the implication ⌜p_implies_q⌝ may contain free-variables,
            # store these in a mask for masked-formula-similitude comparison.
            mask = p.get_variable_set()
            p_prime = unpack_formula(args[1])  # Received as a statement-parameter to prove that p is true in t.
            # Check for mask-formula-similitude and simultaneously,
            # retrieve all free-variable values.
            similitude, free_variables_values = p_prime._is_masked_formula_similar_to(
                o2=p, mask=mask)
            # Build a variable substitution map from the variable values.
            substitution_map = dict((v, k) for k, v in free_variables_values.items())
            # Finally, build the concluding proposition by applying
            # variable substitutions.
            conclusion = q.substitute(
                substitution_map=substitution_map, target_theory=t)
            return conclusion  # TODO: Provide support for statements that are atomic propositional formula, that is without relation or where the objct is a 0-ary relation.

        def verify_args(*args, t: TheoryElaboration) -> bool:
            """

            :param args: A statement (P ⟹ Q), and a statement P
            :param t:
            :return: A formula Q
            """
            verify(
                len(args) == 2,
                'Exactly 2 items are expected in ⌜*args⌝ .',
                args=args, t=t, slf=self)
            p_implies_q = args[0]
            verify(
                t.contains_theoretical_objct(p_implies_q),
                'Statement ⌜p_implies_q⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p_implies_q=p_implies_q, t=t, slf=self)
            p_implies_q = unpack_formula(p_implies_q)
            verify(
                p_implies_q.relation is t.u.r.implication,
                'The relation of formula ⌜p_implies_q⌝ must be an implication.',
                p_implies_q_relation=p_implies_q.relation, p_implies_q=p_implies_q, t=t, slf=self)
            p_prime = args[1]
            verify(
                t.contains_theoretical_objct(p_prime),
                'Statement ⌜p_prime⌝ must be contained in theory ⌜t⌝''s hierarchy.',
                p_prime=p_prime, t=t, slf=self)
            p_prime = unpack_formula(p_prime)
            p = unpack_formula(p_implies_q.parameters[0])
            # The antecedant of the implication may contain free-variables,
            # store these in a mask for masked-formula-similitude comparison.
            mask = p.get_variable_set()
            masked_formula_similitude = p_prime.is_masked_formula_similar_to(o2=p, mask=mask)
            verify(
                masked_formula_similitude,
                'Formula ⌜p⌝ in statement ⌜p_implies_q⌝ must be masked-formula-similar to statement ⌜p_prime⌝.',
                masked_formula_similitude=masked_formula_similitude, p_implies_q=p_implies_q, p=p, p_prime=p_prime, t=t,
                slf=self)
            return True

        if self._modus_ponens is None:
            self._modus_ponens = InferenceRule(
                universe_of_discourse=self.u,
                symbol=Symbol('mp', index=None),
                dashed_name=DashedName('modus-ponens'),
                infer_formula=infer_formula,
                verify_args=verify_args)
        return self._modus_ponens

    @property
    def mp(self) -> InferenceRule:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.modus_ponens


class InferenceRuleInclusionDict(collections.UserDict):
    """A dictionary that exposes well-known objects as properties.

    """

    def __init__(self, t: TheoryElaboration):
        self.t = t
        super().__init__()
        # Well-known objects
        self._absorption = None
        self._biconditional_elimination_left = None
        self._biconditional_elimination_right = None
        self._biconditional_introduction = None
        self._conjunction_elimination_left = None
        self._conjunction_elimination_right = None
        self._conjunction_introduction = None
        self._disjunction_elimination = None  # TODO: IMPLEMENT disjunction_elimination
        self._disjunction_introduction = None
        self._double_negation_elimination = None
        self._double_negation_introduction = None
        self._modus_ponens = None

    @property
    def absorb(self) -> InferenceRuleInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Unabridged property: u.i.absorption

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.absorption

    @property
    def absorption(self) -> InferenceRuleInclusion:
        """The well-known absorption inference-rule: (P ⟹ Q) ⊢ (P ⟹ (P ∧ Q)).

        Abridged property: u.i.absorb

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._absorption is None:
            self._absorption = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.absorption)
        return self._absorption

    @property
    def bel(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Unabridged property: u.i.biconditional_elimination_left

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_elimination_left

    @property
    def ber(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Unabridged property: u.i.biconditional_elimination_right

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_elimination_right

    @property
    def bi(self) -> InferenceRuleInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Unabridged property: u.i.biconditional_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.biconditional_introduction

    @property
    def biconditional_elimination_left(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (left) inference-rule: P ⟺ Q ⊢ P ⟹ Q.

        Abridged property: u.i.bel

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._biconditional_elimination_left is None:
            self._biconditional_elimination_left = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_elimination_left)
        return self._biconditional_elimination_left

    @property
    def biconditional_elimination_right(self) -> InferenceRuleInclusion:
        """The well-known biconditional-elimination (right) inference-rule: P ⟺ Q ⊢ Q ⟹ P.

        Abridged property: u.i.ber()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._biconditional_elimination_right is None:
            self._biconditional_elimination_right = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_elimination_right)
        return self._biconditional_elimination_right

    @property
    def biconditional_introduction(self) -> InferenceRuleInclusion:
        """The well-known biconditional-introduction inference-rule: : P ⟹ Q, Q ⟹ P ⊢ P ⟺ Q.

        Abridged property: u.i.bi

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._biconditional_introduction is None:
            self._biconditional_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.biconditional_introduction)
        return self._biconditional_introduction

    @property
    def conjunction_elimination_left(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Abridged property: t.i.cel()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._conjunction_elimination_left is None:
            self._conjunction_elimination_left = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_elimination_left)
        return self._conjunction_elimination_left

    @property
    def conjunction_elimination_right(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Abridged property: t.i.cer

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._conjunction_elimination_right is None:
            self._conjunction_elimination_right = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_elimination_right)
        return self._conjunction_elimination_right

    @property
    def conjunction_introduction(self) -> InferenceRuleInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Abridged property: t.i.ci()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._conjunction_introduction is None:
            self._conjunction_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.conjunction_introduction)
        return self._conjunction_introduction

    @property
    def cel(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (left) inference-rule: P ∧ Q ⊢ P.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_left()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_elimination_left

    @property
    def cer(self) -> InferenceRuleInclusion:
        """The well-known conjunction-elimination (right) inference-rule: P ∧ Q ⊢ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_elimination_right()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_elimination_right

    @property
    def ci(self) -> InferenceRuleInclusion:
        """The well-known conjunction-introduction inference-rule: P, Q ⊢ P ∧ Q.

        Unabridged property: universe_of_discourse.inference_rules.conjunction_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.conjunction_introduction

    @property
    def di(self) -> InferenceRuleInclusion:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Unabridged property: u.i.disjunction_introduction

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.disjunction_introduction

    @property
    def disjunction_introduction(self) -> InferenceRuleInclusion:
        """The well-known disjunction-introduction inference-rule: P ⊢ (P ∨ Q).

        Abridged property: u.i.di

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._disjunction_introduction is None:
            self._disjunction_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.disjunction_introduction)
        return self._disjunction_introduction

    @property
    def dne(self) -> InferenceRuleInclusion:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Original method: universe_of_discourse.inference_rules.double_negation_elimination()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.double_negation_elimination

    @property
    def dni(self) -> InferenceRuleInclusion:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Original method: universe_of_discourse.inference_rules.double_negation_introduction()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.double_negation_introduction

    @property
    def double_negation_elimination(self) -> InferenceRuleInclusion:
        """The well-known double-negation-elimination inference-rule: ¬¬P ⊢ P.

        Abridged property: t.i.dne()

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._double_negation_elimination is None:
            self._double_negation_elimination = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.double_negation_elimination)
        return self._double_negation_elimination

    @property
    def double_negation_introduction(self) -> InferenceRuleInclusion:
        """The well-known double-negation-introduction inference-rule: P ⊢ ¬¬P.

        Abridged property: t.i.dni

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._double_negation_introduction is None:
            self._double_negation_introduction = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.double_negation_introduction)
        return self._double_negation_introduction

    @property
    def modus_ponens(self) -> InferenceRuleInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Abridged property: u.i.mp

        The implication (P ⟹ Q) may contain free-variables. If such is the
        case, the resulting Q' is computed by extracting variable-values
        from P' and applying variable-substitution.


        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        if self._modus_ponens is None:
            self._modus_ponens = InferenceRuleInclusion(
                t=self.t,
                i=self.t.u.i.modus_ponens)
        return self._modus_ponens

    @property
    def mp(self) -> InferenceRuleInclusion:
        """The well-known modus-ponens inference-rule: (P ⟹ Q), P ⊢ Q.

        Unabridged property: u.i.modus_ponens

        If the well-known inference-rule does not exist in the universe-of-discourse,
        the inference-rule is automatically created.
        """
        return self.modus_ponens


class UniverseOfDiscourse(SymbolicObjct):
    def __init__(self, symbol: (None, str, Symbol) = None, dashed_name: (None, str, DashedName) = None,
                 echo: (None, bool) = None):
        echo = get_config(echo, configuration.echo_universe_of_discourse, configuration.echo_default,
                          fallback_value=False)
        self.axioms = dict()
        self.definitions = dict()
        self.formulae = dict()
        self._inference_rules = InferenceRuleDict(u=self)
        self._relations = RelationDict(u=self)
        self.theories = dict()
        self.simple_objcts = dict()
        self.symbolic_objcts = dict()
        self.theories = dict()
        self.variables = dict()
        # Unique name indexes
        self.symbol_indexes = dict()
        self.headers = dict()
        self.dashed_names = dict()
        # Well-known objects
        self._falsehood_simple_objct = None
        self._truth_simple_objct = None

        if symbol is None:
            base = '𝒰'
            index = index_universe_of_discourse_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = index_universe_of_discourse_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        if dashed_name is None:
            dashed_name = f'universe-of-discourse-{str(symbol.index)}'
        super().__init__(
            is_universe_of_discourse=True,
            is_theory_foundation_system=False,
            symbol=symbol,
            dashed_name=dashed_name,
            universe_of_discourse=None,
            echo=False)
        super()._declare_class_membership(classes.universe_of_discourse)
        if echo:
            self.echo()

    def axiom(
            self, natural_language, header=None, symbol=None, echo=None):
        """Elaborate a new axiom in this universe-of-discourse.

        :param natural_language:
        :param symbol:
        :param echo:
        :return:
        """
        return self.elaborate_axiom(natural_language=natural_language, header=header, symbol=symbol, echo=echo)

    @property
    def i(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self.inference_rules

    @property
    def inference_rules(self):
        """A python dictionary of inference-rules contained in this universe-of-discourse,
        where well-known inference-rules are directly available as properties."""
        return self._inference_rules

    @property
    def falsehood_simple_objct(self):
        """The falsehood simple-object if it exists in this universe-of-discourse,
        otherwise None."""
        return self._falsehood_simple_objct

    @falsehood_simple_objct.setter
    def falsehood_simple_objct(self, o):
        verify(
            self._falsehood_simple_objct is None,
            'The falsehood simple-objct exists already in this'
            'universe-of-discourse')
        self._falsehood_simple_objct = o

    @property
    def r(self):
        """A python dictionary of relations contained in this universe-of-discourse,
        where well-known relations are directly available as properties."""
        return self.relations

    @property
    def relations(self):
        """A python dictionary of relations contained in this universe-of-discourse,
        where well-known relations are directly available as properties."""
        return self._relations

    @property
    def truth_simple_objct(self):
        """The truth simple-objct if it exists in this universe-of-discourse,
        otherwise None."""
        return self._truth_simple_objct

    @truth_simple_objct.setter
    def truth_simple_objct(self, o):
        verify(
            self._truth_simple_objct is None,
            'The truth simple-objct exists already in this'
            'universe-of-discourse')
        self._truth_simple_objct = o

    def cross_reference_axiom(self, a: Axiom) -> bool:
        """Cross-references an axiom in this universe-of-discourse.

        :param a: an axiom.
        """
        verify(
            a.symbol not in self.axioms.keys() or a is self.axioms[a.symbol],
            'The symbol of parameter ⌜a⌝ is already referenced as a distinct axiom in this universe-of-discourse.',
            a=a,
            universe_of_discourse=self)
        if a not in self.axioms:
            self.axioms[a.symbol] = a
            return True
        else:
            return False

    def cross_reference_definition(self, d: Definition) -> bool:
        """Cross-references a definition in this universe-of-discourse.

        :param d: a definition.
        """
        verify(
            d.symbol not in self.definitions.keys() or d is self.definitions[d.symbol],
            'The symbol of parameter ⌜d⌝ is already referenced as a distinct definition in this universe-of-discourse.',
            a=d,
            universe_of_discourse=self)
        if d not in self.definitions:
            self.definitions[d.symbol] = d
            return True
        else:
            return False

    def cross_reference_formula(self, phi: Formula):
        """Cross-references a formula in this universe-of-discourse.

        :param phi: a formula.
        """
        verify(
            isinstance(phi, Formula),
            'Cross-referencing a formula in a universe-of-discourse requires '
            'an object of type Formula.')
        verify(
            phi.symbol not in self.formulae.keys() or phi is self.formulae[
                phi.symbol],
            'Cross-referencing a formula in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if phi not in self.formulae:
            self.formulae[phi.symbol] = phi

    def cross_reference_inference_rule(self, ir: InferenceRule) -> bool:
        """Cross-references an inference-rule in this universe-of-discourse.

        :param ir: an inference-rule.
        """
        verify(
            is_in_class(ir, classes.inference_rule),
            'Parameter ⌜ir⌝ is not an inference-rule.',
            ir=ir,
            universe_of_discourse=self)
        verify(
            ir.symbol not in self.inference_rules.keys() or ir is self.inference_rules[ir.symbol],
            'The symbol of parameter ⌜ir⌝ is already referenced as a distinct inference-rule in this universe-of-discourse.',
            ir=ir,
            universe_of_discourse=self)
        if ir not in self.inference_rules:
            self.inference_rules[ir.symbol] = ir
            return True
        else:
            return False

    def cross_reference_relation(self, r: Relation):
        """Cross-references a relation in this universe-of-discourse.

        :param r: a relation.
        """
        verify(
            isinstance(r, Relation),
            'Cross-referencing a relation in a universe-of-discourse requires '
            'an object of type Relation.')
        verify(
            r.symbol not in self.relations.keys() or r is self.relations[
                r.symbol],
            'Cross-referencing a relation in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if r not in self.relations:
            self.relations[r.symbol] = r

    def cross_reference_simple_objct(self, o: SimpleObjct):
        """Cross-references a simple-objct in this universe-of-discourse.

        :param o: a simple-objct.
        """
        verify(
            isinstance(o, SimpleObjct),
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'an object of type SimpleObjct.')
        verify(
            o.symbol not in self.simple_objcts.keys() or o is
            self.simple_objcts[
                o.symbol],
            'Cross-referencing a simple-objct in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if o not in self.simple_objcts:
            self.simple_objcts[o.symbol] = o

    def cross_reference_symbolic_objct(self, o: SymbolicObjct):
        """Cross-references a symbolic-objct in this universe-of-discourse.

        :param o: a symbolic-objct.
        """
        verify(
            isinstance(o, SymbolicObjct),
            'Cross-referencing a symbolic-objct in a universe-of-discourse requires '
            'an object of type SymbolicObjct.')
        verify(
            o.symbol not in self.symbolic_objcts.keys() or o is
            self.symbolic_objcts[
                o.symbol],
            'Cross-referencing a symbolic-objct in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if o not in self.symbolic_objcts:
            self.symbolic_objcts[o.symbol] = o
        if o.header is not None:
            # If the symbolic_objct has a header,
            # assure the unicity of this header in the universe-of-discourse.
            verify(o.header not in self.headers.keys(),
                   'The header of symbolic_objct o1 is already referenced by o2.',
                   o1=o)
            self.headers[o.header] = o
        if o.dashed_name is not None:
            # If the symbolic_objct has a dashed-name,
            # assure the unicity of this dashed-name in the universe-of-discourse.
            verify(o.dashed_name not in self.dashed_names.keys(),
                   'The dashed-name of symbolic-objct o1 is already referenced by o2.',
                   o1=o)
            self.dashed_names[o.header] = o

    def cross_reference_theory(self, t: TheoryElaboration):
        """Cross-references a theory in this universe-of-discourse.

        :param t: a formula.
        """
        verify(
            isinstance(t, TheoryElaboration),
            'Cross-referencing a theory in a universe-of-discourse requires '
            'an object of type Theory.')
        verify(
            t.symbol not in self.theories.keys() or t is self.theories[
                t.symbol],
            'Cross-referencing a theory in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if t not in self.theories:
            self.theories[t.symbol] = t

    def cross_reference_variable(self, x: FreeVariable):
        """Cross-references a free-variable in this universe-of-discourse.

        :param x: a formula.
        """
        verify(
            isinstance(x, FreeVariable),
            'Cross-referencing a free-variable in a universe-of-discourse requires '
            'an object of type FreeVariable.')
        verify(
            x.symbol not in self.variables.keys() or x is self.variables[
                x.symbol],
            'Cross-referencing a free-variable in a universe-of-discourse requires '
            'that it is referenced with a unique symbol.')
        if x not in self.variables:
            self.variables[x.symbol] = x

    def declare_formula(
            self, relation, *parameters, symbol=None, lock_variable_scope=None, echo=None):
        """Declare a new :term:`formula` in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, ...).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        phi = Formula(
            relation=relation, parameters=parameters,
            universe_of_discourse=self, symbol=symbol,
            lock_variable_scope=lock_variable_scope,
            echo=echo
        )
        return phi

    def declare_free_variable(self, symbol=None, echo=None):
        """Declare a free-variable in this universe-of-discourse.

        A shortcut function for FreeVariable(universe_of_discourse=u, ...)

        :param symbol:
        :return:
        """
        x = FreeVariable(
            universe_of_discourse=self, symbol=symbol,
            status=FreeVariable.scope_initialization_status, echo=echo)
        return x

    def declare_simple_objct(
            self, symbol: (None, str, Symbol) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Shortcut for SimpleObjct(theory=t, ...)"""
        return SimpleObjct(
            symbol=symbol, dashed_name=dashed_name,
            universe_of_discourse=self, echo=echo)

    def declare_symbolic_objct(
            self, symbol=None):
        """"""
        return SymbolicObjct(
            symbol=symbol,
            universe_of_discourse=self)

    def declare_theory(
            self,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            extended_theory: (None, TheoryElaboration) = None,
            extended_theory_limit: (None, Statement) = None,
            include_inconsistency_introduction_inference_rule=None,
            stabilized: bool = False,
            echo: bool = False):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for Theory(universe_of_discourse, ...).

        :param symbol:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return TheoryElaboration(
            u=self,
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            include_inconsistency_introduction_inference_rule=include_inconsistency_introduction_inference_rule,
            stabilized=stabilized,
            echo=echo)

    def include_falsehood_simple_objct(self):
        """Assure the existence of the falsehood simple-objct in this
        universe-of-discourse."""
        # Assure the existence of dependent theoretical-objcts.
        # N/A.
        # Assure the existence of falsehood.
        if self.falsehood_simple_objct is None:
            self.falsehood_simple_objct = self.o('⊥')

    def include_truth_simple_objct(self):
        """Assure the existence of the truth simple-objct in this
        universe-of-discourse."""
        # Assure the existence of dependent theoretical-objcts.
        # N/A.
        # Assure the existence of truth.
        if self.truth_simple_objct is None:
            self.truth_simple_objct = self.o('⊤')

    def postulate_axiom(
            self, natural_language, symbol=None, theory=None, reference=None,
            title=None, echo=None):
        """Postulate a new axiom in the designated theory."""
        verify(
            theory.universe_of_discourse is self,
            'The universe-of-discourse of the theory parameter is distinct '
            'from this universe-of-discourse.')
        return AxiomInclusion(
            natural_language=natural_language, symbol=symbol, t=theory,
            reference=reference, title=title, echo=echo)

    def elaborate_axiom(
            self, natural_language, header=None, symbol=None, echo=None):
        """Elaborate a new axiom 𝑎 in this universe-of-discourse."""
        return Axiom(
            u=self, natural_language=natural_language, header=header, symbol=symbol, echo=echo)

    def pose_definition(
            self,
            natural_language: str,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Pose a new definition in the current universe-of-discourse."""
        return Definition(
            natural_language=natural_language, u=self,
            symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def take_note(
            self, t, natural_language, symbol=None, reference=None,
            title=None, echo=None, category=None):
        """Take a note in theory 𝑡.

        Shortcut for Note(theory=t, ...)"""
        verify(
            t.universe_of_discourse is self,
            'This universe-of-discourse 𝑢₁ (self) is distinct from the universe-of-discourse 𝑢₂ of the theory '
            'parameter 𝑡.')
        return Note(theory=t, natural_language=natural_language, symbol=symbol,
                    reference=reference, title=title, category=category, echo=echo)

    def echo(self):
        return repm.prnt(self.repr_as_declaration())

    def f(
            self, relation, *parameters, symbol=None,
            lock_variable_scope=None):
        """Declare a new formula in this universe-of-discourse.

        Shortcut for self.elaborate_formula(...)."""
        return self.declare_formula(
            relation, *parameters, symbol=symbol,
            lock_variable_scope=lock_variable_scope)

    def get_symbol_max_index(self, base):
        """Return the highest index for that symbol-base in the universe-of-discourse."""
        if base in self.symbol_indexes.keys():
            return self.symbol_indexes[base]
        else:
            return 0

    def index_symbol(self, base):
        """Given a symbol-base S (i.e. an unindexed symbol), returns a unique integer n
        such that (S, n) is a unique identifier in this instance of UniverseOfDiscourse.

        :param base: The symbol-base.
        :return:
        """
        if base not in self.symbol_indexes:
            self.symbol_indexes[base] = 1
        else:
            self.symbol_indexes[base] += 1
        return self.symbol_indexes[base]

    def definition(
            self,
            natural_language: str,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Pose a new definition in the current universe-of-discourse.

        Shortcut for: u.pose_definition(...)"""
        return self.pose_definition(
            natural_language=natural_language,
            symbol=symbol, header=header, dashed_name=dashed_name, echo=echo)

    def o(
            self, symbol: (None, str, Symbol) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Declare a simple-objct in this universe-of-discourse.

        Shortcut for self.declare_simple_objct(universe_of_discourse=self, ...)"""
        return self.declare_simple_objct(
            symbol=symbol, dashed_name=dashed_name, echo=echo)

    def repr_as_declaration(self) -> str:
        return f'Let {self.repr_fully_qualified_name()} be a universe-of-discourse.'

    def so(self, symbol=None):
        return self.declare_symbolic_objct(
            symbol=symbol)

    def t(
            self,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            extended_theory: (None, TheoryElaboration) = None,
            extended_theory_limit: (None, Statement) = None,
            include_inconsistency_introduction_inference_rule=None,
            stabilized: bool = False,
            echo: bool = False):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for self.declare_theory(...).

        :param symbol:
        :param is_theory_foundation_system:
        :param extended_theory:
        :return:
        """
        return self.declare_theory(
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            extended_theory=extended_theory,
            extended_theory_limit=extended_theory_limit,
            include_inconsistency_introduction_inference_rule=include_inconsistency_introduction_inference_rule,
            stabilized=stabilized,
            echo=echo)

    # @FreeVariableContext()
    @contextlib.contextmanager
    def v(
            self, symbol=None, echo=None):
        """Declare a free-variable in this universe-of-discourse.

        This method is expected to be as in a with statement,
        it yields an instance of FreeVariable,
        and automatically lock the variable scope when the with left.
        Example:
            with u.v('x') as x, u.v('y') as y:
                # some code...

        To manage variable scope extensions and locking expressly,
        use declare_free_variable() instead.
        """
        # return self.declare_free_variable(symbol=symbol)
        x = FreeVariable(
            universe_of_discourse=self, symbol=symbol,
            status=FreeVariable.scope_initialization_status, echo=echo)
        yield x
        x.lock_scope()


class BiconditionalIntroductionStatement(FormulaStatement):
    """A statement inferred by the biconditional-introduction inference-rule.

    Requirements:
    -------------
    The biconditional relation.
    """

    def __init__(
            self, conditional_phi, conditional_psi, symbol=None, category=None,
            theory=None,
            reference=None, title=None, echo=None):
        category = statement_categories.proposition if category is None else category
        self.conditional_phi = conditional_phi
        self.conditional_psi = conditional_psi
        valid_proposition = BiconditionalIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, conditional_phi=conditional_phi,
            conditional_psi=conditional_psi)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol, echo=echo)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by biconditional introduction")}'
            output = output + f'\n\t{self.conditional_phi.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conditional_phi.repr_as_ref())}.'
            output = output + f'\n\t{self.conditional_psi.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conditional_psi.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class BiconditionalIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the biconditional-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, conditional_phi, conditional_psi, symbol=None, category=None,
            reference=None, title=None, echo=None):
        """Given two conditionals phi, and psi, infer a statement
        using the biconditional-introduction inference-rule."""
        return BiconditionalIntroductionStatement(
            conditional_phi=conditional_phi, conditional_psi=conditional_psi,
            symbol=symbol,
            category=category, theory=theory, reference=reference, title=title, echo=echo)

    @staticmethod
    def execute_algorithm(
            theory: TheoryElaboration, conditional_phi: FormulaStatement,
            conditional_psi: FormulaStatement):
        """Execute the biconditional algorithm."""
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(conditional_phi, FormulaStatement)
        assert isinstance(conditional_psi, FormulaStatement)
        verify(
            theory.contains_theoretical_objct(conditional_phi),
            'The conditional phi of the biconditional-introduction is not contained in the '
            'theory hierarchy.',
            conditional=conditional_phi, theory=theory)
        verify(
            theory.contains_theoretical_objct(conditional_psi),
            'The conditional psi of the biconditional-introduction is not contained in the '
            'theory hierarchy.',
            antecedent=conditional_psi, theory=theory)
        verify(
            isinstance(
                theory.universe_of_discourse.biconditional_relation, Relation),
            'The usage of the biconditional-introduction inference-rule in a theory requires the '
            'biconditional relation in that theory universe.')

        # Build the valid proposition
        # But, in order to do this, we must re-create new variables
        # with a new scope.
        # TODO: Move this variable re-creation procedure to a dedicated function
        variables_list = conditional_phi.get_variable_set().union(
            conditional_psi.get_variable_set())
        substitution_map = dict(
            (source_variable, theory.universe_of_discourse.v(
                source_variable.symbol.base)) for source_variable in
            variables_list)
        valid_proposition = theory.universe_of_discourse.f(
            theory.universe_of_discourse.biconditional_relation,
            conditional_phi.substitute(
                substitution_map=substitution_map, target_theory=theory),
            conditional_psi.substitute(
                substitution_map=substitution_map, target_theory=theory)
        )
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the introduction of the inteference rule with
        # a theory statement.


class ConjunctionIntroductionStatement(FormulaStatement):
    """

    Definition:
    -----------
    A conjunction-introduction is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P is true)
    given a proposition (Q is true)
    infers the proposition (P and Q)
    and infers the proposition not(P and Q) if either or both of P or Q is not true.

    Requirements:
    -------------
    The conjunction relation.
    """

    def __init__(
            self, conjunct_p, conjunct_q, symbol=None, category=None, theory=None,
            reference=None, title=None):
        category = statement_categories.proposition if category is None else category
        self.conjunct_p = conjunct_p
        self.conjunct_q = conjunct_q
        valid_proposition = ConjunctionIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, conjunct_p=conjunct_p, conjunct_q=conjunct_q)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by conjunction introduction")}'
            output = output + f'\n\t{self.conjunct_p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conjunct_p.repr_as_ref())}.'
            output = output + f'\n\t{self.conjunct_q.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conjunct_q.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class ConjunctionIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the conjunction-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, conjunct_p, conjunct_q, symbol=None, category=None,
            reference=None, title=None):
        """Given two conjuncts, infer a statement
        using the conjunction-introduction inference-rule."""
        return ConjunctionIntroductionStatement(
            conjunct_p=conjunct_p, conjunct_q=conjunct_q, symbol=symbol,
            category=category, theory=theory, reference=reference, title=title)

    @staticmethod
    def execute_algorithm(
            theory: TheoryElaboration, conjunct_p: FormulaStatement,
            conjunct_q: FormulaStatement):
        """Execute the conjunction algorithm."""
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(conjunct_p, FormulaStatement)
        assert isinstance(conjunct_q, FormulaStatement)
        verify(
            theory.contains_theoretical_objct(conjunct_p),
            'The conjunct P of the conjunction-introduction is not contained in the '
            'theory hierarchy.',
            conditional=conjunct_p, theory=theory)
        verify(
            theory.contains_theoretical_objct(conjunct_q),
            'The conjunct Q of the conjunction-introduction is not contained in the '
            'theory hierarchy.',
            antecedent=conjunct_q, theory=theory)
        verify(
            isinstance(
                theory.universe_of_discourse.conjunction_relation, Relation),
            'The usage of the conjunction-introduction inference-rule in a theory requires the '
            'conjunction relation in that theory universe.')

        # Build the valid proposition as p and q
        # But, in order to do this, we must re-create new variables
        # with a new scope.
        # TODO: Move this variable re-creation procedure to a dedicated function
        variables_list = conjunct_p.get_variable_set().union(
            conjunct_q.get_variable_set())
        substitution_map = dict(
            (source_variable, theory.universe_of_discourse.v(
                source_variable.symbol.base)) for source_variable in
            variables_list)
        valid_proposition = theory.universe_of_discourse.f(
            theory.universe_of_discourse.conjunction_relation,
            conjunct_p.substitute(
                substitution_map=substitution_map, target_theory=theory),
            conjunct_q.substitute(
                substitution_map=substitution_map, target_theory=theory)
        )
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the introduction of the inteference rule with
        # a theory statement.


class DoubleNegationIntroductionStatement(FormulaStatement):
    """The double-negation inference-rule: P ⟹ ¬¬P.

    Requirements:
    -------------
    - The negation-relation must exist in the universe-of-discourse.
    """

    def __init__(
            self, p, symbol=None, category=None, theory=None,
            reference=None, title=None):
        category = statement_categories.proposition if category is None else category
        self.p = p
        valid_proposition = DoubleNegationIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by double_negation introduction")}'
            output = output + f'\n\t{self.p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.p.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class DoubleNegationIntroductionStatement(FormulaStatement):
    """The double-negation inference-rule: P ⟹ ¬¬P.

    Requirements:
    -------------
    - The negation-relation must exist in the universe-of-discourse.
    """

    def __init__(
            self, p, symbol=None, category=None, theory=None,
            reference=None, title=None):
        category = statement_categories.proposition if category is None else category
        self.p = p
        valid_proposition = DoubleNegationIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by double_negation introduction")}'
            output = output + f'\n\t{self.p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.p.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class InferredProposition(FormulaStatement):
    """A proposition inferred from an inference-rule in the current theory-elaboration.
    """

    def __init__(
            self,
            *args,
            i: InferenceRule,
            t: TheoryElaboration,
            symbol: (None, str, Symbol) = None,
            header: (None, str, ObjctHeader) = None,
            dashed_name: (None, str, DashedName) = None,
            echo: (None, bool) = None):
        """Include (aka allow) an inference_rule in a theory-elaboration.
        """
        self._inference_rule = i
        verify(
            self._inference_rule.verify_args(*args, t=t),
            'Parameters ⌜*args⌝ are not compatible with inference-rule ⌜self⌝',
            args=args, slf=self, t=t)
        valid_proposition = self._inference_rule.infer_formula(*args, t=t)
        super().__init__(
            theory=t,
            valid_proposition=valid_proposition,
            category=statement_categories.proposition,
            symbol=symbol,
            header=header,
            dashed_name=dashed_name,
            echo=False)
        # t.crossreference_inferred_proposition(self)
        super()._declare_class_membership(declarative_class_list.inferred_proposition)
        if echo:
            repm.prnt(self.repr_as_statement())

    @property
    def inference_rule(self) -> InferenceRule:
        """Return the inference-rule upon which this inference-rule-inclusion is based.
        """
        return self._inference_rule

    def repr_as_statement(self, output_proofs=True) -> str:
        """Return a representation that expresses and justifies the statement."""
        text = f'Inferred Proposition {self.repr_as_title(cap=True)}: “{self.valid_proposition.repr_as_formula()}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


def apply_negation(phi: Formula):
    """Apply negation to a formula phi."""
    return phi.u.f(phi.u.r.lnot, phi.u.f(phi.u.r.lnot, phi))


def apply_double_negation(phi: Formula):
    """Apply double-negation to a formula phi."""
    return apply_negation(apply_negation(phi))


class DoubleNegationIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the double_negation-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, p, symbol=None, category=None,
            reference=None, title=None):
        """Given a proposition P, infer a statement
        using the double_negation-introduction inference-rule."""
        return DoubleNegationIntroductionStatement(
            p=p, symbol=symbol,
            category=category, theory=theory, reference=reference, title=title)

    @staticmethod
    def execute_algorithm(
            theory: TheoryElaboration, p: FormulaStatement):
        """Execute the double_negation algorithm."""
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(p, FormulaStatement)
        verify(
            theory.contains_theoretical_objct(p),
            'The proposition P of the double-negation-introduction is not contained in the '
            'theory hierarchy.',
            conditional=p, theory=theory)

        # Build the valid proposition as p and q
        # But, in order to do this, we must re-create new variables
        # with a new scope.
        # TODO: Move this variable re-creation procedure to a dedicated function
        variables_list = p.get_variable_set()
        substitution_map = dict(
            (source_variable, theory.universe_of_discourse.v(
                source_variable.symbol.base)) for source_variable in
            variables_list)
        valid_proposition = theory.universe_of_discourse.f(
            theory.universe_of_discourse.relations.negation,
            theory.universe_of_discourse.f(
                theory.universe_of_discourse.relations.negation,
                p.substitute(substitution_map=substitution_map, target_theory=theory)
            )
        )
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the introduction of the inteference rule with
        # a theory statement.


class ModusPonensStatement(FormulaStatement):
    """
    TODO: Make ModusPonens a subclass of InferenceRule.

    Definition:
    -----------
    A modus-ponens is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P implies Q)
    given a proposition (P is True)
    infers the proposition (Q is True)

    Requirements:
    -------------
    The parent theory must expose the implication attribute.
    """

    def __init__(
            self, conditional, antecedent, symbol=None, category=None, theory=None,
            reference=None, title=None):
        category = statement_categories.proposition if category is None else category
        self.conditional = conditional
        self.antecedent = antecedent
        valid_proposition = ModusPonensInferenceRuleOBSOLETE.execute_algorithm(
            t=theory, conditional=conditional, antecedent=antecedent)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof by modus ponens")}'
            output = output + f'\n\t{self.conditional.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.conditional.repr_as_ref())}.'
            output = output + f'\n\t{self.antecedent.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.antecedent.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class ModusPonensInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the modus-ponens inference-rule."""

    @staticmethod
    def infer(
            theory, conditional, antecedent, symbol=None, category=None,
            reference=None, title=None):
        """Given a conditional and an antecedent, infer a statement
        using the modus-ponens inference-rule."""
        return ModusPonensStatement(
            conditional=conditional, antecedent=antecedent, symbol=symbol,
            category=category, theory=theory, reference=reference, title=title)

    @staticmethod
    def execute_algorithm(
            t: TheoryElaboration,
            conditional: FormulaStatement,
            antecedent: FormulaStatement):
        """Execute the modus-ponens algorithm."""
        verify(
            t.contains_theoretical_objct(conditional),
            'The conditional of the modus-ponens is not contained in the '
            'theory hierarchy.',
            conditional=conditional, theory=t)
        verify(
            t.contains_theoretical_objct(antecedent),
            'The antecedent of the modus-ponens is not contained in the '
            'theory hierarchy.',
            antecedent=antecedent, theory=t)
        verify(
            isinstance(
                t.universe_of_discourse.r.implication,
                Relation),
            'The usage of the ModusPonens class in a theory requires the '
            'implication-relation in the universe-of-discourse.')
        verify(
            conditional.valid_proposition.relation is t.universe_of_discourse.r.implication,
            'The root relation of the conditional formula is not the implication-relation defined in this universe-of-discourse.')
        p_prime = conditional.valid_proposition.parameters[0]
        q_prime = conditional.valid_proposition.parameters[1]
        mask = p_prime.get_variable_set()
        # Check p consistency
        # If the p statement is present in the theory,
        # it necessarily mean that p is true,
        # because every statement in the theory is a valid proposition.
        assert isinstance(antecedent, FormulaStatement)
        similitude, _values = antecedent.valid_proposition._is_masked_formula_similar_to(
            o2=p_prime, mask=mask)
        assert antecedent.valid_proposition.is_masked_formula_similar_to(
            o2=p_prime, mask=mask)
        # Build q by variable substitution
        substitution_map = dict((v, k) for k, v in _values.items())
        valid_proposition = q_prime.substitute(
            substitution_map=substitution_map, target_theory=t)
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the inclusion of this inference-rule in the theory.


# class InferenceRules(repm.Representation):
#    def __init__(self, python_name: str, natural_language_name: str):
#        super().__init__(python_name=python_name, natural_language_name=natural_language_name)
#        self.conjunction_introduction = ConjunctionIntroductionInferenceRule
#        self.modus_ponens = ModusPonensInferenceRule
#
#
# inference_rules = InferenceRules('inference_rules', 'inference-rules')


class InconsistencyIntroductionStatement(FormulaStatement):
    """

    Requirements:
    -------------

    """

    def __init__(
            self, p, not_p, symbol=None, category=None, theory=None,
            reference=None, title=None):
        if title is None:
            title = 'THEORY INCONSISTENCY'
        category = statement_categories.proposition if category is None else category
        self.p = p
        self.not_p = not_p
        valid_proposition = InconsistencyIntroductionInferenceRuleOBSOLETE.execute_algorithm(
            theory=theory, p=p, not_p=not_p)
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            category=category, reference=reference, title=title,
            symbol=symbol)
        # The theory is proved inconsistent!
        theory.prove_inconsistent(self)
        if configuration.warn_on_inconsistency:
            warnings.warn(f'{self.repr_as_statement(output_proofs=True)}', InconsistencyWarning)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula()}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Proof of inconsistency")}'
            output = output + f'\n\t{self.p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.p.repr_as_ref())}.'
            output = output + f'\n\t{self.not_p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.not_p.repr_as_ref())}.'
            output = output + f'\n\t{"─" * 71}┤'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


class InconsistencyIntroductionInferenceRuleOBSOLETE(InferenceRuleOBSOLETE):
    """An implementation of the inconsistency-introduction inference-rule."""

    @staticmethod
    def infer(
            theory, p, not_p, symbol=None, category=None,
            reference=None, title=None):
        """"""
        return InconsistencyIntroductionStatement(
            p=p, not_p=not_p, symbol=symbol,
            category=category, theory=theory, reference=reference, title=title)

    @staticmethod
    def execute_algorithm(theory, p, not_p):
        """Execute the theory-inconsistency algorithm."""
        assert isinstance(theory, TheoryElaboration)
        assert isinstance(p, FormulaStatement)
        verify(
            theory.contains_theoretical_objct(p),
            'The p of the theory-inconsistency is not contained in the '
            'theory hierarchy.',
            conditional=p, theory=theory)
        verify(
            theory.contains_theoretical_objct(not_p),
            'The not-p of the theory-inconsistency is not contained in the '
            'theory hierarchy.',
            antecedent=not_p, theory=theory)
        verify(not_p.valid_proposition.relation is theory.universe_of_discourse.relations.negation,
               'The relation of not_p is not the negation relation.')
        not_p_prime = theory.universe_of_discourse.f(
            theory.universe_of_discourse.relations.negation, p.valid_proposition)
        verify(not_p_prime.is_formula_equivalent_to(not_p.valid_proposition), 'not_p is not formula-equialent to ¬(P).',
               p=p, not_p=not_p, not_p_prime=not_p_prime)
        # Build q by variable substitution
        valid_proposition = theory.universe_of_discourse.f(
            theory.universe_of_discourse.relations.inconsistent, theory)
        return valid_proposition

    @staticmethod
    def initialize(theory):
        a1 = theory.a()
        # TODO: Justify the inclusion of this inference-rule in the theory.


# foundation_theory = None
# ft = None
# commutativity_of_equality = None
## implies = None
# equality = None
# tru = None
# fls = None
# has_truth_value = None

pass
