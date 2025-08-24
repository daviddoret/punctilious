r"""

TODO: IMPLEMENT EQUAL AND STRICTLY LESS THAN ORDERS

"""

from __future__ import annotations
import typing
import collections
import collections.abc
import functools

# package modules
import punctilious.util as util
import punctilious.connective_library as cl
import punctilious.labeled_rooted_plane_tree_library as afl
import punctilious.natural_number_0_sequence_library as sl
import punctilious.connective_sequence_library as csl
import punctilious.binary_relation_library as brl
import punctilious.ternary_boolean_library as tbl


# Binary relation classes

class IsEqualTo(brl.BinaryRelation):
    r"""The formulas equipped with the standard equality order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{F}, = )`.

    """

    @util.readonly_class_property
    def is_antisymmetric(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object.
        :param y: A Python object.
        :return: `True` or `False`.
        """
        x: Formula = Formula.from_any(x)
        y: Formula = Formula.from_any(y)
        return x.is_formula_equivalent_to(y)


class RecursiveSequenceOrder(brl.BinaryRelation):
    r"""The labeled rooted plane trees equipped with the standard strictly less-than order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{F}_0, < )`.

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> Formula:
        """By design, we choose 0() as the least element.

        Connectives do not have an obvious least element.

        :return:
        """
        return Formula(
            t=rptl.RootedPlaneTree.least_element,
            s=nn0sl.NaturalNumber0Sequence(0)
        )

    @classmethod
    def rank(cls, x: object) -> int:
        r"""Returns the rank of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A Python object interpretable as a (0-based) natural number.
        :return: An integer.
        """
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        # build a finite sequence of (0-based) natural numbers S = s0, s1, ..., sn,
        # such that s0 is `x`'s main element,
        # and s1, ..., sn are the recursive ranks of its sub-formulas.
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(x.root_label)
        for subtree in x.iterate_immediate_subtrees():
            subtree_rank: int = cls.rank(subtree)
            t: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(subtree_rank)
            s: nn0sl.NaturalNumber0Sequence = s.concatenate_with(t)
        raw_rank: int = nn0sl.RefinedGodelNumberOrder.rank(s)  # Retrieve the canonical rank of the sequence.
        r: int = raw_rank - 1  # "- 1" because the empty sequence is not encoded.
        return r

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object interpretable as a (0-based) natural number.
        :param y: A Python object interpretable as a (0-based) natural number.
        :return: `True` or `False`.
        """
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        y: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(y)
        n1: int = x.rank
        n2: int = y.rank
        return n1 < n2

    @classmethod
    def successor(cls, x: object) -> object:
        r"""Returns the successor of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A Python object interpretable as a (0-based) natural number.
        :return: The successor of `x`.
        """
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        n: int = cls.rank(x)
        n += 1
        y: LabeledRootedPlaneTree = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> LabeledRootedPlaneTree:
        r"""Returns the (0-based) natural number of `x` such that its rank in :math:`( \mathbb{N}_0, < ) = n`.

        :param n: A positive integer.
        :return: A (0-based) natural number.
        """
        n = int(n)
        if n < 0:
            raise util.PunctiliousException("`n` must be a positive integer.", n=n)
        n += 1  # Corrects the absence of the empty sequence in the encoding.
        # unrank the (0-based) natural sequence that is encoded in the rank.
        s: nn0sl.NaturalNumber0Sequence = nn0sl.RefinedGodelNumberOrder.unrank(n)
        main_element: int = s[0]
        subtrees = []
        for i, m in enumerate(s[1:], 1):
            subtree = cls.unrank(m)
            subtrees.append(subtree)
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_immediate_subtrees(*subtrees, n=main_element)
        return t


# Classes


class Formula(brl.ClassWithOrder, tuple):
    """

    Definition
    _____________

    A `Formula` is a pair (ϕ, M) where:

    - ϕ is a labeled rooted plane tree of tree-size n.
    - M is a bijective map between the subset of natural-numbers N,
       and a set of connectives C.

    """

    def __eq__(self, phi) -> bool:
        """Returns `True` if this formula is equal to formula `phi`, `False` otherwise.

        See :attr:`Formula.is_equal_to` for a definition of formula equality.

        :param phi: A formula.
        :return: `True` if this formula is equal to formula `c`, `False` otherwise.
        """
        return self.is_equal_to(phi)

    def __hash__(self):
        return self.compute_hash(self)

    def __init__(self, t: afl.FlexibleLabeledRootedPlaneTree, s: sl.FlexibleConnectiveSequence):
        super(Formula, self).__init__()
        self._immediate_sub_formulas = None
        self._sub_formulas = None

    def __new__(cls, t: afl.FlexibleLabeledRootedPlaneTree, s: csl.FlexibleConnectiveSequence):
        t: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(t)
        s: csl.ConnectiveSequence = csl.ConnectiveSequence.from_any(s)
        t: afl.LabeledRootedPlaneTree = t.canonical_labeled_rooted_plane_tree  # Canonize the labeled rooted plane tree
        if s.length != t.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" labeled tree.",
                s_length=s.length, phi_tree_size=t.tree_size, s=s, phi=t)
        psi = super(Formula, cls).__new__(cls, (t, s,))
        psi = cls._from_cache(psi)
        return psi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    _cache: dict[int, Formula] = dict()  # Cache mechanism.

    _HASH_SEED: int = 11701184968249671969  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def compute_hash(cls, o: Formula) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with an formula.
        :return: The hash of the formula that is structurally equivalent to `o`.
        """
        return hash((Formula, cls._HASH_SEED, o.labeled_rooted_plane_tree, o.connective_sequence,))

    @classmethod
    def _from_cache(cls, o: FlexibleFormula):
        """Cache mechanism used in the constructor."""
        hash_value: int = Formula.compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    @functools.cached_property
    def arity(self) -> int:
        r"""Returns the arity of the formula.

        Definition: arity of a formula
        The arity of a formula :math:`\Phi = (\Psi, S)`
        where math:`Psi` is a labeled rooted plane tree, and :math:`S` is a connective-sequence,
        is the arity of its labeled rooted plane tree :math:`Psi`.

        :return: the arity of the formula.
        """
        return self.labeled_rooted_plane_tree.degree

    @functools.cached_property
    def labeled_rooted_plane_tree(self) -> afl.LabeledRootedPlaneTree:
        """Returns the LRPT component of this formula.


        :return:
        """
        return tuple.__getitem__(self, 0)

    @functools.cached_property
    def connective_sequence(self) -> csl.ConnectiveSequence:
        """

        `connective_sequence` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 1)

    @functools.cached_property
    def formula_degree(self) -> int:
        """The `formula_degree` of a `Formula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        return self.labeled_rooted_plane_tree.formula_degree

    @classmethod
    def from_any(cls,
                 o: FlexibleFormula) -> Formula:
        if isinstance(o, Formula):
            return o
        if isinstance(o, collections.abc.Iterable):
            return Formula(*o)
        if isinstance(o, collections.abc.Generator):
            return Formula(*o)
        raise util.PunctiliousException('Formula data validation failure', o=o)

    def get_connective_by_sequence_element(self, i: int) -> cl.Connective:
        return self.connective_sequence[i]

    @functools.cached_property
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
        sub_formulas: list[Formula] = list()
        for sub_formula in self.iterate_immediate_sub_formulas():
            sub_formulas.append(sub_formula)
        return tuple(sub_formulas)

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    def is_formula_equivalent_to(self, phi: Formula):
        """Returns `True` if this :class:`Formula` is formula-equivalent
        to :class:`Formula` `phi`.

        Formal definition:
        Two formulas phi and psi are formula-equivalent if and only if:
        - the labeled rooted plane tree of phi is labeled rooted plane tree-equivalent to the labeled rooted plane tree of psi,
        - the connective-sequence of phi is connective-sequence-equivalent to the connective-sequence of psi.

        :param phi:
        :return:
        """
        phi: Formula = Formula.from_any(phi)
        return self.labeled_rooted_plane_tree.is_labeled_rooted_plane_tree_equivalent_to(
            phi.labeled_rooted_plane_tree) and self.connective_sequence.is_connective_sequence_equivalent_to(
            phi.connective_sequence)

    def is_immediate_sub_formula_of(self, phi: Formula) -> bool:
        """Returns `True` if `phi` is an immediate sub-formula of the current `Formula`, `False` otherwise.

        :param phi:
        :return:
        """
        phi: Formula = Formula.from_any(phi)
        return any(self.is_formula_equivalent_to(psi) for psi in phi.iterate_immediate_sub_formulas())

    def is_immediate_super_formula_of(self, phi: Formula):
        """Returns `True` if :class:`Formula` phi is an immediate sub-formula of this :class:`Formula`.

        :param phi:
        :return:
        """
        phi: Formula = Formula.from_any(phi)
        return phi.is_immediate_sub_formula_of(self)

    @functools.cached_property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this formula is increasing, `False` otherwise.

        Definition - increasing formula:
        An formula is increasing
        or increasing under canonical order,
        if its immediate subformulas are ordered.

        Definition - increasing formula:
        A formula :math:`\phi = c(\psi_0, \psi1, \cdots, \psi_l)` is increasing,
        or increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} \ge \psi_i`.

        :return: `True` if this formula is increasing, `False` otherwise.
        """
        return all(
            self.immediate_sub_formulas[i + 1] >= self.immediate_sub_formulas[i] for i in range(0, self.arity - 1))

    @functools.cached_property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this formula is strictly increasing, `False` otherwise.

        Definition - strictly increasing formula:
        An formula is strictly increasing
        or strictly increasing under canonical order,
        if its immediate subformulas are strictly ordered.

        Definition - strictly increasing formula:
        A formula :math:`\phi = c(\psi_0, \psi1, \cdots, \psi_l)` is strictly increasing,
        or strictly increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} > \psi_i`.

        :return: `True` if this formula is strictly increasing, `False` otherwise.
        """
        return all(
            self.immediate_sub_formulas[i + 1] > self.immediate_sub_formulas[i] for i in range(0, self.arity - 1))

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return RecursiveSequenceOrder

    def is_sub_formula_of(self, phi: Formula) -> bool:
        """Returns `True` if `phi` is a sub-formula of the current `Formula`, `False` otherwise.

        :param phi:
        :return:
        """
        phi: Formula = Formula.from_any(phi)
        return any(self.is_formula_equivalent_to(psi) for psi in phi.iterate_sub_formulas())

    def is_super_formula_of(self, phi: Formula):
        """Returns `True` if :class:`Formula` phi is a sub-formula of this :class:`Formula`.

        :param phi:
        :return:
        """
        phi: Formula = Formula.from_any(phi)
        return phi.is_sub_formula_of(self)

    def iterate_connectives(self) -> collections.abc.Generator[cl.Connective, None, None]:
        """Iterate the `Formula` connectives, following the depth-first, ascending-nodes algorithm.

        :return: None
        """
        i: int
        c: cl.Connective
        for i in self.labeled_rooted_plane_tree.natural_number_sequence:
            yield self.get_connective_by_sequence_element(i)

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`Formula`.

        See :attr:`Formula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`Formula`.
        """
        for phi, s in zip(self.labeled_rooted_plane_tree.iterate_immediate_subtrees(),
                          self.labeled_rooted_plane_tree.iterate_immediate_sub_sequences()):
            s: tuple[int, ...] = util.deduplicate_integer_sequence(s)
            t: tuple[cl.Connective, ...] = tuple(
                self.get_connective_by_sequence_element(i) for i in s)
            yield Formula(phi, t)

    def iterate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        for phi, s in zip(self.labeled_rooted_plane_tree.iterate_subtrees(),
                          self.labeled_rooted_plane_tree.iterate_sub_sequences()):
            s: tuple[int, ...] = util.deduplicate_integer_sequence(s)
            t: tuple[cl.Connective, ...] = tuple(
                self.get_connective_by_sequence_element(i) for i in s)
            yield Formula(phi, t)

    @functools.cached_property
    def main_connective(self) -> cl.Connective:
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
        return self.labeled_rooted_plane_tree.represent_as_function(connectives=self.connective_sequence)

    @functools.cached_property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of a `Formula` is the `sequence_max_value` of its `abstract_formula`."""
        return self.labeled_rooted_plane_tree.sequence_max_value

    @functools.cached_property
    def sub_formulas(self) -> tuple[Formula, ...]:
        """The `sub_formulas` of an `Formula` `phi` is the tuple of `Formula` elements that are present
        in the formula tree of `phi`, including `phi` itself.

        Formal definition
        ____________________

        - If phi is an atomic formula, the sub-formulas of phi is the tuple (phi).
        - If phi is a non-atomic formula, the sub-formulas of phi is the tuple
           composed of phi, and all sub-formulas of the immediate sub-formulas of phi,
           in ascending order.
        - Nothing else is a sub-formula.

        This definition is a generalization of the term `formula` defined by (Mancosu 2021, definition 2.2, p. 14)
        for propositional-logic.

        See also
        __________

        - :attr:`Formula.immediate_sub_formulas`

        References
        ____________

        - Mancosu 2021.

        :return: A tuple of the sub-formulas.

        """
        sub_formulas: list[Formula] = list()
        for sub_formula in self.iterate_sub_formulas():
            sub_formulas.append(sub_formula)
        return tuple(sub_formulas)

    def substitute_sub_formulas(self, m: dict[FlexibleFormula, FlexibleFormula]) -> Formula:
        """Returns a new :class:`Formula` similar to the current :class:`Formula` except that
        all sub-formulas present in the map `m` domain,
        are substituted with corresponding :class:`Formula` elements in map `m` codomain,
        following the depth-first, ascending-nodes algorithm.

        :param m: A map Formula --> Formula.
        :return:
        """
        domain: tuple[Formula, ...] = tuple(Formula.from_any(x) for x in m.keys())
        codomain: tuple[Formula, ...] = tuple(Formula.from_any(y) for y in m.values())
        m: dict[Formula, Formula] = dict(zip(domain, codomain))
        sub_formulas: list[Formula] = []
        immediate_abstract_formulas: list[afl.LabeledRootedPlaneTree] = []
        for phi in self.iterate_immediate_sub_formulas():
            if phi in m.keys():
                psi = m[phi]
                sub_formulas.append(psi)
                immediate_abstract_formulas.append(psi.labeled_rooted_plane_tree)
            else:
                sub_formulas.append(phi)
                immediate_abstract_formulas.append(phi.labeled_rooted_plane_tree)
        abstract_formula: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree()
        raise NotImplementedError("Complete implementation")

    @functools.cached_property
    def tree_size(self) -> int:
        """The `tree_size` of a `Formula` is the number of vertices in the `RootedPlaneTree` of its `abstract_formula`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.labeled_rooted_plane_tree.tree_size


# Data types

FlexibleFormula = typing.Union[
    Formula, tuple[
        csl.FlexibleConnectiveSequence, afl.FlexibleLabeledRootedPlaneTree], collections.abc.Iterator, collections.abc.Generator, None]
