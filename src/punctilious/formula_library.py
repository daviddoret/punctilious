from __future__ import annotations
import typing
import collections
import collections.abc

# package modules
import util
import connective_library
import abstract_formula_library as afl
import sequence_library as sl


# Data validation


def data_validate_formula(
        o: FlexibleFormula) -> Formula:
    if isinstance(o, Formula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return Formula(*o)
    if isinstance(o, collections.abc.Generator):
        return Formula(*o)
    raise util.PunctiliousException('Formula data validation failure', o=o)


# Classes


class Formula(tuple):
    """A `Formula` is a pair (ϕ, M) where:
     - ϕ is an abstract formula of tree-size n.
     - M is a bijective map between the subset of natural-numbers N,
       and a set of connectives C.
    """

    def __eq__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`Formula`,
        returns `True` if `t` is formula-equivalent to this :class:`Formula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: Formula = data_validate_formula(t)
            return self.is_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((Formula, self.abstract_formula, self.connective_sequence,))

    def __init__(self, phi: afl.FlexibleAbstractFormula, s: sl.FlexibleConnectiveSequence):
        super(Formula, self).__init__()
        self._immediate_sub_formulas = None
        self._sub_formulas = None

    def __ne__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`Formula`,
        returns `True` if `t` is not formula-equivalent to this :class:`Formula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: Formula = data_validate_formula(t)
            return not self.is_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __new__(cls, phi: afl.FlexibleAbstractFormula, s: sl.FlexibleConnectiveSequence):
        phi: afl.AbstractFormula = afl.data_validate_abstract_formula(phi)
        s: sl.ConnectiveSequence = sl.data_validate_connective_sequence(s)
        phi: afl.AbstractFormula = phi.canonical_abstract_formula  # Canonize the abstract-formula
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    @property
    def abstract_formula(self) -> afl.AbstractFormula:
        """

        `abstract_formula` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 0)

    @property
    def connective_sequence(self) -> sl.ConnectiveSequence:
        """

        `connective_sequence` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 1)

    @property
    def formula_degree(self) -> int:
        """The `formula_degree` of a `Formula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        return self.abstract_formula.formula_degree

    def get_connective_by_sequence_element(self, i: int) -> connective.Connective:
        return self.connective_sequence[i]

    @property
    def immediate_sub_formulas(self) -> tuple[Formula, ...]:
        """The `immediate_sub_formulas` of a `Formula` `phi` is the tuple of `Formula` elements that are the
        immediate children formulas of `phi` in the formula tree, or equivalently the formulas of degree 0 in `phi`.

        The term `immediate sub-formula` is used by (Mancosu 2021, p. 17-18) in the context of propositional logic.

        See also:
        - :attr:`Formula.sub_formulas`

        References:
        - Mancosu 2021.

        :return:
        """
        if self._sub_formulas is None:
            sub_formulas: list[Formula] = list()
            for sub_formula in self.iterate_immediate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def is_formula_equivalent_to(self, phi: Formula):
        """Returns `True` if this :class:`Formula` is formula-equivalent
        to :class:`Formula` `phi`.

        Formal definition:
        Two formulas phi and psi are formula-equivalent if and only if:
        - the abstract-formula of phi is abstract-formula-equivalent to the abstract-formula of psi,
        - the connective-sequence of phi is connective-sequence-equivalent to the connective-sequence of psi.

        :param phi:
        :return:
        """
        phi: Formula = data_validate_formula(phi)
        return self.abstract_formula.is_abstract_formula_equivalent_to(
            phi.abstract_formula) and self.connective_sequence.is_connective_sequence_equivalent_to(
            phi.connective_sequence)

    def is_immediate_sub_formula_of(self, phi: Formula) -> bool:
        """Returns `True` if `phi` is an immediate sub-formula of the current `Formula`, `False` otherwise.

        :param phi:
        :return:
        """
        phi: Formula = data_validate_formula(phi)
        return any(self.is_formula_equivalent_to(psi) for psi in phi.iterate_immediate_sub_formulas())

    def is_sub_formula_of(self, phi: Formula) -> bool:
        """Returns `True` if `phi` is a sub-formula of the current `Formula`, `False` otherwise.

        :param phi:
        :return:
        """
        phi: Formula = data_validate_formula(phi)
        return any(self.is_formula_equivalent_to(psi) for psi in phi.iterate_sub_formulas())

    def iterate_connectives(self) -> collections.abc.Generator[connective.Connective, None, None]:
        """Iterate the `Formula` connectives, following the depth-first, ascending-nodes algorithm.

        :return: None
        """
        i: int
        c: connective.Connective
        for i in self.abstract_formula.natural_number_sequence:
            yield self.get_connective_by_sequence_element(i)

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`Formula`.

        See :attr:`Formula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`Formula`.
        """
        for phi, s in zip(self.abstract_formula.iterate_immediate_sub_formulas(),
                          self.abstract_formula.iterate_immediate_sub_sequences()):
            s: tuple[int, ...] = util.deduplicate_integer_sequence(s)
            t: tuple[connective.Connective, ...] = tuple(
                self.get_connective_by_sequence_element(i) for i in s)
            yield Formula(phi, t)

    def iterate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        for phi, s in zip(self.abstract_formula.iterate_sub_formulas(),
                          self.abstract_formula.iterate_sub_sequences()):
            s: tuple[int, ...] = util.deduplicate_integer_sequence(s)
            t: tuple[connective.Connective, ...] = tuple(
                self.get_connective_by_sequence_element(i) for i in s)
            yield Formula(phi, t)

    @property
    def main_connective(self) -> connective.Connective:
        """The `main_connective` of a :class:`Formula` `phi` is the :class:`Connective` that corresponds
        to the root node of the formula tree.

        By definition of a :class:`Formula` as a pair (phi, S) where S is sequence of connectives,
        the `main_connective` is the first element of S.

        The term `main connective` is defined by Mancosu 2021, p. 17 in the context of propositional logic.

        References:
         - Mancosu 2021

        :return: a :class:`Connective`
        """
        return self.connective_sequence[0]

    def represent_as_function(self) -> str:
        """Returns a string representation of the `Formula` using function notation.
        """
        # TODO: TEST THIS
        return self.abstract_formula.represent_as_function(connectives=self.connective_sequence)

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of a `Formula` is the `sequence_max_value` of its `abstract_formula`."""
        return self.abstract_formula.sequence_max_value

    @property
    def sub_formulas(self) -> tuple[Formula, ...]:
        """The `sub_formulas` of an `Formula` `phi` is the tuple of `Formula` elements that are present
        in the formula tree of `phi`, including `phi` itself.

        Formal definition:
         - If phi is an atomic formula, the sub-formulas of phi is the tuple (phi).
         - If phi is a non-atomic formula, the sub-formulas of phi is the tuple
           composed of phi, and all sub-formulas of the immediate sub-formulas of phi,
           in ascending order.
        - Nothing else is a sub-formula.

        This definition is a generalization of the term `formula` defined by (Mancosu 2021, definition 2.2, p. 14)
        for propositional-logic.

        See also:
        - :attr:`Formula.immediate_sub_formulas`

        References:
        - Mancosu 2021.

        :return: A tuple of the sub-formulas.
        """
        if self._sub_formulas is None:
            sub_formulas: list[Formula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def substitute_sub_formulas(self, m: dict[FlexibleFormula, FlexibleFormula]) -> Formula:
        """Returns a new :class:`Formula` similar to the current :class:`Formula` except that
        all sub-formulas present in the map `m` domain,
        are substituted with corresponding :class:`Formula` elements in map `m` codomain,
        following the depth-first, ascending-nodes algorithm.

        :param m: A map Formula --> Formula.
        :return:
        """
        domain: tuple[Formula, ...] = tuple(data_validate_formula(x) for x in m.keys())
        codomain: tuple[Formula, ...] = tuple(data_validate_formula(y) for y in m.values())
        m: dict[Formula, Formula] = dict(zip(domain, codomain))
        sub_formulas: list[Formula] = []
        immediate_abstract_formulas: list[afl.AbstractFormula] = []
        for phi in self.iterate_immediate_sub_formulas():
            if phi in m.keys():
                psi = m[phi]
                sub_formulas.append(psi)
                immediate_abstract_formulas.append(psi.abstract_formula)
            else:
                sub_formulas.append(phi)
                immediate_abstract_formulas.append(phi.abstract_formula)
        abstract_formula: afl.AbstractFormula = afl.AbstractFormula()
        raise NotImplementedError("Complete implementation")

    @property
    def tree_size(self) -> int:
        """The `tree_size` of a `Formula` is the number of vertices in the `RootedPlaneTree` of its `abstract_formula`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.abstract_formula.tree_size


# Data types

FlexibleFormula = typing.Union[
    Formula, tuple[
        sl.FlexibleConnectiveSequence, afl.FlexibleAbstractFormula], collections.abc.Iterator, collections.abc.Generator, None]

# Cache management


_formula_cache = dict()  # cache mechanism assuring that unique  formulas are only instantiated once.


def retrieve_formula_from_cache(o: FlexibleFormula):
    """cache mechanism assuring that unique  formulas are only instantiated once."""
    global _formula_cache
    o: Formula = data_validate_formula(o)
    if hash(o) in _formula_cache.keys():
        return _formula_cache[hash(o)]
    else:
        _formula_cache[hash(o)] = o
        return o
