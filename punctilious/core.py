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

    objct = Cat(cod='objct', ref_prefix='objct', sym_prefix='ℴ')
    """An object declaration statement."""

    note = Cat(cod='note', ref_prefix='note', sym_prefix='𝒩')
    """A textual note that is not formally part of the theory but may shed light on the theory for human readers."""

    proposition = Cat('proposition')
    """."""

    theorem = Cat('theorem')
    """."""

    theory = Cat(cod='theory', ref_prefix='theory', sym_prefix='𝔗')
    """A theory."""


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

    def __init__(self, theory, cat, counter, ref=None, sym=None, dashed_name=None):
        assert isinstance(theory, Theory) or theory is None  # The only object for which no theory linkage is
        # justified is the universe-of-discourse theory.
        assert isinstance(cat, Cat)
        self.theory = theory
        self.cat = cat
        self.counter = counter
        if cat == cats.theory:
            # Theories have a simplified reference scheme: theory-n where n is the theory counter.
            self.ref = f'{self.cat.ref_prefix}-{self.counter}' if ref is None else ref
        else:
            # Non-theories have a reference scheme linked to their parent theory: theory-n-i where n is the theory
            # counter and i is the statement counter.
            self.ref = f'{self.cat.ref_prefix}-{self.theory.counter}-{self.counter}' if ref is None else ref
        self.sym = f'{self.cat.sym_prefix}{subscriptify(self.counter)}' if sym is None else sym
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
    def __init__(self, theory, counter, ref=None, text=None):
        cat = cats.note
        super().__init__(theory=theory, cat=cat, counter=counter, ref=ref)
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
    def __init__(self, theory, counter, ref=None, sym=None, text=None, citation=None):
        cat = cats.axiom
        super().__init__(theory=theory, cat=cat, counter=counter, ref=ref, sym=sym)
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


class Objct(Statement):
    def __init__(self, theory, counter, ref=None, sym=None, dashed_name=None):
        cat = cats.objct
        super().__init__(theory=theory, cat=cat, counter=counter, ref=ref, sym=sym, dashed_name=dashed_name)

    def __str__(self):
        return self.str()

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} by an object denoted as ⌜ {self.dashed_name} ⌝, ⌜ {self.sym} ⌝, and ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


class ObjctObsolete:
    def __init__(self, sym=None, dashed_name=None, uid=None, parent_formula_default_str_fun=None):
        self.uid = uuid.uuid4() if uid is None else uid
        self.sym = sym
        self.dashed_name = dashed_name
        self.parent_formula_default_str_fun = parent_formula_default_str_fun
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


class Variable:
    def __init__(self, nam=None, alt_nam_dic=None, uid=None):
        self.uid = uuid.uuid4() if uid is None else uid
        self.nam = "x" if nam is None else nam
        self.alt_nam_dic = {} if alt_nam_dic is None else alt_nam_dic

    def __repr__(self):
        return f'variable {self.str()} ({self.uid})'

    def __str__(self):
        return self.str()

    def is_antivariable_equal_to(self, y):
        """Two formula-atomic-components x and y are antivariable-equal if and only
        x and y are objcts (ie neither is a variable),
        and x and y are references to the same objct.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert y.is_formula_atomic_component
        return False

    is_formula_atomic_component = True
    """x is a formula-atomic-component if and only if it is an object or a variable."""

    is_object = False

    is_variable = True

    def is_variable_equal_to(self, y):
        """Two formula-atomic-components x and y are variable-equal if and only if
        x or y or both are variables or x and y are antivariable-equal.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert y.is_formula_atomic_component
        return True

    def str(self, **kwargs):
        return self.nam


class FormulaStringFunctions:

    @staticmethod
    def infix(formula, sub=False, **kwargs):
        """[relation, x, y] --> x relation y"""
        assert formula.first_level_cardinality == 3
        return f'{"(" if sub else ""}{formula.content[1].str(sub=True, mod=rep_modes.sym)} {formula.content[0].str(sub=True, mod=rep_modes.sym)} {formula.content[2].str(sub=True, mod=rep_modes.sym)}{")" if sub else ""}'

    @staticmethod
    def condensed_unary_postfix(formula, sub=False, **kwargs):
        """[relation, x] --> xrelation"""
        assert formula.first_level_cardinality == 2
        return f'{"(" if sub else ""}{formula.content[1].str(sub=True, mod=rep_modes.sym)}{formula.content[0].str(sub=True, mod=rep_modes.sym)}{")" if sub else ""}'

    @staticmethod
    def function(formula, **kwargs):
        """[relation, x, y, ...] --> relation(x, y, ...)"""
        assert formula.first_level_cardinality > 0
        relation = formula.content[0]
        arguments = ", ".join(argument.str(sub=True) for argument in formula.content[1:])
        return f'{relation}({arguments})'


class FreeFormula:
    """A free-formula 𝜑 is a formula linked to a theory but not stated as a statement.

    Data structure:
    A free-formula 𝜑 is a container for a python tuple,
    which is either of the form (o) where o is an object,
    of the form (x) where x is a variable,
    or of the form (a, b, c, ...) where a, b, c, ... are free-formulas.
    """

    def __init__(self, tup):
        if isinstance(tup, (Objct, Variable)):
            # If a leaf formula was passed as an instance of Objct or Variable,
            # pack it in a tuple for data structure consistency.
            tup = tuple([tup])
        assert tup is not None and isinstance(tup, tuple) and len(tup) > 0
        self.is_leaf = True if len(tup) == 1 else False
        if len(tup) == 1:
            assert isinstance(tup, (Objct, Variable))
            self.tup = tup
        else:
            tup = (
                subformula if isinstance(subformula, FreeFormula)
                else FreeFormula(subformula) for subformula in tup)
            self.tup = tup

    @property
    def first_level_cardinality(self):
        """The first-level-cardinality of a formula is the number
        of first-level components in the formula."""
        return len(self.tup)

    def is_antivariable_equal_to(self, psi):
        """Two formula phi and psi are antivariable-equal if and only
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is antivariable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert psi is not None and isinstance(psi, FreeFormula)
        phi = self
        if phi.first_level_cardinality != psi.first_level_cardinality:
            return False
        elif phi.is_leaf:
            # We assume that objcts and variables are theory-singletons,
            # i.e. they are not instanciated multiple times in the theory,
            # and thus we may rely on the python is operator to check equality.
            return phi.tup[0] is psi.tup[0]
        else:
            XXXXX RESUME HERE XXXXX
            return all(phi_i.is_antivariable_equal_to(psi_i) for phi_i, psi_i in zip(phi.tup, psi.tup))

    def is_variable_equal_to(self, psi):
        """Two formula phi and psi are variable-equal if and only if
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is variable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert psi is not None and isinstance(psi, FreeFormula)
        phi = self
        return all(phi_i.is_variable_equal_to(psi_i) for phi_i, psi_i in zip(phi.tup, psi.tup))


class FormulaStatement(Statement):
    """The content of a formula is immutable. This is a key difference with theories."""

    def __init__(self, theory, counter, ref=None, sym=None, free_formula=None, justif=None):
        cat = cats.formula_statement
        super().__init__(theory=theory, cat=cat, counter=counter, ref=ref, sym=sym)
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

    def str(self, mod=None, sub=False, **kwargs):
        """
        Returns a string representation of the formula.

        :param mod:
        :param sub: True if formula is a sub-formula embedded in a parent formula. Depending on preferences,
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
                        and self.content[0].parent_formula_default_str_fun is not None:
                    return self.content[0].parent_formula_default_str_fun(self, sub=sub, sym=True, **kwargs)
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


class StatementObsolete:
    """A statement is tuple (t, ⊢, phi) where:
    t is a theory,
    ⊢ is the prove object,
    phi is a formula-variable."""

    """A formula A is a syntactic consequence within some formal system FS of a set Γ of formulas 
    if there is a formal proof in FS of A from the set Γ. This is denoted Γ ⊢FS A.
    Source: https://en.wikipedia.org/wiki/Logical_consequence"""

    """Does not prove symbol: ⊬.
    Prove symbol: ⊢."""

    def __init__(self, theory, counter, content, justification, cat=None):
        assert isinstance(theory, Theory)
        assert isinstance(counter, int)
        # assert isinstance(content, (Axiom, Formula))
        # assert isinstance(justification, Justification)
        self.cat = cat
        self.theory = theory
        self.counter = counter
        self.ref = f'statement-{self.theory.counter}-{self.counter}'
        self.content = content
        self.justification = justification

    def __str__(self):
        return self.str()

    def __repr__(self):
        return f'statement: {self.str()}'

    @staticmethod
    def get_counter():
        StatementObsolete._counter = StatementObsolete._counter + 1
        return StatementObsolete._counter

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        match mod:
            case rep_modes.sym:
                raise Exception('The symbol representation mode is not supported for statements.')
            case rep_modes.ref:
                return self.ref
            case rep_modes.dashed_name:
                raise Exception('The dashed-name representation mode is not supported for statements.')
            case rep_modes.definition:
                if self.cat == cats.note:
                    return self.content.str(mod=rep_modes.definition)
                else:
                    return f'{self.ref}: {self.content} | {self.justification}'


class Theory(Statement):
    """The content of a theory is enriched by proofs. This is a key difference with formula whose content is
    immutable."""

    def __init__(self, theory=None, counter=None, ref=None, sym=None, dashed_name=None):
        cat = cats.theory
        counter = Theory._get_counter() if counter is None else counter
        super().__init__(theory=theory, cat=cat, counter=counter, ref=ref, sym=sym, dashed_name=dashed_name)
        self._statement_counter = 0  # TODO: replace this with the computation of max + 1 from statements list.
        self.statements = []
        self.free_formulas = []
        if theory is None:
            # This theory is not linked to a parent theory,
            # in consequence it will not be output as part of the append_theory method,
            # thus we output the theory definition here.
            print(self.str(mod=rep_modes.definition))

    _counter = 0

    def append_axiom(self, text, citation=None):
        counter = self._get_statement_counter()
        axiom = Axiom(theory=self, counter=counter, text=text)
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

    def assure_free_formula(self, tup):
        pass

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
        note = Note(theory=self, counter=counter, text=text)
        self.statements.append(note)
        if Theory.echo_statement:
            print(note.str(mod=rep_modes.definition))
        return note

    def append_objct(self, sym=None, dashed_name=None):
        counter = self._get_statement_counter()
        objct = Objct(theory=self, counter=counter, sym=sym, dashed_name=dashed_name)
        self.statements.append(objct)
        if Theory.echo_statement:
            print(objct.str(mod=rep_modes.definition))
        return objct

    def append_theory(self, dashed_name=None):
        counter = self._get_statement_counter()
        theory = Theory(theory=self, counter=counter, dashed_name=dashed_name)
        self.statements.append(theory)
        if Theory.echo_statement:
            print(theory.str(mod=rep_modes.definition))
        return theory

    echo_init = True

    echo_statement = True

    @staticmethod
    def _get_counter():
        Theory._counter = Theory._counter + 1
        return Theory._counter

    def _get_statement_counter(self):
        self._statement_counter = self._statement_counter + 1
        return self._statement_counter

    def str(self, mod=None, **kwargs):
        mod = rep_modes.ref if mod is None else mod
        assert isinstance(mod, RepMode)
        assert mod in (rep_modes.ref, rep_modes.sym, rep_modes.dashed_name, rep_modes.definition)
        match mod:
            case rep_modes.definition:
                return f'Let {self.dashed_name} by a theory denoted as ⌜ {self.dashed_name} ⌝, ⌜ {self.sym} ⌝, and ⌜ {self.ref} ⌝.'
            case _:
                return super().str(mod=mod, **kwargs)


universe_of_discourse = Theory(sym='𝒰', dashed_name='universe-of-discourse')

class_membership = ObjctObsolete(sym='is-a', dashed_name='class-membership',
                                 parent_formula_default_str_fun=FormulaStringFunctions.infix)
"""
The class membership operator

Makes it possible to express membership to classes, such as natural numbers, truth values, etc.
"""

class_nature = ObjctObsolete(sym='class', dashed_name='class')
"""
The nature of being a class.
"""

proves = ObjctObsolete(sym='⊢', dashed_name='proof-operator',
                       parent_formula_default_str_fun=FormulaStringFunctions.infix)
"""
The proves operator
"""

axiom_truth = universe_of_discourse.append_axiom(
    text='If 𝕿 is a theory, if 𝖆 is an axiom, and if 𝕿 ⊢ 𝖆 is a statement in 𝕿, then 𝖆 is taken to be true in 𝕿.')
universe_of_discourse.append_axiom(axiom_truth)
