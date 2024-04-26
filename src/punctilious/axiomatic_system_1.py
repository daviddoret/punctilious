from __future__ import annotations

import abc
import collections
import dataclasses
import typing
import warnings


class CustomException(Exception):
    """A punctilious generic exception."""

    def __init__(self, message: str, **kwargs):
        self.message = message
        self.kwargs = kwargs
        super().__init__()

    def __str__(self) -> str:
        return self.rep()

    def __repr__(self) -> str:
        return self.rep()

    def rep(self) -> str:
        return ', '.join(f'{key}: {value}' for key, value in self.kwargs.items())


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

    def __init__(self, c: typing.Optional[Connective] = None, terms: FlexibleTupl = None):
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

    def rep(self, **kwargs) -> str:
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        if isinstance(self.c, NullaryConnective):
            return f'{self.c.rep()}'
        elif isinstance(self.c, BinaryConnective):
            term_0: str = self.term_0.rep(**kwargs) if self.term_0 is not None else '?'
            term_1: str = self.term_1.rep(**kwargs) if self.term_1 is not None else '?'
            return f'{'(' if parenthesis else ''}{term_0} {self.c.rep()} {term_1}{')' if parenthesis else ''}'
        else:
            c: str = self.c.rep(**kwargs) if self.c is not None else '?'
            terms: str = ', '.join(term.rep(**kwargs) if term is not None else '?' for term in self)
            return f'{'(' if parenthesis else ''}{c}({terms}){')' if parenthesis else ''}'

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

    def __new__(cls, c: Connective, terms: FlexibleTupl = None):
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

    def __init__(self, c: Connective, terms: FlexibleTupl = None):
        self._c = c

    def __eq__(self, other):
        """python-equality of formulas is not formula-equivalence."""
        return self is other

    def __hash__(self):
        """python-equality of formulas is not formula-equivalence."""
        return hash(id(self))

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
        parenthesis = kwargs.get('parenthesis', False)
        kwargs['parenthesis'] = True
        if isinstance(self.c, NullaryConnective):
            return f'{self.c.rep()}'
        elif isinstance(self.c, BinaryConnective):
            return f'{'(' if parenthesis else ''}{self.term_0.rep(**kwargs)} {self.c.rep()} {self.term_1.rep(**kwargs)}{')' if parenthesis else ''}'
        else:
            terms: str = ', '.join(term.rep(**kwargs) for term in self)
            return f'{'(' if parenthesis else ''}{self.c.rep(**kwargs)}({terms}){')' if parenthesis else ''}'

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


def coerce_enumeration(elements: FlexibleEnumeration):
    """Coerce elements to an enumeration.
    If elements is None, coerce it to an empty enumeration."""
    if isinstance(elements, Enumeration):
        return elements
    elif isinstance(elements, EnumerationBuilder):
        return elements.to_enumeration()
    elif elements is None:
        return Enumeration(elements=None)
    elif isinstance(elements, typing.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return Enumeration(elements=elements)
    else:
        raise TypeError(f'elements cannot be coerced to enumeration')


def coerce_enumeration_builder(elements: FlexibleEnumeration):
    if isinstance(elements, EnumerationBuilder):
        return elements
    elif isinstance(elements, Enumeration):
        return elements.to_enumeration_builder()
    elif elements is None:
        return EnumerationBuilder(elements=None)
    elif isinstance(elements, typing.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return EnumerationBuilder(elements=elements)
    else:
        raise TypeError(f'elements cannot be coerced to enumeration')


def coerce_map(m: FlexibleMap):
    if isinstance(m, Map):
        return m
    elif isinstance(m, MapBuilder):
        return m.to_map()
    elif isinstance(m, dict):
        domain: Enumeration = coerce_enumeration(elements=m.keys())
        codomain: Tupl = coerce_tupl(elements=m.values())
        return Map(domain=domain, codomain=codomain)
    else:
        raise TypeError('m could not be safely coerced to map.')


def coerce_tupl(elements: FlexibleTupl):
    if isinstance(elements, Tupl):
        return elements
    elif isinstance(elements, TuplBuilder):
        return elements.to_tupl()
    elif elements is None:
        return Tupl(elements=None)
    elif isinstance(elements, collections.abc.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return Tupl(elements=elements)
    else:
        raise TypeError('elements could not be safely coerced to tuple.')


def coerce_tupl_builder(elements: FlexibleTupl):
    if isinstance(elements, TuplBuilder):
        return elements
    elif isinstance(elements, Tupl):
        return elements.to_tupl_builder()
    elif elements is None:
        return TuplBuilder(elements=None)
    elif isinstance(elements, collections.abc.Iterable):
        """This may be ambiguous when we pass a single formula (that is natively iterable)."""
        return TuplBuilder(elements=elements)
    else:
        raise TypeError('elements could not be safely coerced to tuple.')


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
        return Formula(c=self._c, terms=[self.term_1, term_2])

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
    return Formula(c=NullaryConnective(rep=rep))


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
    enumeration: FreeArityConnective
    implies: BinaryConnective
    inference_rule: TernaryConnective
    is_a: BinaryConnective
    map: BinaryConnective
    transformation: TernaryConnective
    tupl: FreeArityConnective


connectives = Connectives(
    enumeration=let_x_be_a_free_arity_connective(rep='enumeration'),
    implies=let_x_be_a_binary_connective(rep='implies'),
    inference_rule=let_x_be_a_ternary_connective(rep='inference-rule'),
    is_a=let_x_be_a_binary_connective(rep='is-a'),
    map=let_x_be_a_binary_connective(rep='map'),
    transformation=let_x_be_a_ternary_connective(rep='transformation'),
    tupl=let_x_be_a_free_arity_connective(rep='tuple')
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


def is_formula_equivalent_with_variables(phi: FlexibleFormula, psi: FlexibleFormula, v: FlexibleEnumeration,
                                         variables_map: dict[Formula, Formula] = None):
    """Two formulas phi and psi are formula-equivalent-with-variables with regards to variables V if and only if:
     - All formulas in V are not sub-formula of phi,
     - We declare a new formula psi' where every sub-formula that is an element of V,
       is substituted by the formula that is at the exact same position in the tree.
     - And the phi and psi' are formula-equivalent.

     Note: is-formula-equivalent-with-variables is not commutative.

    :param phi:
    :param psi:
    :param v:
    :param variables_map: (conditional) a mapping between variables and their assigned values.
    :return:
    """
    if variables_map is None:
        variables_map: dict[Formula, Formula] = dict()
    phi: Formula = coerce_formula(phi=phi)
    psi: Formula = coerce_formula(phi=psi)
    psi_value: Formula
    v: Tupl = coerce_tupl(elements=v)
    if phi in v:
        # Sub-formulas in phi cannot be elements of variables.
        return False
    if psi in v:
        # psi is a variable
        if psi in variables_map.items():
            # psi's value is already mapped
            if is_formula_equivalent(psi, variables_map[psi]):
                # psi is consistent with its mapped value
                # substitute the variable with its value
                # print(f'variable {psi}')
                psi_value: Formula = variables_map[psi]
                # print(f'    substituted with {psi}.')
            else:
                # psi is not consistent with its mapped value
                return False
        else:
            # print(f'variable {psi}')
            # substitute the variable with its value
            # set the variable value
            psi_value = phi
            variables_map[psi] = psi_value
            # print(f'    set to {phi}.')
    else:
        psi_value = psi
    if (is_connective_equivalent(c=phi.c, d=psi_value.c)) and (phi.arity == 0) and (psi_value.arity == 0):
        # Base case
        return True
    elif (is_connective_equivalent(c=phi.c, d=psi_value.c)) and (phi.arity == psi_value.arity) and all(
            is_formula_equivalent_with_variables(phi=phi_prime, psi=psi_prime, v=v, variables_map=variables_map) for
            phi_prime, psi_prime in zip(phi, psi_value)):
        # Inductive step
        return True
    else:
        # Extreme case
        return False


def assert_formula_equivalent_with_variables(phi: FlexibleFormula, psi: FlexibleFormula,
                                             v: FlexibleEnumeration, variables_map: dict[Formula, Formula] = None):
    output: bool = is_formula_equivalent_with_variables(phi=phi, psi=psi, v=v, variables_map=variables_map)
    if not output:
        raise CustomException(
            message='Formulas phi and psi are not formula-equivalent-with-variables with regards to variables v.',
            phi=phi, psi=psi, v=v)


def is_enumeration_equivalent(phi: FlexibleEnumeration, psi: FlexibleEnumeration) -> bool:
    """Two enumerations phi and psi are enumeration-equivalent if and only if:
     - for every sub-formula phi' in phi, there is a formula-equivalent sub-formula psi' in psi.
     - for every sub-formula psi' in psi, there is a formula-equivalent sub-formula phi' in phi.

    :param phi:
    :param psi:
    :return:
    """
    phi: Formula = coerce_enumeration(elements=phi)
    psi: Formula = coerce_enumeration(elements=psi)

    test_1 = all(any(is_formula_equivalent(phi=phi_prime, psi=psi_prime) for psi_prime in psi) for phi_prime in phi)
    test_2 = all(any(is_formula_equivalent(phi=psi_prime, psi=phi_prime) for phi_prime in phi) for psi_prime in psi)

    return test_1 and test_2


def replace_formulas(phi: FlexibleFormula, m: FlexibleMap) -> Formula:
    """Performs a top-down, left-to-right replacement of formulas in formula phi."""
    phi: Formula = coerce_formula(phi=phi)
    m: Map = coerce_map(m=m)
    if m.is_defined_in(phi=phi):
        # phi must be replaced at its root.
        # the replacement algorithm stops right there (i.e.: no more recursion).
        assigned_value: Formula = m.get_assigned_value(phi=phi)
        return assigned_value
    else:
        # build the replaced formula.
        fb: FormulaBuilder = FormulaBuilder(c=phi.c)
        # recursively apply the replacement algorithm on phi terms.
        for term in phi:
            term_substitute = replace_formulas(phi=term, m=m)
            fb.append(term=term_substitute)
        return fb.to_formula()


class TuplBuilder(FormulaBuilder):
    """A utility class to help build tuples. It is mutable and thus allows edition."""

    def __init__(self, elements: FlexibleTupl):
        super().__init__(c=connectives.tupl, terms=elements)

    def to_tupl(self) -> Tupl:
        elements: tuple[Formula, ...] = tuple(coerce_formula(phi=element) for element in self)
        phi: Tupl = Tupl(elements=elements)
        return phi

    def to_formula(self) -> Formula:
        """Return a Collection."""
        return self.to_tupl()


class Tupl(Formula):
    """A tuple is a formula c(t0, t1, ..., tn) where:
     - c is a node with the collection connective.
     - ti is a formula.

     The empty-tuple is the tuple c().

     Python implementation: in python, the word 'tuple' is reserved. For this reason, the word 'tupl' is used instead
     to implement this object."""

    def __new__(cls, elements: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        o: tuple = super().__new__(cls, c=connectives.tupl, terms=elements)
        return o

    def __init__(self, elements: FlexibleTupl = None):
        super().__init__(c=connectives.tupl, terms=elements)

    def has_element(self, phi: Formula) -> bool:
        """Return True if the tuple has phi as one of its elements."""
        return any(is_formula_equivalent(phi=phi, psi=term) for term in self)

    def to_tupl_builder(self) -> TuplBuilder:
        return TuplBuilder(elements=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_tupl_builder()


FlexibleTupl = typing.Optional[typing.Union[Tupl, TuplBuilder, typing.Iterable[FlexibleFormula]]]
"""FlexibleTupl is a flexible python type that may be safely coerced into a Tupl or a TupleBuilder."""


class MapBuilder(FormulaBuilder):
    """A utility class to help build maps. It is mutable and thus allows edition."""

    def __init__(self, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        domain: EnumerationBuilder = coerce_enumeration_builder(elements=domain)
        codomain: TuplBuilder = coerce_tupl_builder(elements=codomain)
        super().__init__(c=connectives.map, terms=(domain, codomain,))

    @property
    def codomain(self) -> TuplBuilder:
        return coerce_tupl_builder(elements=self.term_1)

    @property
    def domain(self) -> EnumerationBuilder:
        return coerce_enumeration_builder(elements=self.term_0)

    def get_assigned_value(self, phi: FlexibleFormula) -> FlexibleFormula:
        """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
        if self.is_defined_in(phi=phi):
            index_position: int = self.domain.get_element_index(phi=phi)
            return self.codomain[index_position]
        else:
            raise IndexError('Map domain does not contain this element')

    def is_defined_in(self, phi: FlexibleFormula) -> bool:
        return self.domain.has_element(phi=phi)

    def to_map(self) -> Map:
        keys: Tupl = coerce_tupl(elements=self.term_0)
        values: Tupl = coerce_tupl(elements=self.term_0)
        phi: Map = Map(domain=keys, codomain=values)
        return phi

    def to_formula(self) -> Formula:
        """Return a formula."""
        return self.to_map()


class Map(Formula):
    """A map is a formula m(t0(k0, k1, ..., kn), t1(l0, l1, ..., ln)) where:
     - m is a node with the map connective.
     - t0 is an enumaration named the keys enumaration.
     - t1 is a tuple named the values tuple.
     - the cardinality of t0 is equal to the cardinality of 1.

     The empty-map is the map m(t0(), t1()).

    """

    def __new__(cls, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        domain: Enumeration = coerce_enumeration(elements=domain)
        codomain: Tupl = coerce_tupl(elements=codomain)
        if len(domain) != len(codomain):
            raise ValueError('Map: |keys| != |values|')
        o: tuple = super().__new__(cls, c=connectives.map, terms=(domain, codomain,))
        return o

    def __init__(self, domain: FlexibleEnumeration = None, codomain: FlexibleTupl = None):
        domain: Enumeration = coerce_enumeration(elements=domain)
        codomain: Tupl = coerce_tupl(elements=codomain)
        super().__init__(c=connectives.map, terms=(domain, codomain,))

    @property
    def codomain(self) -> Tupl:
        return coerce_tupl(elements=self.term_1)

    @property
    def domain(self) -> Enumeration:
        return coerce_enumeration(elements=self.term_0)

    def get_assigned_value(self, phi: Formula) -> Formula:
        """Given phi an element of the map domain, returns the corresponding element psi of the codomain."""
        if self.is_defined_in(phi=phi):
            index_position: int = self.domain.get_element_index(phi=phi)
            return self.codomain[index_position]
        else:
            raise IndexError('Map domain does not contain this element')

    def is_defined_in(self, phi: Formula) -> bool:
        return self.domain.has_element(phi=phi)

    def to_map_builder(self) -> MapBuilder:
        return MapBuilder(domain=self.term_0, codomain=self.term_1)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_map_builder()


FlexibleMap = typing.Optional[typing.Union[Map, MapBuilder, typing.Dict[Formula, Formula]]]
"""FlexibleMap is a flexible python type that may be safely coerced into a Map or a MapBuilder."""


class EnumerationBuilder(FormulaBuilder):
    """A utility class to help build enumeration. It is mutable and thus allows edition."""

    def __init__(self, elements: FlexibleEnumeration):
        if elements is None:
            elements: FlexibleEnumeration = set()
        unique_elements: set = set(elements)
        if len(unique_elements) != len(elements):
            warnings.warn('Element repetitions are removed from enumerations.')
        super().__init__(c=connectives.enumeration, terms=unique_elements)

    def get_element_index(self, phi: FlexibleFormula) -> typing.Optional[int]:
        """Return the index of phi if phi is formula-equivalent with an element of the enumeration, None otherwise."""
        if self.has_element(phi=phi):
            # two formulas that are formula-equivalent may not be equal.
            # for this reason we must first find the first formula-equivalent element in the enumeration.
            inside_element: Formula = next(term for term in self if is_formula_equivalent(phi=phi, psi=term))
            # and then we can retrieve its index position.
            index_position: int = self.index(inside_element)
            return index_position
        else:
            return None

    def has_element(self, phi: FlexibleFormula) -> bool:
        """Return True if the enumeration has an element that is formula-equivalent with phi."""
        return any(is_formula_equivalent(phi=phi, psi=term) for term in self)

    def to_enumeration(self) -> Enumeration:
        elements: tuple[Formula, ...] = tuple(coerce_formula(phi=element) for element in self)
        phi: Enumeration = Enumeration(elements=elements)
        return phi

    def to_formula(self) -> Formula:
        """Return a Collection."""
        return self.to_enumeration()


class Enumeration(Formula):
    """In axiomatic-system-1, an enumeration is a formula c(t0, t1, ..., tn) where:
     - c is a node with the 'enumeration' connective.
     - ti is a formula.

    Distinctive objects:
     - The empty-enumeration is the formula c().

    By definition, the sub-formulas of a formula phi are ordered and can repeat themselves. The justification for
    enumeration is the intention of considering the sub-formulas without their ordering, and without repetitions.
    Enumerations are equivalent to computable sets.

    TODO: Enumeration: Because sub-formulas are natively ordered, it is disturbing that formula-equivalence
        becomes somehow unpredictable when used on enumerations. In effect, we cannot commit on a particular
        ordering of sub-formulas and the python set() function used during initialization is unpredictable.
        Future improvement: find an elegant algorithm that canonically orders formulas.
    """

    def __new__(cls, elements: FlexibleEnumeration = None):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        unique_elements: set = set(elements)
        if len(unique_elements) != len(elements):
            warnings.warn('Element repetitions are removed from enumerations.')
        o: tuple = super().__new__(cls, c=connectives.enumeration, terms=unique_elements)
        return o

    def __init__(self, elements: FlexibleEnumeration = None):
        unique_elements: set = set(elements)
        if len(unique_elements) != len(elements):
            warnings.warn('Element repetitions are removed from enumerations.')
        super().__init__(c=connectives.enumeration, terms=unique_elements)

    def get_element_index(self, phi: Formula) -> typing.Optional[int]:
        """Return the index of phi if phi is formula-equivalent with an element of the enumeration, None otherwise."""
        if self.has_element(phi=phi):
            # two formulas that are formula-equivalent may not be equal.
            # for this reason we must first find the first formula-equivalent element in the enumeration.
            inside_element: Formula = next(term for term in self if is_formula_equivalent(phi=phi, psi=term))
            # and then we can retrieve its index position.
            index_position: int = self.index(inside_element)
            return index_position
        else:
            return None

    def has_element(self, phi: Formula) -> bool:
        """Return True if the enumeration has an element that is formula-equivalent with phi."""
        return any(is_formula_equivalent(phi=phi, psi=term) for term in self)

    def to_enumeration_builder(self) -> EnumerationBuilder:
        return EnumerationBuilder(elements=self)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_enumeration_builder()


FlexibleEnumeration = typing.Optional[typing.Union[Enumeration, EnumerationBuilder, typing.Iterable[FlexibleFormula]]]
"""FlexibleEnumeration is a flexible python type that may be safely coerced into an Enumeration or a EnumerationBuilder."""


class TransformationBuilder(FormulaBuilder):

    def __init__(self, premises: FlexibleTupl, conclusion: FlexibleFormula,
                 variables: FlexibleTupl):
        premises: EnumerationBuilder = EnumerationBuilder(elements=premises)
        variables: EnumerationBuilder = EnumerationBuilder(elements=variables)
        super().__init__(c=connectives.inference_rule, terms=(premises, conclusion, variables,))

    @property
    def conclusion(self) -> FormulaBuilder:
        return self[1]

    @property
    def premises(self) -> EnumerationBuilder:
        return self[0]

    def to_transformation(self) -> Transformation:
        premises = self.premises.to_enumeration()
        conclusion: Formula = self.conclusion.to_formula()
        variables = self.variables.to_enumeration()
        t: Transformation = Transformation(premises=premises, conclusion=conclusion, variables=variables)
        return t

    def to_formula(self) -> Formula:
        """Return a Transformation."""
        return self.to_transformation()

    @property
    def variables(self) -> EnumerationBuilder:
        return self[2]


class Transformation(Formula):
    """A transformation is a formula t(P, c, V) where:
     - t has the transformation connective,
     - P is an enumeration whose children are called premises,
     - c is a formula called conclusion,
     - V is a enumeration whose children are variables.
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

    def __new__(cls, premises: FlexibleTupl, conclusion: FlexibleFormula,
                variables: FlexibleEnumeration):
        # When we inherit from tuple, we must implement __new__ instead of __init__ to manipulate arguments,
        # because tuple is immutable.
        premises: Tupl = coerce_tupl(elements=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(elements=variables)
        o: tuple = super().__new__(cls, c=connectives.tupl,
                                   terms=(premises, conclusion, variables,))
        return o

    def __init__(self, premises: FlexibleTupl, conclusion: FlexibleFormula,
                 variables: FlexibleEnumeration):
        premises: Tupl = coerce_tupl(elements=premises)
        conclusion: Formula = coerce_formula(phi=conclusion)
        variables: Enumeration = coerce_enumeration(elements=variables)
        super().__init__(c=connectives.inference_rule, terms=(premises, conclusion, variables,))

    def __call__(self, arguments: FlexibleTupl) -> Formula:
        """A shortcut for self.apply_transformation()"""
        return self.apply_transformation(arguments=arguments)

    def apply_transformation(self, arguments: FlexibleTupl) -> Formula:
        """

        :param arguments: A tuple of arguments, whose order matches the order of the transformation premises.
        :return:
        """
        # step 1: confirm every argument is compatible with its premise and retrieve variable values
        variables_map: MapBuilder = MapBuilder()
        assert_formula_equivalent_with_variables(phi=arguments, psi=self.premises, v=self.variables,
                                                 variables_map=variables_map)

        # step 2:
        print(variables_map)

        pass
        # TODO: Pursue implementation here.

    @property
    def conclusion(self) -> Formula:
        return self[1]

    @property
    def premises(self) -> Tupl:
        return self[0]

    def to_transformation_builder(self) -> TransformationBuilder:
        premises: TuplBuilder = self.premises.to_tupl_builder()
        conclusion: FormulaBuilder = self.conclusion.to_formula_builder()
        variables: EnumerationBuilder = self.variables.to_enumeration_builder()
        return TransformationBuilder(premises=premises, conclusion=conclusion, variables=variables)

    def to_formula_builder(self) -> FormulaBuilder:
        return self.to_transformation_builder()

    @property
    def variables(self) -> Enumeration:
        return self[2]
# x = let_x_be_a_variable(rep='x')
# x | connectives.is_a | y
# ir = InferenceRuleBuilder()
