from __future__ import annotations
import typing
import collections
import itertools

# package modules
import util
import rooted_plane_tree_library as rpt
import sequence_library as sl
from punctilious.sequence_library import NaturalNumberSequence


# Formula declarations


def declare_abstract_formula_from_tree_of_integer_tuple_pairs(p) -> AbstractFormula:
    """Declares a :class:`AbstractFormula` object from a tree of integer/tuple pairs.

    Use case:
    Tree of integer/tuple pairs is a natural pythonic data structure to express abstract formulas.

    Definition:
    A tree of integer/tuple pairs `T` defined as:
     T := (n, T')
    where:
     - n is a natural number
     - T' is (possibly empty) tuple of trees of integer/tuple pairs.

    Sample tree of integer/tuple pairs:
    (0, ((1,(),),(0,((2,(),),(1,(),),),),(2,(),),),)
    ...which maps to formula:
    0(1,0(2,1),2)

    :param p: A tree of integer/tuple pairs.
    :return: a :class:`AbstractFormula`.
    """

    t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=p)
    t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_tuple_tree(t)
    s: sl.NaturalNumberSequence = sl.NaturalNumberSequence(*s)
    phi: AbstractFormula = AbstractFormula(t, s)
    return phi


def declare_abstract_formula_from_immediate_sub_formulas(
        n: int | None,
        s: tuple[FlexibleAbstractFormula, ...] | None) -> AbstractFormula:
    """Given a root natural number n,
    and a tuple of abstract-formulas s,
    declares a new formula 𝜓 := n(s_0, s_1, ..., s_n) where s_i is an element of s.

    :param n:
    :param s:
    :return:
    """
    if n is None:
        n: int = 0
    if s is None:
        s: tuple[AbstractFormula, ...] = ()
    s: tuple[AbstractFormula, ...] = tuple(
        data_validate_abstract_formula(o=phi) for phi in s)
    # Retrieves the children trees
    t: tuple[rpt.RootedPlaneTree, ...] = tuple(phi.rooted_plane_tree for phi in s)
    # Declare the new parent tree
    t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_immediate_subtrees(*t)
    # Declare the natural-number-sequence by appending n to the concatenation of the
    # children natural-number-sequences.
    u: sl.NaturalNumberSequence = sl.NaturalNumberSequence(n) + sl.concatenate_natural_number_sequences(
        *(phi.natural_number_sequence for phi in s))
    phi: AbstractFormula = AbstractFormula(t=t, s=u)
    return phi


# Transformation functions


def extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p):
    """Given a tree of integer/tuple pairs, extracts:
     - its tree of tuples,
     - and its sequence of integers,
    following the depth-first ascending-nodes algorithm.

    :param p: the tree of integer/tuple pairs
    :return: a pair (T, S) where T is a tree of tuples, and S is a sequence of integers.
    """
    if len(p) != 2:
        raise util.PunctiliousException('The length of the pair is not equal to 2.', len_t=len(p), t=p)
    i: int = p[0]
    children = p[1]
    if len(children) == 0:
        # this is a leaf
        return (), (i,)
    else:
        t: list = []
        s: tuple[int, ...] = (i,)
        for sub_p in children:
            sub_t, sub_s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=sub_p)
            t.append(sub_t)
            s += sub_s
        t: tuple[tuple, ...] = tuple(t)
        return t, s


def declare_canonical_abstract_formula_from_tree_of_integer_tuple_pairs(p):
    """
    """
    t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p)
    return AbstractFormula(t, s)


# Data validation functions


def data_validate_abstract_formula(
        o: FlexibleAbstractFormula) -> AbstractFormula:
    if isinstance(o, AbstractFormula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return AbstractFormula(*o)
    if isinstance(o, collections.abc.Generator):
        return AbstractFormula(*o)
    raise util.PunctiliousException("`AbstractFormula` data validation failure. `o` is of unknown type.",
                                    type_of_o=type(o), o=o)


# Classes


class AbstractFormula(tuple):
    """A :class:`AbstractFormula` is a tuple `(T, S)` such that:
     - `T` is a rooted-plane-tree,
     - `S` is a sequence of natural numbers.

    """

    def __eq__(self, phi) -> bool:
        """Returns `True` if this abstract-formula is equal to abstract-formula `phi`, `False` otherwise.

        See :attr:`AbstractFormula.is_equal_to` for a definition of abstract-formula equality.

        :param phi: An abstract-formula.
        :return: `True` if this abstract-formula is equal to abstract-formula `phi`, `False` otherwise.
        """
        return self.is_equal_to(phi)

    def __hash__(self):
        return hash((AbstractFormula, self.rooted_plane_tree, self.natural_number_sequence,))

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleNaturalNumberSequence):
        super(AbstractFormula, self).__init__()
        self._canonical_abstract_formula: AbstractFormula | None = None
        self._contains_unique_immediate_subformulas: AbstractFormula | None = None
        self._immediate_sub_formulas: tuple[AbstractFormula, ...] | None = None
        self._sub_formulas: tuple[AbstractFormula, ...] | None = None

    def __ne__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`AbstractFormula`,
        returns `True` if `t` is not abstract-formula-equivalent to this :class:`AbstractFormula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: AbstractFormula = data_validate_abstract_formula(t)
            return not self.is_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleNaturalNumberSequence):
        t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_any(t)
        s: sl.NaturalNumberSequence = sl.NaturalNumberSequence.from_any(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`AbstractFormula` data validation error. The size of the `RootedPlaneGraph` is not equal to the length of the `UnrestrictedSequence`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        phi = super(AbstractFormula, cls).__new__(cls, (t, s))
        phi = retrieve_abstract_formula_from_cache(phi)
        return phi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    @property
    def arity(self) -> int:
        """The :attr:`AbstractFormula.arity` is the number of immediate sub-formulas it contains.

        :return:
        """
        return len(self.immediate_sub_formulas)

    @property
    def canonical_abstract_formula(self) -> AbstractFormula:
        """

        Definition: the canonical-abstract-formula `phi` of an abstract-formula `psi`
        is a formula such that:
         - their rooted-plane-tree are rooted-plane-tree-equivalent,
         - the natural-number-sequence of `phi` is the canonical-naturel-number-sequence
           of the natural-number-sequence of `psi`

        :return:
        """
        if self.is_canonical:
            return self
        elif self._canonical_abstract_formula is not None:
            return self._canonical_abstract_formula
        else:
            self._canonical_abstract_formula: AbstractFormula = AbstractFormula(
                t=self.rooted_plane_tree,
                s=self.natural_number_sequence.canonical_natural_number_sequence)
            return self._canonical_abstract_formula

    @property
    def formula_degree(self) -> int:
        """The `formula_degree` of an :class:`AbstractFormula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al., 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rpt.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_subtrees():
            if t.degree > 0:
                i += 1
        return i

    def get_sub_formula_by_path(self, p: tuple[int, ...]) -> AbstractFormula:
        """Given a path `p`, returns the corresponding sub-formula.

        Definition - sub-formula path:
        A sub-formula path is a finite sequence of natural numbers >= 0, of length > 0,
        that gives the index position of the sub-formulas, following the depth-first algorithm,
        starting with 0 meaning the original tree.

        It follows that for any formula `phi`, the path (0) returns the formula itself.

        :param p:
        :return:
        """
        p: tuple[int, ...] = tuple(int(n) for n in p)
        if p[0] != 0:
            raise util.PunctiliousException("The first element of the path is not equal to 0.", p0=p[0], p=p,
                                            phi=self)
        if p == (0,):
            return self
        else:
            phi: AbstractFormula = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= phi.tree_degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate sub-formulas in phi.", n_index=i, n_value=j,
                        phi=phi)
                phi: AbstractFormula = phi.immediate_sub_formulas[j]
            return phi

    @property
    def immediate_sub_formulas(self) -> tuple[AbstractFormula, ...]:
        """The `immediate_sub_formulas` of an :class:`AbstractFormula` `phi` is the tuple of :class:`AbstractFormula` elements
        that are the immediate children formulas of `phi` in the formula tree, or equivalently the formulas
        of degree 0 in `phi`.

        The term `immediate sub-formula` is used by (Mancosu 2021, p. 17-18).

        See also:
        - :attr:`AbstractFormula.sub_formulas`

        References:
        - Mancosu 2021.

        :return:
        """
        if self._immediate_sub_formulas is None:
            sub_formulas = list()
            for phi in self.iterate_immediate_sub_formulas():
                sub_formulas.append(phi)
            self._immediate_sub_formulas = tuple(sub_formulas)
        return self._immediate_sub_formulas

    @property
    def immediate_subformulas_are_unique(self) -> bool:
        """Returns `True` if all immediate subformulas contained in this :class:`AbstractFormula`
        are unique.

        Trivial case:
        If the :class:`AbstractFormula` is a leaf, i.e. it contains no immediate subformulas,
        then all of its immediate subformulas are unique.

        :return:
        """
        if self._contains_unique_immediate_subformulas is None:
            unique_values: set[AbstractFormula] = set()
            psi: AbstractFormula
            for psi in self.iterate_immediate_sub_formulas():
                if psi in unique_values:
                    self._contains_unique_immediate_subformulas = False
                unique_values.add(psi)
            self._contains_unique_immediate_subformulas = True
        return self._contains_unique_immediate_subformulas

    def is_abstract_formula_equivalent_to(self, phi: AbstractFormula):
        """Returns `True` if this :class:`AbstractFormula` is abstract-formula-equivalent
        to :class:`AbstractFormula` `phi`.

        Formal definition:
        Two abstract-formulas phi and psi are abstract-formula-equivalent if and only if:
        - the rooted-plane-tree of phi is rooted-plane-tree-equivalent to the rooted-plane-tree of psi,
        - the natural-numbers-sequence of phi is natural-numbers-sequence-equivalent to the natural-numbers-sequence of psi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return self.rooted_plane_tree.is_rooted_plane_tree_equivalent_to(
            phi.rooted_plane_tree) and self.natural_number_sequence.is_natural_number_sequence_equivalent_to(
            phi.natural_number_sequence)

    @property
    def is_canonical(self) -> bool:
        """Returns `True` if this abstract-formula is in canonical form.

        Definition:
        An abstract-formula `phi` is `canonical` if and only if
        its natural-number-sequence is a restricted-growth-function-sequence.

        :return: `True` if this abstract-formula is in canonical form, `False` otherwise.
        """
        return self.natural_number_sequence.is_restricted_growth_function_sequence

    def is_canonical_abstract_formula_equivalent_to(self, phi: AbstractFormula):
        """Returns `True` if this :class:`AbstractFormula` is canonical-abstract-formula-equivalent
        to :class:`AbstractFormula` `phi`.

        Formal definition:
        Two abstract-formulas phi and psi are canonical-abstract-formula-equivalent if and only if:
        - the canonical-abstract-formula of phi is abstract-formula-equivalent
          to the canonical-abstract-formula of psi.

        Intuitive definition:
        Two formulas are canonical-abstract-formula-equivalent if they have the same "structure".

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return self.canonical_abstract_formula.is_abstract_formula_equivalent_to(
            phi.canonical_abstract_formula)

    def is_equal_to(self, phi: FlexibleAbstractFormula):
        """Under :class:`AbstractFormula` canonical ordering,
        returns `True` if the current :class:`AbstractFormula` is equal to `phi`,
        `False` otherwise.

        See :attr:`AbstractFormula.is_less_than` for a definition of abstract-formula canonical-ordering.

        :param phi: A :class:`AbstractFormula`.
        :return: `True` if the current :class:`AbstractFormula` is equal to `s`, `False` otherwise.
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return self.is_abstract_formula_equivalent_to(phi)

    def is_less_than_or_equal_to(self, phi: FlexibleAbstractFormula) -> bool:
        """Under :class:`AbstractFormula` canonical ordering,
        returns `True` if the current :class:`RootedPlaneTree` is less than or equal to `s`,
        `False` otherwise.

        See :attr:`AbstractFormula.is_less_than` for a definition of abstract-formula canonical-ordering.

        :param phi: A :class:`AbstractFormula`.
        :return: `True` if the current :class:`AbstractFormula` is equal to `s`, `False` otherwise.
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return self.is_equal_to(phi) or self.is_less_than(phi)

    def is_less_than(self, phi: FlexibleAbstractFormula) -> bool:
        """Under :class:`AbstractFormula` canonical ordering,
        returns `True` if the current :class:`AbstractFormula` is less than `phi`,
        `False` otherwise.

        Definition: canonical ordering of abstract-formula, denoted :math:`\prec`,
        is defined as rooted-plane-tree-first, natural-number-sequence second.

        :param phi: A :class:`AbstractFormula`.
        :return: `True` if the current :class:`AbstractFormula` is equal to `phi`, `False` otherwise.
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        if self.is_abstract_formula_equivalent_to(phi):
            return False
        elif self.rooted_plane_tree.is_less_than(phi.rooted_plane_tree):
            return True
        elif phi.rooted_plane_tree.is_less_than(self.rooted_plane_tree):
            return False
        elif self.natural_number_sequence.is_less_than(phi.natural_number_sequence):
            return True
        elif phi.natural_number_sequence.is_less_than(self.natural_number_sequence):
            return False
        raise util.PunctiliousException("Unreachable condition")

    def is_immediate_sub_formula_of(self, phi: AbstractFormula):
        """Returns `True` if this :class:`AbstractFormula` is an immediate sub-formula of :class:`AbstractFormula` phi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        psi: AbstractFormula
        for psi in phi.iterate_immediate_sub_formulas():
            if self.is_abstract_formula_equivalent_to(psi):
                return True
        return False

    def is_immediate_super_formula_of(self, phi: AbstractFormula):
        """Returns `True` if :class:`AbstractFormula` phi is an immediate super-formula of this :class:`AbstractFormula`.

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return phi.is_immediate_sub_formula_of(self)

    def is_sub_formula_of(self, phi: AbstractFormula):
        """Returns `True` if this :class:`AbstractFormula` is a sub-formula of :class:`AbstractFormula` phi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        psi: AbstractFormula
        for psi in phi.iterate_sub_formulas():
            if self.is_abstract_formula_equivalent_to(psi):
                return True
        return False

    def is_super_formula_of(self, phi: AbstractFormula):
        """Returns `True` if :class:`AbstractFormula` phi is a sub-formula of this :class:`AbstractFormula`.

        :param phi:
        :return:
        """
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        return phi.is_sub_formula_of(self)

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`AbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`AbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_immediate_subtrees(),
                                              self.iterate_immediate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_immediate_sub_sequences(self) -> typing.Generator[
        NaturalNumberSequence, None, None]:
        """Iterates the immediate (children) sub-:class:`UnrestrictedSequence` of this :class:`AbstractFormula`.

        Note:
            A sub-sequence of an abstract-formula is determined by:
             - 1) the parent rgf sequence,
             - and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rpt.RootedPlaneTree
        for child_tree in self.rooted_plane_tree.iterate_immediate_subtrees():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + child_tree.size]
            sub_sequence: NaturalNumberSequence = NaturalNumberSequence(*sub_sequence)
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_sub_sequences(self) -> collections.abc.Generator[sl.NaturalNumberSequence, None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_subtrees()):
            # retrieves the sub-sequence in the sequence
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + sub_tree.size]
            sub_sequence: sl.NaturalNumberSequence = sl.NaturalNumberSequence(*sub_sequence)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the sub-formulas of the :class:`AbstractFormula` using the `depth-first, ascending nodes` algorithm.

        See :attr:`AbstractFormula.sub_formulas` for a definition of the term `sub-formula`.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: sl.NaturalNumberSequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_subtrees(),
                                              self.iterate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    @property
    def main_element(self) -> int:
        """The `main_element` of an :class:`AbstractFormula` is the first element of its
        attr:`AbstractFormula.natural_numbers_sequence`, that corresponds to the root
        node of the attr:`AbstractFormula.rooted_plane_tree`.

        The term `main element` was coined in reference to the term `main connective`
         (cf. Mancosu 2021, p. 17), because abstract-formulas are composed of sequences,
         and thus `main connective` is reserved for "concrete" formulas.

        References:
         - Mancosu 2021

        :return: 1
        """
        return self.natural_number_sequence[0]

    @property
    def natural_number_sequence(self) -> sl.NaturalNumberSequence:
        """Returns the :class:`NaturalNumberSequence` component of this :class:`AbstractFormula`.

        Shortcut: self.s.

        :return:
        """
        return super().__getitem__(1)

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        """Returns a string representation of the :class:`AbstractFormula` using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.natural_numbers_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of
        the :attr:`AbstractFormula.natural_numbers_sequence`. Default: `None`.
        :return:
        """
        if connectives is None:
            connectives = self.natural_number_sequence
        else:
            if len(connectives) != len(self.natural_number_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the abstract-formula's natural-number-sequence.",
                    connectives_length=len(connectives),
                    natural_number_sequence_length=self.natural_number_sequence.length,
                    connectives=connectives,
                    natural_number_sequence=self.natural_number_sequence,
                    abstract_formula=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    @property
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        """The :class:`RootedPlaneTree` component of this :class:`AbstractFormula`.

        Shortcut: self.t."""
        return super().__getitem__(0)

    @property
    def s(self) -> sl.NaturalNumberSequence:
        """A shortcut for self.natural_numbers_sequence."""
        return self.natural_number_sequence

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of an :class:`AbstractFormula` is the `max_value` of its `natural_numbers_sequence`."""
        return self.natural_number_sequence.max_value

    @property
    def sub_formulas(self) -> tuple[AbstractFormula, ...]:
        """The `sub_formulas` of an :class:`AbstractFormula` `phi` is the tuple of :class:`AbstractFormula` elements that are present
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
        - :attr:`AbstractFormula.immediate_sub_formulas`

        References:
        - Mancosu 2021.

        :return: A tuple of the sub-formulas.
        """
        if self._sub_formulas is None:
            sub_formulas: list[AbstractFormula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def substitute_sub_formulas(self, m: dict[
        FlexibleAbstractFormula, FlexibleAbstractFormula]) -> AbstractFormula:
        """Returns a new :class:`AbstractFormula`
        similar to the current :class:`AbstractFormula` except that
        all sub-abstract-formulas present in the map `m` domain,
        are substituted with corresponding :class:`AbstractFormula` elements in map `m` codomain,
        following the depth-first, ascending-nodes algorithm.

        :param m: A map AbstractFormula --> AbstractFormula.
        :return:
        """
        domain: tuple[AbstractFormula, ...] = tuple(
            data_validate_abstract_formula(x) for x in m.keys())
        codomain: tuple[AbstractFormula, ...] = tuple(
            data_validate_abstract_formula(y) for y in m.values())
        m: dict[AbstractFormula, AbstractFormula] = dict(zip(domain, codomain))
        immediate_sub_formulas: list[AbstractFormula] = []
        phi: AbstractFormula
        for phi in self.iterate_immediate_sub_formulas():
            if phi in m.keys():
                phi = m[phi]
                immediate_sub_formulas.append(phi)
            else:
                immediate_sub_formulas.append(phi)
        psi: AbstractFormula = AbstractFormula()
        raise NotImplementedError("Complete implementation here")

    @property
    def t(self) -> rpt.RootedPlaneTree:
        """A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @property
    def tree_degree(self) -> int:
        """The `tree_degree` of an :class:`AbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_degree` and `formula_degree`.
        """
        return self.rooted_plane_tree.degree

    @property
    def tree_size(self) -> int:
        """The `tree_size` of an :class:`AbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


# Flexible types to facilitate data validation

FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, sl.FlexibleNaturalNumberSequence], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

AF = AbstractFormula  # An alias for AbstractFormula

# Cache Management

_abstract_formula_cache = dict()  # cache mechanism assuring that unique abstract formulas are only instantiated once.


def retrieve_abstract_formula_from_cache(o: FlexibleAbstractFormula):
    """cache mechanism assuring that unique abstract formulas are only instantiated once."""
    global _abstract_formula_cache
    o: AbstractFormula = data_validate_abstract_formula(o)
    if hash(o) in _abstract_formula_cache.keys():
        return _abstract_formula_cache[hash(o)]
    else:
        _abstract_formula_cache[hash(o)] = o
        return o
