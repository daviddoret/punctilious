from __future__ import annotations
import typing
import collections
import abc
import itertools

# package modules
import util
import rooted_plane_tree as rpt
import sequence_library as sl
from punctilious.sequence_library import NaturalNumberSequence


# Formula declarations


def declare_formula_from_tree_of_integer_tuple_pairs(p) -> AbstractFormula:
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
    t: rpt.RootedPlaneTree = rpt.build_rooted_plane_tree_from_tuple_tree(t)
    s: sl.NaturalNumberSequence = sl.NaturalNumberSequence(*s)
    phi: AbstractFormula = AbstractFormula(t, s)
    return phi


def declare_abstract_formula_from_immediate_sub_formulas(
        n: int,
        s: tuple[
               FlexibleAbstractFormula] | None) -> AbstractFormula:
    """Given a root natural number n,
    and a tuple of abstract-formulas s,
    declares a new formula 𝜓 n(s_0, s_1, ..., s_n) where s_i is an element of s.

    :param n:
    :param s:
    :return:
    """
    if s is None:
        s = ()
    s: tuple[AbstractFormula, ...] = tuple(
        data_validate_abstract_formula(o=phi) for phi in s)
    phi: AbstractFormula
    # Retrieves the children trees
    t: tuple[rpt.RootedPlaneTree, ...] = tuple(phi.rooted_plane_tree for phi in s)
    # Declare the new parent tree
    t: rpt.RootedPlaneTree = rpt.RootedPlaneTree(*t)
    u: sl.NaturalNumberSequence = (n,) + itertools.chain.from_iterable(
        phi.natural_numbers_sequence for phi in s)
    phi: AbstractFormula = AbstractFormula(t=u, s=u)
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


def extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs_DUPLICATE(p):
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

    def __eq__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`AbstractFormula`,
        returns `True` if `t` is abstract-formula-equivalent to this :class:`AbstractFormula`,
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
            return self.is_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((AbstractFormula, self.rooted_plane_tree, self.natural_numbers_sequence,))

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleNaturalNumbersSequence):
        super(AbstractFormula, self).__init__()
        self._immediate_sub_formulas = None
        self._sub_formulas = None

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

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleNaturalNumbersSequence):
        t: rpt.RootedPlaneTree = rpt.data_validate_rooted_plane_tree(t)
        s: sl.NaturalNumberSequence = sl.data_validate_natural_number_sequence(s)
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
            phi.rooted_plane_tree) and self.natural_numbers_sequence.is_natural_number_sequence_equivalent_to(
            phi.natural_numbers_sequence)

    @property
    def is_canonical(self) -> bool:
        """Returns `True` if this abstract-formula is in canonical form.

        Definition:
        An abstract-formula `phi` is `canonical` if and only if
        its natural-number-sequence is a restricted-growth-function-sequence.

        :return: `True` if this abstract-formula is in canonical form, `False` otherwise.
        """
        return self.natural_numbers_sequence.is_restricted_growth_function_sequence

    def is_sub_formula_of(self, phi: AbstractFormula):
        """Returns `True` if this :class:`AbstractFormula` if a sub-formula of :class:`AbstractFormula` phi.

        :param phi:
        :return:
        """
        XXXX
        phi: AbstractFormula = data_validate_abstract_formula(phi)
        psi: AbstractFormula
        for psi in self.iterate_sub_formulas():
            if psi == phi:
                return True
        return False

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`AbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`AbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_immediate_subtrees(),
                                              self.iterate_immediate_sub_restricted_growth_function_sequences()):
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
            sub_sequence: tuple[int, ...] = self.natural_numbers_sequence[i:i + child_tree.size]
            sub_sequence: NaturalNumberSequence = NaturalNumberSequence(*sub_sequence)
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_immediate_sub_restricted_growth_function_sequences(self) -> typing.Generator[
        sl.RestrictedGrowthFunctionSequence, None, None]:
        """Iterates the direct child sub-sequences of this :class:`AbstractFormula`,
        applying canonical labeling to resulting sequences.

        Note: the immediate sub-sequences are determined by:
         - 1) the parent sequence,
         - and 2) the rooted plane tree.
        """
        s: sl.NaturalNumberSequence
        for s in self.iterate_immediate_sub_sequences():
            sub_sequence: sl.RestrictedGrowthFunctionSequence = sl.apply_canonical_labeling(
                s)
            # yield this child RGF sequence
            yield sub_sequence

    def iterate_sub_sequences(self) -> collections.abc.Generator[sl.NaturalNumberSequence, None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_subtrees()):
            # retrieves the sub-sequence in the sequence
            sub_sequence: tuple[int, ...] = self.natural_numbers_sequence[i:i + sub_tree.size]
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
        return self.natural_numbers_sequence[0]

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        """Returns a string representation of the :class:`AbstractFormula` using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.natural_numbers_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of
        the :attr:`AbstractFormula.natural_numbers_sequence`. Default: `None`.
        :return:
        """
        if connectives is None:
            connectives = self.natural_numbers_sequence
        else:
            if len(connectives) != len(self.natural_numbers_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the abstract-formula's RGF sequence.",
                    connectives_length=len(connectives),
                    rgf_sequence_length=self.natural_numbers_sequence.length,
                    connectives=connectives,
                    rgf_sequence=self.natural_numbers_sequence,
                    abstract_formula=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    @property
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        """Shortcut: self.t."""
        return self[0]

    @property
    def s(self) -> sl.NaturalNumberSequence:
        """A shortcut for self.natural_numbers_sequence."""
        return self.natural_numbers_sequence

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of an :class:`AbstractFormula` is the `max_value` of its `natural_numbers_sequence`."""
        return self.natural_numbers_sequence.max_value

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

    @property
    def natural_numbers_sequence(self) -> sl.NaturalNumberSequence:
        """Shortcut: self.s.

        :return:
        """
        return self[1]


class CanonicalAbstractFormula_OBSOLETE(AbstractFormula):
    """A :class:`CanonicalAbstractFormula` is a tuple `(T, S)` such that:
     - `T` is a rooted-plane-tree,
     - `S` is an RGF sequence.

    """

    def get_sub_formula_by_path(self, p: tuple[int, ...]) -> CanonicalAbstractFormula:
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
            phi: CanonicalAbstractFormula = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= phi.tree_degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate sub-formulas in phi.", n_index=i, n_value=j,
                        phi=phi)
                phi: CanonicalAbstractFormula = phi.immediate_sub_formulas[j]
            return phi

    @property
    def immediate_sub_formulas(self) -> tuple[CanonicalAbstractFormula, ...]:
        """The `immediate_sub_formulas` of an `CanonicalAbstractFormula` `phi` is the tuple of `CanonicalAbstractFormula` elements
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

    def is_sub_formula_of(self, phi: CanonicalAbstractFormula):
        """Returns `True` if this :class:`CanonicalAbstractFormula` if a sub-formula of :class:`CanonicalAbstractFormula` phi.

        :param phi:
        :return:
        """
        XXXX
        phi: CanonicalAbstractFormula = data_validate_canonical_abstract_formula(phi)
        psi: CanonicalAbstractFormula
        for psi in self.iterate_sub_formulas():
            if psi == phi:
                return True
        return False

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[CanonicalAbstractFormula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`CanonicalAbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`CanonicalAbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_immediate_subtrees(),
                                              self.iterate_immediate_sub_restricted_growth_function_sequences()):
            sub_formula = CanonicalAbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_immediate_sub_sequences(self) -> typing.Generator[
        tuple[int, ...], None, None]:
        """Iterates the direct sub-sequences of this `CanonicalAbstractFormula`.

        Note:
            A sub-sequence is not an RGF sequence, i.e. its initial value may not be equal to 0,
            and it may contain maximal values that are greater than the ones allowed by restricted growth.

        Note:
            The child rgf sequences are determined by 1) the parent rgf sequence,
            and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rpt.RootedPlaneTree
        # truncated_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[1:]
        for child_tree in self.rooted_plane_tree.iterate_immediate_subtrees():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[i:i + child_tree.size]
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_immediate_sub_restricted_growth_function_sequences(self) -> typing.Generator[
        sl.RestrictedGrowthFunctionSequence, None, None]:
        """Iterates the direct child sub-sequences of this `CanonicalAbstractFormula`.

        Note: the child rgf sequences are determined by 1) the parent rgf sequence,
        and 2) the rooted plane tree.
        """
        s: sl.RestrictedGrowthFunctionSequence
        for s in self.iterate_immediate_sub_sequences():
            # transform the sequence into an RGF sequence, restarting from initial value 0
            sub_sequence: sl.RestrictedGrowthFunctionSequence = sl.apply_canonical_labeling(
                s)
            # yield this child RGF sequence
            yield sub_sequence

    def iterate_sub_sequences(self) -> collections.abc.Generator[tuple[int, ...], None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_subtrees()):
            # retrieves the sub-sequence in the root RGF sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[i:i + sub_tree.size]
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_restricted_growth_function_sequences(self) -> \
            collections.abc.Generator[sl.RestrictedGrowthFunctionSequence, None, None]:
        s: sl.RestrictedGrowthFunctionSequence
        for s in self.iterate_sub_sequences():
            # converts ths sub-sequence to an RGF sequence, which modifies all values to start with 1.
            sub_sequence: sl.RestrictedGrowthFunctionSequence = sl.apply_canonical_labeling(
                s)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_formulas(self) -> collections.abc.Generator[CanonicalAbstractFormula, None, None]:
        """Iterates the sub-formulas of the `CanonicalAbstractFormula` using the `depth-first, ascending nodes` algorithm.

        See :attr:`AbstractFormula.sub_formulas` for a definition of the term `sub-formula`.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: sl.RestrictedGrowthFunctionSequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_subtrees(),
                                              self.iterate_sub_restricted_growth_function_sequences()):
            sub_formula = CanonicalAbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        """Returns a string representation of the :class:`CanonicalAbstractFormula` using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.restricted_growth_function_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of
        the :attr:`AbstractFormula.restricted_growth_function_sequence`. Default: `None`.
        :return:
        """
        if connectives is None:
            connectives = self.restricted_growth_function_sequence
        else:
            if len(connectives) != len(self.restricted_growth_function_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the canonical-abstract-formula's RGF sequence.",
                    connectives_length=len(connectives),
                    rgf_sequence_length=self.restricted_growth_function_sequence.length,
                    connectives=connectives,
                    rgf_sequence=self.restricted_growth_function_sequence,
                    abstract_formula=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    @property
    def restricted_growth_function_sequence(self) -> sl.RestrictedGrowthFunctionSequence:
        """Shortcut: self.s.

        :return:
        """
        return self[1]

    @property
    def sub_formulas(self) -> tuple[CanonicalAbstractFormula, ...]:
        """The `sub_formulas` of an `CanonicalAbstractFormula` `phi` is the tuple of `CanonicalAbstractFormula` elements that are present
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
            sub_formulas: list[CanonicalAbstractFormula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def substitute_sub_formulas(self, m: dict[
        FlexibleCanonicalAbstractFormula, FlexibleCanonicalAbstractFormula]) -> CanonicalAbstractFormula:
        """Returns a new :class:`CanonicalAbstractFormula`
        similar to the current :class:`CanonicalAbstractFormula` except that
        all sub-abstract-formulas present in the map `m` domain,
        are substituted with corresponding :class:`CanonicalAbstractFormula` elements in map `m` codomain,
        following the depth-first, ascending-nodes algorithm.

        :param m: A map AbstractFormula --> AbstractFormula.
        :return:
        """
        domain: tuple[CanonicalAbstractFormula, ...] = tuple(
            data_validate_canonical_abstract_formula(x) for x in m.keys())
        codomain: tuple[CanonicalAbstractFormula, ...] = tuple(
            data_validate_canonical_abstract_formula(y) for y in m.values())
        m: dict[CanonicalAbstractFormula, CanonicalAbstractFormula] = dict(zip(domain, codomain))
        immediate_sub_formulas: list[CanonicalAbstractFormula] = []
        phi: CanonicalAbstractFormula
        for phi in self.iterate_immediate_sub_formulas():
            if phi in m.keys():
                phi = m[phi]
                immediate_sub_formulas.append(phi)
            else:
                immediate_sub_formulas.append(phi)
        psi: CanonicalAbstractFormula = CanonicalAbstractFormula()
        raise NotImplementedError("Complete implementation here")


# Flexible types to facilitate data validation

FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, sl.FlexibleNaturalNumbersSequence], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

AF = AbstractFormula  # An alias for AbstractFormula

# Cache Management

_abstract_formula_cache = dict()  # cache mechanism assuring that unique abstract formulas are only instantiated once.


def retrieve_abstract_formula_from_cache(o: FlexibleAbstractFormula):
    """cache mechanism assuring that unique canonical abstract formulas are only instantiated once."""
    global _abstract_formula_cache
    o: AbstractFormula = data_validate_abstract_formula(o)
    if hash(o) in _abstract_formula_cache.keys():
        return _abstract_formula_cache[hash(o)]
    else:
        _abstract_formula_cache[hash(o)] = o
        return o
