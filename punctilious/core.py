import uuid as uuid
from string import Template

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


class Cat:
    def __init__(self, cod, sym_prefix=None, ref_prefix=None):
        self.cod = cod
        self.sym_prefix = sym_prefix
        self.ref_prefix = ref_prefix

    def __str__(self):
        return self.cod


class RepMode:
    def __init__(self, cod):
        self.cod = cod

    def __str__(self):
        return self.cod


class cats:
    """The list of theory-objcts categories."""

    axiom = Cat(cod='axiom', ref_prefix='axiom', sym_prefix='𝒜')
    """."""

    definition = Cat('definition')
    """."""

    formula_statement = Cat(cod='formula-statement', ref_prefix='formula-statement', sym_prefix='𝜑')
    """A formula-statement."""

    free_formula = Cat(cod='free-formula', ref_prefix='free-formula', sym_prefix='𝜓')
    """A free-formula."""

    lemma = Cat('lemma')
    """."""

    objct_decl = Cat(cod='objct', ref_prefix='objct', sym_prefix='ℴ')
    """An object declaration statement."""

    note = Cat(cod='note', ref_prefix='note', sym_prefix='𝒩')
    """A textual note that is not formally part of the theory but may shed light on the theory for human readers."""

    proposition = Cat('proposition')
    """."""

    rel_decl = Cat(cod='rel', ref_prefix='rel', sym_prefix='◇')
    """A relation is a specialized objct which is used semantically to denote a relation.
    By convention, the relation in a formula is positioned at the first position."""

    theorem = Cat('theorem')
    """."""

    theory = Cat(cod='theory', ref_prefix='theory', sym_prefix='𝔗')
    """A theory."""

    var_decl = Cat(cod='var', ref_prefix='var', sym_prefix='𝒙')
    """A variable declaration statement."""


class rep_modes:
    """The list of representation modes for objcts."""

    sym = RepMode('sym')
    """Symbolic representation to be used in formula."""

    ref = RepMode('ref')
    """Referential representation to be used as theory internal links."""

    dashed_name = RepMode('dashed_name')
    """Dashed name that must be unambiguous within the related theory."""

    definition = RepMode('def')
    """Formal definition."""


def listify(*args):
    return ', '.join([str(x) for x in args if x is not None])


class Statement:
    """A Statement is an abstract object that has a position in a theory."""

    """A statement is tuple (t, ⊢, phi) where:
    t is a theory,
    ⊢ is the prove object,
    phi is a formula-variable."""

    """A formula A is a syntactic consequence within some formal system FS of a set Γ of formulas 
    if there is a formal proof in FS of A from the set Γ. This is denoted Γ ⊢FS A.
    Source: https://en.wikipedia.org/wiki/Logical_consequence"""

    """Does not prove symbol: ⊬.
    Prove symbol: ⊢."""

    def __init__(self, theory, cat, position, ref=None, sym=None, dashed_name=None):
        assert isinstance(theory, Theory) or theory is None  # The only object for which no theory linkage is
        # justified is the universe-of-discourse theory.
        assert isinstance(cat, Cat)
        self.theory = theory
        self.cat = cat
        self.position = position
        if cat == cats.theory:
            # Theories have a simplified reference scheme: theory-n where n is the theory counter.
            self.ref = f'{self.cat.ref_prefix}-{self.position}' if ref is None else ref
        else:
            # Non-theories have a reference scheme linked to their parent theory: theory-n-i where n is the theory
            # counter and i is the statement counter.
            self.ref = f'{self.cat.ref_prefix}-{self.theory.position}-{self.position}' if ref is None else ref
        self.sym = f'{self.cat.sym_prefix}{subscriptify(self.position)}' if sym is None else sym
        self.dashed_name = dashed_name

    def __repr__(self):
        return f'{self.ref} [{listify(self.sym, self.dashed_name)}]'

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.sym if mod is None else mod
        assert isinstance(mod, RepMode)
        match mod:
            case rep_modes.sym:
                return self.sym
            case rep_modes.ref:
                return self.ref
            case rep_modes.dashed_name:
                return self.dashed_name


class Note(Statement):
    def __init__(self, theory, position, ref=None, text=None):
        cat = cats.note
        super().__init__(theory=theory, cat=cat, position=position, ref=ref)
        self.text = text

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'{self.ref}: {self.text}'
            case _:
                return super().str(mod=mod, **kwargs)


class Axiom(Statement):
    def __init__(self, theory, position, ref=None, sym=None, text=None, citation=None):
        cat = cats.axiom
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym)
        self.text = text
        self.citation = citation

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                citation = '' if self.citation is None else f' [{self.citation}]'
                return f'{self.str(by_ref=True)}: {self.text}{citation}'
            case _:
                return super().str(mod=mod, **kwargs)


class ObjctDecl(Statement):
    def __init__(self, theory, position, ref=None, sym=None, dashed_name=None):
        cat = cats.objct_decl
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym, dashed_name=dashed_name)

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} be an object denoted as long-name ⌜ {self.dashed_name} ⌝, symbol ⌜ {self.sym} ⌝, and reference ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


class ObjctObsolete:
    def __init__(self, sym=None, dashed_name=None, uid=None, formula_str_fun=None):
        self.uid = uuid.uuid4() if uid is None else uid
        self.sym = sym
        self.dashed_name = dashed_name
        self.formula_str_fun = formula_str_fun
        """The default str function to be applied to the parent formula when this objct is the first component of 
        that formula."""

    def __repr__(self):
        return f'object {self.str()} ({self.uid})'

    def __str__(self):
        return self.str()

    def is_antivariable_equal_to(self, y):
        """Two formula-atomic-components x and y are antivariable-equal if and only
        x and y are objcts (ie neither is a variable),
        and x and y are references to the same objct.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        # QUESTION: Should we only the uid attribute or use the python is operator?
        assert y.is_formula_atomic_component
        x = self
        return x.uid == y.uid

    is_formula_atomic_component = True
    """x is a formula-atomic-component if and only if it is an object or a variable."""

    is_object = True

    is_variable = False

    def is_variable_equal_to(self, y):
        """Two formula-atomic-components x and y are variable-equal if and only if
        x or y or both are variables or x and y are antivariable-equal.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert y.is_formula_atomic_component
        x = self
        return y.is_variable or x.is_antivariable_equal_to(y)

    def str(self, **kwargs):
        return self.sym


class RelDecl(Statement):
    """A relation-declaration."""

    def __init__(self, theory, position, ref=None, sym=None, dashed_name=None, formula_str_fun=None):
        cat = cats.rel_decl
        # If formula_str_fun is not expressly defined,
        # we fallback on the function representation method.
        formula_str_fun = formula_str_funs.function if formula_str_fun is None else formula_str_fun
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym, dashed_name=dashed_name)
        self.formula_str_fun = formula_str_fun

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} be a relation denoted as long-name ⌜ {self.dashed_name} ⌝, symbol ⌜ {self.sym} ⌝, and reference ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


class VarDecl(Statement):
    def __init__(self, theory, position, ref=None, sym=None, dashed_name=None):
        cat = cats.var_decl
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym, dashed_name=dashed_name)

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} be a variable denoted as long-name ⌜ {self.dashed_name} ⌝, symbol ⌜ {self.sym} ⌝, and reference ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


class formula_str_funs:

    @staticmethod
    def infix(formula, is_subformula=False, **kwargs):
        """[relation, x, y] --> x relation y"""
        assert formula.first_level_cardinality == 3
        return f'{"(" if is_subformula else ""}{formula.content[1].str(is_subformula=True, mod=rep_modes.sym)} {formula.content[0].str(is_subformula=True, mod=rep_modes.sym)} {formula.content[2].str(is_subformula=True, mod=rep_modes.sym)}{")" if is_subformula else ""}'

    @staticmethod
    def condensed_unary_postfix(formula, is_subformula=False, **kwargs):
        """[relation, x] --> xrelation"""
        assert formula.first_level_cardinality == 2
        return f'{"(" if is_subformula else ""}{formula.content[1].str(is_subformula=True, mod=rep_modes.sym)}{formula.content[0].str(is_subformula=True, mod=rep_modes.sym)}{")" if is_subformula else ""}'

    @staticmethod
    def function(formula, **kwargs):
        """[relation, x, y, ...] --> relation(x, y, ...)"""
        assert formula.first_level_cardinality > 0
        relation = formula.content[0]
        arguments = ", ".join(argument.str(is_subformula=True) for argument in formula.content[1:])
        return f'{relation}({arguments})'

    @staticmethod
    def formal(formula, **kwargs):
        """[relation, x, y, ...] --> (relation, x, y, ...)"""
        assert formula.first_level_cardinality > 0
        components = ", ".join(argument.str(is_subformula=True) for argument in formula.tup)
        return f'({components})'


def formula_equality_by_variable_symbols(phi, psi):
    """Two free-formula phi and psi are antivariable-equal if and only
    the first-level-cardinality of x and y are equal,
    and for i = 1 to first-level-cardinality of phi,
    phi_i is antivariable-equal with psi_i.
    TODO: Reword the above precisely to account for leaf objects
    Note: if x and y are antivariable-equal, they are variable-equal."""
    assert phi is not None
    # Retrieve phi's tuple if it is a FreeFormula
    phi_tup = phi.tup if isinstance(phi, FreeFormula) else phi
    # Embed phi in a tuple if it is a valid leaf object
    phi_tup = tuple([phi]) if isinstance(phi, (ObjctDecl, RelDecl, VarDecl)) else phi_tup
    assert isinstance(phi_tup, tuple)
    assert psi is not None
    # Retrieve psi's tuple if it is a FreeFormula
    psi_tup = psi.tup if isinstance(psi, FreeFormula) else psi
    # Embed psi in a tuple if it is a valid leaf object
    psi_tup = tuple([psi]) if isinstance(psi, (ObjctDecl, RelDecl, VarDecl)) else psi_tup
    assert isinstance(psi_tup, tuple)
    if len(phi_tup) != len(psi_tup):
        return False
    elif len(phi_tup) == 1:
        # We assume that leaf components (objcts, relations and variables) are theory-singletons,
        # i.e. they are not instanciated multiple times in the theory,
        # and thus we may rely on the python is operator to check equality.
        return phi_tup[0] is psi_tup[0]
    else:
        return all(formula_equality_by_variable_symbols(phi_i, psi_i) for phi_i, psi_i in zip(phi_tup, psi_tup))


def traverse_two_formula_trees(phi, psi, _var_list_1=None, _var_list_2=None):
    """This function traverses simultaneously two formula-trees,
    and returns False as soon as it identifies any inequality between them,
    considering that Variables are not compared on names but on positions.
    It eventually returns True if traversal is completed and no inequality were found.
    """
    assert phi is not None and psi is not None
    _var_list_1 = list() if _var_list_1 is None else _var_list_1
    _var_list_2 = list() if _var_list_2 is None else _var_list_2
    assert isinstance(_var_list_1, list) and isinstance(_var_list_2, list)
    # If phi or psi are FreeFormula, unpack their internal tuple-trees.
    phi = phi.tup if isinstance(phi, FreeFormula) else phi
    psi = psi.tup if isinstance(psi, FreeFormula) else psi
    if type(phi) != type(psi):
        # After FreeFormula unpacking, if the types of phi and psi
        # are distinct, it follows that the two formula are unequal.
        return False, _var_list_1, _var_list_2
    if isinstance(phi, tuple) and isinstance(psi, tuple):
        if len(phi) != len(psi):
            return False, _var_list_1, _var_list_2
        for component_1, component_2 in zip(phi, psi):
            equality, _var_list_1, _var_list_2 = traverse_two_formula_trees(
                component_1, component_2, _var_list_1, _var_list_2)
            if not equality:
                return False, _var_list_1, _var_list_2
    else:
        if isinstance(phi, (ObjctDecl, RelDecl)):
            return phi is psi, _var_list_1, _var_list_2
        elif isinstance(phi, VarDecl):
            if phi not in _var_list_1:
                _var_list_1.append(phi)
            idx_1 = _var_list_1.index(phi)
            if psi not in _var_list_2:
                _var_list_2.append(psi)
            idx_2 = _var_list_2.index(psi)
            return idx_1 == idx_2, _var_list_1, _var_list_2
        else:
            raise TypeError()


def formula_equality_by_variable_position(phi, psi, phi_positions=None, psi_positions=None):
    """When comparing two formula, the names assigned to variables are not significant, i.e. if x = y, the (x + 3) = (y + 3).
    Thus we are more interested in variable relative positions in the formula,
    rather than their names."""
    # RESUME WORK HERE.
    assert phi is not None
    # Retrieve phi's tuple if it is a FreeFormula
    phi_tup = phi.tup if isinstance(phi, FreeFormula) else phi
    # Embed phi in a tuple if it is a valid leaf object
    phi_tup = tuple([phi]) if isinstance(phi, (ObjctDecl, RelDecl, VarDecl)) else phi_tup
    assert isinstance(phi_tup, tuple)
    assert psi is not None
    # Retrieve psi's tuple if it is a FreeFormula
    psi_tup = psi.tup if isinstance(psi, FreeFormula) else psi
    # Embed psi in a tuple if it is a valid leaf object
    psi_tup = tuple([psi]) if isinstance(psi, (ObjctDecl, RelDecl, VarDecl)) else psi_tup
    assert isinstance(psi_tup, tuple)
    return traverse_two_formula_trees(phi_tup, psi_tup)


leaf_classes = (ObjctDecl, RelDecl, VarDecl)
leaf_cats = (cats.objct_decl, cats.rel_decl, cats.var_decl)


class FreeFormula:
    """A free-formula 𝜑 is a formula linked to a theory but not stated as a true statement.

    Data structure:
    A free-formula 𝜑 is a container for a python tuple,
    which is either of the form (o) where o is an object,
    of the form (x) where x is a variable,
    or of the form (a, b, c, ...) where a, b, c, ... are free-formulas.
    """

    def __init__(self, theory, tup):
        assert theory is not None and isinstance(theory, Theory)
        self.theory = theory
        if isinstance(tup, leaf_classes):
            # If a leaf formula was passed as an instance of Objct or Variable,
            # pack it in a tuple for data structure consistency.
            tup = tuple([tup])
        assert tup is not None and isinstance(tup, tuple) and len(tup) > 0
        self.is_leaf = True if len(tup) == 1 else False
        if self.is_leaf:
            # This is free-leaf-formula.
            assert isinstance(tup[0], leaf_classes)
            self.tup = tup
            self.relation_set = frozenset([tup[0]]) if isinstance(tup[0], RelDecl) else frozenset()
            self.objct_set = frozenset([tup[0]]) if isinstance(tup[0], ObjctDecl) else frozenset()
            self.variable_set = frozenset([tup[0]]) if isinstance(tup[0], VarDecl) else frozenset()
        else:
            # This is not a free-leaf-formula.
            # We must thus assure that all subformula are properly
            # registered in the theory free-formula set.
            tup = tuple(theory.assure_free_formula(subformula) for subformula in tup)
            self.tup = tup
            # The relation-set, objct-set, and variable-set
            # are built as the union of the child sets.
            self.relation_set = frozenset.union(*[subformula.relation_set for subformula in tup])
            self.objct_set = frozenset.union(*[subformula.objct_set for subformula in tup])
            self.variable_set = frozenset.union(*[subformula.variable_set for subformula in tup])

    def __repr__(self):
        return self.str(str_fun=formula_str_funs.formal)

    def __str__(self):
        return self.str()

    @property
    def first_level_cardinality(self):
        """The first-level-cardinality of a formula is the number
        of first-level components in the formula."""
        return len(self.tup)

    def is_anti_variable_equal_to(self, psi):
        """Two formula phi and psi are antivariable-equal if and only
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is antivariable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        return formula_equality_by_variable_symbols(self, psi)

    def is_variable_equal_to(self, psi):
        """Two formula phi and psi are variable-equal if and only if
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is variable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert psi is not None and isinstance(psi, FreeFormula)
        phi = self
        return all(phi_i.is_variable_equal_to(psi_i) for phi_i, psi_i in zip(phi.tup, psi.tup))

    def is_relation(self):
        """By convention, if the first component of a free-formula is a relation,
        then the free-relation is a free-relation-formula."""
        return self.tup[0].cat == cats.rel_decl

    def str(self, str_fun=None, is_subformula=False, **kwargs):
        if self.is_leaf:
            return f'({self.tup[0].sym})'
        if str_fun is None and isinstance(self.tup[0], RelDecl):
            # If str_fun is not expressly passed as a parameter,
            # and if this free-formula is a free-relation-formula,
            # then the default representation of the free-formula
            # is determined by the formula_str_fun attribute of the relation.
            str_fun = self.tup[0].formula_str_fun
        if str_fun is None:
            # We fall back on the formal representation approach,
            # because we have the assurance that it will always work.
            str_fun = formula_str_funs.formal
        return str_fun(self, **kwargs)


class FormulaStatement(Statement):
    """The content of a formula is immutable. This is a key difference with theories."""

    def __init__(self, theory, position, ref=None, sym=None, free_formula=None, justif=None):
        cat = cats.formula_statement
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym)
        assert free_formula is not None
        assert isinstance(free_formula, tuple)
        self.is_leaf = True if len(free_formula) == 1 else False
        free_formula = (component for component in free_formula)
        # TODO: Loop through sub-formulas.
        # If sub-formula is a formula, it is ok.
        # If sub-formula is an objct, it is ok.
        # If sub-formula is a variable, it is ok.
        # If sub-formula is a tuple, convert it to formula and substitute.
        self.content = free_formula
        self.justif = justif

    def __str__(self):
        return self.str()

    def str(self, mod=None, is_subformula=False, **kwargs):
        """
        Returns a string representation of the formula.

        :param mod:
        :param is_subformula: True if formula is a sub-formula embedded in a parent formula. Depending on preferences,
        this may result in the sub-formula being enclosed in parentheses to avoid ambiguity.
        :return: A string representation of the formula.
        """
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        match mod:
            case rep_modes.definition:
                if len(self.content) == 1 and self.content[0].is_formula_atomic_component:
                    return self.content[0].str(sym=True, **kwargs)
                elif len(self.content) > 1 and self.content[0].is_object \
                        and self.content[0].formula_str_fun is not None:
                    return self.content[0].formula_str_fun(self, sub=is_subformula, sym=True, **kwargs)
                else:
                    raise Exception("Oops, no str_fun was found to convert this formula to string.")
            case _:
                return super().str(mod=mod, **kwargs)


class JustificationMethod:
    """Known methods to justify theory statements."""

    def __init__(self, cod, template):
        self.cod = cod
        if isinstance(template, str):
            template = Template(template)
        self.template = template

    def str(self):
        return self.cod

    def __repr__(self):
        return f'justification method: {self.str()}'

    def __str__(self):
        return self.str()


class justification_methods:
    is_axiom = JustificationMethod('axiom', 'By axiomatic choice.')
    axiom_encoding = JustificationMethod('axiom-encoding', 'By encoding of $justifying_statement.')
    statement_derivation = JustificationMethod('statement-derivation', 'By derivation from $justifying_statement.')


class Justification:
    def __init__(self, method, justifying_statement=None):
        assert isinstance(method, JustificationMethod)
        assert not (method == justification_methods.is_axiom and justifying_statement is not None)
        assert not (method == justification_methods.axiom_encoding and justifying_statement is None)
        assert not (method == justification_methods.statement_derivation and justifying_statement is None)
        self.method = method
        self.justifying_statement = justifying_statement

    def str(self):
        return self.method.template.safe_substitute(
            justifying_statement=self.justifying_statement)

    def __repr__(self):
        return f'justification: {self.str()}'

    def __str__(self):
        return self.str()


class Theory(Statement):
    """The content of a theory is enriched by proofs. This is a key difference with formula whose content is
    immutable."""

    def __init__(self, theory=None, position=None, ref=None, sym=None, dashed_name=None):
        cat = cats.theory
        position = Theory._get_counter() if position is None else position
        super().__init__(theory=theory, cat=cat, position=position, ref=ref, sym=sym, dashed_name=dashed_name)
        self._statement_max_position = 0  # TODO: replace this with the computation of max + 1 from statements list.
        self.statements = []
        self.free_formulas = []
        if theory is None:
            # This theory is not linked to a parent theory,
            # in consequence it will not be output as part of the append_theory method,
            # thus we output the theory definition here.
            print(self.str(mod=rep_modes.definition))

    position = 0

    def append_axiom(self, text, citation=None):
        counter = self._get_statement_counter()
        axiom = Axiom(theory=self, position=counter, text=text)
        self.statements.append(axiom)
        if Theory.echo_statement:
            print(axiom.str(mod=rep_modes.definition))
        return axiom

    def append_axiom_statement(self, statement_content, justification):
        """Elaborate the theory by appending a new statement to it."""
        assert isinstance(statement_content, Axiom)
        # TODO: Check proof consistency / validity
        statement_formula = FormulaStatement((proves, self, statement_content))
        statement_counter = self._get_statement_counter()
        statement = StatementObsolete(self, statement_counter, statement_formula, justification)
        self.statements.append(statement)
        if Theory.echo_statement:
            print(statement.str(mod=rep_modes.definition))
        return statement

    def assure_free_formula(self, phi):
        """A free-formula is not appended to a theory because we assure the
        unicity of formula in theories. Thus it is 'assured'."""

        assert phi is not None

        if isinstance(phi, FreeFormula):
            # If a free-formula was passed as the argument,
            # return it directly after checking it is
            # an element of this theory free-formula set.
            # This condition is a bit superfluous
            # but it makes it possible to call this method in a loose manner.
            assert phi.theory == self
            return phi

        assert isinstance(phi, (tuple, ObjctDecl, RelDecl, VarDecl))
        if isinstance(phi, (ObjctDecl, RelDecl, VarDecl)):
            # If phi is a leaf object,
            # embed it in a tuple for data structure consistency.
            phi = tuple([phi])

        free_formula = next((psi for psi in self.free_formulas if psi.is_anti_variable_equal_to(phi)), None)
        if free_formula is not None:
            # The free-formula is already present in the theory free-formula set.
            # Return the existing formula to prevent formula duplicates in the theory.
            return free_formula

        # The free-formula is not already present in the theory free-formula set,
        # we thus must append it in the set.
        # Note that FreeFormula.__init__ will assure that subformula are
        # properly registered in the theory free-formula set.
        free_formula = FreeFormula(theory=self, tup=phi)
        self.free_formulas.append(free_formula)
        return free_formula

    def append_formula_statement(self, tup, justification):
        """Elaborate the theory by appending a new formula-statement to it."""
        assert isinstance(tup, FormulaStatement)
        # TODO: Check proof consistency / validity
        statement_formula = FormulaStatement((proves, self, tup))
        statement_counter = self._get_statement_counter()
        statement = StatementObsolete(self, statement_counter, statement_formula, justification)
        self.statements.append(statement)
        if Theory.echo_statement:
            print(statement.str(mod=rep_modes.definition))
        return statement

    def append_note(self, text):
        counter = self._get_statement_counter()
        note = Note(theory=self, position=counter, text=text)
        self.statements.append(note)
        if Theory.echo_statement:
            print(note.str(mod=rep_modes.definition))
        return note

    def append_objct(self, sym=None, dashed_name=None):
        counter = self._get_statement_counter()
        objct = ObjctDecl(theory=self, position=counter, sym=sym, dashed_name=dashed_name)
        self.statements.append(objct)
        if Theory.echo_statement:
            print(objct.str(mod=rep_modes.definition))
        return objct

    def append_relation(self, sym=None, dashed_name=None, formula_str_fun=None):
        counter = self._get_statement_counter()
        relation = RelDecl(theory=self, position=counter, sym=sym, dashed_name=dashed_name,
                           formula_str_fun=formula_str_fun)
        self.statements.append(relation)
        if Theory.echo_statement:
            print(relation.str(mod=rep_modes.definition))
        return relation

    def append_theory(self, dashed_name=None):
        counter = self._get_statement_counter()
        theory = Theory(theory=self, position=counter, dashed_name=dashed_name)
        self.statements.append(theory)
        if Theory.echo_statement:
            print(theory.str(mod=rep_modes.definition))
        return theory

    def append_variable(self, sym=None, dashed_name=None):
        counter = self._get_statement_counter()
        variable = VarDecl(theory=self, position=counter, sym=sym, dashed_name=dashed_name)
        self.statements.append(variable)
        if Theory.echo_statement:
            print(variable.str(mod=rep_modes.definition))
        return variable

    echo_init = True

    echo_statement = True

    @staticmethod
    def _get_counter():
        Theory.position = Theory.position + 1
        return Theory.position

    def _get_statement_counter(self):
        self._statement_max_position = self._statement_max_position + 1
        return self._statement_max_position

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} be a theory denoted as long-name ⌜ {self.dashed_name} ⌝, symbol ⌜ {self.sym} ⌝, and reference ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


universe_of_discourse = Theory(sym='𝒰', dashed_name='universe-of-discourse')
uod = universe_of_discourse

class_membership = uod.append_relation(sym='is-a', dashed_name='class-membership',
                                       formula_str_fun=formula_str_funs.infix)
"""
The class membership operator

Makes it possible to express membership to classes, such as natural numbers, truth values, etc.
"""

class_nature = uod.append_objct(sym='class', dashed_name='class')
"""
The nature of being a class.
"""

proves = uod.append_relation(sym='⊢', dashed_name='proof-operator',
                             formula_str_fun=formula_str_funs.infix)
"""
The proves operator
"""

axiom_truth = universe_of_discourse.append_axiom(
    text='If 𝕿 is a theory, if 𝖆 is an axiom, and if 𝕿 ⊢ 𝖆 is a statement in 𝕿, then 𝖆 is taken to be true in 𝕿.')
universe_of_discourse.append_axiom(axiom_truth)
