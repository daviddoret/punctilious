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


class FormulaBuilder(list):
    """A mutable object to edit and elaborate formulas.
    Note: formula-builder may be syntactically inconsistent."""

    def __init__(self, c: typing.Optional[Connective] = None, terms: FlexibleElements = None):
        """
        :param FlexibleTerms terms: A collection of terms."""
        self.c: typing.Optional[Connective] = c

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

    def append(self, term: FlexibleFormula) -> FormulaBuilder:
        """Append a new term to the formula."""
        term = coerce_formula_builder(phi=term)
        super().append(term)
        return term

    def assure_term(self, i: int) -> None:
        """Assure the presence of an i-th term (i being the 0-based index).
        Nodes are initialized with None connective."""
        while len(self) <= i:
            self.append(FormulaBuilder())

    def iterate_canonical(self):
        """A top-down, left-to-right iteration."""
        yield self
        for t in self:
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

    def to_formula(self) -> Formula:
        terms: tuple[Formula, ...] = tuple(coerce_formula(phi=term) for term in self)
        phi: Formula = Formula(c=self.c, terms=terms)
        return phi

    def validate_formula_builder(self) -> bool:
        """Validate the syntactical consistency of a candidate formula."""
        # TODO: validate_formula_builder: check no infinite loops
        # TODO: validate_formula_builder: check all nodes have a connective
        return True


class Formula(tuple):
    """An immutable formula modeled as an edge-ordered, node-colored tree."""

    def __new__(cls, c: Connective, terms: FlexibleElements = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple
        if isinstance(terms, collections.abc.Iterable):
            elements = tuple(coerce_formula(phi=term) for term in terms)
            o = super().__new__(cls, elements)
        elif terms is None:
            o = super().__new__(cls)
        else:
            raise ValueError()
        return o

    def __init__(self, c: Connective, terms: FlexibleElements = None):
        self._c = c

    def __repr__(self):
        return self.rep()

    def __str__(self):
        return self.rep()

    @property
    def arity(self) -> int:
        """The arity of a formula is equal to the number of terms that are direct children of its root node."""
        return len(self)

    @property
    def c(self) -> Connective:
        return self._c

    def rep(self, **kwargs) -> str:
        kwargs['parenthesis'] = True
        terms: str = ', '.join(term.rep(**kwargs) for term in self)
        return f'{self.c.rep(**kwargs)}({terms})'

    @property
    def term_0(self) -> Formula:
        # TODO: Terms.term_0: raise custom error if there is no term_0
        return self[0]

    @property
    def term_1(self) -> Formula:
        # TODO: Terms.term_1: raise custom error if there is no term_1
        return self[1]

    def to_formula_builder(self) -> FormulaBuilder:
        """Returns a formula-builder that is equivalent to this formula.
        This makes it possible to edit the formula-builder to elaborate new formulas."""
        terms: tuple[FormulaBuilder, ...] = tuple(coerce_formula_builder(phi=term) for term in self)
        phi: FormulaBuilder = FormulaBuilder(c=self.c, terms=terms)
        return phi


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


class FreeArityConnective(Connective):
    """A free-arity connective is a connective without constraint on its arity,
    that is its number of descendant notes."""

    def __init__(self, rep: str):
        super().__init__(rep=rep)


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


def let_x_be_a_free_arity_connective(rep: str):
    return FreeArityConnective(rep=rep)


class Connectives(typing.NamedTuple):
    collection: FreeArityConnective
    implies: BinaryConnective
    inference_rule: TernaryConnective
    is_a: BinaryConnective
    transformation: TernaryConnective


connectives = Connectives(
    transformation=let_x_be_a_ternary_connective(rep='transformation'),
    collection=let_x_be_a_free_arity_connective(rep='collection'),
    implies=let_x_be_a_binary_connective(rep='implies'),
    inference_rule=let_x_be_a_ternary_connective(rep='inference-rule'),
    is_a=let_x_be_a_binary_connective(rep='is-a')
)


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
            is_formula_equivalent(phi=phi_prime, psi=psi_prime) for phi_prime, psi_prime in zip(phi, psi)):
        # Inductive step
        return True
    else:
        # Extreme case
        return False


class CollectionBuilder(FormulaBuilder):
    """A utility class to help build collections. It is mutable and thus allows edition."""

    def __init__(self, terms: typing.Optional[typing.Iterable[FlexibleFormula, ...]]):
        super().__init__(c=connectives.collection, terms=terms)

    def to_collection(self) -> Collection:
        elements: tuple[Formula, ...] = tuple(coerce_formula(phi=element) for element in self)
        phi: Collection = Collection(elements=elements)
        return phi

    def to_formula(self) -> Formula:
        """Return a Collection."""
        return self.to_collection()


class Collection(Formula):
    """A collection is a formula c(t0, t1, ..., tn) where:
     - c is a node with the collection connective.
     - ti is a formula.

     The empty-collection is the collection c()."""

    def __new__(cls, elements: FlexibleCollection = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, c=connectives.collection, terms=elements)
        return o

    def __init__(self, elements: FlexibleCollection = None):
        super().__init__(c=connectives.collection, terms=elements)


FlexibleCollection = typing.Optional[typing.Union[Collection, typing.Iterable[FlexibleFormula]]]


class TransformationBuilder(FormulaBuilder):

    def __init__(self, premises: typing.Optional[typing.Iterable[FlexibleFormula]], conclusion: FlexibleFormula,
                 variables: typing.Optional[typing.Iterable[FlexibleFormula]]):
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


class Transformation:
    """A transformation is a formula t(P, c, V) where:
     - t has the transformation connective,
     - P is a collection-formula whose children are called premises,
     - c is a formula called conclusion,
     - V is a collection-formula whose children are variables.
    From a transformation, the following algorithm is derived:
    Phi --> psi
    t(Phi) --> psi
    map every formula in Phi collection in-order with the premises
    confirm that they are formula-with-variables-equivalent
    confirm that every variable has strictly one mapped formula
    map all variables with their respective formulas
    return the conclusion by substituting variables with formulas
    # TODO: Transformation: rewrite the above clearly
    """
    pass

# x = let_x_be_a_variable(rep='x')
# x | connectives.is_a | y
# ir = InferenceRuleBuilder()
