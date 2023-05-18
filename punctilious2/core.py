from types import SimpleNamespace
import repm
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

    def __repr__(self):
        return self.repr_as_symbol()

    def __str__(self):
        return self.repr_as_symbol()

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
        #assert False

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
    A direct-axiom-inference-statement is a proposition that follows directly from an axion.

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
        self.axioms = tuple()
        self.formulae = tuple()
        self.relations = tuple()
        self.simple_objcts = tuple()
        self.statements = tuple()
        self.symbolic_objcts = tuple()
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
        and return its 0-based index in Theory.symbolic_objcts."""
        assert isinstance(s, SymbolicObjct)
        s.theory = s.theory if hasattr(s, 'theory') else self
        assert s.theory is self
        if s not in self.symbolic_objcts:
            self.symbolic_objcts = self.symbolic_objcts + tuple([s])
        return self.symbolic_objcts.index(s)

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
            self.simple_objcts = self.simple_objcts + tuple([o])

        # phi = SimpleObjctDeclarationFormula(theory=self, simple_objct=simple_objct)
        # position = self._get_next_position()
        # statement = PropositionStatement(theory=self, position=position, phi=phi)
        # self.append_statement(statement=statement)

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
        and return the 0-based index of the formula in Theory.symbolic_objcts."""
        assert isinstance(r, Relation)
        r.theory = r.theory if hasattr(r, 'theory') else self
        assert r.theory is self
        if r not in self.relations:
            self.relations = self.relations + tuple([r])
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
    """

    def __init__(self, theory, arity, formula_rep=None, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
        self.formula_rep = Formula.reps.function_call if formula_rep is None else formula_rep
        self.relation_index = theory.crossreference_relation(self)
        capitalizable = False if symbol is None else capitalizable
        symbol = f'◆{repm.subscriptify(self.relation_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, symbol=symbol, capitalizable=capitalizable)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity

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

    def __init__(self, theory, symbol=None, capitalizable=False):
        assert isinstance(theory, Theory)
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
_implies = Relation(theory=universe_of_discourse, symbol='implies', arity=2, formula_rep=Formula.reps.infix_operator)
_is = Relation(theory=universe_of_discourse, symbol='is', arity=2, formula_rep=Formula.reps.infix_operator)
_true = SimpleObjct(theory=universe_of_discourse, symbol='true', capitalizable=True)


class ModusPonensStatement(FormulaStatement):
    """

    Definition:
    -----------
    A modus-ponens-statement is a valid rule-of-inference propositional-logic argument that,
    given a proposition (P implies Q)
    given a proposition (P is True)
    infers the proposition (Q is True)
    """

    def __init__(self, theory, p_implies_q, p_is_true, category=None):
        # Check p_implies_q consistency
        assert isinstance(p_implies_q, FormulaStatement)
        assert p_implies_q.valid_proposition.relation is _implies
        p = p_implies_q.valid_proposition.parameters[0]
        q = p_implies_q.valid_proposition.parameters[1]
        # Check p_is_true consistency
        assert isinstance(p_is_true, FormulaStatement)
        assert p_is_true.valid_proposition.relation is _is
        assert p is p_is_true.valid_proposition.parameters[0]
        assert p_is_true.valid_proposition.parameters[1] is _true
        # State q_is_true
        q_is_true = Formula(theory=theory, relation=_is, parameters=(p, _true))
        super().__init__(theory=theory, valid_proposition=q_is_true, category=category)
        assert p_implies_q.statement_index < self.statement_index
        assert p_is_true.statement_index < self.statement_index

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement.

        The representation is in two parts:
        - The formula that is being stated,
        - The justification for the formula."""
        output = f'\n\n{repm.serif_bold(self.repr_as_symbol(capitalized=True))}: {self.truth_object.repr_as_formula()}'
        output = output + f'\n{repm.serif_bold("Proof:")} Follows directly from {repm.serif_bold(self.axiom.repr_as_symbol())}.'
        return output
