from __future__ import annotations
import typing
import collections
import itertools

# package modules
import util
import rooted_plane_tree as rpt
import sequence_library as sl


def data_validate_canonical_abstract_formula(
        o: FlexibleCanonicalAbstractFormula) -> CanonicalAbstractFormula:
    if isinstance(o, CanonicalAbstractFormula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return CanonicalAbstractFormula(*o)
    if isinstance(o, collections.abc.Generator):
        return CanonicalAbstractFormula(*o)
    raise util.PunctiliousException('CanonicalAbstractFormula data validation failure', type_of_o=type(o), o=o)


_canonical_abstract_formula_cache = dict()  # cache mechanism assuring that unique abstract formulas are only instantiated once.


def retrieve_canonical_abstract_formula_from_cache(o: FlexibleCanonicalAbstractFormula):
    """cache mechanism assuring that unique canonical abstract formulas are only instantiated once."""
    global _canonical_abstract_formula_cache
    o: CanonicalAbstractFormula = data_validate_canonical_abstract_formula(o)
    if hash(o) in _canonical_abstract_formula_cache.keys():
        return _canonical_abstract_formula_cache[hash(o)]
    else:
        _canonical_abstract_formula_cache[hash(o)] = o
        return o


class CanonicalAbstractFormula(tuple):

    def __eq__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`CanonicalAbstractFormula`,
        returns `True` if `t` is abstract-formula-equivalent to this :class:`CanonicalAbstractFormula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: CanonicalAbstractFormula = data_validate_canonical_abstract_formula(t)
            return self.is_canonical_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((CanonicalAbstractFormula, self.rooted_plane_tree, self.restricted_growth_function_sequence,))

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleRestrictedGrowthFunctionSequence):
        super(CanonicalAbstractFormula, self).__init__()
        self._immediate_sub_formulas = None
        self._sub_formulas = None

    def __ne__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`CanonicalAbstractFormula`,
        returns `True` if `t` is not abstract-formula-equivalent to this :class:`CanonicalAbstractFormula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: CanonicalAbstractFormula = data_validate_canonical_abstract_formula(t)
            return not self.is_canonical_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleRestrictedGrowthFunctionSequence):
        t: rpt.RootedPlaneTree = rpt.data_validate_rooted_plane_tree(t)
        s: sl.RestrictedGrowthFunctionSequence = sl.data_validate_restricted_growth_function_sequence(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`CanonicalAbstractFormula` data validation error. The size of the `RootedPlaneGraph` is not equal to the length of the `RestrictedGrowthFunctionSequence`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        phi = super(CanonicalAbstractFormula, cls).__new__(cls, (t, s))
        phi = retrieve_canonical_abstract_formula_from_cache(phi)
        return phi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    @property
    def formula_degree(self) -> int:
        """The `formula_degree` of an `CanonicalAbstractFormula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rpt.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_depth_first_ascending():
            if t.degree > 0:
                i += 1
        return i

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

    def is_canonical_abstract_formula_equivalent_to(self, phi: CanonicalAbstractFormula):
        """Returns `True` if this :class:`CanonicalAbstractFormula` is abstract-formula-equivalent
        to :class:`CanonicalAbstractFormula` `phi`.

        Formal definition:
        Two abstract-formulas phi and psi are abstract-formula-equivalent if and only if:
        - the rooted-plane-tree of phi is rooted-plane-tree-equivalent to the rooted-plane-tree of psi,
        - the RGF-sequence of phi is sequence-equivalent to the RGF-sequence of psi.

        :param phi:
        :return:
        """
        phi: CanonicalAbstractFormula = data_validate_canonical_abstract_formula(phi)
        return self.rooted_plane_tree.is_rooted_plane_tree_equivalent_to(
            phi.rooted_plane_tree) and self.restricted_growth_function_sequence.is_restricted_growth_function_sequence_equivalent_to(
            phi.restricted_growth_function_sequence)

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
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_direct_ascending(),
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
        for child_tree in self.rooted_plane_tree.iterate_direct_ascending():
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
            sub_sequence: sl.RestrictedGrowthFunctionSequence = sl.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
                s)
            # yield this child RGF sequence
            yield sub_sequence

    def iterate_sub_sequences(self) -> collections.abc.Generator[tuple[int, ...], None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_depth_first_ascending()):
            # retrieves the sub-sequence in the root RGF sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[i:i + sub_tree.size]
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_restricted_growth_function_sequences(self) -> \
            collections.abc.Generator[sl.RestrictedGrowthFunctionSequence, None, None]:
        s: sl.RestrictedGrowthFunctionSequence
        for s in self.iterate_sub_sequences():
            # converts ths sub-sequence to an RGF sequence, which modifies all values to start with 1.
            sub_sequence: sl.RestrictedGrowthFunctionSequence = sl.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
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
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_depth_first_ascending(),
                                              self.iterate_sub_restricted_growth_function_sequences()):
            sub_formula = CanonicalAbstractFormula(child_tree, child_sequence)
            yield sub_formula

    @property
    def main_sequence_element(self) -> int:
        """The `main_sequence_element` of an `CanonicalAbstractFormula` is the first element of the
        attr:`AbstractFormula.restricted_growth_function_sequence`, that corresponds to the root
        node of the attr:`AbstractFormula.rooted_plane_tree`.

        By the definition of restricted growth function, the `main_sequence_element` is
        always equal to 0.

        Note that this is 0 by design choice of using 0 as the initial value
        of RGF sequences, instead of 1 which is usual in the literature. In effect, using
        0 is consistent with the design choice of using 0-based indexes in tuples,
        which is a natural choice in Python implementations.

        The term `main_sequence_element` was designed in reference to the term `main connective`,
        cf. Mancosu 2021, p. 17.

        References:
         - Mancosu 2021

        :return: 1
        """
        return self.restricted_growth_function_sequence[0]

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
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        """Shortcut: self.t."""
        return self[0]

    @property
    def s(self) -> sl.RestrictedGrowthFunctionSequence:
        """A shortcut for self.restricted_growth_function_sequence."""
        return self.restricted_growth_function_sequence

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of an `CanonicalAbstractFormula` is the `max_value` of its `restricted_growth_function_sequence`."""
        return self.restricted_growth_function_sequence.max_value

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

    @property
    def t(self) -> rpt.RootedPlaneTree:
        """A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @property
    def tree_degree(self) -> int:
        """The `tree_degree` of an `CanonicalAbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_degree` and `formula_degree`.
        """
        return self.rooted_plane_tree.degree

    @property
    def tree_size(self) -> int:
        """The `tree_size` of an `CanonicalAbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


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


def declare_formula_from_tree_of_integer_tuple_pairs(p) -> CanonicalAbstractFormula:
    """Declares a :class:`CanonicalAbstractFormula` object from a tree of integer / tuple pairs (n, T) where i is a natural number,
    and T a tree of integer / tuple pairs.

    Definition:
    A tree of integer tuple pairs `T` defined as:
     T := (n, T')
    where:
     - n is a natural number
     - T' is tree of integer tuple pairs.


    :param p:
    :return:
    """

    t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=p)
    t = rpt.build_rooted_plane_tree_from_tuple_tree(t)
    s = sl.RestrictedGrowthFunctionSequence(*s)
    phi = CanonicalAbstractFormula(t, s)
    return phi


def Declare_formula_from_immediate_sub_formulas(
        immediate_sub_formulas: tuple[FlexibleCanonicalAbstractFormula]) -> CanonicalAbstractFormula:
    """Given a sequence of abstract-formulas 𝛷, declares a new formula 𝜓 such that:
     - the formulas in 𝛷 are mapped to the immediate sub-formulas

    :param immediate_sub_formulas:
    :return:
    """
    immediate_sub_formulas: tuple[CanonicalAbstractFormula, ...] = tuple(
        data_validate_canonical_abstract_formula(o=phi) for phi in immediate_sub_formulas)
    phi: CanonicalAbstractFormula
    s: sl.RestrictedGrowthFunctionSequence = itertools.chain.from_iterable(
        phi.restricted_growth_function_sequence for phi in immediate_sub_formulas)
    phi = CanonicalAbstractFormula(t=t, s=s)
    raise NotImplementedError('review approach completely')


FlexibleCanonicalAbstractFormula = typing.Union[
    CanonicalAbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, sl.FlexibleRestrictedGrowthFunctionSequence], collections.abc.Iterator, collections.abc.Generator, None]


def data_validate_non_canonical_abstract_formula(
        o: FlexibleNonCanonicalAbstractFormula) -> NonCanonicalAbstractFormula:
    if isinstance(o, NonCanonicalAbstractFormula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return NonCanonicalAbstractFormula(*o)
    if isinstance(o, collections.abc.Generator):
        return NonCanonicalAbstractFormula(*o)
    raise util.PunctiliousException('NonCanonicalAbstractFormula data validation failure', type_of_o=type(o), o=o)


_non_canonical_abstract_formula_cache = dict()  # cache mechanism assuring that unique abstract formulas are only instantiated once.


def retrieve_non_canonical_abstract_formula_from_cache(o: FlexibleNonCanonicalAbstractFormula):
    """cache mechanism assuring that unique canonical abstract formulas are only instantiated once."""
    global _non_canonical_abstract_formula_cache
    o: NonCanonicalAbstractFormula = data_validate_non_canonical_abstract_formula(o)
    if hash(o) in _non_canonical_abstract_formula_cache.keys():
        return _non_canonical_abstract_formula_cache[hash(o)]
    else:
        _non_canonical_abstract_formula_cache[hash(o)] = o
        return o


class NonCanonicalAbstractFormula(tuple):

    def __eq__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`NonCanonicalAbstractFormula`,
        returns `True` if `t` is abstract-formula-equivalent to this :class:`NonCanonicalAbstractFormula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: NonCanonicalAbstractFormula = data_validate_non_canonical_abstract_formula(t)
            return self.is_non_canonical_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((NonCanonicalAbstractFormula, self.rooted_plane_tree, self.unrestricted_sequence,))

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleUnrestrictedSequence):
        super(NonCanonicalAbstractFormula, self).__init__()
        self._immediate_sub_formulas = None
        self._sub_formulas = None

    def __ne__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`NonCanonicalAbstractFormula`,
        returns `True` if `t` is not abstract-formula-equivalent to this :class:`NonCanonicalAbstractFormula`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: NonCanonicalAbstractFormula = data_validate_non_canonical_abstract_formula(t)
            return not self.is_non_canonical_abstract_formula_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: sl.FlexibleUnrestrictedSequence):
        t: rpt.RootedPlaneTree = rpt.data_validate_rooted_plane_tree(t)
        s: sl.UnrestrictedSequence = sl.data_validate_unrestricted_sequence(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`NonCanonicalAbstractFormula` data validation error. The size of the `RootedPlaneGraph` is not equal to the length of the `UnrestrictedSequence`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        phi = super(NonCanonicalAbstractFormula, cls).__new__(cls, (t, s))
        phi = retrieve_non_canonical_abstract_formula_from_cache(phi)
        return phi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    @property
    def formula_degree(self) -> int:
        """The `formula_degree` of an `NonCanonicalAbstractFormula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rpt.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_depth_first_ascending():
            if t.degree > 0:
                i += 1
        return i

    def get_sub_formula_by_path(self, p: tuple[int, ...]) -> NonCanonicalAbstractFormula:
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
            phi: NonCanonicalAbstractFormula = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= phi.tree_degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate sub-formulas in phi.", n_index=i, n_value=j,
                        phi=phi)
                phi: NonCanonicalAbstractFormula = phi.immediate_sub_formulas[j]
            return phi

    @property
    def immediate_sub_formulas(self) -> tuple[NonCanonicalAbstractFormula, ...]:
        """The `immediate_sub_formulas` of an `NonCanonicalAbstractFormula` `phi` is the tuple of `NonCanonicalAbstractFormula` elements
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

    def is_non_canonical_abstract_formula_equivalent_to(self, phi: NonCanonicalAbstractFormula):
        """Returns `True` if this :class:`NonCanonicalAbstractFormula` is non-canonical-abstract-formula-equivalent
        to :class:`NonCanonicalAbstractFormula` `phi`.

        Formal definition:
        Two non-canonical-abstract-formulas phi and psi are non-canonical-abstract-formula-equivalent if and only if:
        - the rooted-plane-tree of phi is rooted-plane-tree-equivalent to the rooted-plane-tree of psi,
        - the unrestricted-sequence of phi is unrestricted-sequence-equivalent to the unrestricted-sequence of psi.

        :param phi:
        :return:
        """
        phi: NonCanonicalAbstractFormula = data_validate_non_canonical_abstract_formula(phi)
        return self.rooted_plane_tree.is_rooted_plane_tree_equivalent_to(
            phi.rooted_plane_tree) and self.unrestricted_sequence.is_unrestricted_sequence_equivalent_to(
            phi.unrestricted_sequence)

    def is_sub_formula_of(self, phi: NonCanonicalAbstractFormula):
        """Returns `True` if this :class:`NonCanonicalAbstractFormula` if a sub-formula of :class:`NonCanonicalAbstractFormula` phi.

        :param phi:
        :return:
        """
        XXXX
        phi: NonCanonicalAbstractFormula = data_validate_non_canonical_abstract_formula(phi)
        psi: NonCanonicalAbstractFormula
        for psi in self.iterate_sub_formulas():
            if psi == phi:
                return True
        return False

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[NonCanonicalAbstractFormula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`NonCanonicalAbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`NonCanonicalAbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_direct_ascending(),
                                              self.iterate_immediate_sub_unrestricted_sequences()):
            sub_formula = NonCanonicalAbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_immediate_sub_sequences(self) -> typing.Generator[
        tuple[int, ...], None, None]:
        """Iterates the direct sub-sequences of this `NonCanonicalAbstractFormula`.

        Note:
            A sub-sequence is not an RGF sequence, i.e. its initial value may not be equal to 0,
            and it may contain maximal values that are greater than the ones allowed by restricted growth.

        Note:
            The child rgf sequences are determined by 1) the parent rgf sequence,
            and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rpt.RootedPlaneTree
        # truncated_sequence: tuple[int, ...] = self.unrestricted_sequence[1:]
        for child_tree in self.rooted_plane_tree.iterate_direct_ascending():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.unrestricted_sequence[i:i + child_tree.size]
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_immediate_sub_unrestricted_sequences(self) -> typing.Generator[
        sl.UnrestrictedSequence, None, None]:
        """Iterates the direct child sub-sequences of this `NonCanonicalAbstractFormula`.

        Note: the child rgf sequences are determined by 1) the parent rgf sequence,
        and 2) the rooted plane tree.
        """
        s: sl.UnrestrictedSequence
        for s in self.iterate_immediate_sub_sequences():
            # transform the sequence into an RGF sequence, restarting from initial value 0
            sub_sequence: sl.UnrestrictedSequence = sl.convert_arbitrary_sequence_to_unrestricted_sequence(
                s)
            # yield this child RGF sequence
            yield sub_sequence

    def iterate_sub_sequences(self) -> collections.abc.Generator[tuple[int, ...], None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_depth_first_ascending()):
            # retrieves the sub-sequence in the root RGF sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.unrestricted_sequence[i:i + sub_tree.size]
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_unrestricted_sequences(self) -> \
            collections.abc.Generator[sl.UnrestrictedSequence, None, None]:
        s: sl.UnrestrictedSequence
        for s in self.iterate_sub_sequences():
            # converts ths sub-sequence to an RGF sequence, which modifies all values to start with 1.
            sub_sequence: sl.UnrestrictedSequence = sl.convert_arbitrary_sequence_to_unrestricted_sequence(
                s)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_formulas(self) -> collections.abc.Generator[NonCanonicalAbstractFormula, None, None]:
        """Iterates the sub-formulas of the `NonCanonicalAbstractFormula` using the `depth-first, ascending nodes` algorithm.

        See :attr:`AbstractFormula.sub_formulas` for a definition of the term `sub-formula`.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: sl.UnrestrictedSequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_depth_first_ascending(),
                                              self.iterate_sub_unrestricted_sequences()):
            sub_formula = NonCanonicalAbstractFormula(child_tree, child_sequence)
            yield sub_formula

    @property
    def main_sequence_element(self) -> int:
        """The `main_sequence_element` of an `NonCanonicalAbstractFormula` is the first element of the
        attr:`AbstractFormula.unrestricted_sequence`, that corresponds to the root
        node of the attr:`AbstractFormula.rooted_plane_tree`.

        By the definition of restricted growth function, the `main_sequence_element` is
        always equal to 0.

        Note that this is 0 by design choice of using 0 as the initial value
        of RGF sequences, instead of 1 which is usual in the literature. In effect, using
        0 is consistent with the design choice of using 0-based indexes in tuples,
        which is a natural choice in Python implementations.

        The term `main_sequence_element` was designed in reference to the term `main connective`,
        cf. Mancosu 2021, p. 17.

        References:
         - Mancosu 2021

        :return: 1
        """
        return self.unrestricted_sequence[0]

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        """Returns a string representation of the :class:`NonCanonicalAbstractFormula` using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.unrestricted_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of
        the :attr:`AbstractFormula.unrestricted_sequence`. Default: `None`.
        :return:
        """
        if connectives is None:
            connectives = self.unrestricted_sequence
        else:
            if len(connectives) != len(self.unrestricted_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the non-canonical-abstract-formula's RGF sequence.",
                    connectives_length=len(connectives),
                    rgf_sequence_length=self.unrestricted_sequence.length,
                    connectives=connectives,
                    rgf_sequence=self.unrestricted_sequence,
                    abstract_formula=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    @property
    def unrestricted_sequence(self) -> sl.UnrestrictedSequence:
        """Shortcut: self.s.

        :return:
        """
        return self[1]

    @property
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        """Shortcut: self.t."""
        return self[0]

    @property
    def s(self) -> sl.UnrestrictedSequence:
        """A shortcut for self.unrestricted_sequence."""
        return self.unrestricted_sequence

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of an `NonCanonicalAbstractFormula` is the `max_value` of its `unrestricted_sequence`."""
        return self.unrestricted_sequence.max_value

    @property
    def sub_formulas(self) -> tuple[NonCanonicalAbstractFormula, ...]:
        """The `sub_formulas` of an `NonCanonicalAbstractFormula` `phi` is the tuple of `NonCanonicalAbstractFormula` elements that are present
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
            sub_formulas: list[NonCanonicalAbstractFormula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def substitute_sub_formulas(self, m: dict[
        FlexibleNonCanonicalAbstractFormula, FlexibleNonCanonicalAbstractFormula]) -> NonCanonicalAbstractFormula:
        """Returns a new :class:`NonCanonicalAbstractFormula`
        similar to the current :class:`NonCanonicalAbstractFormula` except that
        all sub-abstract-formulas present in the map `m` domain,
        are substituted with corresponding :class:`NonCanonicalAbstractFormula` elements in map `m` codomain,
        following the depth-first, ascending-nodes algorithm.

        :param m: A map AbstractFormula --> AbstractFormula.
        :return:
        """
        domain: tuple[NonCanonicalAbstractFormula, ...] = tuple(
            data_validate_non_canonical_abstract_formula(x) for x in m.keys())
        codomain: tuple[NonCanonicalAbstractFormula, ...] = tuple(
            data_validate_non_canonical_abstract_formula(y) for y in m.values())
        m: dict[NonCanonicalAbstractFormula, NonCanonicalAbstractFormula] = dict(zip(domain, codomain))
        immediate_sub_formulas: list[NonCanonicalAbstractFormula] = []
        phi: NonCanonicalAbstractFormula
        for phi in self.iterate_immediate_sub_formulas():
            if phi in m.keys():
                phi = m[phi]
                immediate_sub_formulas.append(phi)
            else:
                immediate_sub_formulas.append(phi)
        psi: NonCanonicalAbstractFormula = NonCanonicalAbstractFormula()
        raise NotImplementedError("Complete implementation here")

    @property
    def t(self) -> rpt.RootedPlaneTree:
        """A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @property
    def tree_degree(self) -> int:
        """The `tree_degree` of an `NonCanonicalAbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_degree` and `formula_degree`.
        """
        return self.rooted_plane_tree.degree

    @property
    def tree_size(self) -> int:
        """The `tree_size` of an `NonCanonicalAbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


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


def declare_formula_from_tree_of_integer_tuple_pairs(p) -> NonCanonicalAbstractFormula:
    """Declares a :class:`NonCanonicalAbstractFormula` object from a tree of integer / tuple pairs (n, T) where i is a natural number,
    and T a tree of integer / tuple pairs.

    Definition:
    A tree of integer tuple pairs `T` defined as:
     T := (n, T')
    where:
     - n is a natural number
     - T' is tree of integer tuple pairs.


    :param p:
    :return:
    """

    t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=p)
    t = rpt.build_rooted_plane_tree_from_tuple_tree(t)
    s = sl.UnrestrictedSequence(*s)
    phi = NonCanonicalAbstractFormula(t, s)
    return phi


def declare_formula_from_immediate_sub_formulas(
        immediate_sub_formulas: tuple[FlexibleNonCanonicalAbstractFormula]) -> NonCanonicalAbstractFormula:
    """Given a sequence of abstract-formulas 𝛷, declares a new formula 𝜓 such that:
     - the formulas in 𝛷 are mapped to the immediate sub-formulas

    :param immediate_sub_formulas:
    :return:
    """
    immediate_sub_formulas: tuple[NonCanonicalAbstractFormula, ...] = tuple(
        data_validate_non_canonical_abstract_formula(o=phi) for phi in immediate_sub_formulas)
    phi: NonCanonicalAbstractFormula
    s: sl.UnrestrictedSequence = itertools.chain.from_iterable(
        phi.unrestricted_sequence for phi in immediate_sub_formulas)
    phi = NonCanonicalAbstractFormula(t=t, s=s)
    raise NotImplementedError('review approach completely')


FlexibleNonCanonicalAbstractFormula = typing.Union[
    NonCanonicalAbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, sl.FlexibleUnrestrictedSequence], collections.abc.Iterator, collections.abc.Generator, None]
