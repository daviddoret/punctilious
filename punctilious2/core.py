from types import SimpleNamespace


class SymbolicScheme:
    """
    Definition
    ----------
    A symbolic-scheme is a conventional method used to assign symbolic-names to objects.
    """

    def __init__(self, python, dashed, symbol):
        self.python = python
        self.dashed = dashed
        self.symbol = symbol

    def __repr__(self):
        return self.python

    def __str__(self):
        return self.python

    def str(self, scheme=None):
        assert isinstance(scheme, SymbolicScheme)
        return getattr(self, scheme.python)


_dashed = SymbolicScheme(python='dashed', dashed='dashed', symbol='dashed')
_python = SymbolicScheme(python='python', dashed='python', symbol='python')
_symbol = SymbolicScheme(python='symbol', dashed='symbol', symbol='symbol')

schemes = SimpleNamespace(
    dashed=_dashed,
    python=_python,
    symbol=_symbol)


class SymbolicObjct:
    """
    Definition
    ----------
    A symbolic-objct is a python object instance that is assigned symbolic names.
    """

    def __init__(self, python=None, dashed=None, symbol=None):
        self.python = python
        self.dashed = dashed
        self.symbol = symbol

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def str(self, scheme):
        assert scheme is not None and isinstance(scheme, SymbolicScheme)
        if hasattr(self, scheme.python):
            return getattr(self, scheme.python)
        else:
            return getattr(self, schemes.python.python)


class FormulaComponent(SymbolicObjct):
    """
    Definition
    ----------
    Given a formula 𝜑, a formula-component 𝔁 is an object that assigns meaning to 𝜑.

    The following are supported classes of formula-components:
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Formula(FormulaComponent):
    def __init__(self, component, subformula=None, **kwargs):
        super().__init__(**kwargs)
        assert component is not None and isinstance(component, FormulaComponent)
        self.is_relation = isinstance(component, Relation)
        self.is_leaf = not self.is_relation
        assert self.is_leaf or subformula is not None and isinstance(subformula, tuple) and len(subformula) > 0
        self.subformula = subformula
        self.component = component
        self.cardinality = len(subformula) if self.is_relation else None


class TheoreticalStatement:
    """
    Definition
    ----------
    A theoretical-statement 𝒮 is a tuple (𝒯, n, 𝜑, 𝒫) where:
    * 𝒯 is a theory
    * n is a natural number representing the unique position of 𝒮 in 𝒯
    * 𝜑 is a valid-formula in 𝒯 of the form ⟨◆, 𝒯, 𝜓⟩ where:
        * ◆ is a theoretical-relation
        * 𝜓 is a free-formula
    * 𝒫 is a proof of 𝜑 in 𝒯 based on predecessors of 𝒮
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


class Theory(FormulaComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.statements = list()

    def _get_next_position(self):
        # TODO: Make _get_next_position robust against concurrency issues
        return len(self.statements) + 1

    def append_statement(self, statement):
        # TODO: Validate statement in append_statement
        self.statements.append(statement)

    def append_theoretical_statement(self, phi, proof):
        position = self._get_next_position()
        statement = TheoreticalStatement(theory=self, position=position, phi=phi, proof=proof)
        self.append_statement(statement=statement)


class Proof:
    """TODO: Define the proof class"""

    def __init__(self):
        pass


class Relation(FormulaComponent):
    """
    Definition
    ----------
    A relation ◆ is a formula-component for formula that contain nested-formula.
    It assigns the following meaning to its composite formula 𝜑:
    𝜑 establishes a relation between its ordered nested subformula.
    A relation ◆ has a fixed arity.
    """

    def __init__(self, arity, **kwargs):
        super().__init__(**kwargs)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity


class TheoreticalRelation(Relation):
    """
    Definition:
    A theoretical-relation ◆ is a relation that express theoretical-statements.

    Note:
    Simply put, theoretical-relations is a list of pre-defined relations
    that makes it possible to elaborate theories.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


_relation_declaration = TheoreticalRelation(dashed='relation-declaration', arity=2)
_simple_objct_declaration = TheoreticalRelation(dashed='simple-objct-declaration', arity=2)
_theory_declaration = TheoreticalRelation(dashed='theory-declaration', arity=2)
_theory_extension = TheoreticalRelation(dashed='theory-extension', arity=2)
_variable_declaration = TheoreticalRelation(dashed='variable-declaration', arity=2)

theoretical_relations = SimpleNamespace(
    relation_declaration=_relation_declaration,
    simple_objct_declaration=_simple_objct_declaration,
    theory_declaration=_theory_declaration,
    theory_extension=_theory_extension,
    variable_declaration=_variable_declaration)

universe_of_discourse = Theory(python='U', dashed='universe-of-discourse', symbol='𝒰')
