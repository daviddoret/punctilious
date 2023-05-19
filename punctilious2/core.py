from types import SimpleNamespace
import repm


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
    but that is linked to a theory but that is not necessarily constitutive of the theory.
    """

    def __init__(self, theory, symbol, capitalizable=False):
        assert theory is not None and isinstance(theory, Theory)
        assert isinstance(symbol, str) and len(symbol) > 0
        assert isinstance(capitalizable, bool)
        self.theory = theory
        self.symbol = symbol
        self.capitalizable = capitalizable
        self.theory.crossreference_symbolic_objct(s=self)

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
        if not self.theory.is_1_equivalent(o2.theory):
            return False
        if self.symbol != o2.symbol:
            return False
        return True

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be a symbolic-objct denoted as ⌜ {self.repr_as_symbol()} ⌝.'

    def repr_as_symbol(self, capitalized=False):
        return self.symbol.capitalize() if (capitalized and self.capitalizable) else self.symbol

    def repr(self):
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


class FreeVariable:
    """


    Defining properties:
    --------------------
    The defining-properties of a free-variable are:
     * Being a free-variable
     * The scope-formula of the free-variable
     * The index-position of the free-variable in its scope-formula
    """

    def __init__(self, formula):
        assert isinstance(formula, Formula)
        formula_index = None  # TODO: Implement FreeVariable.formula_index
        formula = formula

    def is_defining_property_equivalent_to(self, o2, skip_formula_verification=False):
        """Returns true if this free-variable and o2 are defining-property-equivalent.

        Parameters:
        -----------
        o2 : SymbolicObject
            The symbolic-object with which to verify defining-property-equivalence.
        skip_formula_verification : bool
            True if this function is called from Formula.is_defining_property_equivalent_to()
            to avoid infinite loops.

        Definition:
        -----------
        A free-variable 𝐱 and a symbolic-object o₂ are defining-property-equivalent if and only if:
         1. o₂ is free-variable.
         2. 𝐱 and o₂ are linked to otherwiseᵃ defining-property-equivalent formulae.
         3. 𝐱 and o₂ have equal variable-position with respect to their parent formulae.

        ᵃ. That is, they satisfy all conditions required by defining-property-equivalent
           except for those conditions applying to this free-variable, a necessary
           condition to avoid circular definition.

        """
        assert isinstance(o2, SymbolicObjct)
        if not isinstance(o2, FreeVariable):
            return False
        if not skip_formula_verification:
            if not self.formula.is_defining_property_equivalent_to(o2.formula):
                return False
        if self.formula_index != o2.formula_index:
            return False
        return True


class FreeVariablePlaceholder:
    """

    Definition:
    -----------
    A free-variable-placeholder is a transitory object used during formula construction.
    It makes it possible to build formula with variable-parameters.
    Then, during the final step of formula construction, these placeholders
    are replaced by definitive free-variable objects.
    The reason why this approach was necessary are:
     * When building a formula as a single python statement, we cannot reference the formula:
        e.g. phi = Formula(t1, r1, (Variable('x', formula=???))
     * When building a formula as a single python statement, we cannot call multiple times the constructor:
        e.g. phi = Formula(t1, r1, (Variable('x'), Variable('x'))
        This second issue could be solved by complex static constructors but the approach
        of late cross-referencing variables at the end of the construction process seemed
        much simpler.
    """

    def __init__(self, symbol):
        assert isinstance(symbol, str)
        self.symbol = symbol
        # Late-binding with the parent formula will be used
        # to populate the following properties.
        self.formula = None
        self.free_variable = None


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
    """

    reps = SimpleNamespace(
        function_call=repm.Representation('function_call'),
        infix_operator=repm.Representation('infix_operator'),
        prefix_operator=repm.Representation('prefix_operator'),
        suffix_operator=repm.Representation('prefix_operator')
    )

    def __init__(self, theory, relation, parameters, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        self.free_variables = dict()  # TODO: Check how to make dict immutable after construction.
        self.formula_index = theory.crossreference_formula(self)
        capitalizable = False if symbol is None else capitalizable
        symbol = f'𝜑{repm.subscriptify(self.formula_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)
        assert relation is not None and isinstance(relation, Relation)
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple([parameters])
        assert len(parameters) > 0
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
        assert isinstance(x, FreeVariablePlaceholder)
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

    def is_defining_property_equivalent_to(self, o2):
        """Returns true if this formula and o2 are defining-property-equivalent.

        Definition:
        -----------
        A formula φ and a symbolic-object o₂ are defining-property-equivalent if and only if:
         1. o₂ is a formula.
         2. The relations of φ and o₂ are defining-property-equivalent.
         3. The parameter ordered tuples of φ and o₂ are pair-wise defining-property-equivalent.ᵃ

        ᵃ. See the special case of variables defining-property-equivalence.

        Note:
        -----
        Intuitively, defining-property-equivalence state that two formula express the
        same thing, in the same way.
        For instance, formula (¬(True)) and (False) are not defining-property-equivalent,
        because the former expresses the negation of truth (which is equal to false),
        and the latter expresses falsehood "directly".
        It follows that two formula may yield equal values and not be defining-property-equivalent.
        But two formula that are defining-property-equivalent necessarily yield the same value.
        """
        assert isinstance(o2, SymbolicObjct)
        if not isinstance(o2, Formula):
            return False
        if not self.relation.is_defining_property_equivalent(o2):
            return False
        # Arities are necessarily equal.
        for i in range(len(self.parameters)):
            if not self.parameters[i].is_defining_property_equivalent_to(o2.parameters[i]):
                return False
        return True

    def repr_as_function_call(self):
        return f'{self.relation.symbol}({", ".join([p.repr() for p in self.parameters])})'

    def repr_as_infix_operator(self):
        assert self.relation.arity == 2
        return f'({self.parameters[0].repr()} {self.relation.symbol} {self.parameters[1].repr()})'

    def repr_as_suffix_operator(self):
        assert self.relation.arity == 1
        return f'({self.parameters[0].repr()}){self.relation.symbol}'

    def repr_as_prefix_operator(self):
        assert self.relation.arity == 1
        return f'{self.relation.symbol}({self.parameters[0].repr()})'

    def repr_as_formula(self):
        match self.relation.formula_rep:
            case Formula.reps.function_call:
                return self.repr_as_function_call()
            case Formula.reps.infix_operator:
                return self.repr_as_infix_operator()
            case Formula.reps.prefix_operator:
                return self.repr_as_prefix_operator()
            case Formula.reps.suffix_operator:
                return self.repr_as_suffix_operator()
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


class Axiom(Statement):
    """

    Definition:
    -----------
    An axiom is a theory-statement that expresses an axiom in free textual form.

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


class FormulaStatement(Statement):
    """
    TODO: MAKE IT AN ABSTRACT CLASS

    Definition:
    -----------
    An formula-statement is a statement that expresses the validity of a formula in the parent theory.

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


class DirectAxiomInferenceStatement(FormulaStatement):
    """

    Definition:
    -----------
    A direct-axiom-inference-statement is a valid-proposition that follows directly from an axion.
    """

    def __init__(self, theory, axiom, valid_proposition, category=None):
        assert isinstance(theory, Theory)
        assert isinstance(axiom, Axiom)
        assert isinstance(valid_proposition, Formula)
        self.axiom = axiom
        super().__init__(theory=theory, valid_proposition=valid_proposition, category=category)
        assert axiom.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.valid_proposition.repr_as_formula()}'
        output = output + f'\n{repm.serif_bold("Proof:")} Follows directly from {repm.serif_bold(self.axiom.repr_as_symbol())}.'
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
    def __init__(self, theory=None, is_universe_of_discourse=None, symbol=None, capitalizable=False):
        global universe_of_discourse
        self.symbols = dict()
        self.axioms = tuple()
        self.formulae = tuple()
        self.relations = Tuple()
        self.simple_objcts = Tuple()
        self.statements = tuple()
        self.symbolic_objcts = dict()
        self.theories = tuple()
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
        assert isinstance(a, Axiom)
        a.theory = a.theory if hasattr(a, 'theory') else self
        assert a.theory is self
        if a not in self.axioms:
            self.axioms = self.axioms + tuple([a])
        return self.axioms.index(a)

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

    def repr_as_theory(self):
        """Return a representation that expresses and justifies the theory."""
        output = f'\n\n{repm.serif_bold(self.repr_as_symbol(capitalized=True))}'
        output = output + f'\n\n{repm.serif_bold("Simple-objcts:")}'
        output = output + '\n' + '\n'.join(o.repr_as_declaration() for o in self.simple_objcts)
        output = output + f'\n\n{repm.serif_bold("Relations:")}'
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
        self.formula_rep = Formula.reps.function_call if formula_rep is None else formula_rep
        self.python_name = python_name
        self.formula_is_proposition = formula_is_proposition
        capitalizable = False if symbol is None else capitalizable
        symbol = f'◆{repm.subscriptify(self.relation_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity
        self.relation_index = theory.crossreference_relation(self)

    def is_defining_property_equivalent_to(self, o2):
        """Returns true if this relation and o2 are defining-property-equivalent.

        Parameters:
        -----------
        o2 : SymbolicObject
            The symbolic-object with which to verify defining-property-equivalence.

        Definition:
        -----------
        A relation r and a symbolic-object o₂ are defining-property-equivalent if and only if:
        Necessary conditions:
         1. r and o₂ symbolic-equivalent.
        Unnecessary but valid conditions:
         2. o₂ is a relation.
         3. r and o₂ are linked to defining-property-equivalent theories.
         4. r and o₂ have equal arity.

        Note:
        If two relations are defined with exactly the same theoretical constraints,
        but are defined with distinct symbols, they are not defining-property-equivalent.
        """
        return self.is_symbol_equivalent(o2)

    def repr_as_declaration(self):
        return f'Let {self.repr_as_symbol()} be a {self.repr_arity_as_text()} relation denoted as ⌜ {self.repr_as_symbol()} ⌝.'

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

_relation_declaration = TheoreticalRelation(theory=u, arity=2, symbol='relation-declaration')
_simple_objct_declaration = TheoreticalRelation(theory=u, arity=2, symbol='simple-objct-declaration')
_theory_declaration = TheoreticalRelation(theory=u, arity=2, symbol='theory-declaration')
_theory_extension = TheoreticalRelation(theory=u, arity=2, symbol='theory-extension')
_variable_declaration = TheoreticalRelation(theory=u, arity=2, symbol='variable-declaration')

theoretical_relations = SimpleNamespace(
    relation_declaration=_relation_declaration,
    simple_objct_declaration=_simple_objct_declaration,
    theory_declaration=_theory_declaration,
    theory_extension=_theory_extension,
    variable_declaration=_variable_declaration)


# console = rich.console.Console()


class ModusPonensStatement(FormulaStatement):
    """

    Definition:
    -----------
    A modus-ponens-statement is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P implies Q)
    given a proposition (P is True)
    infers the proposition (Q is True)
    """

    def __init__(self, theory, p_implies_q, p, category=None):
        # Check p_implies_q consistency
        assert isinstance(p_implies_q, FormulaStatement)
        assert p_implies_q.theory is theory  # TODO: Extend this to parent theories
        assert p_implies_q.valid_proposition.relation is propositional_logic.relations.implies
        p_prime = p_implies_q.valid_proposition.parameters[0]
        q = p_implies_q.valid_proposition.parameters[1]
        # Check p consistency
        # If the p statement is present in the theory,
        # it necessarily mean that p is true,
        # because every statement in the theory is a valid proposition.
        assert isinstance(p, FormulaStatement)
        assert p.theory is theory  # TODO: Extend this to parent theories
        assert p.is_variable_equivalent_to(p_prime)
        # State q
        super().__init__(theory=theory, valid_proposition=q, category=category)
        # assert p_implies_q.statement_index < self.statement_index
        # assert p.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\n{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.truth_object.repr_as_formula()}'
        output = output + f'\n{repm.serif_bold("Proof:")} Follows directly from {repm.serif_bold(self.axiom.repr_as_symbol())}.'
        return output


propositional_logic = Theory(theory=universe_of_discourse)
SimpleObjct(theory=propositional_logic, symbol='true', capitalizable=True, python_name='true')
SimpleObjct(theory=propositional_logic, symbol='false', capitalizable=True, python_name='false')
Relation(theory=propositional_logic, symbol='implies', arity=2, formula_rep=Formula.reps.infix_operator,
         python_name='implies', formula_is_proposition=True)
Relation(
    theory=propositional_logic, symbol='=', arity=2, formula_rep=Formula.reps.infix_operator,
    python_name='equal', formula_is_proposition=True)

pass
