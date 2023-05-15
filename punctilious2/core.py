from types import SimpleNamespace

utf8_subscript_dictionary = {'0': u'₀',
                             '1': u'₁',
                             '2': u'₂',
                             '3': u'₃',
                             '4': u'₄',
                             '5': u'₅',
                             '6': u'₆',
                             '7': u'₇',
                             '8': u'₈',
                             '9': u'₉',
                             'a': u'ₐ',
                             'e': u'ₑ',
                             'o': u'ₒ',
                             'x': u'ₓ',
                             # '???': u'ₔ',
                             'h': u'ₕ',
                             'k': u'ₖ',
                             'l': u'ₗ',
                             'm': u'ₘ',
                             'n': u'ₙ',
                             'p': u'ₚ',
                             's': u'ₛ',
                             't': u'ₜ',
                             '+': u'₊',
                             '-': u'₋',
                             '=': u'₌',
                             '(': u'₍',
                             ')': u'₎',
                             'j': u'ⱼ',
                             'i': u'ᵢ',  # Alternative from the Unicde Phonetic Extensions block: ᵢ
                             'r': u'ᵣ',  # Source: Unicode Phonetic Extensions block.
                             'u': u'ᵤ',  # Source: Unicode Phonetic Extensions block.
                             'v': u'ᵥ',  # Source: Unicode Phonetic Extensions block.
                             'β': u'ᵦ',  # Source: Unicode Phonetic Extensions block.
                             'γ': u'ᵧ',  # Source: Unicode Phonetic Extensions block.
                             # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
                             'φ': u'ᵩ',  # Source: Unicode Phonetic Extensions block.
                             'χ': u'ᵪ'  # Source: Unicode Phonetic Extensions block.
                             }


def subscriptify(s=None, fmt=None, **kwargs):
    """Converts to unicode-subscript the string s.

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
        * https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    """
    global utf8_subscript_dictionary
    if isinstance(s, int):
        s = str(s)
    if s is None or s == '':
        return ''
    return ''.join([utf8_subscript_dictionary.get(c, c) for c in s])


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
    A symbolic-objct is a python object instance that is assigned symbolic names,
    but that is linked to a theory but that is not necessarily constitutive of the theory.
    """

    def __init__(self, theory, python, dashed, symbol):
        assert theory is not None and isinstance(theory, Theory)
        self.theory = theory
        self.python = python
        self.dashed = dashed
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def str(self, scheme):
        assert scheme is not None and isinstance(scheme, SymbolicScheme)
        if hasattr(self, scheme.python):
            return getattr(self, scheme.python)
        else:
            return getattr(self, schemes.python.python)


class TheoreticalObjct(SymbolicObjct):
    """
    Definition
    ----------
    Given a theory 𝒯, a theoretical-object 𝔁 is an object
    that is constitutive of 𝒯 and that may be referenced in 𝒯 formulae.

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

    def __init__(self, theory, python, dashed, symbol):

        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)


class Formula(TheoreticalObjct):
    """

    Definition
    ----------
    A formula 𝜑 is a tuple (◆, 𝒳) where:
    * ◆ is a relation.
    * 𝒳 is a finite tuple of parameters
      whose elements are theoretical-objects, possibly formulae.
    """

    def __init__(self, theory, relation, parameters, python=None, dashed=None, symbol=None):
        assert isinstance(theory, Theory)
        self.formula_index = theory.link_formula(self)
        python = f'f{self.formula_index + 1}' if python is None else python
        dashed = f'formula-{self.formula_index + 1}' if dashed is None else dashed
        symbol = f'𝜑{subscriptify(self.formula_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)
        assert relation is not None and isinstance(relation, Relation)
        self.relation = relation
        assert parameters is not None and isinstance(parameters, tuple) and len(parameters) > 0
        self.parameters = parameters


class RelationDeclarationFormula(Formula):
    def __init__(self, theory, relation, python, dashed, symbol):
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


class TheoryStatement:
    def __init__(self, theory, position):
        self.theory = theory
        self.position = position


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


class SimpleObjctDeclarationStatement(TheoryStatement):
    def __init__(self, theory, position, simple_objct_component):
        phi = SimpleObjctDeclarationFormula(theory=theory, simple_objct=simple_objct_component)
        super().__init__(theory, position)


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
    def __init__(self, theory=None, is_universe_of_discourse=None, python=None, dashed=None, symbol=None):
        global universe_of_discourse
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
        self.theory_index = theory.link_theory(self)
        python = f't{self.theory_index + 1}' if python is None else python
        dashed = f'theory-{self.theory_index + 1}' if dashed is None else dashed
        symbol = f'𝒯{subscriptify(self.theory_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)

    def append_formula_component(self, formula_component):
        assert formula_component is not None \
               and isinstance(formula_component, TheoreticalObjct) \
               and formula_component.theory is self
        formula_components = self.formula_components
        index = len(formula_components) + 1
        self.formula_components = formula_components + tuple([formula_component])
        return index

    def append_statement(self, statement):
        # TODO: Validate statement in append_statement
        self.statements.append(statement)

    def append_theoretical_statement(self, phi, proof):
        position = self._get_next_position()
        statement = PropositionStatement(theory=self, position=position, phi=phi, proof=proof)
        self.append_statement(statement=statement)

    def declare_simple_objct(self, python=None, dashed=None, symbol=None):
        simple_objct = SimpleObjct(theory=self, python=python, dashed=dashed, symbol=symbol)
        phi = SimpleObjctDeclarationFormula(theory=self, simple_objct=simple_objct)
        position = self._get_next_position()
        statement = PropositionStatement(theory=self, position=position, phi=phi)
        self.append_statement(statement=statement)

    def declare_relation(self, python=None, dashed=None, symbol=None, arity=None):
        relation = Relation(arity=arity, python=python, dashed=dashed, symbol=symbol)
        phi = RelationDeclarationFormula(theory=self, relation=relation)
        position = self._get_next_position()
        statement = PropositionStatement(theory=self, position=position, phi=phi)
        self.append_statement(statement=statement)

    def link_symbolic_objct(self, s):
        """During construction, cross-link a symbolic_objct 𝓈
        with its parent theory if it is not already cross-linked,
        and return its 0-based index in Theory.symbolic_objcts."""
        assert isinstance(s, SymbolicObjct)
        o.theory = o.theory if hasattr(o, 'theory') else self
        assert o.theory is self
        if o not in self.symbolic_objcts:
            self.symbolic_objcts = self.symbolic_objcts + tuple([o])
        return self.symbolic_objcts.index(o)

    def link_formula(self, phi):
        """During construction, cross-link a formula phi
        with its parent theory if it is not already cross-linked,
        and return its 0-based index in Theory.formulae."""
        assert isinstance(phi, Formula)
        phi.theory = phi.theory if hasattr(phi, 'theory') else self
        assert phi.theory is self
        if phi not in self.formulae:
            self.formulae = self.formulae + tuple([phi])
        return self.formulae.index(phi)

    def link_simple_objct(self, o):
        """During construction, cross-link a simple-objct ℴ
        with its parent theory if it is not already cross-linked,
        and return its 0-based index in Theory.simple_objcts."""
        assert isinstance(o, SimpleObjct)
        o.theory = o.theory if hasattr(o, 'theory') else self
        assert o.theory is self
        if o not in self.simple_objcts:
            self.simple_objcts = self.simple_objcts + tuple([o])
        return self.simple_objcts.index(o)

    def link_theory(self, t):
        """During construction, cross-link a theory 𝒯
        with its parent theory if it is not already cross-linked,
        and return its 0-based index in Theory.theories."""
        assert isinstance(t, Theory)
        t.theory = t.theory if hasattr(t, 'theory') else self
        assert t.theory is self
        if t not in self.theories:
            self.theories = self.theories + tuple([t])
        return self.theories.index(t)

    def link_relation(self, r):
        """During construction, cross-link a relation r
        with its parent theory if it is not already cross-linked,
        and return the 0-based index of the formula in Theory.symbolic_objcts."""
        assert isinstance(r, Relation)
        r.theory = r.theory if hasattr(r, 'theory') else self
        assert r.theory is self
        if r not in self.relations:
            self.relations = self.relations + tuple([r])
        return self.relations.index(r)

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

    def __init__(self, theory, arity, python=None, dashed=None, symbol=None):
        assert isinstance(theory, Theory)
        self.relation_index = theory.link_relation(self)
        python = f'f{self.relation_index + 1}' if python is None else python
        dashed = f'formula-{self.relation_index + 1}' if dashed is None else dashed
        symbol = f'𝜑{subscriptify(self.relation_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)
        assert arity is not None and isinstance(arity, int) and arity > 0
        self.arity = arity


class SimpleObjct(TheoreticalObjct):
    """
    Definition
    ----------
    A simple-objct-component ℴ is a theoretical-object that has no special attribute,
    and whose sole function is to provide the meaning of being itself.
    """

    def __init__(self, theory, python=None, dashed=None, symbol=None):
        assert isinstance(theory, Theory)
        self.simple_objct_index = theory.link_simple_objct(self)
        if python is None or dashed is None or symbol is None:
            python = f'o{self.simple_objct_index + 1}' if python is None else python
            dashed = f'simple-objct-{self.simple_objct_index + 1}' if dashed is None else dashed
            symbol = f'ℴ{subscriptify(self.simple_objct_index + 1)}' if symbol is None else symbol
        if python is None or dashed is None or symbol is None:
            # Force the theory attribute
            # because get_symbolic_object_1_index() needs it.
            self.theory = theory
            formula_index = theory.link_symbolic_objct(self)
            python = f'o{formula_index}' if python is None else python
            dashed = f'object-{formula_index}' if dashed is None else dashed
            symbol = f'ℴ{subscriptify(formula_index)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)


class TheoreticalRelation(Relation):
    """
    Definition:
    A theoretical-relation ◆ is a relation that express theoretical-statements.

    Note:
    Simply put, theoretical-relations is a list of pre-defined relations
    that makes it possible to elaborate theories.

    """

    def __init__(self, theory, arity, python, dashed, symbol):
        super().__init__(theory=theory, arity=arity, python=python, dashed=dashed, symbol=symbol)


universe_of_discourse = Theory(theory=None, is_universe_of_discourse=True, python='U', dashed='universe-of-discourse', symbol='𝒰')
u = universe_of_discourse

_relation_declaration = TheoreticalRelation(theory=u, arity=2, python='relation_declaration', dashed='relation-declaration', symbol='relation-declaration')
_simple_objct_declaration = TheoreticalRelation(theory=u, arity=2, python='simple_objct_declaration', dashed='simple-objct-declaration', symbol='simple-objct-declaration')
_theory_declaration = TheoreticalRelation(theory=u, arity=2, python='theory_declaration', dashed='theory-declaration', symbol='theory-declaration')
_theory_extension = TheoreticalRelation(theory=u, arity=2, python='theory_extension', dashed='theory-extension', symbol='theory-extension')
_variable_declaration = TheoreticalRelation(theory=u, arity=2, python='variable_declaration', dashed='variable-declaration', symbol='variable-declaration')

theoretical_relations = SimpleNamespace(
    relation_declaration=_relation_declaration,
    simple_objct_declaration=_simple_objct_declaration,
    theory_declaration=_theory_declaration,
    theory_extension=_theory_extension,
    variable_declaration=_variable_declaration)
