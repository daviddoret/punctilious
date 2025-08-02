# Feature flags
from __future__ import annotations

# Python native packages
import typing
import collections
# import weakref
import functools

# Punctilious modules
import punctilious.util as util
import punctilious.binary_relation_library as brl
import punctilious.dyck_word_library as dwl
import punctilious.ternary_boolean_library as tbl
import punctilious.catalan_number_library as cnl


# General functions

def count_rooted_plane_trees_of_size_x(n: int) -> int:
    """Returns the number of distinct rooted plane trees whose size (aka number of nodes) equals `x`.

    :param n: The size (aka number of nodes) of the trees.
    :return: The number of distinct trees.
    """
    n = int(n)
    if n < 0:
        raise util.PunctiliousException("")
    return cnl.get_catalan_number(n=n)


# Binary relation classes

class DyckWordLexicographicOrder(brl.BinaryRelation):
    r"""The Dyck word lexicographic relation order of rooted plane trees.

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        See the proof under :meth:`dwl.LexicographicOrder.is_order_isomorphic_with_n_strictly_less_than`.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> object:
        return RootedPlaneTree()

    @classmethod
    def rank(cls, x: object) -> int:
        r"""

        Note
        -----
        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        """
        x: RootedPlaneTree = RootedPlaneTree.from_any(x)
        d: dwl.DyckWord = x.dyck_word
        return dwl.lexicographic_order.rank(d)

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: RootedPlaneTree = RootedPlaneTree.from_any(x)
        y: RootedPlaneTree = RootedPlaneTree.from_any(y)
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
        n: int = int(n)
        d: dwl.DyckWord = dwl.LexicographicOrder.unrank(n)
        t: RootedPlaneTree = RootedPlaneTree.from_dyck_word(d)
        return t


class IsEqualTo(brl.BinaryRelation):
    r"""The equality binary-relation for rooted plane trees.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{T}, = )`.

    """

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: RootedPlaneTree = RootedPlaneTree.from_any(x)
        y: RootedPlaneTree = RootedPlaneTree.from_any(y)
        return x.is_rooted_plane_tree_equivalent_to(y)


class RootedPlaneTree(brl.OrderIsomorphicToNaturalNumber0AndStrictlyLessThanStructure, tuple):
    r"""A `RootedPlaneTree` is an immutable, finite (and computable) rooted plane tree,
    aka rooted ordered tree.

    Reminder
    ------------
    Theorem 3.11 A graph G is a tree if and only if every two vertices of G are connected by a unique path.
    Chartrand, Lesniak, and Zhang, Graphs & Digraphs: Sixth Edition, p. 65.

    """

    def __hash__(self):
        return self._compute_hash(self)

    def __init__(self, *children: FlexibleRootedPlaneTree, tuple_tree: TupleTree = None):
        r"""

        If all parameters are passed as None or empty tuples, a single node `RootedPlaneTree` is returned.

        :param children: A tuple of FlexibleRootedPlaneTree instances.
        :param tuple_tree: A `TupleTree` structure.
        """
        super(RootedPlaneTree, self).__init__()
        self._subtrees: tuple[RootedPlaneTree, ...] | None = None

    def __new__(cls, *children: FlexibleRootedPlaneTree, tuple_tree: TupleTree = None):
        if tuple_tree is not None:
            t = RootedPlaneTree.from_tuple_tree(tuple_tree)
            t = super(RootedPlaneTree, cls).__new__(cls, t)
            t = RootedPlaneTree._from_cache(t)
            return t
        elif children is not None:
            children: tuple[RootedPlaneTree, ...] = tuple(
                RootedPlaneTree.from_any(child) for child in children)
            t = super(RootedPlaneTree, cls).__new__(cls, children)
            t = RootedPlaneTree._from_cache(t)
            return t
        elif children is None and tuple_tree is None:
            t = super(RootedPlaneTree, cls).__new__(cls, tuple())
            t = RootedPlaneTree._from_cache(t)
            return t
        else:
            raise util.PunctiliousException('Invalid input parameters', children=children, tuple_tree=tuple_tree)

    def __repr__(self):
        return self.represent_as_anonymous_function()

    def __str__(self):
        return self.represent_as_anonymous_function()

    _cache: dict[int, RootedPlaneTree] = dict()  # Cache mechanism.

    # Not supported because RootedPlaneTree primarily inherits from tuple.
    # __slots__ = ('__weakref__',)  # Enables caching mechanism with weakref.
    # _cache = weakref.WeakValueDictionary()  #

    _HASH_SEED: int = 327761738191040375  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def _compute_hash(cls, o: FlexibleRootedPlaneTree) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a rooted-plane-tree.
        :return: The hash of the rooted-plane-tree that is structurally equivalent to `o`.
        """
        return hash((RootedPlaneTree, cls._HASH_SEED, tuple(RootedPlaneTree._compute_hash(x) for x in o),))

    @classmethod
    def _from_cache(cls, o: FlexibleRootedPlaneTree):
        r"""Cache mechanism used in the constructor."""
        hash_value: int = RootedPlaneTree._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    @property
    def dyck_word(self) -> dwl.DyckWord:
        r"""The Dyck string representation of this rooted plane tree.

        Definition - Dyck string:
        A Dyck string is a string of balanced parentheses.

        References:
        - https://en.wikipedia.org/wiki/Dyck_language
        - AHU (Aho, Hopcroft, and Ullman)

        :return: A Dyck word.
        """
        if self.is_leaf:
            return dwl.DyckWord("()")
        else:
            child_encodings = [child.dyck_word for child in self.immediate_subtrees]
            raw_string: str = "(" + "".join(child_encodings) + ")"
            return dwl.DyckWord(raw_string)

    @property
    def degree(self) -> int:
        r"""The `degree` of a rooted-plane-tree is the number of immediate subtrees it has.

        :return:
        """
        return super().__len__()

    @classmethod
    def from_any(cls, o: FlexibleRootedPlaneTree) -> RootedPlaneTree:
        r"""Declares a rooted-plane-tree from a Python object that can be interpreted as a rooted-plane-tree.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a rooted-plane-tree.
        :return: a rooted-plane-tree.
        """
        if isinstance(o, RootedPlaneTree):
            return o
        if isinstance(o, collections.abc.Iterable):
            return RootedPlaneTree(*o)
        if isinstance(o, collections.abc.Generator):
            return RootedPlaneTree(*o)
        raise util.PunctiliousException('FlexibleRootedPlaneTree data validation failure', o=o)

    @classmethod
    def from_dyck_word(cls, o: dwl.FlexibleDyckWord) -> RootedPlaneTree:
        r"""Declares a rooted-plane-tree from a Dyck word.

        :param o: a Dyck word.
        :return: a rooted-plane-tree.
        """
        o: dwl.DyckWord = dwl.DyckWord.from_any(o)
        stack = []
        current = None
        for char in o:
            if char == '(':
                new_node = []
                if stack:
                    stack[-1].append(new_node)
                stack.append(new_node)
            elif char == ')':
                if len(stack) > 1:
                    current = stack.pop()
                    # Convert to tuple when popping
                    stack[-1][-1] = tuple(current) if current else ()
                else:
                    current = stack.pop()
                    current = tuple(current) if current else ()

        t: tuple = current if current is not None else ()
        t: RootedPlaneTree = RootedPlaneTree.from_tuple_tree(t)
        return t

    @classmethod
    def from_immediate_subtrees(cls, *t: FlexibleRootedPlaneTree) -> RootedPlaneTree:
        r"""Declares a rooted-plane-tree from a collection of immediate subtrees.

        Given an ordered collection of rooted-plate-trees :math:`T_0, T_1, \cdots, T_n`,
        returns a new rooted-plane tree :math:`S`
        such that :math:`S`'s immediate subtrees are :math:`T_0, T_1, \cdots, T_n`.

        Note:
            This method is redundant with the default constructor.

        :param t: a collection of immediate subtrees.
        :return: a rooted-plane-tree.
        """
        return RootedPlaneTree(*t)

    @classmethod
    def from_tuple_tree(cls, t) -> RootedPlaneTree:
        r"""Declares a rooted-plane-tree from a tree of python tuples.

        :param t: a tree of python tuples.
        :return: a rooted-plane-tree.
        """
        if t is None:
            # Returns the leaf rooted-plane-tree.
            return cls()
        elif len(t) == 0:
            # Returns the leaf rooted-plane-tree.
            return cls()
        else:
            # Recursively declare immediate subtrees from python tuple children.
            children: tuple[RootedPlaneTree, ...] = tuple(RootedPlaneTree.from_tuple_tree(u) for u in t)
            return cls(*children)

    def get_subtree_by_path(self, p: tuple[int, ...]) -> RootedPlaneTree:
        r"""Given a path `p`, returns the corresponding subtree.

        Definition - rooted-plane-tree path:
        A rooted-plane-tree path is a finite sequence of natural numbers >= 0, of length > 0,
        that gives the index position of the sub-plane-trees, following the depth-first algorithm,
        starting with 0 meaning the original tree.

        It follows that for any tree `t`, the path (0) returns the tree itself.

        :param p:
        :return:
        """
        p: tuple[int, ...] = tuple(int(n) for n in p)
        if p[0] != 0:
            raise util.PunctiliousException("The first element of the path is not equal to 0.", p0=p[0], p=p)
        if p == (0,):
            return self
        else:
            t: RootedPlaneTree = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= t.degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate sub-rooted-plane-trees in t.", n_index=i, n_value=j,
                        t=t)
                t: RootedPlaneTree = t.immediate_subtrees[j]
            return t

    @property
    def immediate_subtrees(self) -> tuple[RootedPlaneTree, ...]:
        r"""The tuple of immediate subtrees.

        :return: the tuple of the immediate subtrees.
        """
        # return tuple(super().__iter__()) # alternative implementation.
        return tuple.__new__(tuple, self)  # this implementation seems more "direct".

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this rooted-plane-tree is increasing, `False` otherwise.

        Definition - increasing rooted-plane-tree:
        A rooted-plane-tree is increasing
        or increasing under canonical order,
        if its immediate subtrees are ordered.

        Definition - increasing rooted-plane-tree:
        A rooted-plane-tree :math:`T = (S_0, S1, \cdots, S_l)` is increasing,
        or increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, S_{i + 1} \ge S_i`.

        :return: `True` if this rooted-plane-tree is increasing, `False` otherwise.
        """
        return all(
            self.immediate_subtrees[i + 1] >= self.immediate_subtrees[i] for i in range(0, self.degree - 1))

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return DyckWordLexicographicOrder

    @property
    def is_leaf(self) -> bool:
        r"""Returns `True` if the RootedPlaneTree is a leaf, `False` otherwise.

        A `RootedPlaneTree` is a leaf if and only if it contains no children.
        """
        return self.degree == 0

    def is_rooted_plane_tree_equivalent_to(self, t: FlexibleRootedPlaneTree) -> bool:
        r"""Returns `True` if this rooted-plane-tree is connective-equivalent to rooted-plane-tree `t`.

        Formal definition 1
        _______________________

        A rooted-plane-tree `t` is connective-equivalent to a rooted-plane-tree `u` if and only if
        - degree(t) = degree(u).
        - and immediate sub-rooted-plane-tree t_i of t is-rooted-plane-tree-equivalent to immediate sub-rooted-plane-tree u_i of u with 0 <= i < degree(t) - 1.

        Formal definition 2
        _______________________

        A rooted-plane-tree `t` is connective-equivalent to a rooted-plane-tree `u` if and only if
        the unsorted-inverted-integer AHU of `t` = the unsorted-inverted-integer AHU of `u`.

        :param t: A rooted-plane-tree.
        :return:
        """
        t: RootedPlaneTree = RootedPlaneTree.from_any(t)
        t_i: RootedPlaneTree
        u_i: RootedPlaneTree
        return self.degree == t.degree and all(t_i.is_rooted_plane_tree_equivalent_to(u_i) for t_i, u_i in
                                               zip(t.iterate_immediate_subtrees(), self.iterate_immediate_subtrees()))
        # Equivalent implementation:
        # return t.ahu_unsorted_inverted_integer == self.ahu_unsorted_inverted_integer

    @property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this rooted-plane-tree is strictly increasing, `False` otherwise.

        Definition - strictly increasing rooted-plane-tree:
        A rooted-plane-tree is strictly increasing
        or strictly increasing under canonical order,
        if its immediate subtrees are strictly ordered.

        Definition - strictly increasing rooted-plane-tree:
        A rooted-plane-tree :math:`T = (S_0, S1, \cdots, S_l)` is strictly increasing,
        or strictly increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, S_{i} < S_{i+1}`.

        Use case
        --------

        This property is important to create a model of finite sets and ordered sets using labeled rooted plane trees,
        which further makes it possible to create a model finite maps, etc.

        :return: `True` if this rooted-plane-tree is strictly increasing, `False` otherwise.
        """
        return all(
            self.immediate_subtrees[i] < self.immediate_subtrees[i + 1] for i in range(0, self.degree - 1))

    def iterate_immediate_subtrees(self) -> typing.Generator[RootedPlaneTree, None, None]:
        r"""Generator function that iterates the immediate subtrees of this rooted-plane-tree.
        following the canonical vertex ordering.

        :yields: RootedPlaneTree - a subtree.
        :return: None
        """
        yield from super().__iter__()

    def iterate_subtrees(self) -> typing.Generator[RootedPlaneTree, None, None]:
        r"""Generator function that iterates recursively the subtrees of this rooted-plane-tree.
        using the depth-first / canonical vertex ordering algorithm.

        :yields: RootedPlaneTree - a subtree.
        :return: None
        """
        yield self  # Yield the initial rooted-plane-tree itself.
        for child in self.immediate_subtrees:  # Recursively yield subtrees from the immediate subtrees.
            yield from child.iterate_subtrees()

    @util.readonly_class_property
    def least_element(cls) -> RootedPlaneTree:
        return cls.is_strictly_less_than_relation.least_element

    def represent_as_anonymous_function(self) -> str:
        output: str = "★"
        if not self.is_leaf:
            output += "("
        for i, child in enumerate(self.immediate_subtrees):
            if i > 0:
                output += ", "
            output += child.represent_as_anonymous_function()
        if not self.is_leaf:
            output += ")"
        return output

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        if connectives is None:
            # By default, represent connectives with natural numbers.
            connectives: tuple[int] = tuple(range(0, self.size))
        if len(connectives) != self.size:
            raise util.PunctiliousException("The length of the connectives `c` is not equal to "
                                            "the size of the rooted-plane-tree `t`.",
                                            c_length=len(connectives),
                                            c=connectives,
                                            t_size=self.size,
                                            t=self)
        output: str = str(connectives[0])
        if not self.is_leaf:
            output += "("
        j = 1
        for child in self.immediate_subtrees:
            if j > 1:
                output += ", "
            sub_sequence = connectives[j:j + child.size]
            output += child.represent_as_function(connectives=sub_sequence)
            j += child.size
        if not self.is_leaf:
            output += ")"
        return output

    def represent_as_multiline_string_vertical_tree_representation(self, prefix="", is_root=True, is_first=True,
                                                                   is_last=True) -> str:
        r"""Returns a multiline string representation of this `RootedPlaneTree`.

        May be useful to get a quick visual understanding of the tree structure.

        Sample
        -------

        .. code-block:: text

            ⬤━┳━⬤
              ┣━⬤━━━⬤
              ┣━⬤━┳━⬤
              ┃   ┣━⬤
              ┃   ┗━⬤
              ┗━⬤━━━⬤

        """
        output: str = ""
        if is_root:
            output = "⬤"
        elif is_first and is_last:
            output = "━━━⬤"
        elif is_first and not is_last:
            output = "━┳━⬤"
        elif not is_last:
            output = " ┣━⬤"
        elif is_last:
            output = " ┗━⬤"
        elif self.is_leaf:
            output = "━━━⬤"
        if not is_root and not is_first:
            output = "\n" + prefix + output
        # Update the prefix for child levels
        if is_root:
            new_prefix = prefix + " "
        elif is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + " ┃  "

        child_count: int = len(self.immediate_subtrees)
        for i, child in enumerate(self.immediate_subtrees):
            is_first_child = (i == 0)
            is_last_child = (i == child_count - 1)
            output = output + child.represent_as_multiline_string_vertical_tree_representation(new_prefix, False,
                                                                                               is_first_child,
                                                                                               is_last_child)
        return output

    def select_sub_tree_from_path_sequence(self, s: tuple[int, ...]) -> RootedPlaneTree:
        # TODO: Implement data-validation, including first element == 1
        current_rooted_plane_tree: RootedPlaneTree = self
        for i, n in enumerate(s):
            if i != 0:
                current_rooted_plane_tree = current_rooted_plane_tree.immediate_subtrees[n - 1]
        return current_rooted_plane_tree

    @property
    def size(self):
        r"""Returns the size of this `RootedPlaneTree`.

        Definition: the size of a rooted plan tree is the total number of vertices in the graph."""
        return 1 + sum(child.size for child in self.immediate_subtrees)

    def substitute_subtree(self, m: dict[FlexibleRootedPlaneTree, FlexibleRootedPlaneTree]) -> RootedPlaneTree:
        raise NotImplementedError('TO BE IMPLEMENTED')

    @property
    def subtrees(self) -> tuple[RootedPlaneTree, ...]:
        r"""The tuple of subtrees ordered by the depth-first / canonical vertex ordering algorithm.

        :return: the tuple of the subtrees.
        """
        if self._subtrees is None:
            self._subtrees = tuple(self.iterate_subtrees())
        return self._subtrees

    def to_list(self) -> list:
        r"""Returns a Python `list` of equivalent structure. This is useful to manipulate formulas because
        lists are mutable."""
        return list(self.immediate_subtrees)


FlexibleRootedPlaneTree = typing.Union[
    RootedPlaneTree, tuple[RootedPlaneTree, ...], collections.abc.Iterator, collections.abc.Generator, None]

TupleTree: typing.TypeAlias = typing.Union[int, tuple["TupleTree", ...]]
r"""A `TupleTree` is a tree of tuples whose leafs are empty empty tuples.

It allows to express RootedPlaneTree using python tuple syntax, e.g.: ( (), (), ( (), (), ), )

"""

RPT = RootedPlaneTree  # An alias for RootedPlaneTree.
dyck_word_lexicographic_order = DyckWordLexicographicOrder
is_equal_to = IsEqualTo
trivial_rooted_plane_tree = RootedPlaneTree()
empty_rooted_plane_tree = RootedPlaneTree()
