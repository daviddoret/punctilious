from __future__ import annotations

import abc
import collections
import dataclasses
import typing


class Connective:
    """A node color in a formula tree."""

    def __init__(self, rep: str):
        """

        :param rep: A default text representation of the connective.
        """
        self._rep = rep

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def rep(self, **kwargs):
        return self._rep

    def to_formula(self) -> Formula:
        return Formula(c=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return FormulaBuilder(c=self)


class TermsBuilder(list):
    """A mutable collection of formula terms."""

    def __init__(self, terms: FlexibleTerms = None):
        # When inheriting from list, we implement __init__ and not __new__.
        # Reference: https://stackoverflow.com/questions/9432719/python-how-can-i-inherit-from-the-built-in-list-type
        super().__init__(self)
        if isinstance(terms, collections.abc.Iterable):
            coerced_tuple = tuple(coerce_formula_builder(term) for term in terms)
            for term in coerced_tuple:
                self.append(term=term)
        elif terms is not None:
            raise ValueError()

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def append(self, term: FlexibleFormula):
        term = coerce_formula_builder(phi=term)
        super().append(term)

    def assure_term(self, i: int) -> None:
        """Assure the presence of an i-th term (i being the 0-based index).
        Nodes are initialized with None connective."""
        while len(self) <= i:
            self.append(FormulaBuilder())

    def rep(self, **kwargs) -> str:
        kwargs['parenthesis'] = True
        return ', '.join(term.rep(**kwargs) for term in self)

    @property
    def term_0(self) -> FormulaBuilder:
        self.assure_term(i=0)
        return self[0]

    @term_0.setter
    def term_0(self, term: FlexibleFormula):
        term = coerce_formula_builder(phi=term)
        if len(self) == 0:
            self.append(term)
        else:
            self[0] = term

    @property
    def term_1(self) -> FormulaBuilder:
        self.assure_term(i=1)
        return self[1]

    @term_1.setter
    def term_1(self, term: FlexibleFormula):
        term = coerce_formula_builder(phi=term)
        if len(self) < 2:
            if len(self) == 0:
                self.assure_term(i=0)
            self.append(term)
        else:
            self[1] = term

    def to_terms(self) -> Terms:
        """Return an immutable terms collection that is equivalent to this term-builder."""
        terms: tuple[Formula, ...] = tuple(coerce_formula(phi=term) for term in self)
        terms: Terms = Terms(terms=terms)
        return terms


class FormulaBuilder:
    """A mutable object to edit and elaborate formulas.
    Note: formula-builder may be syntactically inconsistent."""

    def __init__(self, c: typing.Optional[Connective] = None, terms: FlexibleTerms = None):
        """
        :param FlexibleTerms terms: A collection of terms."""
        self.c: typing.Optional[Connective] = c
        self.terms: TermsBuilder = coerce_terms_builder(terms=terms)

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def append_term(self, c: typing.Optional[Connective]) -> FormulaBuilder:
        t = FormulaBuilder(c=c)
        self.terms.append(t)
        return t

    def assure_term(self, i: int) -> None:
        self.terms.assure_term(i=i)

    def iterate_canonical(self):
        """A top-down, left-to-right iteration."""
        yield self
        for t in self.terms:
            yield from t.iterate_canonical()

    def rep(self, **kwargs):
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        if len(self.terms) == 0:
            return self.c.rep(**kwargs)
        if len(self.terms) == 2:
            return f'{"(" if parenthesis else ""}{self.term_0.rep(**kwargs)} {self.c.rep(**kwargs)} {self.term_1.rep(**kwargs)}{")" if parenthesis else ""}'
        else:
            return f'{"(" if parenthesis else ""}{self.c.rep(**kwargs)}({self.terms.rep(**kwargs)}){")" if parenthesis else ""}'

    @property
    def term_0(self) -> FormulaBuilder:
        """A shortcut for self.terms.term_0"""
        return self.terms.term_0

    @term_0.setter
    def term_0(self, term: FormulaBuilder) -> None:
        self.terms.term_0 = term

    @property
    def term_1(self) -> FormulaBuilder:
        """A shortcut for self.terms.term_1"""
        return self.terms.term_1

    @term_1.setter
    def term_1(self, term: FormulaBuilder) -> None:
        self.terms.term_1 = term

    def to_formula(self) -> Formula:
        terms: Terms = self.terms.to_terms()
        phi: Formula = Formula(c=self.c, terms=terms)
        return phi

    def validate_formula_builder(self) -> bool:
        """Validate the syntactical consistency of a candidate formula."""
        # TODO: validate_formula_builder: check no infinite loops
        # TODO: validate_formula_builder: check all nodes have a connective
        return True


class Terms(tuple):
    """An immutable collection of formula terms."""

    def __new__(cls, terms: FlexibleTerms = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        if isinstance(terms, collections.abc.Iterable):
            terms = tuple(coerce_formula(phi=term) for term in terms)
            return super().__new__(cls, terms)
        elif terms is None:
            return super().__new__(cls)
        else:
            raise ValueError()

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    def rep(self, **kwargs) -> str:
        kwargs['parenthesis'] = True
        return ', '.join(term.rep(**kwargs) for term in self)

    @property
    def term_0(self) -> Formula:
        # TODO: Terms.term_0: raise custom error if there is no term_0
        return self[0]

    @property
    def term_1(self) -> Formula:
        # TODO: Terms.term_1: raise custom error if there is no term_1
        return self[1]

    def to_terms_builder(self) -> TermsBuilder:
        """Return a mutable terms-builder that is equivalent to this terms."""
        terms: tuple[FormulaBuilder, ...] = tuple(coerce_formula_builder(phi=term) for term in self)
        terms: TermsBuilder = TermsBuilder(terms=terms)
        return terms


class Formula:
    """An immutable formula modeled as an edge-ordered, node-colored tree."""

    def __init__(self, c: Connective, terms: typing.Optional[Terms] = None):
        if terms is None:
            terms = Terms()
        self._c = c
        self._terms = terms

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def arity(self) -> int:
        """The arity of a formula is equal to the number of terms that are direct children of its root node."""
        return len(self.terms)

    @property
    def c(self) -> Connective:
        return self._c

    def rep(self, **kwargs) -> str:
        kwargs['parenthesis'] = True
        return f'{self.c.rep(**kwargs)}({self.terms.rep(**kwargs)})'

    @property
    def term_0(self) -> Formula:
        """A shortcut for Formula.terms.term_0."""
        return self.terms.term_0

    @property
    def term_1(self) -> Formula:
        return self.terms.term_1

    @property
    def terms(self) -> Terms:
        return self._terms

    def to_formula_builder(self) -> FormulaBuilder:
        """Returns a formula-builder that is equivalent to this formula.
        This makes it possible to edit the formula-builder to elaborate new formulas."""
        terms: TermsBuilder = self.terms.to_terms_builder()
        phi: FormulaBuilder = FormulaBuilder(c=self.c, terms=terms)
        return phi


def coerce_terms(terms: FlexibleTerms = None) -> Terms:
    if isinstance(terms, Terms):
        return terms
    elif isinstance(terms, TermsBuilder):
        return terms.to_terms()
    elif terms is None:
        return Terms()
    else:
        return Terms(*terms)


def coerce_terms_builder(terms: FlexibleTerms = None):
    if isinstance(terms, TermsBuilder):
        return terms
    elif isinstance(terms, Terms):
        return terms.to_terms_builder()
    elif terms is None:
        return TermsBuilder()
    else:
        return TermsBuilder(terms=terms)


def coerce_formula_builder(phi: FlexibleFormula = None):
    if isinstance(phi, FormulaBuilder):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula_builder()
    elif isinstance(phi, Formula):
        return phi.to_formula_builder()
    elif phi is None:
        return FormulaBuilder()
    else:
        raise TypeError()


def coerce_formula(phi: FlexibleFormula):
    if isinstance(phi, Formula):
        return phi
    elif isinstance(phi, Connective):
        return phi.to_formula()
    elif isinstance(phi, FormulaBuilder):
        return phi.to_formula()
    else:
        raise TypeError()


FlexibleFormula = typing.Optional[typing.Union[Connective, Formula, FormulaBuilder]]
FlexibleTerms = typing.Optional[typing.Union[typing.Iterable, Terms, TermsBuilder]]


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective with a constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self, rep: str, fixed_arity_constraint: int):
        self._fixed_arity_constraint = fixed_arity_constraint
        super().__init__(rep=rep)

    @property
    def fixed_arity_constraint(self) -> int:
        return self._fixed_arity_constraint


class NullaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=0)


class SimpleObject(NullaryConnective):
    """An alias for nullary-connective."""
    pass


class UnaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=1)


class InfixPartialFormula:
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and glueing all this together with the InfixPartialFormula class.
    """

    def __init__(self, c: Connective, term_1: FlexibleFormula):
        self._c = c
        self._term_1 = term_1

    def __or__(self, term_2: FlexibleFormula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and glueing all this together with the InfixPartialFormula class.
        """
        return FormulaBuilder(c=self._c, terms=[self.term_1, term_2])

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def c(self) -> Connective:
        return self._c

    def rep(self, **kwargs):
        kwargs['parenthesis'] = True
        return f'{self.c.rep(**kwargs)}({self.term_1.rep(**kwargs)}, ?)'

    @property
    def term_1(self) -> Connective:
        return self._term_1


class BinaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=2)

    def __ror__(self, other: FlexibleFormula):
        """Pseudo math notation. x | p | ?."""
        return InfixPartialFormula(c=self, term_1=other)


class TernaryConnective(FixedArityConnective):

    def __init__(self, rep: str):
        super().__init__(rep=rep, fixed_arity_constraint=3)


def let_x_be_a_variable(rep: str):
    return NullaryConnective(rep=rep)


def let_x_be_a_simple_object(rep: str):
    return SimpleObject(rep=rep)


def let_x_be_a_binary_connective(rep: str):
    return BinaryConnective(rep=rep)


def let_x_be_a_ternary_connective(rep: str):
    return TernaryConnective(rep=rep)


def let_x_be_a_unary_connective(rep: str):
    return UnaryConnective(rep=rep)


class Connectives(typing.NamedTuple):
    collection: Connective
    implies: Connective
    inference_rule: Connective
    is_a: Connective


def is_connective_equivalent(c: Connective, d: Connective) -> bool:
    """Two connectives are connective-equivalent if and only if they are the same object."""
    return c is d


def is_formula_equivalent(phi: FlexibleFormula, psi: FlexibleFormula) -> bool:
    """Two formulas phi and psi are formula-equivalent if and only if:
    Base case:
     - phi connective = psi connective
     - phi arity = 0
     - psi arity = 0
     Inductive step:
     - phi connective = psi connective
     - phi arity = psi arity
     - following order, for all child formula phi' in phi, the child formula psi' in psi is formula-equivalent
     Extreme case:
     - otherwise phi and psi are not formula-equivalent.

    :param phi:
    :param psi:
    :return:
    """
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    if (is_connective_equivalent(c=phi.c, d=psi.c)) and (phi.arity == 0) and (psi.arity == 0):
        # Base case
        return True
    elif (is_connective_equivalent(c=phi.c, d=psi.c)) and (phi.arity == psi.arity) and all(
            is_formula_equivalent(phi=phi_prime, psi=psi_prime) for phi_prime, psi_prime in zip(phi.terms, psi.terms)):
        # Inductive step
        return True
    else:
        # Extreme case
        return False


connectives = Connectives(
    collection=let_x_be_a_binary_connective(rep=', '),
    implies=let_x_be_a_binary_connective(rep='implies'),
    inference_rule=let_x_be_a_ternary_connective(rep='inference-rule'),
    is_a=let_x_be_a_binary_connective(rep='is-a')
)


class InferenceRuleBuilder(FormulaBuilder):
    def __init__(self, premises: typing.Optional[typing.Iterable[FlexibleFormula, ...]], conclusion: FlexibleFormula,
                 variables: typing.Optional[typing.Iterable[FlexibleFormula, ...]]):
        premises: FormulaBuilder = FormulaBuilder(c=connectives.collection, terms=premises)
        variables: FormulaBuilder = FormulaBuilder(c=connectives.collection, terms=variables)
        super().__init__(c=connectives.inference_rule, terms=[premises, conclusion, variables])

    @property
    def conclusion(self) -> FormulaBuilder:
        return self.terms[1]

    @property
    def premises(self) -> FormulaBuilder:
        return self.terms[0]

    @property
    def variables(self) -> FormulaBuilder:
        return self.terms[2]

# x = let_x_be_a_variable(rep='x')
# x | connectives.is_a | y
# ir = InferenceRuleBuilder()
