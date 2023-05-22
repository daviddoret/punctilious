import textwrap
from types import SimpleNamespace
import repm

configuration = SimpleNamespace(
    text_output_indent=2,
    text_output_statement_column_width=70,
    text_output_justification_column_width=40,
    text_output_total_width=122
)


class Tuple(tuple):
    """Tuple subclasses the native tuple class.
    The resulting supports setattr, getattr, hasattr,
    which are convenient to create friendly programmatic shortcuts."""
    pass


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


class SymbolicObjct:
    """
    Definition
    ----------
    A symbolic-objct is a python object instance that is assigned symbolic names,
    that is linked to a theory, but that is not necessarily constitutive of the theory.
    """

    def __init__(self, theory, symbol, capitalizable=False):
        assert theory is not None and isinstance(theory, Theory)
        assert isinstance(symbol, str) and len(symbol) > 0
        assert isinstance(capitalizable, bool)
        self.theory = theory
        self.symbol = symbol
        self.capitalizable = capitalizable
        self.theory.crossreference_symbolic_objct(s=self)

    def __hash__(self):
        # Symbols are unique within their theories,
        # thus hashing can be safely based on the key: theory + symbol.
        # With a special case for the root theory (universe-of-discourse),
        # where the theory is its own circular theory,
        # and hash of the symbol is sufficient.
        return hash(self.symbol) if self is self.theory else hash((self.theory, self.symbol))

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
        if self is universe_of_discourse and o2 is universe_of_discourse:
            # A universe-of-discourse is a root theory,
            # this condition avoids an infinite loop
            # while testing 1-equivalence in the next condition.
            return True
        if not self.theory.is_symbol_equivalent(o2.theory):
            return False
        if self.symbol != o2.symbol:
            return False
        return True

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be a symbolic-objct denoted as ⌜ {self.repr_as_symbol()} ⌝.'

    def repr_as_symbol(self, capitalized=False):
        return self.symbol.capitalize() if (capitalized and self.capitalizable) else self.symbol

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

    def __init__(self, theory, symbol, capitalizable):
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

    def get_variable_set(self):
        """Return the set of variables contained in o (self), including o itself.

        This function recursively traverse formula components (relation + parameters)
        to compile the set of variables contained in o."""
        return self._get_variable_set()

    def _get_variable_set(self, _variable_set=None):
        _variable_set = set() if _variable_set is None else _variable_set
        if isinstance(self, Formula):
            _variable_set = _variable_set.union(self.relation._get_variable_set(_variable_set=_variable_set))
            for p in self.parameters:
                _variable_set = _variable_set.union(p._get_variable_set(_variable_set=_variable_set))
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
                parameter_output, _values = self.parameters[i]._is_masked_formula_similar_to(
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
                if not newly_observed_value.is_formula_equivalent_to(already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        if o2 in mask:
            variable = self
            newly_observed_value = o2
            if variable in _values:
                already_observed_value = _values[variable]
                if not newly_observed_value.is_formula_equivalent_to(already_observed_value):
                    return False, _values
            else:
                _values[variable] = newly_observed_value
        return True, _values

    def substitute(self, substitution_map):
        """Given a theoretical-objct o₁ (self),
        and a substitution map 𝐌,
        return a theoretical-objct o₂
        where all components, including o₂ itself,
        have been substituted if present in 𝐌.

        Note
        ----
        The result of substitution depends on the order
        of traversal of o₁. The substitution() method
        uses the canonical-traversal-method which is:
        top-down, depth-first, relation-before-parameters.

        Parameters
        ----------
        substitution_map : dict
            A dictionary of theoretical-objct pairs (o, o'),
            where o is the original theoretical-objct in o₁,
            and o' is the substitute theoretical-objct in o₂.

        """
        substitution_map = dict() if substitution_map is None else substitution_map
        assert isinstance(substitution_map, dict)
        for key, value in substitution_map.items():
            assert isinstance(key, TheoreticalObjct)
            assert isinstance(value, TheoreticalObjct)
            # A relation could not be replaced by a simple-objct, etc.
            # to prevent the creation of an ill-formed theoretical-objct.
            assert type(key) == type(value) or isinstance(value, FreeVariable) or isinstance(key, FreeVariable)
            # If these are formula, their arity must be equal
            # to prevent the creation of an ill-formed formula.
            assert not isinstance(key, Formula) or key.arity == value.arity
        if self in substitution_map:
            return substitution_map[self]
        elif isinstance(self, Formula):
            # A formula is a special case that must be decomposed into its components.
            relation = self.relation.substitute(substitution_map=substitution_map)
            parameters = tuple(p.substitute(substitution_map=substitution_map) for p in self.parameters)
            return Formula(theory=self.theory, relation=relation, parameters=parameters)
        else:
            return self


class FreeVariable(TheoreticalObjct):
    """


    Defining properties:
    --------------------
    The defining-properties of a free-variable are:
     * Being a free-variable
     * The scope-formula of the free-variable
     * The index-position of the free-variable in its scope-formula
    """

    def __init__(self, theory, symbol=None):
        assert isinstance(theory, Theory)
        self.variable_index = theory.crossreference_variable(self)
        symbol = f'𝐱{repm.subscriptify(self.variable_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=False)

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
    """

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

    function_call_representation = repm.Representation(name='function-call', sample='◆(𝐱₁, 𝐱₂ ,… ,𝐱ₙ)')
    infix_operator_representation = repm.Representation(name='infix-operator', sample='𝐱₁ ◆ 𝐱₂')
    prefix_operator_representation = repm.Representation(name='prefix-operator', sample='◆𝐱')
    postfix_operator_representation = repm.Representation(name='postfix-operator', sample='𝐱◆')

    def __init__(self, theory, relation, parameters, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        self.formula_index = theory.crossreference_formula(self)
        capitalizable = False if symbol is None else capitalizable
        symbol = f'𝜑{repm.subscriptify(self.formula_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)
        assert relation is not None and isinstance(relation, (Relation, FreeVariable))
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple([parameters])
        assert len(parameters) > 0
        # TODO: The following verification shed light on a difficulty: if
        #   we substitute relations, the resulting formula has variable-relations,
        #   but variable-relations do not have an arity attribute...
        assert isinstance(relation, FreeVariable) or len(parameters) == relation.arity
        self.parameters = parameters
        self.cross_reference_variables()

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

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
        return self.relation.formula_is_proposition

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
            if not self.parameters[i].is_formula_equivalent_to(o2.parameters[i]):
                return False
        return True

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
        return f'{self.relation.symbol}({", ".join([p.repr(expanded=expanded) for p in self.parameters])})'

    def repr_as_infix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        assert self.relation.arity == 2
        return f'({self.parameters[0].repr(expanded=expanded)} {self.relation.symbol} {self.parameters[1].repr(expanded=expanded)})'

    def repr_as_postfix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        assert self.relation.arity == 1
        return f'({self.parameters[0].repr(expanded=expanded)}){self.relation.symbol}'

    def repr_as_prefix_operator(self, expanded=None):
        expanded = True if expanded is None else expanded
        assert isinstance(expanded, bool)
        assert self.relation.arity == 1
        return f'{self.relation.symbol}({self.parameters[0].repr(expanded=expanded)})'

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
        assert theory is not None, isinstance(theory, Theory)
        assert relation is not None, isinstance(relation, Relation)
        formula_relation = theoretical_relations.relation_declaration
        super().__init__(theory=theory, relation=formula_relation, parameters=(theory, relation), python=python,
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

    def __init__(self, theory, simple_objct, python=None, dashed=None, symbol=None):
        assert theory is not None and isinstance(theory, Theory)
        assert simple_objct is not None, isinstance(simple_objct, SimpleObjct)
        relation = theoretical_relations.simple_objct_declaration
        super().__init__(theory=theory, relation=relation, parameters=(theory, simple_objct), python=python,
                         dashed=dashed, symbol=symbol)


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

    reps = SimpleNamespace(
        proposition=repm.Representation('proposition'),
        corollary=repm.Representation('corollary'),
        lemma=repm.Representation('lemma'),
        theorem=repm.Representation('theorem')
    )

    def __init__(self, theory, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        self.statement_index = theory.crossreference_statement(self)
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)


class FreeTextAxiom(Statement):
    """

    Definition:
    -----------
    An free-text-axiom is a theory-statement that expresses an axiom in free textual form.

    """

    def __init__(self, theory, axiom_text, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        assert isinstance(axiom_text, str)
        self.axiom_text = axiom_text
        capitalizable = True if symbol is None else capitalizable
        assert isinstance(capitalizable, bool)
        self.axiom_index = theory.crossreference_axiom(self)
        symbol = f'axiom-{self.axiom_index + 1}' if symbol is None else symbol
        assert isinstance(symbol, str)
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement."""
        return f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.axiom_text}'


class FreeTextDefinition(Statement):
    """

    Definition:
    -----------
    A definition is a free-text theory-statement that introduces some new context in
     the theory but does not extend the theory. To be formalized, it must be
     formalized as definition-formal.

    """

    def __init__(self, theory, text, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        assert isinstance(text, str)
        self.text = text
        capitalizable = True if symbol is None else capitalizable
        assert isinstance(capitalizable, bool)
        self.definition_index = theory.crossreference_definition(self)
        symbol = f'definition-{self.definition_index + 1}' if symbol is None else symbol
        assert isinstance(symbol, str)
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement."""
        text = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.text}'
        return '\n'.join(textwrap.wrap(text=text, width=70,
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

    def __init__(self, theory, valid_proposition, category=None):
        assert isinstance(theory, Theory)
        assert isinstance(valid_proposition, Formula)
        # Theory statements must be logical propositions.
        assert valid_proposition.is_proposition
        self.valid_proposition = valid_proposition
        # TODO: Implement distinct counters per category
        self.statement_index = theory.crossreference_statement(self)
        category = Statement.reps.proposition if category is None else category
        capitalizable = True
        symbol = f'{category}-{self.statement_index + 1}'
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

    def repr_as_formula(self, expanded=None):
        return self.valid_proposition.repr_as_formula(expanded=expanded)


class FormalAxiom(FormulaStatement):
    """

    Definition:
    -----------
    A formal-axiom is a valid-proposition directly inferred from a free-text-axiom.

    """

    def __init__(self, theory, axiom, valid_proposition, category=None):
        assert isinstance(theory, Theory)
        assert isinstance(axiom, FreeTextAxiom)
        assert isinstance(valid_proposition, Formula)
        self.axiom = axiom
        super().__init__(theory=theory, valid_proposition=valid_proposition, category=category)
        assert axiom.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        output = output + f'\n\t{repm.serif_bold("Proof by direct axiom inference")}'
        output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.axiom.repr_as_symbol())}.'
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
        assert phi is not None and isinstance(phi, Formula)
        assert isinstance(proof, Proof)
        self.theory = theory
        self.position = position
        self.phi = phi
        self.proof = proof


class FormalDefinition(FormulaStatement):
    """

    Definition:
    A theoretical-statement that states that x = some other theoretical-object.
    When an object is defined like this, it means that for every formula
    where x is present, the same formula with the substitution of x by x' can be substituted in all theories.
    TODO: QUESTION: Should we create a base "Alias" object that is distinct from simple-objct???
    XXXXXXX
    """
    def __init__(self, theory, free_text_definition, valid_proposition, category=None):
        assert isinstance(theory, Theory)
        assert isinstance(free_text_definition, FreeTextDefinition)
        assert isinstance(valid_proposition, Formula)
        assert theory.has_objct_in_hierarchy(valid_proposition)
        self.free_text_definition = free_text_definition
        super().__init__(theory=theory, valid_proposition=valid_proposition, category=category)
        assert free_text_definition.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.valid_proposition.repr_as_formula(expanded=True)}'
        output = output + f'\n\t{repm.serif_bold("Proof by direct definition inference")}'
        output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.free_text_definition.repr_as_symbol())}.'
        return output


class AtheoreticalStatement:
    """
    Definition
    ----------
    A theoretical-statement 𝒮 is a tuple (𝒯, n, …) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * … is any number of decorative attributes informally related to 𝒮 for human explanatory purposes
    """

    def __init__(self, theory, position):
        assert isinstance(theory, Theory)
        assert isinstance(position, int) and position > 0
        self.theory = theory
        self.position = position


class Note(AtheoreticalStatement):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text


class Theory(TheoreticalObjct):
    def __init__(
            self, theory=None, is_universe_of_discourse=None,
            symbol=None, capitalizable=False, extended_theories=None):
        global universe_of_discourse
        self.symbols = dict()
        self.axioms = tuple()
        self.definitions = tuple()
        self.formulae = tuple()
        self.relations = Tuple()
        self.simple_objcts = Tuple()
        self.statements = tuple()
        self.symbolic_objcts = dict()
        self.theories = tuple()
        self.variables = tuple()
        extended_theories = set() if extended_theories is None else extended_theories
        assert isinstance(extended_theories, set)
        for extended_theory in extended_theories:
            assert isinstance(extended_theory, Theory)
        self.extended_theories = extended_theories
        is_universe_of_discourse = False if is_universe_of_discourse is None else is_universe_of_discourse
        if is_universe_of_discourse:
            assert theory is None
            theory = self
        if theory is None:
            # If the parent theory is not specified,
            # we make the assumption that the parent theory is the universe-of-discourse.
            theory = universe_of_discourse
            # Force the initialization of the theory attribute,
            # because theory.get_symbolic_object_1_index()
            # must be called before super().
            self.theory = theory
        assert theory is not None and isinstance(theory, Theory)
        assert theory is not None and isinstance(theory, Theory)
        assert isinstance(theory, Theory)
        self.theory_index = theory.crossreference_theory(self)
        capitalizable = True if symbol is None else capitalizable
        symbol = f'theory-{self.theory_index + 1}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

    def crossreference_symbolic_objct(self, s):
        """During construction, cross-reference a symbolic_objct 𝓈
        with its parent theory if it is not already cross-referenced,
        assuring symbol uniqueness."""
        assert isinstance(s, SymbolicObjct)
        s.theory = s.theory if hasattr(s, 'theory') else self
        assert s.theory is self
        if s.symbol in self.symbolic_objcts:
            # Within a theory, every symbol must be unique.
            assert s is self.symbolic_objcts[s.symbol]
        else:
            self.symbolic_objcts[s.symbol] = s

    def crossreference_axiom(self, a):
        """During construction, cross-reference an axiom 𝒜
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.axioms."""
        assert isinstance(a, FreeTextAxiom)
        a.theory = a.theory if hasattr(a, 'theory') else self
        assert a.theory is self
        if a not in self.axioms:
            self.axioms = self.axioms + tuple([a])
        return self.axioms.index(a)

    def crossreference_definition(self, d):
        """During construction, cross-reference a definition 𝒟
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.axioms."""
        assert isinstance(d, FreeTextDefinition)
        d.theory = d.theory if hasattr(d, 'theory') else self
        assert d.theory is self
        if d not in self.definitions:
            self.definitions = self.definitions + tuple([d])
        return self.definitions.index(d)

    def crossreference_formula(self, phi):
        """During construction, cross-reference a formula phi
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.formulae."""
        assert isinstance(phi, Formula)
        phi.theory = phi.theory if hasattr(phi, 'theory') else self
        assert phi.theory is self
        if phi not in self.formulae:
            self.formulae = self.formulae + tuple([phi])
        return self.formulae.index(phi)

    def crossreference_simple_objct(self, o):
        """During construction, cross-reference a simple-objct ℴ
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.simple_objcts."""
        assert isinstance(o, SimpleObjct)
        o.theory = o.theory if hasattr(o, 'theory') else self
        assert o.theory is self
        if o not in self.simple_objcts:
            self.simple_objcts = Tuple(self.simple_objcts + tuple([o]))
            # The new Tuple instance does not hold the attributes
            # of its predecessor. We must thus reset all attributes.
            # TODO: Implement Tuple.append to improe this.
            for o in self.simple_objcts:
                if o.python_name is not None:
                    set_attr(self.simple_objcts, o.python_name, o)
        return self.simple_objcts.index(o)

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

    def crossreference_theory(self, t):
        """During construction, cross-reference a theory 𝒯
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.theories."""
        assert isinstance(t, Theory)
        t.theory = t.theory if hasattr(t, 'theory') else self
        assert t.theory is self
        if t not in self.theories:
            self.theories = self.theories + tuple([t])
        return self.theories.index(t)

    def crossreference_relation(self, r):
        """During construction, cross-reference a relation r
        with its parent theory if it is not already cross-referenced,
        and return the 0-based index of the formula in Theory.relations."""
        assert isinstance(r, Relation)
        r.theory = r.theory if hasattr(r, 'theory') else self
        assert r.theory is self
        # The new Tuple instance does not hold the attributes
        # of its predecessor. We must thus reset all attributes.
        # TODO: Implement Tuple.append to improe this.
        if r not in self.relations:
            self.relations = Tuple(self.relations + tuple([r]))
            for r in self.relations:
                if r.python_name is not None:
                    set_attr(self.relations, r.python_name, r)
        return self.relations.index(r)

    def crossreference_variable(self, x):
        """During construction, cross-reference a variable x
        with its parent theory if it is not already cross-referenced,
        and return its 0-based index in Theory.variables."""
        assert isinstance(x, FreeVariable)
        x.theory = x.theory if hasattr(x, 'theory') else self
        assert x.theory is self
        if x not in self.variables:
            self.variables = self.variables + tuple([x])
        return self.variables.index(x)

    def get_theory_extension(self):
        """Return the set of all theories that includes this theory and all the theories it extends recursively."""
        theory_extension = {self}
        for t in self.extended_theories:
            if t not in theory_extension:
                theory_extension = theory_extension.union(t.get_theory_extension())
        return theory_extension

    def has_objct_in_hierarchy(self, o):
        """Return True if o is in this theory's hierarchy, False otherwise."""
        assert isinstance(o, TheoreticalObjct)
        return o.theory in self.get_theory_extension()

    def repr_as_theory(self):
        """Return a representation that expresses and justifies the theory."""
        output = f'\n{repm.serif_bold(self.repr_as_symbol(capitalized=True))}'
        output = output + f'\n{repm.serif_bold("Extended theories:")}'
        output = output + f'\nThe following theories are extended by {repm.serif_bold(self.repr_as_symbol())}.'
        output = output + ''.join('\n\t ⁃ ' + t.repr_as_symbol() for t in self.extended_theories)
        output = output + f'\n\n{repm.serif_bold("Simple-objct declarations:")}'
        output = output + '\n' + '\n'.join(o.repr_as_declaration() for o in self.simple_objcts)
        output = output + f'\n\n{repm.serif_bold("Relation declarations:")}'
        output = output + '\n' + '\n'.join(r.repr_as_declaration() for r in self.relations)
        output = output + f'\n\n{repm.serif_bold("Theory elaboration:")}'
        output = output + '\n\n' + '\n\n'.join(s.repr_as_statement() for s in self.statements)
        return output

    def prnt(self):
        repm.prnt(self.repr_as_theory())


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
    formula_is_proposition : bool
        True if formula based on this relation are logical-propositions,
        i.e. the relation is a function whose domain is the set of truth values {True, False}.
        False otherwise.
        When True, the formula may be used as a theory-statement.
    """

    def __init__(self, theory, arity, formula_rep=None, symbol=None, capitalizable=False, python_name=None,
                 formula_is_proposition=False):
        assert isinstance(theory, Theory)
        assert isinstance(formula_is_proposition, bool)
        self.formula_rep = Formula.function_call_representation if formula_rep is None else formula_rep
        self.python_name = python_name
        self.formula_is_proposition = formula_is_proposition
        capitalizable = False if symbol is None else capitalizable
        self.relation_index = theory.crossreference_relation(self)
        symbol = f'◆{repm.subscriptify(self.relation_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity

    def repr_as_declaration(self):
        output = f'Let {self.repr_as_symbol()} be a {self.repr_arity_as_text()} relation denoted as ⌜ {self.repr_as_symbol()} ⌝'
        output = output + f', that signals well-formed formulae in {self.formula_rep} syntax (e.g.: ⌜ {self.formula_rep.sample.replace("◆", self.symbol)} ⌝).'
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

    def __init__(self, theory, symbol=None, capitalizable=False, python_name=None):
        assert isinstance(theory, Theory)
        self.python_name = python_name
        self.simple_objct_index = theory.crossreference_simple_objct(self)
        capitalizable = False if symbol is None else capitalizable
        symbol = f'ℴ{repm.subscriptify(self.simple_objct_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)

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


universe_of_discourse = Theory(theory=None, is_universe_of_discourse=True, symbol='universe-of-discourse',
                               capitalizable=True)
u = universe_of_discourse

meta_theory = Theory(theory=universe_of_discourse, symbol='meta-theory', capitalizable=True)
def generate_meta_theory():
    global meta_theory
    # TODO: re-organize foundation theories

generate_meta_theory()


_relation_declaration = TheoreticalRelation(theory=meta_theory, arity=2, symbol='relation-declaration')
_simple_objct_declaration = TheoreticalRelation(theory=meta_theory, arity=2, symbol='simple-objct-declaration')
_theory_declaration = TheoreticalRelation(theory=meta_theory, arity=2, symbol='theory-declaration')
_theory_extension = TheoreticalRelation(theory=meta_theory, arity=2, symbol='theory-extension')
_variable_declaration = TheoreticalRelation(theory=meta_theory, arity=2, symbol='variable-declaration')


theoretical_relations = SimpleNamespace(
    relation_declaration=_relation_declaration,
    simple_objct_declaration=_simple_objct_declaration,
    theory_declaration=_theory_declaration,
    theory_extension=_theory_extension,
    variable_declaration=_variable_declaration)


# console = rich.console.Console()
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
        self.premises = premises
        self.conclusion = conclusion


class ModusPonens(FormulaStatement):
    """
    TODO: Make ModusPonens a subclass of InferenceRule.

    Definition:
    -----------
    A modus-ponens is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P implies Q)
    given a proposition (P is True)
    infers the proposition (Q is True)
    """

    def __init__(self, theory, p_implies_q, p, category=None):
        # Check p_implies_q consistency
        assert isinstance(p_implies_q, FormulaStatement)
        th = theory.get_theory_extension()
        assert theory.has_objct_in_hierarchy(p_implies_q)
        assert theory.has_objct_in_hierarchy(p)
        assert p_implies_q.valid_proposition.relation is implication
        p_prime = p_implies_q.valid_proposition.parameters[0]
        q_prime = p_implies_q.valid_proposition.parameters[1]
        mask = p_prime.get_variable_set()
        # Check p consistency
        # If the p statement is present in the theory,
        # it necessarily mean that p is true,
        # because every statement in the theory is a valid proposition.
        assert isinstance(p, FormulaStatement)
        assert p.theory is theory  # TODO: Extend this to parent theories
        similitude, _values = p.valid_proposition._is_masked_formula_similar_to(o2=p_prime, mask=mask)
        assert p.valid_proposition.is_masked_formula_similar_to(o2=p_prime, mask=mask)
        # State q
        self.p_implies_q = p_implies_q
        self.p = p
        # Build q by variable substitution
        substitution_map = dict((v, k) for k, v in _values.items())
        q = q_prime.substitute(substitution_map=substitution_map)
        super().__init__(theory=theory, valid_proposition=q, category=category)
        # assert p_implies_q.statement_index < self.statement_index
        # assert p.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.valid_proposition.repr_as_formula()}'
        output = output + f'\n\t{repm.serif_bold("Proof by modus ponens")}'
        output = output + f'\n\t{self.p_implies_q.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.p_implies_q.repr_as_symbol())}.'
        output = output + f'\n\t{self.p.repr_as_formula(expanded=True):<70} │ Follows from {repm.serif_bold(self.p.repr_as_symbol())}.'
        output = output + f'\n\t{"─" * 71}┤'
        output = output + f'\n\t{self.valid_proposition.repr_as_formula(expanded=True):<70} │ ∎'
        return output


foundation_theory = Theory(theory=universe_of_discourse, symbol='foundation-theory')
commutativity_of_equality = None
implication = None
equality = None

def generate_propositional_logic():
    global commutativity_of_equality
    global foundation_theory
    global implication
    global equality

    implication = Relation(theory=foundation_theory, symbol='implies', arity=2, formula_rep=Formula.infix_operator_representation,
             python_name='implies', formula_is_proposition=True)

    axiom_1 = FreeTextAxiom(theory=foundation_theory, axiom_text='= is a binary relation such that, given any two theoretical-objcts x and y, if x=y then y=x, and for every statement including x or y, the same statement is valid with the other. ')
    equality = Relation(theory=foundation_theory, symbol='=', arity=2, formula_rep=Formula.infix_operator_representation, python_name='equal_operator', formula_is_proposition=True)
    # TODO: Complete the formalization of axiom_1
    x1 = FreeVariable(theory=foundation_theory)
    x2 = FreeVariable(theory=foundation_theory)
    x1_equal_x2 = Formula(theory=foundation_theory, relation=equality, parameters=(x1, x2))
    x2_equal_x1 = Formula(theory=foundation_theory, relation=equality, parameters=(x2, x1))
    commutativity_of_equality = FormalAxiom(theory=foundation_theory, axiom=axiom_1,
                                            valid_proposition=Formula(theory=foundation_theory, relation=implication,
                     parameters=(x1_equal_x2, x2_equal_x1)))


    SimpleObjct(theory=foundation_theory, symbol='true', capitalizable=True, python_name='true')
    SimpleObjct(theory=foundation_theory, symbol='false', capitalizable=True, python_name='false')

generate_propositional_logic()

pass
