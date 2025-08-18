"""

"""

from __future__ import annotations
import typing
import collections
import functools
# import itertools

# package modules
import punctilious.util as util
import punctilious.rooted_plane_tree_library as rptl
import punctilious.natural_number_0_sequence_library as nn0sl
import punctilious.binary_relation_library as brl
import punctilious.ternary_boolean_library as tbl
import punctilious.cantor_pairing_library as cpl


# General functions


def count_lrpt_of_size_exactly_x_and_label_max_value_y(tree_size: int, label_max_value: int) -> int:
    r"""Returns the number of distinct LRPTs
    whose size (number of nodes) is exactly equal to `x`,
    and whose labels are (0-based) natural numbers with maximal value equal to `y`.

    :param tree_size: The size of the tree (aka number of nodes).
    :param label_max_value: The maximal value of labels.
    :return: The number of distinct LRPTs.
    """
    tree_size: int = int(tree_size)
    label_max_value: int = int(label_max_value)
    if tree_size < 1:
        raise util.PunctiliousException("`tree_size` < 1", tree_size=tree_size, label_max_value=label_max_value)
    if label_max_value < 0:
        raise util.PunctiliousException("`label_max_value` < 0", tree_size=tree_size,
                                        label_max_value=label_max_value)
    number_of_trees_of_size_n: int = rptl.count_rooted_plane_trees_of_size_x(tree_size)
    number_of_labelled_trees: int = number_of_trees_of_size_n ** (label_max_value + 1)
    return number_of_labelled_trees


def count_lrpt_of_size_up_to_x_and_label_max_value_y(tree_size: int,
                                                     label_max_value: int) -> int:
    r"""Returns the number of distinct LRPTs
    whose size (number of nodes) is less than or equal to `x`,
    and whose labels are (0-based) natural numbers with maximal value equal to `y`.

    :param tree_size: The size of the tree (aka number of nodes).
    :param label_max_value: The maximal value of labels.
    :return: The number of distinct LRPTs.
    """
    tree_size: int = int(tree_size)
    label_max_value: int = int(label_max_value)
    if tree_size < 1:
        raise util.PunctiliousException("`tree_size` < 1", tree_size=tree_size, label_max_value=label_max_value)
    if label_max_value < 0:
        raise util.PunctiliousException("`label_max_value` < 0", tree_size=tree_size,
                                        label_max_value=label_max_value)
    number_of_labelled_trees: int = 0
    for tree_size_iteration in range(1, tree_size + 1):
        number_of_labelled_trees += count_lrpt_of_size_exactly_x_and_label_max_value_y(
            tree_size_iteration, label_max_value
        )
    return number_of_labelled_trees


# Binary relation classes

class IsEqualTo(brl.BinaryRelation):
    r"""The LRPTs equipped with the standard equality order relation.

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
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        y: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(y)
        return x.is_labeled_rooted_plane_tree_equivalent_to(y)


class RecursiveSequenceOrder(brl.BinaryRelation):
    r"""The LRPTs equipped with the standard strictly less-than order relation.

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
    def least_element(cls) -> LabeledRootedPlaneTree:
        """By design, we choose 0() as the least element.

        :return:
        """
        return LabeledRootedPlaneTree(
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
        # and s1, ..., sn are the recursive ranks of its subtrees.
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(x.main_element)
        for subtree in x.iterate_immediate_subtrees():
            subtree_rank: int = cls.rank(subtree)
            t: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(subtree_rank)
            s: nn0sl.NaturalNumber0Sequence = s.concatenate_with(t)
        ## then take the reverse sequence.
        ## the rational is that the punctilious use case is focused on formula manipulation,
        ## and high element values are first expected to occur to the right than to the left.
        # s = s.reverse
        raw_rank: int = nn0sl.AS1L2RL3O.rank(s)  # Retrieve the canonical rank of the sequence.
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
        s: nn0sl.NaturalNumber0Sequence = nn0sl.AS1L2RL3O.unrank(n)
        ## then take the reverse sequence.
        ## the rational is that the punctilious use case is focused on formula manipulation,
        ## and high element values are first expected to occur to the right than to the left.
        # s = s.reverse
        main_element: int = s[0]
        subtrees = []
        for i, m in enumerate(s[1:], 1):
            subtree = cls.unrank(m)
            subtrees.append(subtree)
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_immediate_subtrees(n=main_element,
                                                                                   s=subtrees)
        return t


class CantorPairingOrder(brl.BinaryRelation):
    r"""The Cantor pairing order of LRPTs.

    Note
    -----

    An LRPT can be defined as a tuple (T, S) where T is an LRP and S a (0-based) natural number sequence.
    Assuming there exists ranking functions for LRPs and (0-based) natural number sequences,
    then the Cantor pairing solution may be applied.

    Bibliography
    --------------

    - https://en.wikipedia.org/wiki/Pairing_function
    - https://www.cantorsparadise.org/cantor-pairing-function-e213a8a89c2b/

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Note
        ------

        The properties of this order is dependent on the properties
        of the chosen underlying orders for LRPs and (0-based) natural number sequences.

        """
        return tbl.TernaryBoolean.NOT_AVAILABLE

    @util.readonly_class_property
    def least_element(cls) -> LabeledRootedPlaneTree:
        """By design, we choose 0() as the least element.

        :return:
        """
        return LabeledRootedPlaneTree(
            t=rptl.RootedPlaneTree.least_element,
            s=nn0sl.NaturalNumber0Sequence(0)
        )

    @classmethod
    def rank(cls, x: object) -> int:
        r"""Applies the Cantor pairing function to the LRP and NN0 sequence."""
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        rpt_rank: int = x.rooted_plane_tree.rank
        s: int = x.natural_number_sequence.rank
        return cpl.cantor_pairing(rpt_rank, s)

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(x)
        y: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: object) -> object:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        r"""Applies the inverse Cantor pairing function.
        """
        x: int
        y: int
        x, y = cpl.cantor_pairing_inverse(n)
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.unrank(x)
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence.unrank(y)
        return LabeledRootedPlaneTree(t, s)


# Classes

class LabeledRootedPlaneTree(brl.ClassWithOrder, tuple):
    r"""A labeled rooted plane tree (LRPT).

     Definition
     ----------------------------------
     An LRPT is a tuple :math:`(T, S)` such that:

     - :math:`T` is a finite rooted plane tree (RPT),
     - :math:`S` is a finite sequence of (0-based) natural numbers,
     - :math:`|T| = |S|`.

    """

    def __hash__(self):
        return self._compute_hash(self)

    def __init__(self, t: rptl.FlexibleRootedPlaneTree, s: nn0sl.FlexibleNaturalNumber0Sequence):
        super(LabeledRootedPlaneTree, self).__init__()
        self._is_abstract_map: bool | None = None
        self._is_abstract_inference_rule: bool | None = None

    def __new__(cls, t: rptl.FlexibleRootedPlaneTree, s: nn0sl.FlexibleNaturalNumber0Sequence):
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_any(t)
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence.from_any(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`LabeledRootedPlaneTree` data validation error. The size of the tree `t` is not equal to the length of the sequence `s`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        lrpt = super(LabeledRootedPlaneTree, cls).__new__(cls, (t, s))
        # lrpt = cls._from_cache(lrpt)
        return lrpt

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    # _cache: dict[int, LabeledRootedPlaneTree] = dict()  # Cache mechanism.

    _HASH_SEED: int = 11651462149556646224  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def _compute_hash(cls, o: LabeledRootedPlaneTree) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a LRPT.
        :return: The hash of the LRPT that is structurally equivalent to `o`.
        """
        return hash((LabeledRootedPlaneTree, cls._HASH_SEED, o.rooted_plane_tree, o.natural_number_sequence,))

    # @classmethod
    # def _from_cache(cls, o: FlexibleLabeledRootedPlaneTree):
    #    r"""Cache mechanism used in the constructor."""
    #    hash_value: int = LabeledRootedPlaneTree._compute_hash(o)
    #    if hash_value in cls._cache.keys():
    #        return cls._cache[hash_value]
    #    else:
    #        cls._cache[hash_value] = o
    #        return o

    @functools.cached_property
    def abstract_inference_rule_conclusion(self) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-inference-rule, returns its conclusion.

        See :attr:`LabeledRootedPlaneTree.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the conclusion of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_subtrees[2]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-inference-rule.")

    @functools.cached_property
    def abstract_inference_rule_premises(self) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-inference-rule, returns its premises.

        See :attr:`LabeledRootedPlaneTree.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the premises of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_subtrees[1]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-inference-rule.")

    @functools.cached_property
    def abstract_inference_rule_variables(self) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-inference-rule, returns its variables.

        See :attr:`LabeledRootedPlaneTree.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the variables of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_subtrees[0]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-inference-rule.")

    @classmethod
    def abstract_map_from_preimage_and_image(
            cls,
            n: int,
            p: FlexibleLabeledRootedPlaneTree,
            i: FlexibleLabeledRootedPlaneTree) -> LabeledRootedPlaneTree:
        r"""Declares a new abstract-map.

        :param n: The main-element of the abstract-map.
        :param p: The preimage of the abstract-map.
        :param i: The image of the abstract-map.
        :return: The resulting abstract-map.
        """
        return LabeledRootedPlaneTree.from_immediate_subtrees(n=n, s=(p, i,))

    @functools.cached_property
    def abstract_map_preimage_sequence(self) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-map, returns its preimage sequence.

        See :attr:`LabeledRootedPlaneTree.is_abstract_map` for a detailed description of abstract-maps.

        :return: the preimage sequence of this map.
        """
        if self.is_abstract_map:
            return self.immediate_subtrees[0]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-map.")

    @functools.cached_property
    def abstract_map_image_sequence(self) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-map, returns its image sequence.

        See :attr:`LabeledRootedPlaneTree.is_abstract_map` for a detailed description of abstract-maps.

        :return: the image sequence of this map.
        """
        if self.is_abstract_map:
            return self.immediate_subtrees[1]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-map.")

    @functools.cached_property
    def abstract_set_arity(self) -> int:
        r"""Returns the arity of this abstract-set.

        Note
        ______

        This is equivalent to the degree of the LRPT.

        See also
        _________

        Cf.: :prop:`LabeledRootedPlaneTree.is_abstract_set`.

        :return: `True` or `False`.
        """
        return self.degree

    @functools.cached_property
    def abstract_set_elements(self) -> tuple[LabeledRootedPlaneTree, ...]:
        r"""Returns the elements of this abstract-set.

        Note
        ______

        This is equivalent to the immediate subtrees of the LRPT.

        See also
        _________

        Cf.: :prop:`LabeledRootedPlaneTree.is_abstract_set`.

        :return: A tuple of LRPTs.
        """
        return self.immediate_subtrees

    @functools.cached_property
    def degree(self) -> int:
        r"""Returns the degree of this LRPT.

        Definition
        ----------------

        The degree of an LRPT is the number of immediate subtrees under the root.

        :return:
        """
        return len(self.immediate_subtrees)

    @functools.cached_property
    def canonical_abstract_set(self) -> LabeledRootedPlaneTree:
        r"""Returns the canonical abstract-set of this abstract-set.

        In short:

        - Remove duplicate elements.
        - Canonically order elements.

        See also
        _________

        Cf.: :prop:`LabeledRootedPlaneTree`.

        :return: A canonical abstract-set.
        """
        s: tuple[LabeledRootedPlaneTree, ...] = ()
        t: LabeledRootedPlaneTree
        for t in self.abstract_set_elements:
            if t not in s:
                s = s + (t,)
        s = tuple(sorted(s))
        abstract_set: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_immediate_subtrees(
            n=self.main_element,
            s=s)
        return abstract_set

    @functools.cached_property
    def canonical_labeled_rooted_plane_tree(self) -> LabeledRootedPlaneTree:
        r"""The canonical LRPT of this LRPT.

        Definition: the canonical-LRPT `t` of a LRPT `psi`
        is a formula such that:

        - their rooted-plane-tree are rooted-plane-tree-equivalent,
        - the natural-number-sequence of `t` is the canonical-naturel-number-sequence
           of the natural-number-sequence of `psi`

        :return: The canonical-LRPT of this LRPT.
        """
        if self.is_canonical:
            return self
        else:
            return LabeledRootedPlaneTree(
                t=self.rooted_plane_tree,
                s=self.natural_number_sequence.restricted_growth_function_sequence)

    def derive_abstract_inference_rule(self, p: FlexibleLabeledRootedPlaneTree) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-inference-rule, derives a theorem
        from the finite (computable) sequence of premises `p`.

        See :attr:`LabeledRootedPlaneTree.is_abstract_inference_rule` for a detailed description of abstract-inference-rule.

        :param p: a finite (computable) sequence of premises, in the order expected by the inference-rule.
        :return: the theorem derived from this abstract-inference-rule, given premises `p`.
        """
        p: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(p)
        if self.is_abstract_inference_rule:
            if p.degree != self.abstract_inference_rule_premises.degree:
                raise util.PunctiliousException("The number of input premises is not equal to the number"
                                                " of premises expected by the inference-rule.",
                                                input_premises=p,
                                                expected_premises=self.abstract_inference_rule_premises,
                                                inference_rule=self)
            v: dict[LabeledRootedPlaneTree, LabeledRootedPlaneTree | None]  # A mapping for variable values

            i: LabeledRootedPlaneTree  # An input premise
            e: LabeledRootedPlaneTree  # An expected premise
            for i, e in zip(p.iterate_immediate_subtrees(), self.abstract_inference_rule_premises):
                ok, v = _compute_abstract_inference_rule_variables(v, i, e)
                if not ok:
                    pass
                else:
                    pass
        # TODO: IMPLEMENT INFERENCE-RULE LOGIC
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-inference-rule.")

    @functools.cached_property
    def formula_degree(self) -> int:
        r"""The `formula_degree` of an LRPT is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al., 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rptl.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_subtrees():
            if t.degree > 0:
                i += 1
        return i

    @classmethod
    def from_any(
            cls,
            o: FlexibleLabeledRootedPlaneTree) -> LabeledRootedPlaneTree:
        if isinstance(o, LabeledRootedPlaneTree):
            return o
        if isinstance(o, collections.abc.Iterable):
            return LabeledRootedPlaneTree(*o)
        if isinstance(o, collections.abc.Generator):
            return LabeledRootedPlaneTree(*o)
        raise util.PunctiliousException("`LabeledRootedPlaneTree` data validation failure. `o` is of unknown type.",
                                        type_of_o=type(o), o=o)

    @classmethod
    def from_immediate_subtrees(
            cls,
            n: int | None,
            s: tuple[FlexibleLabeledRootedPlaneTree, ...] | None = None) -> LabeledRootedPlaneTree:
        r"""Given a root natural number n,
        and a tuple of LRPTs s,
        declares a new formula 𝜓 := n(s_0, s_1, ..., s_n) where s_i is an element of s.

        :param n:
        :param s:
        :return:
        """
        n: int = int(n)
        if n < 0:
            raise util.PunctiliousException("`n` is not a (0-based) natural number.", n=n)
        if s is None:
            s: tuple[LabeledRootedPlaneTree, ...] = ()
        s: tuple[LabeledRootedPlaneTree, ...] = tuple(
            LabeledRootedPlaneTree.from_any(o=sub_lrpt) for sub_lrpt in s)
        # Retrieves the children trees
        sub_rpts: tuple[rptl.RootedPlaneTree, ...] = tuple(sub_lrpt.rooted_plane_tree for sub_lrpt in s)
        # Declare the new parent tree
        rpt: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_immediate_subtrees(*sub_rpts)
        # Declare the natural-number-sequence by appending n to the concatenation of the
        # children natural-number-sequences.
        u: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(
            n) + nn0sl.concatenate_natural_number_0_sequences(
            *(subtree.natural_number_sequence for subtree in s))
        lrpt: LabeledRootedPlaneTree = LabeledRootedPlaneTree(t=rpt, s=u)
        return lrpt

    @classmethod
    def from_tree_of_integer_tuple_pairs(cls, p) -> LabeledRootedPlaneTree:
        r"""Declares a LRPT object from a tree of integer/tuple pairs.

        Use case
        ___________

        Tree of integer/tuple pairs is a natural pythonic data structure to express LRPTs.

        Definition
        ------------

        A tree of integer/tuple pairs `T` defined as:

        .. math::

            T := (n, T\prime)

        where:

        - :math:`n` is a natural number
        - :math:`\prime` is (possibly empty) tuple of trees of integer/tuple pairs.

        Sample
        --------

        The tree of integer/tuple pairs:
        (0, ((1,(),),(0,((2,(),),(1,(),),),),(2,(),),),)

        ...maps to the LRPT:
        0(1,0(2,1),2)

        :param p: A tree of integer/tuple pairs.
        :return: a LRPT.

        """

        t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=p)
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_tuple_tree(t)
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*s)
        lrpt: LabeledRootedPlaneTree = LabeledRootedPlaneTree(t, s)
        return lrpt

    def get_abstract_map_value(self, t: FlexibleLabeledRootedPlaneTree) -> LabeledRootedPlaneTree:
        r"""If this LRPT is an abstract-map, returns the image `t` under this map.

        See :attr:`LabeledRootedPlaneTree.is_abstract_map` for a detailed description of abstract-maps.

        :param t: a preimage element.
        :return: the image of `t` under this map.
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        if self.is_abstract_map:
            i: int = self.abstract_map_preimage_sequence.get_immediate_subtree_index(t)
            return self.abstract_map_image_sequence.immediate_subtrees[i]
        else:
            raise util.PunctiliousException("This LRPT is not an abstract-map.")

    def get_immediate_subtree_index(self, t: FlexibleLabeledRootedPlaneTree):
        r"""Returns the 0-based index position of `t` in this LRPT immediate subtrees.

        Prerequisites:

        - the immediate subtrees of this LRPT are unique, cf. :attr:`LabeledRootedPlaneTree.immediate_subtrees_are_unique`,
        - `t` is an immediate subtree of this LRPT.

        :param t:
        :return:
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        if not self.immediate_subtrees_are_unique:
            raise util.PunctiliousException(
                'The immediate subtrees of this LRPT are not unique.',
                this_tree=self, t=t)
        if not t in self.immediate_subtrees:
            raise util.PunctiliousException('`t` is not an immediate subtrees of this LRPT.',
                                            this_tree=self, t=t)

        return self.immediate_subtrees.index(t)

    def get_subtree_by_path(self, p: tuple[int, ...]) -> LabeledRootedPlaneTree:
        r"""Given a path `p`, returns the corresponding subtree.

        Definition - subtree path:
        A subtree path is a finite sequence of natural numbers >= 0, of length > 0,
        that gives the index position of the subtrees, following the depth-first algorithm,
        starting with 0 meaning the original tree.

        It follows that for any tree `t`, the path (0) returns the tree itself.

        :param p:
        :return:
        """
        p: tuple[int, ...] = tuple(int(n) for n in p)
        if p[0] != 0:
            raise util.PunctiliousException("The first element of the path is not equal to 0.", p0=p[0], p=p,
                                            this_lrpt=self)
        if p == (0,):
            return self
        else:
            lrpt: LabeledRootedPlaneTree = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= lrpt.tree_degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate subtrees in t.", n_index=i, n_value=j,
                        lrpt=lrpt)
                lrpt: LabeledRootedPlaneTree = lrpt.immediate_subtrees[j]
            return lrpt

    def has_abstract_set_element(self, t: FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if `t` is an element of this abstract-set, `False` otherwise.

        Cf. :prop:`LabeledRootedPlaneTree.is_abstract_set`.

        :param t: An abstract-set.
        :return: `True` or `False`
        """
        return self.has_immediate_subtree(t)

    def has_immediate_subtree(self, t: FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if `t` is a subtree of this LRPT, `False` otherwise.

        :param t: An LRPT.
        :return: `True` or `False`
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        return t in self.immediate_subtrees

    def has_subtree(self, t: LabeledRootedPlaneTree):
        r"""Returns `True` if LRPT t is a subtree of this LRPT.

        :param t:
        :return:
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        return t.is_subtree_of(self)

    @functools.cached_property
    def height(self):
        r"""Returns the height (aka level) of the LRPT.

        Definition
        ------------
        The height (aka level) of an LRPT is the height of its RPT..

        Notation
        ---------
        If :math:`T` is an LRPT, :math:`h(T) denotes its height.`

        Bibliography
        -------------
        - Gross, Jonathan L., and Jay Yellen, eds. Handbook of Graph Theory. Discrete Mathematics and Its Applications. CRC Press, 2004.


        """
        return self.rooted_plane_tree.height

    @functools.cached_property
    def immediate_subtrees(self) -> tuple[LabeledRootedPlaneTree, ...]:
        r"""The `immediate_subtrees` of an LRPT `t` is the tuple of LRPT elements
        that are the immediate children trees of `t` in the formula tree, or equivalently the formulas
        of degree 0 in `t`.

        The term `immediate subtree` is used by (Mancosu 2021, p. 17-18).

        See also:

        - :attr:`LabeledRootedPlaneTree.subtrees`

        References:

        - Mancosu 2021.

        :return:
        """
        subtrees: tuple[LabeledRootedPlaneTree, ...] = ()
        subtree: LabeledRootedPlaneTree
        for subtree in self.iterate_immediate_subtrees():
            subtrees = subtrees + (subtree,)
        return subtrees

    @functools.cached_property
    def immediate_subtrees_are_unique(self) -> bool:
        r"""Returns `True` if all immediate subtrees contained in this LRPT
        are unique.

        Trivial case:
        If the LRPT is a leaf, i.e. it contains no immediate subtrees,
        then all of its immediate subtrees are unique.

        :return:
        """
        unique_values: set[LabeledRootedPlaneTree] = set()
        psi: LabeledRootedPlaneTree
        for psi in self.iterate_immediate_subtrees():
            if psi in unique_values:
                return False
            unique_values.add(psi)
        return True

    @functools.cached_property
    def is_abstract_map(self) -> bool:
        r"""Returns `True` if this LRPT is an abstract-map, `False` otherwise.

        Intuitive definition: abstract-map
        ______________________________________

        Intuitively, an abstract-map is a LRPT that is structurally
         equivalent to a finite (computable) map.

        Syntactical definition
        _________________________________

        An abstract map :math:`M` is an LRPT such that:
        - its degree equal 2,
        - its first subtree, denoted as the preimage, is a canonical abstract set,
        - its second subtree, denoted as the image, has equal degree with its first subtree.

        Note
        _____

        The following properties and methods are available when a LRPT is an abstract-map:

        - :attr:`LabeledRootedPlaneTree.abstract_map_preimage`
        - :attr:`LabeledRootedPlaneTree.abstract_map_image`
        - :meth:`LabeledRootedPlaneTree.get_abstract_map_value`

        :return: `True` or `False`.

        """
        return self.degree == 2 and \
            self.immediate_subtrees[0].degree == self.immediate_subtrees[1].degree and \
            self.immediate_subtrees[0].is_canonical_abstract_set

    @functools.cached_property
    def is_abstract_inference_rule(self) -> bool:
        r"""Returns `True` if this LRPT is an abstract-inference-rule, `False` otherwise.

        Intuitive definition: abstract-inference-rule
        ___________________________________________________

        Intuitively, an abstract-inference-rule is a LRPT that is structurally
         equivalent to an inference rule.

        Formal definition: abstract-inference-rule
        ______________________________________________

        An abstract-inference-rule :math:`I` is a tuple :math:`(V, P, C)` where:

        - :math:`V` is a finite sequence of unique elements denoted as the variables,
        - :math:`P` is a finite sequence of unique elements denoted as the premises,
        - :math:`C` is denoted as the conclusion.

        Formal definition: abstract-inference-rule
        _______________________________________________

        A LRPT is an abstract-inference-rule if and only if:

         - its arity equals 3.

        Note
        _____

        The following complementary properties and methods are available when a LRPT is an abstract-map:

        - :attr:`abstract_inference_rule_variables`
        - :attr:`abstract_inference_rule_premises`
        - :attr:`abstract_inference_rule_conclusion`
        - :meth:`derive_abstract_inference_rule`

        :return: `True` if this LRPT is an abstract-inference-rule, `False` otherwise.

        """
        if self._is_abstract_inference_rule is None:
            self._is_abstract_inference_rule = \
                self.degree == 3
        return self._is_abstract_inference_rule

    @functools.cached_property
    def is_abstract_set(self) -> bool:
        r"""Returns `True` if this LRPT is an abstract-set, `False` otherwise.

        Intuitive definition: abstract-set
        ______________________________________

        Intuitively, an abstract-set is an LRPT that is structurally
         equivalent to a finite (computable) mathematical set.

        Syntactic definition: abstract-set
        ___________________________________

        A finite (computable) abstract-set :math:`S` if and only if it is an LRPT.

        Syntactic definition: canonical abstract-set
        ______________________________________________

        An abstract-set is canonical if and only if:

        - its immediate subtrees are unique,
        - its immediate subtrees are canonically ordered.

        Note
        _____

        The following properties and methods are available when a LRPT is an abstract-map:

        - :attr:`LabeledRootedPlaneTree.canonical_abstract_set`
        - :attr:`LabeledRootedPlaneTree.has_abstract_set_element`
        - :attr:`LabeledRootedPlaneTree.is_abstract_set_element_of`

        :return: `True` or `False`.

        """
        return True

    def is_abstract_set_element_of(self, t: FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if this LRPT is an element of abstract-set `t`, `False` otherwise.

        Cf. :prop:`LabeledRootedPlaneTree.is_abstract_set`.

        :param t: An abstract-set.
        :return: `True` or `False`
        """
        return self.is_immediate_subtree_of(t)

    @functools.cached_property
    def is_canonical_abstract_set(self) -> bool:
        r"""Returns `True` if this LRPT is a canonical abstract set, `False` otherwise.

        Syntactic definition: canonical abstract-set
        ______________________________________________

        An abstract-set is canonical if and only if:

        - its immediate subtrees are unique,
        - its immediate subtrees are canonically ordered.

        See also
        __________

        - :attr:`LabeledRootedPlaneTree.is_abstract_set`

        :return: `True` or `False`.

        """
        return self == self.canonical_abstract_set

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    def is_immediate_subtree_of(self, t: FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if this LRPT is an immediate subtree of `t`, `False` otherwise.

        :param t: An LRPT.
        :return: `True` or `False`
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        return self in t.immediate_subtrees

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return RecursiveSequenceOrder

    def is_labeled_rooted_plane_tree_equivalent_to(self, t: LabeledRootedPlaneTree):
        r"""Returns `True` if this LRPT is LRPT-equivalent
        to LRPT `t`.

        Formal definition:
        Two LRPTs t and psi are LRPT-equivalent if and only if:

        - the rooted-plane-tree of t is rooted-plane-tree-equivalent to the rooted-plane-tree of psi,
        - the natural-numbers-sequence of t is natural-numbers-sequence-equivalent to the natural-numbers-sequence of psi.

        :param t:
        :return:
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        return self.rooted_plane_tree.is_rooted_plane_tree_equivalent_to(
            t.rooted_plane_tree) and self.natural_number_sequence.is_natural_number_0_sequence_equivalent_to(
            t.natural_number_sequence)

    def is_labeled_rooted_plane_tree_equivalent_to_with_variables(self, t: LabeledRootedPlaneTree,
                                                                  v: LabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if this LRPT is LRPT-equivalent to LRPT `t`,
        after substitution of variables with assigned values in this LRPT,
        according to variables and assigned values in abstract-map `v`.

        :param t: A LRPT.
        :param v: An abstract-map whose preimage is denoted as the variables, and image as the assigned values.
        :return: `True` if trees are equivalent given above conditions, `False` otherwise.
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        v: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(v)
        if not v.is_abstract_map:
            raise util.PunctiliousException("`v` is not an abstract-map", v=v, t=t,
                                            this_labeled_rooted_plane_tree=self)
        psi: LabeledRootedPlaneTree = self.substitute_subtrees_with_map(m=v)
        return psi.is_labeled_rooted_plane_tree_equivalent_to(t)

    @functools.cached_property
    def is_canonical(self) -> bool:
        r"""Returns `True` if this LRPT is in canonical form.

        Definition:
        A LRPT `t` is `canonical` if and only if
        its natural-number-sequence is a restricted-growth-function-sequence.

        :return: `True` if this LRPT is in canonical form, `False` otherwise.
        """
        return self.natural_number_sequence.is_restricted_growth_function_sequence

    def is_canonical_labeled_rooted_plane_tree_equivalent_to(self, t: LabeledRootedPlaneTree):
        r"""Returns `True` if this LRPT is canonical-LRPT-equivalent
        to LRPT `t`.

        Formal definition:
        Two LRPTs t and psi are canonical-LRPT-equivalent if and only if:

        - the canonical-LRPT of t is LRPT-equivalent
          to the canonical-LRPT of psi.

        Intuitive definition:
        Two trees are canonical-LRPT-equivalent if they have the same "structure".

        :param t:
        :return:
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        return self.canonical_labeled_rooted_plane_tree.is_labeled_rooted_plane_tree_equivalent_to(
            t.canonical_labeled_rooted_plane_tree)

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return RecursiveSequenceOrder

    @functools.cached_property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this LRPT is increasing, `False` otherwise.

        Definition - increasing LRPT:
        A LRPT is increasing
        or increasing under canonical order,
        if its immediate subtrees are ordered.

        Definition - increasing LRPT:
        A LRPT :math:`\t = c(\psi_0, \psi1, \cdots, \psi_l)` is increasing,
        or increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} \ge \psi_i`.

        :return: `True` if this LRPT is increasing, `False` otherwise.
        """
        return all(
            self.immediate_subtrees[i + 1] >= self.immediate_subtrees[i] for i in range(0, self.degree - 1))

    @functools.cached_property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this LRPT is strictly increasing, `False` otherwise.

        Definition - strictly increasing LRPT:
        A LRPT is strictly increasing
        or strictly increasing under canonical order,
        if its immediate subtrees are strictly ordered.

        Definition - strictly increasing LRPT:
        A LRPT :math:`\t = c(\psi_0, \psi1, \cdots, \psi_l)` is strictly increasing,
        or strictly increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} > \psi_i`.

        :return: `True` if this LRPT is strictly increasing, `False` otherwise.
        """
        return all(
            self.immediate_subtrees[i + 1] > self.immediate_subtrees[i] for i in range(0, self.degree - 1))

    def is_subtree_of(self, t: LabeledRootedPlaneTree):
        r"""Returns `True` if this LRPT is a subtree of LRPT t.

        :param t:
        :return:
        """
        t: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(t)
        psi: LabeledRootedPlaneTree
        for psi in t.iterate_subtrees():
            if self.is_labeled_rooted_plane_tree_equivalent_to(psi):
                return True
        return False

    def iterate_immediate_subtrees(self) -> collections.abc.Generator[LabeledRootedPlaneTree, None, None]:
        r"""Iterates the immediate subtrees of the LRPT.

        See :attr:`LabeledRootedPlaneTree.immediate_subtrees` for a definition of the term `immediate subtree`.

        :return: A generator of LRPT.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_immediate_subtrees(),
                                              self.iterate_immediate_sub_sequences()):
            subtree: LabeledRootedPlaneTree = LabeledRootedPlaneTree(child_tree, child_sequence)
            yield subtree

    def iterate_immediate_sub_sequences(self) -> typing.Generator[
        nn0sl.NaturalNumber0Sequence, None, None]:
        r"""Iterates the immediate (children) sub-:class:`UnrestrictedSequence` of this LRPT.

        Note:

        A sub-sequence of a LRPT is determined by:

        - 1) the parent rgf sequence,
        - and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rptl.RootedPlaneTree
        for child_tree in self.rooted_plane_tree.iterate_immediate_subtrees():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + child_tree.size]
            sub_sequence: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*sub_sequence)
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_sub_sequences(self) -> collections.abc.Generator[nn0sl.NaturalNumber0Sequence, None, None]:
        i: int
        sub_tree: rptl.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_subtrees()):
            # retrieves the sub-sequence in the sequence
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + sub_tree.size]
            sub_sequence: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*sub_sequence)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_subtrees(self) -> collections.abc.Generator[LabeledRootedPlaneTree, None, None]:
        r"""Iterates the subtrees of the LRPT using the `depth-first, ascending nodes` algorithm.

        See :attr:`LabeledRootedPlaneTree.subtrees` for a definition of the term `subtree`.

        :return:
        """
        child_tree: rptl.RootedPlaneTree
        child_sequence: nn0sl.NaturalNumber0Sequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_subtrees(),
                                              self.iterate_sub_sequences()):
            subtree = LabeledRootedPlaneTree(child_tree, child_sequence)
            yield subtree

    @util.readonly_class_property
    def least_element(cls) -> LabeledRootedPlaneTree:
        return cls.is_strictly_less_than_relation.least_element

    @functools.cached_property
    def main_element(self) -> int:
        r"""The `main_element` of an LRPT is the first element of its
        attr:`LabeledRootedPlaneTree.natural_numbers_sequence`, that corresponds to the root
        node of the attr:`LabeledRootedPlaneTree.rooted_plane_tree`.

        The term `main element` was coined in reference to the term `main connective`
         (cf. Mancosu 2021, p. 17), because LRPTs are composed of sequences,
         and thus `main connective` is reserved for "concrete" formulas.

        References:

        - Mancosu 2021

        :return: 1
        """
        return self.natural_number_sequence[0]

    @functools.cached_property
    def natural_number_sequence(self) -> nn0sl.NaturalNumber0Sequence:
        r"""Returns the :class:`NaturalNumberSequence` component of this LRPT.

        Shortcut: self.s.

        :return:
        """
        return super().__getitem__(1)

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        r"""Returns a string representation of the LRPT using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`LabeledRootedPlaneTree.natural_numbers_sequence` .

        :param connectives: A tuple of connectives of length equal to the length of the :attr:`LabeledRootedPlaneTree.natural_numbers_sequence` . Default: `None`.

        :return:

        """
        if connectives is None:
            connectives = self.natural_number_sequence
        else:
            if len(connectives) != len(self.natural_number_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the LRPT's natural-number-sequence.",
                    connectives_length=len(connectives),
                    natural_number_sequence_length=self.natural_number_sequence.length,
                    connectives=connectives,
                    natural_number_sequence=self.natural_number_sequence,
                    labeled_tree=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    def represent_as_map_extension(self, connectives: tuple | None = None) -> str:
        r"""Returns a string representation of the LRPT using map notation.

        By default, connectives are represented by their respective values
        in the :attr:`LabeledRootedPlaneTree.natural_numbers_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of the :attr:`LabeledRootedPlaneTree.natural_numbers_sequence`. Default: `None`.

        :return: A string representation of this LRPT.

        """
        if connectives is None:
            connectives = self.natural_number_sequence
        else:
            if len(connectives) != len(self.natural_number_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the LRPT's natural-number-sequence.",
                    connectives_length=len(connectives),
                    natural_number_sequence_length=self.natural_number_sequence.length,
                    connectives=connectives,
                    natural_number_sequence=self.natural_number_sequence,
                    labeled_rooted_plane_tree=self
                )
        output = f"{{ "
        first = True
        for i, preimage, j, image in zip(
                range(1, 1 + self.abstract_map_preimage_sequence.degree),
                self.abstract_map_preimage_sequence.immediate_subtrees,
                range(1 + self.abstract_map_preimage_sequence.degree,
                      1 + 2 * self.abstract_map_preimage_sequence.degree),
                self.abstract_map_image_sequence.immediate_subtrees):
            if not first:
                output = f"{output}, "
            output = f"{output}{preimage} ⟼ {image}"
            first = False
        output = f"{output} }}"

        return output

    @functools.cached_property
    def rooted_plane_tree(self) -> rptl.RootedPlaneTree:
        r"""The :class:`RootedPlaneTree` component of this LRPT.

        Shortcut: self.t.

        """
        return super().__getitem__(0)

    @functools.cached_property
    def s(self) -> nn0sl.NaturalNumber0Sequence:
        r"""A shortcut for self.natural_numbers_sequence.

        """
        return self.natural_number_sequence

    @functools.cached_property
    def sequence_max_value(self) -> int:
        r"""The `sequence_max_value` of an LRPT is the `max_value` of its `natural_numbers_sequence`.

        """
        return self.natural_number_sequence.max_value

    @functools.cached_property
    def subtrees(self) -> tuple[LabeledRootedPlaneTree, ...]:
        r"""The `subtrees` of an LRPT `t` is the tuple of LRPT elements that are present
        in the formula tree of `t`, including `t` itself.

        Formal definition:

        - If t is an atomic formula, the subtrees of t is the tuple (t).
        - If t is a non-atomic formula, the subtrees of t is the tuple
           composed of t, and all subtrees of the immediate subtrees of t,
           in ascending order.
        - Nothing else is a subtree.

        This definition is a generalization of the term `formula` defined by (Mancosu 2021, definition 2.2, p. 14)
        for propositional-logic.

        See also:

        - :attr:`LabeledRootedPlaneTree.immediate_subtrees`

        References:
        - Mancosu 2021.

        :return: A tuple of the subtrees.
        """
        subtrees: tuple[LabeledRootedPlaneTree, ...] = ()
        subtree: LabeledRootedPlaneTree
        for subtree in self.iterate_subtrees():
            subtrees = subtrees + (subtree,)
        return subtrees

    def substitute_subtrees_with_map(self, m: FlexibleLabeledRootedPlaneTree) -> LabeledRootedPlaneTree:
        r"""Returns a new LRPT similar to the current LRPT,
         except that its subtrees present in the map `m` preimage,
         are substituted with their corresponding images,
         giving priority to the substitution of supertrees over subtrees.

        :param m: An abstract-map.
        :return: A substituted tree.

        """
        m: LabeledRootedPlaneTree = LabeledRootedPlaneTree.from_any(m)
        if not m.is_abstract_map:
            raise util.PunctiliousException("`m` is not an abstract-map.", m=m, this_abstract_formula=self)
        if self in m.abstract_map_preimage_sequence.immediate_subtrees:
            # This formula must be substituted according to the substitution map.
            return m.get_abstract_map_value(self)
        else:
            # Pursue substitution recursively.
            t: LabeledRootedPlaneTree
            s: tuple[LabeledRootedPlaneTree, ...] = tuple(t.substitute_subtrees_with_map(m=m) for t in
                                                          self.iterate_immediate_subtrees())
            return LabeledRootedPlaneTree.from_immediate_subtrees(n=self.main_element, s=s)

    @functools.cached_property
    def t(self) -> rptl.RootedPlaneTree:
        r"""A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @functools.cached_property
    def tree_degree(self) -> int:
        r"""The `tree_degree` of an LRPT is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_degree` and `formula_degree`.
        """
        return self.rooted_plane_tree.degree

    @functools.cached_property
    def tree_size(self) -> int:
        r"""The `tree_size` of an LRPT is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


# Transformation functions


def extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p):
    r"""Given a tree of integer/tuple pairs, extracts:

     - its tree of tuples,
     - and its sequence of integers,

    following the depth-first ascending-nodes algorithm.

    :param p: the tree of integer/tuple pairs

    :return: a pair (T, S) where T is a tree of tuples, and S is a sequence of integers.
    """

    if isinstance(p, int):
        return LabeledRootedPlaneTree(t=(()), s=(p,))

    if len(p) == 1:
        return LabeledRootedPlaneTree(t=(()), s=(p[0],))

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


# Flexible types to facilitate data validation

FlexibleLabeledRootedPlaneTree = typing.Union[
    LabeledRootedPlaneTree, tuple[
        rptl.FlexibleRootedPlaneTree, nn0sl.FlexibleNaturalNumber0Sequence], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

cantor_pairing_order = CantorPairingOrder
LRPT = LabeledRootedPlaneTree  # An alias for AbstractFormula
empty_tree: LabeledRootedPlaneTree = LabeledRootedPlaneTree.least_element
trivial_tree: LabeledRootedPlaneTree = LabeledRootedPlaneTree.least_element
recursive_reverse_sequence_order = RecursiveSequenceOrder
RSO = RecursiveSequenceOrder
