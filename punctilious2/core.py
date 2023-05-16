from types import SimpleNamespace
import rich
import rich.console
import rich.markdown

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
                             'i': u'ᵢ',  # Alternative from the Unicode Phonetic Extensions block: ᵢ
                             'r': u'ᵣ',  # Source: Unicode Phonetic Extensions block.
                             'u': u'ᵤ',  # Source: Unicode Phonetic Extensions block.
                             'v': u'ᵥ',  # Source: Unicode Phonetic Extensions block.
                             'β': u'ᵦ',  # Source: Unicode Phonetic Extensions block.
                             'γ': u'ᵧ',  # Source: Unicode Phonetic Extensions block.
                             # '???': u'ᵨ', # Source: Unicode Phonetic Extensions block.
                             'φ': u'ᵩ',  # Source: Unicode Phonetic Extensions block.
                             'χ': u'ᵪ'  # Source: Unicode Phonetic Extensions block.
                             }


def subscriptify(s=None):
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

    def repr_as_dashed_name(self):
        return f'{self.dashed}'

    def repr_as_declaration(self, **kwargs):
        return f'Let {self.repr_as_dashed_name()} be a symbolic-objct denoted as dashed-name ⌜ {self.repr_as_dashed_name()} ⌝, symbol ⌜ {self.repr_as_symbol()} ⌝, and pythonic-name ⌜ {self.repr_as_python_variable()} ⌝.'

    def repr_as_python_variable(self):
        return f'{self.python}'

    def repr_as_symbol(self):
        return f'{self.symbol}'

    frmts = SimpleNamespace(
        dashed_name=repr_as_dashed_name,
        declaration=repr_as_declaration,
        python_variable=repr_as_python_variable,
        symbol=repr_as_symbol)

    def repr(self, frmt=None, **kwargs):
        frmt = SymbolicObjct.frmts.symbol if frmt is None else frmt
        return frmt(self, **kwargs)


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

    def __init__(self, theory, python, dashed, symbol):
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)

    def repr_as_statement_content(self):
        """Returns a representation that may be embedded in a statement.

        :return:
        """
        return self.repr()


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
        self.formula_index = theory.crossreference_formula(self)
        python = f'f{self.formula_index + 1}' if python is None else python
        dashed = f'formula-{self.formula_index + 1}' if dashed is None else dashed
        symbol = f'𝜑{subscriptify(self.formula_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)
        assert relation is not None and isinstance(relation, Relation)
        self.relation = relation
        parameters = parameters if isinstance(parameters, tuple) else tuple([parameters])
        assert len(parameters) > 0
        self.parameters = parameters

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr_as_function_call(self, **kwargs):
        return f'{self.relation.symbol}({", ".join([p.repr(**kwargs) for p in self.parameters])})'

    def repr_as_infix_operator(self, **kwargs):
        assert self.relation.arity == 2
        return f'({self.parameters[0].repr(**kwargs)} {self.relation.symbol} {self.parameters[1].repr(**kwargs)})'

    def repr_as_suffix_operator(self, **kwargs):
        assert self.relation.arity == 1
        return f'({self.parameters[0].repr(**kwargs)}){self.relation.symbol}'

    def repr_as_prefix_operator(self, **kwargs):
        assert self.relation.arity == 1
        return f'{self.relation.symbol}({self.parameters[0].repr(**kwargs)})'

    def repr_formula_by_symbol(self):
        return f'{self.symbol}'

    def repr(self, frmt=None, **kwargs):
        # Use the frmt attached to the formula relation as the default frmt.
        frmt = self.relation.formula_frmt if frmt is None else frmt
        return frmt(self, **kwargs)

    frmts = SimpleNamespace(
        dashed_name=SymbolicObjct.repr_as_dashed_name,
        python_variable=SymbolicObjct.repr_as_python_variable,
        symbol=SymbolicObjct.repr_as_symbol,
        function_call=repr_as_function_call,
        infix_operator=repr_as_infix_operator,
        prefix_operator=repr_as_prefix_operator,
        suffix_operator=repr_as_suffix_operator)


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

    def __init__(self, theory, truth_object, python=None, dashed=None, symbol=None):
        assert isinstance(truth_object, TheoreticalObjct)
        self.truth_object = truth_object
        assert isinstance(theory, Theory)
        self.statement_index = theory.crossreference_statement(self)
        python = f's{self.statement_index + 1}' if python is None else python
        dashed = f'statement-{self.statement_index + 1}' if dashed is None else dashed
        symbol = f'𝒮{subscriptify(self.statement_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)

    def repr(self):
        pass

    def repr_as_statement(self):
        """Return a representation that expresses and justifies the statement."""
        return f'## {self.repr_as_dashed_name()}\n{self.truth_object.repr_as_statement_content()}'


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


class Axiom(TheoreticalObjct):
    """

    Definition
    ----------
    A formula 𝜑 is a tuple (◆, 𝒳) where:
    * ◆ is a relation.
    * 𝒳 is a finite tuple of parameters
      whose elements are theoretical-objects, possibly formulae.
    """

    def __init__(self, theory, text, python=None, dashed=None, symbol=None):
        assert isinstance(theory, Theory)
        self.axiom_index = theory.crossreference_axiom(self)
        python = f'a{self.axiom_index + 1}' if python is None else python
        dashed = f'axiom-{self.axiom_index + 1}' if dashed is None else dashed
        symbol = f'𝒜{subscriptify(self.axiom_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)
        assert text is not None and isinstance(text, str)
        self.text = text

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr_as_statement_content(self):
        """Returns a representation that may be embedded in a statement.

        :return:
        """
        return f'{self.repr_as_dashed_name()}: {self.text}'

    frmts = SimpleNamespace(
        dashed_name=SymbolicObjct.repr_as_dashed_name,
        python_variable=SymbolicObjct.repr_as_python_variable,
        symbol=SymbolicObjct.repr_as_symbol,
        statement=repr_as_statement_content)

    def repr(self, frmt=None, **kwargs):
        # Use the frmt attached to the formula relation as the default frmt.
        frmt = Axiom.frmts.symbol if frmt is None else frmt
        return frmt(self, **kwargs)


class Note(AtheoreticalStatement):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text


class Theory(TheoreticalObjct):
    def __init__(self, theory=None, is_universe_of_discourse=None, python=None, dashed=None, symbol=None):
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
        python = f't{self.theory_index + 1}' if python is None else python
        dashed = f'theory-{self.theory_index + 1}' if dashed is None else dashed
        symbol = f'𝒯{subscriptify(self.theory_index + 1)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)

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
        return f' \n# {self.repr_as_dashed_name()} \n' + \
            '\n'.join(s.repr_as_statement() for s in self.statements)

    def prnt(self):
        prnt(self.repr_as_theory())


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

    def __init__(self, theory, arity, formula_frmt=None, python=None, dashed=None, symbol=None):
        assert isinstance(theory, Theory)
        self.formula_frmt = Formula.frmts.function_call if formula_frmt is None else formula_frmt
        self.relation_index = theory.crossreference_relation(self)
        python = f'r{self.relation_index + 1}' if python is None else python
        dashed = f'relation-{self.relation_index + 1}' if dashed is None else dashed
        symbol = f'◆{subscriptify(self.relation_index + 1)}' if symbol is None else symbol
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
        self.simple_objct_index = theory.crossreference_simple_objct(self)
        if python is None or dashed is None or symbol is None:
            python = f'o{self.simple_objct_index + 1}' if python is None else python
            dashed = f'simple-objct-{self.simple_objct_index + 1}' if dashed is None else dashed
            symbol = f'ℴ{subscriptify(self.simple_objct_index + 1)}' if symbol is None else symbol
        if python is None or dashed is None or symbol is None:
            # Force the theory attribute
            # because get_symbolic_object_1_index() needs it.
            self.theory = theory
            formula_index = theory.crossreference_symbolic_objct(self)
            python = f'o{formula_index}' if python is None else python
            dashed = f'object-{formula_index}' if dashed is None else dashed
            symbol = f'ℴ{subscriptify(formula_index)}' if symbol is None else symbol
        super().__init__(theory=theory, python=python, dashed=dashed, symbol=symbol)
        print(self.repr_as_declaration())

    def repr_as_declaration(self, **kwargs):
        return f'Let {self.repr_as_dashed_name()} be a symbolic-objct denoted as dashed-name ⌜ {self.repr_as_dashed_name()} ⌝, symbol ⌜ {self.repr_as_symbol()} ⌝, and pythonic-name ⌜ {self.repr_as_python_variable()} ⌝.'


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


universe_of_discourse = Theory(theory=None, is_universe_of_discourse=True, python='U', dashed='universe-of-discourse',
                               symbol='𝒰')
u = universe_of_discourse

_relation_declaration = TheoreticalRelation(theory=u, arity=2, python='relation_declaration',
                                            dashed='relation-declaration', symbol='relation-declaration')
_simple_objct_declaration = TheoreticalRelation(theory=u, arity=2, python='simple_objct_declaration',
                                                dashed='simple-objct-declaration', symbol='simple-objct-declaration')
_theory_declaration = TheoreticalRelation(theory=u, arity=2, python='theory_declaration', dashed='theory-declaration',
                                          symbol='theory-declaration')
_theory_extension = TheoreticalRelation(theory=u, arity=2, python='theory_extension', dashed='theory-extension',
                                        symbol='theory-extension')
_variable_declaration = TheoreticalRelation(theory=u, arity=2, python='variable_declaration',
                                            dashed='variable-declaration', symbol='variable-declaration')

theoretical_relations = SimpleNamespace(
    relation_declaration=_relation_declaration,
    simple_objct_declaration=_simple_objct_declaration,
    theory_declaration=_theory_declaration,
    theory_extension=_theory_extension,
    variable_declaration=_variable_declaration)

console = rich.console.Console()


def prnt(s):
    md = rich.markdown.Markdown(s)
    console.log(md)

