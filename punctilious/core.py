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


class Axiom:
    def __init__(self, text=None, citation=None):
        self.counter = self._get_counter()
        self.ref = f'axiom-{self.counter}'
        self.sym = f'𝒜{subscriptify(self.counter)}'
        self.text = text
        self.citation = citation
        if Axiom.echo_init:
            print(self.str(by_ref=False))

    def __repr__(self):
        return f'axiom {self.str()} ({self.uid})'

    def __str__(self):
        return self.str()

    _counter = 0

    echo_init = False

    def _get_counter(self):
        Axiom._counter = Axiom._counter + 1
        return Axiom._counter

    def str(self, by_ref=True, by_sym=False, **kwargs):
        if by_ref:
            return self.ref
        if by_sym:
            return self.sym
        else:
            citation = '' if self.citation is None else f' [{self.citation}]'
            return f'{self.str(by_ref=True)}: {self.text}{citation}'


class Objct:
    def __init__(self, sym, dashed_name, uid=None, parent_formula_default_str_fun=None):
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
        return f'{"(" if sub else ""}{formula.formula_tup[1].str(sub=True)} {formula.formula_tup[0].str(sub=True)} {formula.formula_tup[2].str(sub=True)}{")" if sub else ""}'

    @staticmethod
    def condensed_unary_postfix(formula, sub=False, **kwargs):
        """[relation, x] --> xrelation"""
        assert formula.first_level_cardinality == 2
        return f'{"(" if sub else ""}{formula.formula_tup[1].str(sub=True)}{formula.formula_tup[0].str(sub=True)}{")" if sub else ""}'

    @staticmethod
    def function(formula, **kwargs):
        """[relation, x, y, ...] --> relation(x, y, ...)"""
        assert formula.first_level_cardinality > 0
        relation = formula.formula_tup[0]
        arguments = ", ".join(argument.str(sub=True) for argument in formula.formula_tup[1:])
        return f'{relation}({arguments})'


class Formula:
    """The content of a formula is immutable. This is a key difference with theories."""

    def __init__(self, formula_tup):
        self.formula_tup = tuple() if formula_tup is None else \
            (tuple([formula_tup]) if not isinstance(formula_tup, tuple) else formula_tup)
        if Formula.echo:
            print(self.str())

    def __repr__(self):
        return f'formula {self.str()}'

    def __str__(self):
        return self.str()

    echo = False

    @property
    def first_level_cardinality(self):
        """The first-level-cardinality of a formula is the number
        of first-level components in the formula."""
        return len(self.formula_tup)

    def is_antivariable_equal_to(self, psi):
        """Two formula phi and psi are antivariable-equal if and only
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is antivariable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert psi.is_formula
        phi = self
        return all(phi_i.is_antivariable_equal_to(psi_i) for phi_i, psi_i in zip(phi.formula_tup, psi.formula_tup))

    is_formula = True
    """phi is a formula if and only if phi is a finite and ordered collection
    of formula and/or formula-atomic-components."""

    def is_variable_equal_to(self, psi):
        """Two formula phi and psi are variable-equal if and only if
        the first-level-cardinality of x and y are equal,
        and for i = 1 to first-level-cardinality of phi,
        phi_i is variable-equal with psi_i.
        Note: if x and y are antivariable-equal, they are variable-equal."""
        assert psi.is_formula
        phi = self
        return all(phi_i.is_variable_equal_to(psi_i) for phi_i, psi_i in zip(phi.formula_tup, psi.formula_tup))

    def str(self, sub=False, **kwargs):
        """
        Returns a string representation of the formula.

        :param sub: True if formula is a sub-formula embedded in a parent formula. Depending on preferences,
        this may result in the sub-formula being enclosed in parentheses to avoid ambiguity.
        :return: A string representation of the formula.
        """
        if len(self.formula_tup) == 1 and self.formula_tup[0].is_formula_atomic_component:
            return self.formula_tup[0].str(**kwargs)
        elif len(self.formula_tup) > 1 and self.formula_tup[0].is_object \
                and self.formula_tup[0].parent_formula_default_str_fun is not None:
            return self.formula_tup[0].parent_formula_default_str_fun(self, sub=sub, **kwargs)
        else:
            raise Exception("Oops, no str_fun was found to convert this formula to string.")


class JustificationMethod:

    def __init__(self, nam, template):
        self.nam = nam
        if isinstance(template, str):
            template = Template(template)
        self.template = template

    def str(self):
        return self.nam

    def __repr__(self):
        return f'justification method: {self.str()}'

    def __str__(self):
        return self.str()


is_axiom = JustificationMethod('axiom', 'By axiomatic choice.')
axiom_encoding = JustificationMethod('axiom-encoding', 'By encoding of $justifying_statement.')
statement_derivation = JustificationMethod('statement-derivation', 'By derivation from $justifying_statement.')


class Justification:
    def __init__(self, method, justifying_statement=None):
        assert isinstance(method, JustificationMethod)
        assert justifying_statement is None or isinstance(justifying_statement, Statement)
        assert not (method == is_axiom and justifying_statement is not None)
        assert not (method == axiom_encoding and justifying_statement is None)
        assert not (method == statement_derivation and justifying_statement is None)
        self.method = method
        self.justifying_statement = justifying_statement

    def str(self):
        return self.method.template.safe_substitute(
            justifying_statement=self.justifying_statement)

    def __repr__(self):
        return f'justification: {self.str()}'

    def __str__(self):
        return self.str()


class Statement:
    """A statement is tuple (t, ⊢, phi) where:
    t is a theory,
    ⊢ is the prove object,
    phi is a formula-variable."""

    """A formula A is a syntactic consequence within some formal system FS of a set Γ of formulas 
    if there is a formal proof in FS of A from the set Γ. This is denoted Γ ⊢FS A.
    Source: https://en.wikipedia.org/wiki/Logical_consequence"""

    """Does not prove symbol: ⊬.
    Prove symbol: ⊢."""

    def __init__(self, theory, counter, content, justification):
        assert isinstance(theory, Theory)
        assert isinstance(counter, int)
        assert isinstance(content, (Axiom, Formula))
        assert isinstance(justification, Justification)
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
        Statement._counter = Statement._counter + 1
        return Statement._counter

    def str(self, ref_only=True):
        if ref_only:
            return self.ref
        else:
            return f'{self.ref}: {self.content}      | {self.justification}'


class Theory(Objct):
    """The content of a theory is enriched by proofs. This is a key difference with formula whose content is
    immutable."""

    def __init__(self, sym=None, dashed_name=None):
        self.counter = Theory.get_counter()
        sym = f'𝒯{subscriptify(self.counter)}' if sym is None else sym
        dashed_name = f'theory-{self.counter}' if dashed_name is None else dashed_name
        super().__init__(sym=sym, dashed_name=dashed_name)
        self._statement_counter = 0
        self.statements = []
        if Theory.echo:
            print(self.str(let_definition=True))

    def __repr__(self):
        return f'theory {self}'

    def append_statement(self, statement_content, justification):
        """Elaborate the theory by appending a new statement to it."""
        assert isinstance(statement_content, Formula) or isinstance(statement_content, Axiom)
        # TODO: Check proof consistency / validity
        statement_formula = Formula((proves, self, statement_content))
        statement_counter = self._get_statement_counter()
        statement = Statement(self, statement_counter, statement_formula, justification)
        self.statements.append(statement)
        if Theory.echo_statement:
            print(statement.str(ref_only=False))
        return statement

    _counter = 0

    echo_axiom = False

    echo = True

    echo_statement = False

    @staticmethod
    def get_counter():
        Theory._counter = Theory._counter + 1
        return Theory._counter

    def _get_statement_counter(self):
        self._statement_counter = self._statement_counter + 1
        return self._statement_counter

    def str(self, by_dashed_name=False, by_ref=False, by_sym=True, **kwargs):
        if by_dashed_name:
            return self.dashed_name
        if by_ref:
            return self.ref
        if by_sym:
            return self.sym
        else:
            return f'Let {self.dashed_name}, also denoted as {self.ref} and {self.sym}, be a theory.'


class_membership = Objct(sym='is-a', dashed_name='class-membership', parent_formula_default_str_fun=FormulaStringFunctions.infix)
"""
The class membership operator

Makes it possible to express membership to classes, such as natural numbers, truth values, etc.
"""

class_nature = Objct(sym='class', dashed_name='class')
"""
The nature of being a class.
"""

proves = Objct(sym='⊢', dashed_name='proof-operator', parent_formula_default_str_fun=FormulaStringFunctions.infix)
"""
The proves operator
"""

Axiom.echo_init = True
axiom_truth = Axiom(
    text='If 𝕿 is a theory, if 𝖆 is an axiom, and if 𝕿 ⊢ 𝖆 is a statement in 𝕿, then 𝖆 is taken to be true in 𝕿.')
core_theory = Theory(dashed_name='core-theory')
core_theory.append_statement(axiom_truth, Justification(is_axiom))
