import textwrap
from types import SimpleNamespace
import repm
import contextlib
import abc


class Configuration:
    def __init__(self):
        self.raise_exception_on_verification_failure = True
        self.text_output_indent = 2
        self.text_output_statement_column_width = 70
        self.text_output_justification_column_width = 40
        self.text_output_total_width = 122
        self.output_index_if_max_index_equal_1 = False


configuration = Configuration()


class AtheoreticalStatement:
    """
    Definition
    ----------
    A theoretical-statement 𝒮 is a tuple (𝒯, n, …) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * … is any number of decorative attributes informally related to 𝒮 for human explanatory purposes
    """

    def __init__(self, theory, position, symbol=None):
        assert isinstance(theory, Theory)
        assert isinstance(position, int) and position > 0
        self.theory = theory
        self.position = position
        super().__init__()


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


def verify(assertion, msg, **kwargs):
    if not assertion:
        contextual_information = ''
        for key, value in kwargs.items():
            value_as_string = f'(str conversion failure of type {str(type(value))})'
            try:
                value_as_string = str(value)
            finally:
                pass
            contextual_information += f'\n{key}: {value_as_string}'
        report = f'{msg}\nContextual information:{contextual_information}'
        repm.prnt(report)
        if configuration.raise_exception_on_verification_failure:
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
    """A specialized string-like object to represent things in formulae.

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

    def repr(self, hide_index=False):
        if hide_index:
            return f'{self.base}'
        else:
            return f'{self.base}{repm.subscriptify(self.index)}'


class StatementTitle:
    """A specialized string-like object to represent statement titles.

    """

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

    def repr_full(self, cap=False):
        return repm.serif_bold(
            f'{self.category.natural_name.capitalize() if cap else self.category.natural_name} {self.reference}{" - " + self.title if self.title is not None else ""}')

    def repr_ref(self, cap=False):
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
        self, symbol,
        is_theory_foundation_system=None,
        is_universe_of_discourse=None,
        universe_of_discourse=None):
        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        # By design, every symbolic-objct is a component of a theory,
        # unless it is itself a theory-foundation-system,
        # or it is itself a universe-of-discourse.
        assert is_universe_of_discourse or isinstance(
            universe_of_discourse, UniverseOfDiscourse)
        verify(
            isinstance(symbol, Symbol),
            'The symbol of a symbolic-objct must be of type Symbol.')
        self.symbol = symbol
        self.is_theory_foundation_system = is_theory_foundation_system
        self.is_universe_of_discourse = is_universe_of_discourse
        if not self.is_universe_of_discourse:
            self.universe_of_discourse = universe_of_discourse
            self.universe_of_discourse.cross_reference_symbolic_objct(o=self)
        else:
            self.universe_of_discourse = None

    def __hash__(self):
        # Symbols are unique within their universe-of-discourse,
        # thus hashing can be safely based on the key: U + symbol.
        # With a special case for the universe-of-discourse itself,
        # where hash of the symbol is sufficient.
        return hash(self.symbol) if self.is_universe_of_discourse else hash(
            (self.universe_of_discourse, self.symbol))

    def __repr__(self):
        return self.repr_as_symbol()

    def __str__(self):
        return self.repr_as_symbol()

    def is_symbol_equivalent(self, o2):
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

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be a symbolic-objct denoted as ⌜ {self.repr_as_symbol()} ⌝.'

    def repr_as_symbol(self):
        global configuration
        hide_index = \
            self.symbol.index == 1 and not configuration.output_index_if_max_index_equal_1 and self.universe_of_discourse.get_symbol_max_index(
                self.symbol.base) == 1
        return self.symbol.repr(hide_index=hide_index)

    def repr(self, expanded=None):
        return self.repr_as_symbol()


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
        self, symbol,
        is_theory_foundation_system=None, universe_of_discourse=None):
        # pseudo-class properties. these must be overwritten by
        # the parent constructor after calling __init__().
        # the rationale is that checking python types fails
        # miserably (e.g. because of context managers),
        # thus, implementing explicit functional-types will prove
        # more robust and allow for duck typing.
        self.is_formula = False
        self.is_free_variable = False
        self.is_relation = False
        self.is_simple_objct = False
        self.is_statement = False
        self.is_theoretical_objct = True
        super().__init__(
            symbol=symbol,
            is_theory_foundation_system=is_theory_foundation_system,
            universe_of_discourse=universe_of_discourse)

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

    def is_masked_formula_similar_to(self, o2, mask=None):
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

    def _is_masked_formula_similar_to(self, o2, mask=None, _values=None):
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
        mask = set() if mask is None else mask
        _values = dict() if _values is None else _values
        assert isinstance(o2, TheoreticalObjct)
        assert isinstance(mask, set)
        assert isinstance(_values, dict)
        for x in mask:
            assert isinstance(x, FreeVariable)
        if self is o2:
            # Trivial case.
            return True, _values
        if self.is_formula_equivalent_to(o2):
            # Sufficient condition.
            return True, _values
        if isinstance(self, Formula) and isinstance(o2, Formula):
            # When both o1 and o2 are formula,
            # verify that their components are masked-formula-similar.
            relation_output, _values = self.relation._is_masked_formula_similar_to(
                o2=o2.relation, mask=mask, _values=_values)
            if not relation_output:
                return False, _values
            # Arities are necessarily equal.
            for i in range(len(self.parameters)):
                parameter_output, _values = self.parameters[
                    i]._is_masked_formula_similar_to(
                    o2=o2.parameters[i], mask=mask, _values=_values)
                if not parameter_output:
                    return False, _values
            return True, _values
        if self not in mask and o2 not in mask:
            # We know o1 and o2 are not formula-equivalent,
            # and we know they are not in the mask.
            return False, _values
        if self in mask:
            variable = o2
            newly_observed_value = self
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(
                    already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if o2 in mask:
            variable = self
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
        universe_of_discourse=None, status=None, scope=None):
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
            universe_of_discourse=universe_of_discourse)
        self.universe_of_discourse.cross_reference_variable(x=self)
        self.is_free_variable = True

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
        self, relation, parameters, symbol=None,
        universe_of_discourse=None, lock_variable_scope=None):
        """

        :param theory:
        :param relation:
        :param parameters:
        :param symbol:
        :param arity: Mandatory if relation is a FreeVariable.
        """
        lock_variable_scope = False if lock_variable_scope is None else lock_variable_scope
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        # self.formula_index = theory.crossreference_formula(self)
        if symbol is None:
            symbol_base = '𝜑'
            symbol = Symbol(
                base=symbol_base, index=universe_of_discourse.index_symbol(
                    base=symbol_base))
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse)
        self.is_formula = True
        verify(
            relation.is_relation or relation.is_free_variable,
            'The relation of this formula is neither a relation, nor a '
            'free_variable.',
            formula=self, relation=relation)
        verify(
            relation.universe_of_discourse is self.universe_of_discourse,
            'The universe_of_discourse of the relation of this formula is '
            'distint from the formula unierse_of_disourse.',
            formula=self, relation=relation)
        self.relation = relation
        universe_of_discourse.cross_reference_formula(self)
        parameters = parameters if isinstance(parameters, tuple) else tuple(
            [parameters])
        assert len(parameters) > 0
        arity = len(parameters)
        if isinstance(relation, Relation):
            assert self.relation.arity == arity
        self.arity = arity
        self.parameters = parameters
        self.cross_reference_variables()
        for p in parameters:
            verify(
                p.is_theoretical_objct,
                'This formula parameter is not a theoretical-objct.',
                formula=self, p=p)
            if p.is_free_variable:
                p.extend_scope(self)
        if lock_variable_scope:
            self.lock_variable_scope()

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

    @property
    def is_proposition(self):
        """Tell if the formula is a logic-proposition.

        This property is directly inherited from the formula-is-proposition
        attribute of the formula's relation."""
        return self.relation.signal_proposition

    def is_formula_equivalent_to(self, o2):
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
        if self is o2:
            # Trivial case.
            return True
        assert isinstance(o2, TheoreticalObjct)
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

    def repr_as_formula(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
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


class RelationDeclarationFormula(Formula):
    def __init__(self, theory, relation, symbol):
        assert isinstance(theory, Theory)
        assert isinstance(relation, Relation)
        assert theory.has_objct_in_hierarchy(relation)
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
        assert isinstance(theory, Theory)
        assert isinstance(simple_objct, SimpleObjct)
        assert theory.has_objct_in_hierarchy(simple_objct)
        relation = theoretical_relations.simple_objct_declaration
        super().__init__(
            theory=theory, relation=relation, parameters=(theory, simple_objct),
            python=python,
            dashed=dashed, symbol=symbol)


class StatementCategory(repm.Representation):
    def __init__(self, python_name, symbol_base, natural_name):
        self.symbol_base = symbol_base
        self.natural_name = natural_name
        super().__init__(python_name=python_name)


class StatementCategories(repm.Representation):
    corollary = StatementCategory('corollary', '𝙿', 'corollary')
    formal_definition = StatementCategory(
        'formal_definition', '𝙳', 'formal definition')
    lemma = StatementCategory('lemma', '𝙿', 'lemma')
    natural_language_axiom = StatementCategory(
        'natural_language_axiom', '𝙳', 'natural language axiom')
    natural_language_definition = StatementCategory(
        'natural language definition', '𝙳', 'natural language definition')
    proposition = StatementCategory('proposition', '𝙿', 'proposition')
    theorem = StatementCategory('theorem', '𝙿', 'theorem')


statement_categories = StatementCategories('statement_categories')


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
        self, theory, category, symbol=None,
        reference=None, title=None):
        assert isinstance(theory, Theory)
        universe_of_discourse = theory.universe_of_discourse
        self.statement_index = theory.crossreference_statement(self)
        self.theory = theory
        self.category = category
        self.title = StatementTitle(
            category=category, reference=reference, title=title)
        if symbol is None:
            symbol = Symbol(
                base=self.category.symbol_base, index=self.statement_index)
        super().__init__(
            symbol=symbol,
            universe_of_discourse=universe_of_discourse)

    def repr_as_title(self, cap=False):
        return self.title.repr_full(cap=cap)

    def repr_as_ref(self, cap=False):
        return self.title.repr_ref(cap=cap)


class Axiom(Statement):
    """The NaturalLanguageAxiom pythonic class is a model of the natural-language-axiom formal class.

    Definition:
    -----------
    An natural-language-axiom is a theory-statement that expresses an axiom in natural-language.

    """

    def __init__(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        assert isinstance(theory, Theory)
        assert isinstance(natural_language, str)
        self.natural_language = natural_language
        theory.crossreference_axiom(self)
        super().__init__(
            theory=theory, symbol=symbol, reference=reference,
            category=statement_categories.natural_language_axiom, title=title)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.repr_as_title(cap=True)}: “{self.natural_language}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class Definition(Statement):
    """The NaturalLanguageDefinition pythonic class is a model of the natural-language-definition formal class.

    Definition:
    -----------
    A natural-language-definition is a theory-statement that expresses a definition in natural-language.

    Definition:
    -----------
    A definition is a conservative-extension of a theory, i.e. it may be convenient to prove theorems
    but per se it does not prove new theorems. In this regard, it is distinct from an axiom.

    """

    def __init__(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        assert isinstance(theory, Theory)
        assert isinstance(natural_language, str)
        self.natural_language = natural_language
        theory.crossreference_definition(self)
        super().__init__(
            theory=theory, symbol=symbol, reference=reference,
            category=statement_categories.natural_language_definition,
            title=title)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement."""
        text = f'{self.repr_as_symbol()}: “{self.natural_language}”'
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
        self, theory, valid_proposition, symbol=None, category=None,
        reference=None,
        title=None):
        verify(
            isinstance(theory, Theory),
            'isinstance(theory, Theory)')
        verify(
            isinstance(valid_proposition, Formula),
            'isinstance(valid_proposition, Formula)')
        verify(
            theory.universe_of_discourse is valid_proposition.universe_of_discourse,
            'theory.universe_of_discourse is '
            'valid_proposition.universe_of_discourse')
        universe_of_discourse = theory.universe_of_discourse
        # Theory statements must be logical propositions.
        verify(
            valid_proposition.is_proposition,
            'valid_proposition.is_proposition')
        self.valid_proposition = valid_proposition
        # TODO: Implement distinct counters per category
        self.statement_index = theory.crossreference_statement(self)
        category = statement_categories.proposition if category is None else category
        super().__init__(
            theory=theory, symbol=symbol, category=category,
            reference=reference, title=title)
        # manage theoretical-morphisms
        self.morphism_output = None
        if self.valid_proposition.relation.signal_theoretical_morphism:
            # this formula-statement is a theoretical-morphism.
            # it follows that this statement "yields" new statements in the theory.
            assert self.valid_proposition.relation.implementation is not None
            self.morphism_output = Morphism(
                theory=theory, source_statement=self)

    def __repr__(self):
        return self.repr(expanded=True)

    def __str__(self):
        return self.repr(expanded=True)

    def repr(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        if expanded:
            return self.repr_as_formula(expanded=expanded)
        else:
            return super().repr(expanded=expanded)

    def repr_as_formula(self, expanded=None):
        return self.valid_proposition.repr_as_formula(expanded=expanded)


class DirectAxiomInference(FormulaStatement):
    """

    Definition:
    -----------
    A direct-axiom-inference is a valid-proposition directly inferred from a free-text-axiom.

    """

    def __init__(
        self, valid_proposition, a, symbol=None, theory=None, reference=None,
        title=None, category=None):
        assert isinstance(theory, Theory)
        assert isinstance(a, Axiom)
        assert theory.has_objct_in_hierarchy(a)
        assert isinstance(valid_proposition, Formula)
        self.natural_language_axiom = a
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            symbol=symbol, category=category,
            reference=reference, title=title)
        assert a.statement_index < self.statement_index

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language axiom")}'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {self.natural_language_axiom.repr_as_ref()}.'
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
        assert isinstance(theory, Theory)
        assert isinstance(source_statement, FormulaStatement)
        assert theory.has_objct_in_hierarchy(source_statement)
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
        assert isinstance(theory, Theory)
        assert isinstance(position, int) and position > 0
        assert isinstance(phi, Formula)
        assert theory.has_objct_in_hierarchy(phi)
        assert isinstance(proof, Proof)
        assert theory.has_objct_in_hierarchy(proof)
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
        self, valid_proposition, d, symbol=None, theory=None, reference=None,
        title=None):
        assert isinstance(theory, Theory)
        assert isinstance(d, Definition)
        assert theory.has_objct_in_hierarchy(d)
        assert isinstance(valid_proposition, Formula)
        verify(
            valid_proposition.universe_of_discourse is theory.universe_of_discourse,
            'The UoD of a formal-definition valid-proposition must be '
            'consistent with the UoD of its theory.')
        assert valid_proposition.relation is theory.equality
        self.natural_language_definition = d
        super().__init__(
            theory=theory, valid_proposition=valid_proposition,
            symbol=symbol, category=statement_categories.formal_definition,
            reference=reference, title=title)
        assert d.statement_index < self.statement_index

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{self.repr_as_title(cap=True)}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        if output_proofs:
            output = output + f'\n\t{repm.serif_bold("Derivation from natural language definition")}'
            output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.natural_language_definition.repr_as_symbol())}.'
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


class InferenceRule:
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


class Note(AtheoreticalStatement):
    prefix = 'note'

    def __init__(self, natural_language, symbol=None, theory=None):
        assert isinstance(theory, Theory)
        assert isinstance(natural_language, str)
        self.natural_language = natural_language
        self.note_index = theory.crossreference_note(self)
        if symbol is None:
            # We must cross-reference this statement
            # in advance from Statement.__init__
            # to retrieve its index.
            statement_index = theory.crossreference_statement(self)
            symbol = f'{Note.prefix} {statement_index + 1}'
        else:
            if len(symbol) < len(Note.prefix) or \
                symbol[:len(Note.prefix)] != Note.prefix:
                symbol = f'{Note.prefix} {symbol}'
        assert isinstance(symbol, str)
        super().__init__(
            theory=theory, symbol=symbol)

    def repr_as_statement(self, output_proofs=True):
        """Return a representation that expresses and justifies the statement."""
        text = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: “{self.natural_language}”'
        return '\n'.join(
            textwrap.wrap(
                text=text, width=70,
                subsequent_indent=f'\t',
                break_on_hyphens=False,
                expand_tabs=True,
                tabsize=4))


class Theory(TheoreticalObjct):
    def __init__(
        self, is_theory_foundation_system=None,
        symbol=None, extended_theories=None,
        universe_of_discourse=None, theory_foundation_system=None,
        include_conjunction_introduction_inference_rule: bool = False
    ):
        """

        :param theory: :param is_foundation_system: True if this theory is
        the foundation-system, False otherwise. :param symbol:
         :param extended_theories: :param is_an_element_of_itself:
        """
        # self.symbols = dict()
        self.axioms = tuple()
        self.natural_language_definitions = tuple()
        self.statements = tuple()
        self._theory_foundation_system = theory_foundation_system
        extended_theories = set() if extended_theories is None else extended_theories
        if isinstance(extended_theories, Theory):
            # A shortcut to pass a single extended theory without casting a set.
            extended_theories = {extended_theories}
        assert isinstance(extended_theories, set)
        if theory_foundation_system is not None and \
            theory_foundation_system not in extended_theories:
            extended_theories = extended_theories.union(
                {theory_foundation_system})
        for extended_theory in extended_theories:
            assert isinstance(extended_theory, Theory)
        self.extended_theories = extended_theories
        self._commutativity_of_equality = None
        self._conjunction = None
        self._equality = None
        self._implication = None
        self._negation = None
        self._inequality = None

        is_theory_foundation_system = False if is_theory_foundation_system is None else is_theory_foundation_system
        # if is_theory_foundation_system:
        #    assert theory is None
        #    # theory = self
        # if theory is None:
        # If the parent theory is not specified, we make the assumption
        # that the parent theory is the universe-of-discourse.
        # theory = universe_of_discourse
        # Force the initialization of the theory attribute,
        # because theory.get_symbolic_object_1_index()
        # must be called before super().
        # self.theory = theory
        # assert is_theory_foundation_system or isinstance(theory, Theory)
        if symbol is None:
            base = '𝒯'
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
            is_theory_foundation_system=is_theory_foundation_system,
            universe_of_discourse=universe_of_discourse)
        # Inference Rules
        include_conjunction_introduction_inference_rule = False if \
            include_conjunction_introduction_inference_rule is None else \
            include_conjunction_introduction_inference_rule
        self._includes_conjunction_introduction_inference_rule = False
        if include_conjunction_introduction_inference_rule:
            self.include_conjunction_introduction_inference_rule()
        self._modus_ponens_inference_rule = None

    @property
    def commutativity_of_equality(self):
        """Commutativity-of-equality is a fundamental theory property that enables
        support for SoET. None if the property is not equipped on
        the theory. An instance of FormalAxiom otherwise."""
        if self._commutativity_of_equality is not None:
            return self._commutativity_of_equality
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system.commutativity_of_equality
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
    def conjunction(self):
        """Conjunction is a fundamental theory property.
        None if the property is not equipped on the theory.
        An instance of Relation otherwise."""
        if self._conjunction is not None:
            return self._conjunction
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system._conjunction
        else:
            return None

    @conjunction.setter
    def conjunction(self, r):
        verify(
            self._conjunction is None,
            'A theory conjunction property can only be set once '
            'to prevent inconsistency.')
        self._conjunction = r

    @property
    def conjunction_introduction_inference_rule(self):
        """Some theories may contain the conjunction-introduction inference-rule.

        This property may only be set once to assure the stability of the
        theory."""
        if self._conjunction_introduction_inference_rule is not None:
            return self._conjunction_introduction_inference_rule
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system._conjunction_introduction_inference_rule
        else:
            return None

    @conjunction_introduction_inference_rule.setter
    def conjunction_introduction_inference_rule(self, ir: InferenceRule):
        verify(
            self._conjunction_introduction_inference_rule is None,
            'The conjunction-introduction inference-rule property of a theory can only be '
            'set once to prevent instability.')
        self._conjunction_introduction_inference_rule = ir

    def crossreference_axiom(self, a):
        """During construction, cross-reference an axiom 𝒜
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.axioms."""
        assert isinstance(a, Axiom)
        a.theory = a.theory if hasattr(a, 'theory') else self
        assert a.theory is self
        if a not in self.axioms:
            self.axioms = self.axioms + tuple(
                [a])
        return self.axioms.index(a)

    def crossreference_definition(self, d):
        """During construction, cross-reference a definition 𝒟
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.axioms."""
        assert isinstance(d, Definition)
        d.theory = d.theory if hasattr(d, 'theory') else self
        assert d.theory is self
        if d not in self.natural_language_definitions:
            self.natural_language_definitions = self.natural_language_definitions + tuple(
                [d])
        return self.natural_language_definitions.index(d)

    def crossreference_statement(self, s):
        """During construction, cross-reference a statement 𝒮
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.statements."""
        assert isinstance(s, Statement)
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
        self, valid_proposition, a, symbol=None, reference=None, title=None):
        """Elaborate a new direct-axiom-inference in the theory. Shortcut for FormalAxiom(theory=t, ...)"""
        return DirectAxiomInference(
            valid_proposition=valid_proposition, a=a, symbol=symbol,
            theory=self, reference=reference, title=title)

    def elaborate_direct_definition_inference(
        self, valid_proposition=None, d=None, symbol=None, reference=None,
        title=None):
        """Elaborate a formal-definition in this theory.

        Shortcut for FormalDefinition(theory=t, ...)"""
        return DirectDefinitionInference(
            valid_proposition=valid_proposition, d=d, symbol=symbol,
            theory=self, reference=reference, title=title)

    def infer_by_conjunction_introduction(
        self, conjunct_p, conjunct_q, symbol=None, category=None,
        reference=None, title=None):
        """Apply the conjunction-introduction inference-rule to infer a new statement.

        :param conjunct_p:
        :param conjunct_q:
        :param symbol:
        :param category:
        :param reference:
        :param title:
        :return:
        """
        if not self.includes_conjunction_introduction_inference_rule:
            raise UnsupportedInferenceRuleException(
                'The conjunction-introduction inference-rule is not contained '
                'in this theory.',
                theory=self, conjunct_p=conjunct_p, conjunct_q=conjunct_q)
        else:
            return self.conjunction_introduction_inference_rule.infer(
                theory=self, conjunct_p=conjunct_p, conjunct_q=conjunct_q,
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
    def modus_ponens_inference_rule(self):
        """Some theories may contain the modus-ponens inference-rule.

        This property may only be set once to assure the stability of the
        theory."""
        if self._modus_ponens_inference_rule is not None:
            return self._modus_ponens_inference_rule
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system._modus_ponens_inference_rule
        else:
            return None

    @modus_ponens_inference_rule.setter
    def modus_ponens_inference_rule(self, ir: InferenceRule):
        verify(
            self._modus_ponens_inference_rule is None,
            'The modus-ponens inference-rule property of a theory can only be '
            'set once to prevent instability.')
        self._modus_ponens_inference_rule = ir

    def postulate_axiom(
        self, natural_language, symbol=None, reference=None, title=None):
        """Postulate an axiom expressed in natural-language as the basis of this theory."""
        return self.universe_of_discourse.postulate_axiom(
            natural_language=natural_language, symbol=symbol, theory=self,
            reference=reference, title=title)

    def elaborate_natural_language_definition(
        self, natural_language, symbol=None, reference=None, title=None):
        """Shortcut for NaturalLanguageDefinition(theory=t, ...)"""
        return self.universe_of_discourse.elaborate_natural_language_definition(
            natural_language=natural_language, symbol=symbol, theory=self,
            reference=reference, title=title)

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

    @property
    def equality(self):
        """(None, Relation) Equality is a fundamental theory property that enables
        support for SoET. None if the property is not equipped on
        the theory. An instance of Relation otherwise."""
        if self._equality is not None:
            return self._equality
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system.equality
        else:
            return None

    @equality.setter
    def equality(self, r):
        verify(
            self._equality is None,
            'A theory equality property can only be set once to prevent '
            'inconsistency.')
        verify(
            isinstance(r, Relation),
            'The equality property must be a relation.')
        self._equality = r

    def dai(
        self, valid_proposition, a, symbol=None, reference=None, title=None):
        """Elaborate a new direct-axiom-inference in the theory. Shortcut for
        Theory.elaborate_direct_axiom_inference(...)."""
        return self.elaborate_direct_axiom_inference(
            valid_proposition=valid_proposition, a=a, symbol=symbol,
            reference=reference, title=title)

    def ddi(
        self, valid_proposition=None, d=None, symbol=None, reference=None,
        title=None):
        """Elaborate a formal-definition in this theory.

        Shortcut for FormalDefinition(theory=t, ...)"""
        return self.elaborate_direct_definition_inference(
            valid_proposition=valid_proposition, d=d, symbol=symbol,
            reference=reference, title=title)

    def get_theory_extension(self):
        """Return the set of all theories that includes this theory and all the
        theories it extends recursively."""
        return self._get_theory_extension(theory_extension={self})

    def _get_theory_extension(self, theory_extension):
        for t in self.extended_theories:
            if t not in theory_extension:
                theory_extension = theory_extension.union({t})
                # TODO: Optimize this code by adding a private function and pass the current list to it.
                theory_extension = theory_extension.union(
                    t._get_theory_extension(theory_extension))
        return theory_extension

    def has_objct_in_hierarchy(self, o):
        """Return True if o is in this theory's hierarchy, False otherwise."""
        verify(o is not None, 'Object o is None', theory=self, o=o)
        verify(
            hasattr(o, 'is_theoretical_objct'),
            'Object o does not have the is_theoretical_objct attribute.',
            theory=self, o=o)
        verify(
            o.is_theoretical_objct, 'Object o is not a theoretical_objct.',
            theory=self, o=o)
        return o.theory in self.get_theory_extension()

    @property
    def implication(self):
        """The implication-property is a fundamental property that enables
        support for modus-ponens. None if the implication-property is not equipped on
        the theory. An instance of Relation otherwise."""
        if self._implication is not None:
            return self._implication
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system.implication
        else:
            return None

    @implication.setter
    def implication(self, r):
        verify(
            self._implication is None,
            'A theory implication property can only be set once to prevent '
            'inconsistency.')
        verify(
            isinstance(r, Relation),
            'The implication property must be a relation.')
        self._implication = r

    def include_conjunction_introduction_inference_rule(self):
        """Include the conjunction-introduction inference-rule in this
        theory."""
        verify(
            not self.includes_conjunction_introduction_inference_rule,
            'The conjunction-introduction inference-rule is already included in this theory.')
        # TODO: Justify the inclusion of the inference-rule in the theory
        #   with adequate statements (axioms?).
        # TODO: Move the inclusion of the conjunction relation to the universe,
        #   in an include_conjunction_relation() method on UniverseOfDiscourse.
        self.conjunction = self.universe_of_discourse.r(
            2, '∧', Formula.infix_operator_representation,
            signal_proposition=True)
        self._includes_conjunction_introduction_inference_rule = True

    @property
    def includes_conjunction_introduction_inference_rule(self):
        """True if the conjunction-introduction inference-rule is included in this theory, False otherwise."""
        if self._includes_conjunction_introduction_inference_rule is not None:
            return self._includes_conjunction_introduction_inference_rule
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system.includes_conjunction_introduction_inference_rule
        else:
            return None

    @property
    def inequality(self):
        """(None, Relation) Inequality is a fundamental theory property.
        None if the property is not equipped on the theory.
        An instance of Relation otherwise."""
        if self._inequality is not None:
            return self._inequality
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system._inequality
        else:
            return None

    @inequality.setter
    def inequality(self, r):
        verify(
            self._inequality is None,
            'A theory inequality property can only be set once to prevent '
            'inconsistency.')
        verify(
            isinstance(r, Relation),
            'The inequality property must be a relation.')
        self._inequality = r

    def mp(
        self, conditional, antecedent, symbol=None, category=None,
        reference=None, title=None):
        """Elaborate a new modus-ponens statement in the theory. Shortcut for
        ModusPonens(theory=t, ...)"""
        return self.infer_by_modus_ponens(
            conditional=conditional, antecedent=antecedent, symbol=symbol,
            category=category, reference=reference, title=title)

    @property
    def negation(self):
        """(None, Relation) Inequality is a fundamental theory property.
        None if the property is not equipped on the theory.
        An instance of Relation otherwise."""
        if self._negation is not None:
            return self._negation
        elif self._theory_foundation_system is not None:
            return self._theory_foundation_system._negation
        else:
            return None

    @negation.setter
    def negation(self, r):
        verify(
            self._negation is None,
            'A theory negation property can only be set once to prevent '
            'inconsistency.')
        verify(
            isinstance(r, Relation),
            'The negation property must be a relation.')
        self._negation = r

    def a(self, natural_language, symbol=None, reference=None, title=None):
        """Elaborate a new natural-language-axiom statement. Shortcut function for
        Theory.elaborate_natural_language_axiom(...)."""
        return self.postulate_axiom(
            natural_language=natural_language, symbol=symbol,
            reference=reference, title=title)

    def d(self, natural_language, symbol=None, reference=None, title=None):
        """Elaborate a new natural-language-definition statement. Shortcut function for
        Theory.elaborate_natural_language_definition(...)."""
        return self.elaborate_natural_language_definition(
            natural_language=natural_language, symbol=symbol,
            reference=reference, title=title)

    def repr_as_theory(self, output_proofs=True):
        """Return a representation that expresses and justifies the theory."""
        output = f'\n{repm.serif_bold(self.repr_as_symbol())}'
        output = output + f'\n{repm.serif_bold("Extended theories:")}'
        output = output + f'\nThe following theories are extended by {repm.serif_bold(self.repr_as_symbol())}.'
        output = output + ''.join(
            '\n\t ⁃ ' + t.repr_as_symbol() for t in self.extended_theories)
        output = output + f'\n\n{repm.serif_bold("Simple-objct declarations:")}'
        # TODO: Limit the listed objects to those that are referenced by the theory,
        #   instead of outputting all objects in the universe-of-discourse.
        output = output + '\n' + '\n'.join(
            o.repr_as_declaration() for o in
            self.universe_of_discourse.simple_objcts.values())
        output = output + f'\n\n{repm.serif_bold("Relation declarations:")}'
        output = output + '\n' + '\n'.join(
            r.repr_as_declaration() for r in
            self.universe_of_discourse.relations.values())
        output = output + f'\n\n{repm.serif_bold("Theory elaboration:")}'
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
        repm.prnt(self.repr_as_theory(output_proofs=output_proofs))

    def export_to_text(self, file_path, output_proofs=True):
        """Export this theory to a Unicode textfile."""
        text_file = open(file_path, 'w', encoding='utf-8')
        n = text_file.write(self.repr_as_theory(output_proofs=output_proofs))
        text_file.close()


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
        self, arity, symbol=None, formula_rep=None,
        signal_proposition=None, signal_theoretical_morphism=None,
        implementation=None, universe_of_discourse=None):
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
            universe_of_discourse=universe_of_discourse, symbol=symbol)
        self.is_relation = True
        self.universe_of_discourse.cross_reference_relation(r=self)

    # def repr(self, expanded=None):
    #    return self.repr_as_symbol()

    def repr_as_declaration(self):
        output = f'Let {self.repr_as_symbol()} be a {self.repr_arity_as_text()} relation denoted as ⌜ {self.repr_as_symbol()} ⌝'
        output = output + f', that signals well-formed formulae in {self.formula_rep} syntax (e.g.: ⌜ {self.formula_rep.sample.replace("◆", str(self.repr_as_symbol()))} ⌝).'
        return output

    def repr_arity_as_text(self):
        match self.arity:
            case 1:
                return 'unary'
            case 2:
                return 'binary'
            case 3:
                return 'ternary'
            case _:
                return f'{self.arity}-ary'


class SimpleObjct(TheoreticalObjct):
    """
    Definition
    ----------
    A simple-objct-component ℴ is a theoretical-object that has no special attribute,
    and whose sole function is to provide the meaning of being itself.
    """

    def __init__(
        self, symbol=None,
        universe_of_discourse=None):
        assert isinstance(universe_of_discourse, UniverseOfDiscourse)
        # self.simple_objct_index = theory.crossreference_simple_objct(self)
        if symbol is None:
            base = 'ℴ'
            index = universe_of_discourse.index_symbol(base=base)
            symbol = Symbol(base=base, index=index)
        elif isinstance(symbol, str):
            # If symbol was passed as a string,
            # assume the base was passed without index.
            # TODO: Analyse the string if it ends with index in subscript characters.
            index = universe_of_discourse.index_symbol(base=symbol)
            symbol = Symbol(base=symbol, index=index)
        super().__init__(
            universe_of_discourse=universe_of_discourse, symbol=symbol)
        self.universe_of_discourse.cross_reference_simple_objct(o=self)

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

    def repr_as_declaration(self, **kwargs):
        return f'Let {self.repr_as_symbol()} be a simple-objct denoted as ⌜ {self.repr_as_symbol()} ⌝.'


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
        assert isinstance(theory, Theory)
        assert isinstance(original_expression, FormulaStatement)
        assert theory.has_objct_in_hierarchy(original_expression)
        assert isinstance(equality_statement, FormulaStatement)
        assert theory.has_objct_in_hierarchy(equality_statement)
        assert equality_statement.valid_proposition.relation is theory.equality
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


class UniverseOfDiscourse(SymbolicObjct):
    def __init__(self, symbol=None):
        self.formulae = dict()
        self.relations = dict()
        self.theories = dict()
        self.simple_objcts = dict()
        self.symbol_indexes = dict()
        self.symbolic_objcts = dict()
        self.theories = dict()
        self.variables = dict()

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

        super().__init__(
            is_universe_of_discourse=True,
            is_theory_foundation_system=False,
            symbol=symbol,
            universe_of_discourse=None)

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

    def cross_reference_theory(self, t: Theory):
        """Cross-references a theory in this universe-of-discourse.

        :param t: a formula.
        """
        verify(
            isinstance(t, Theory),
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
        self, relation, *parameters, symbol=None, lock_variable_scope=None):
        """Declare a new :term:`formula` in this universe-of-discourse.

        This method is a shortcut for Formula(universe_of_discourse=self, ...).

        A formula is *declared* in a theory, and not *stated*, because it is not a statement,
        i.e. it is not necessarily true in this theory.
        """
        phi = Formula(
            relation=relation, parameters=parameters,
            universe_of_discourse=self, symbol=symbol,
            lock_variable_scope=lock_variable_scope
        )
        return phi

    def declare_free_variable(self, symbol=None):
        """Declare a free-variable in this universe-of-discourse.

        A shortcut function for FreeVariable(universe_of_discourse=u, ...)

        :param symbol:
        :return:
        """
        x = FreeVariable(
            universe_of_discourse=self, symbol=symbol,
            status=FreeVariable.scope_initialization_status)
        return x

    def declare_relation(
        self, arity, symbol=None, formula_rep=None,
        signal_proposition=None,
        signal_theoretical_morphism=None,
        implementation=None):
        """A shortcut function for Relation(theory=t, ...)

        A relation is **declared** in a theory because it is not a statement.
        """
        return Relation(
            arity=arity, symbol=symbol, formula_rep=formula_rep,
            signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation,
            universe_of_discourse=self)

    def declare_simple_objct(
        self, symbol=None):
        """Shortcut for SimpleObjct(theory=t, ...)"""
        return SimpleObjct(
            symbol=symbol,
            universe_of_discourse=self)

    def declare_symbolic_objct(
        self, symbol=None):
        """"""
        return SymbolicObjct(
            symbol=symbol,
            universe_of_discourse=self)

    def declare_theory(
        self, symbol=None, is_theory_foundation_system=None,
        extended_theories=None,
        theory_foundation_system=None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for Theory(universe_of_discourse, ...).

        :param symbol:
        :param is_theory_foundation_system:
        :param extended_theories:
        :return:
        """
        return Theory(
            symbol=symbol,
            extended_theories=extended_theories,
            is_theory_foundation_system=is_theory_foundation_system,
            universe_of_discourse=self,
            theory_foundation_system=theory_foundation_system)

    def postulate_axiom(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        """Postulate a new axiom in the designated theory."""
        verify(
            theory.universe_of_discourse is self,
            'The universe-of-discourse of the theory parameter is distinct '
            'from this universe-of-discourse.')
        return Axiom(
            natural_language=natural_language, symbol=symbol, theory=theory,
            reference=reference, title=title)

    def elaborate_natural_language_definition(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        """Shortcut for NaturalLanguageAxiom(theory=t, ...)"""
        verify(
            theory.universe_of_discourse is self,
            'The universe-of-discourse of the theory parameter is distinct from this universe-of-discourse.')
        return Definition(
            natural_language=natural_language, symbol=symbol, theory=theory,
            reference=reference, title=title)

    def f(
        self, relation, *parameters, symbol=None,
        lock_variable_scope=None):
        """Declare a new formula in this instance of UniverseOfDiscourse.

        Shortcut for self.elaborate_formula(...)."""
        return self.declare_formula(
            relation, *parameters, symbol=symbol,
            lock_variable_scope=lock_variable_scope)

    def get_symbol_max_index(self, base):
        """Return the highest index for that symbol-base in the universe-of-discourse."""
        return self.symbol_indexes[base]

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

    def a(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        return self.postulate_axiom(
            natural_language=natural_language, symbol=symbol, theory=theory,
            reference=reference, title=title)

    def d(
        self, natural_language, symbol=None, theory=None, reference=None,
        title=None):
        return self.elaborate_natural_language_definition(
            natural_language=natural_language, symbol=symbol, theory=theory,
            reference=reference, title=title)

    def o(
        self, symbol=None):
        """Declare a simple-objct in this universe-of-discourse.

        Shortcut for self.declare_simple_objct(universe_of_discourse=self, ...)"""
        return self.declare_simple_objct(
            symbol=symbol)

    def r(
        self, arity, symbol=None, formula_rep=None,
        signal_proposition=None,
        signal_theoretical_morphism=None,
        implementation=None):
        """Declare a new relation in this universe-of-discourse.

        Shortcut for Theory.declare_relation(...)."""
        return self.declare_relation(
            arity=arity, symbol=symbol, formula_rep=formula_rep,
            signal_proposition=signal_proposition,
            signal_theoretical_morphism=signal_theoretical_morphism,
            implementation=implementation)

    def so(self, symbol=None):
        return self.declare_symbolic_objct(
            symbol=symbol)

    def t(
        self, symbol=None, is_theory_foundation_system=None,
        extended_theories=None,
        theory_foundation_system=None):
        """Declare a new theory in this universe-of-discourse.

        Shortcut for self.declare_theory(...).

        :param symbol:
        :param is_theory_foundation_system:
        :param extended_theories:
        :return:
        """
        return self.declare_theory(
            symbol=symbol,
            is_theory_foundation_system=is_theory_foundation_system,
            extended_theories=extended_theories,
            theory_foundation_system=theory_foundation_system)

    # @FreeVariableContext()
    @contextlib.contextmanager
    def v(
        self, symbol=None):
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
            status=FreeVariable.scope_initialization_status)
        yield x
        x.lock_scope()


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
        valid_proposition = ConjunctionIntroductionInferenceRule.execute_algorithm(
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


class ConjunctionIntroductionInferenceRule(InferenceRule):
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
        theory: Theory, conjunct_p: FormulaStatement,
        conjunct_q: FormulaStatement):
        """Execute the conjunction algorithm."""
        assert isinstance(theory, Theory)
        assert isinstance(conjunct_p, FormulaStatement)
        assert isinstance(conjunct_q, FormulaStatement)
        verify(
            theory.has_objct_in_hierarchy(conjunct_p),
            'The conjunct P of the conjunction-introduction is not contained in the '
            'theory hierarchy.',
            conditional=conjunct_p, theory=theory)
        verify(
            theory.has_objct_in_hierarchy(conjunct_q),
            'The conjunct Q of the conjunction-introduction is not contained in the '
            'theory hierarchy.',
            antecedent=conjunct_q, theory=theory)
        verify(
            isinstance(theory.conjunction, Relation),
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
            theory.conjunction,
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


# universe_of_discourse = Theory(
#    theory=None, is_theory_foundation_system=True,
#    symbol='universe-of-discourse',
#    )
# u = universe_of_discourse

# meta_theory = Theory(
#    theory=universe_of_discourse, symbol='meta-theory')

# console = rich.console.Console()


foundation_theory = None
ft = None
commutativity_of_equality = None
# implies = None
equality = None
tru = None
fls = None
negation = None
has_truth_value = None

pass
