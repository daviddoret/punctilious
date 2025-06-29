from __future__ import annotations
import typing
import collections
import util


def data_validate_rooted_plane_tree(o: FlexibleRootedPlaneTree) -> RootedPlaneTree:
    if isinstance(o, RootedPlaneTree):
        return o
    if isinstance(o, collections.abc.Iterable):
        return RootedPlaneTree(*o)
    if isinstance(o, collections.abc.Generator):
        return RootedPlaneTree(*o)
    raise util.PunctiliousException('FlexibleRootedPlaneTree data validation failure', o=o)


_rooted_plane_tree_index = dict()  # cache mechanism assuring that unique rpts are only instantiated once.


def retrieve_rooted_plane_tree_from_cache(o: FlexibleRootedPlaneTree):
    """cache mechanism assuring that unique rpts are only instantiated once."""
    global _rooted_plane_tree_index
    if hash(o) in _rooted_plane_tree_index.keys():
        return _rooted_plane_tree_index[hash(o)]
    else:
        _rooted_plane_tree_index[hash(o)] = o
        return o


def build_rooted_plane_tree_from_tuple_tree(t: tuple | None = None) -> RootedPlaneTree:
    """Builes a rooted-plane-tree from a tree of python tuples.

    :param t:
    :return:
    """
    if t is None:
        return RootedPlaneTree()
    elif len(t) == 0:
        return RootedPlaneTree()
    else:
        children = tuple(build_rooted_plane_tree_from_tuple_tree(u) for u in t)
        return RootedPlaneTree(*children)


class RootedPlaneTree(tuple):
    """A `RootedPlaneTree` is an immutable, finite (and computable) rooted plane tree,
    aka rooted ordered tree.

    Reminder:
    Theorem 3.11 A graph G is a tree if and only if every two vertices of G are connected by a unique path.
    Chartrand, Lesniak, and Zhang, Graphs & Digraphs: Sixth Edition, p. 65.

    """

    def __eq__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`RootedPlaneTre`,
        returns `True` if `t` is connective-equivalent to this :class:`RootedPlaneTre`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: RootedPlaneTree = data_validate_rooted_plane_tree(t)
            return self.is_rooted_plane_tree_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((RootedPlaneTree, *self.immediate_subtrees,))

    def __init__(self, *children: FlexibleRootedPlaneTree, tuple_tree: TupleTree = None):
        """

        If all parameters are passed as None or empty tuples, a single node `RootedPlaneTree` is returned.

        :param children: A tuple of FlexibleRootedPlaneTree instances.
        :param tuple_tree: A `TupleTree` structure.
        """
        super(RootedPlaneTree, self).__init__()
        self._subtrees: tuple[RootedPlaneTree, ...] | None = None

    def __ne__(self, t):
        """Returns `False` if `t` cannot be interpreted as a :class:`RootedPlaneTree`,
        returns `True` if `t` is not rooted-plane-tree-equivalent to this :class:`RootedPlaneTree`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            t: RootedPlaneTree = data_validate_rooted_plane_tree(t)
            return not self.is_rooted_plane_tree_equivalent_to(t)
        except util.PunctiliousException:
            return False

    def __new__(cls, *children: FlexibleRootedPlaneTree, tuple_tree: TupleTree = None):
        if tuple_tree is not None:
            t = build_rooted_plane_tree_from_tuple_tree(tuple_tree)
            t = super(RootedPlaneTree, cls).__new__(cls, t)
            t = retrieve_rooted_plane_tree_from_cache(t)
            return t
        elif children is not None:
            children: tuple[RootedPlaneTree, ...] = tuple(
                data_validate_rooted_plane_tree(child) for child in children)
            t = super(RootedPlaneTree, cls).__new__(cls, children)
            t = retrieve_rooted_plane_tree_from_cache(t)
            return t
        elif children is None and tuple_tree is None:
            t = super(RootedPlaneTree, cls).__new__(cls, tuple())
            t = retrieve_rooted_plane_tree_from_cache(t)
            return t
        else:
            raise util.PunctiliousException('Invalid input parameters', children=children, tuple_tree=tuple_tree)

    def __repr__(self):
        return self.represent_as_anonymous_function()

    def __str__(self):
        return self.represent_as_anonymous_function()

    @property
    def ahu_unsorted_string(self) -> str:
        """Returns the AHU (Aho, Hopcroft, and Ullman) unsorted encoding of this `RootedPlaneTree`.

        It is unsorted because children are not sorted, because this is an ordered tree.
        In consequence, this AHU encoding is not comparable to the AHU encoding of an unordered tree.

        :return:
        """
        if self.is_leaf:
            return "()"
        child_encodings = [child.ahu_unsorted_string for child in self.immediate_subtrees]
        return "(" + "".join(child_encodings) + ")"

    @property
    def ahu_unsorted_inverted_binary_string(self) -> str:
        """Returns the AHU integer of this `RootedPlaneTree`.

        It is unsorted because children are not sorted, because this is an ordered tree.
        In consequence, this AHU encoding is not comparable to the AHU encoding of an unordered tree.

        It is inverted because `(` is mapped to `1` and `)` is mapped to `0`.
        This avoids leading zeroes in the binary representation of the integer,
        thus avoids any conflict in integer values.

        """
        translation: dict = str.maketrans({'(': '1', ')': '0'})
        return self.ahu_unsorted_string.translate(translation)

    @property
    def ahu_unsorted_inverted_integer(self) -> int:
        """Returns the AHU integer of this `RootedPlaneTree`.

        It is unsorted because children are not sorted, because this is an ordered tree.
        In consequence, this AHU encoding is not comparable to the AHU encoding of an unordered tree.

        It is inverted because `(` is mapped to `1` and `)` is mapped to `0`.
        This avoids leading zeroes in the binary representation of the integer,
        thus avoids any conflict in integer values.

        """
        return int(self.ahu_unsorted_inverted_binary_string, base=2)

    @property
    def immediate_subtrees(self) -> tuple[RootedPlaneTree, ...]:
        """The tuple of immediate subtrees.

        :return: the tuple of the immediate subtrees.
        """
        # return tuple(super().__iter__()) # alternative implementation.
        return tuple.__new__(tuple, self)  # this implementation seems more "direct".

    @property
    def degree(self) -> int:
        """The `degree` of a :class:`RootedPlaneTree` is the number of immediate subtrees it has.

        :return:
        """
        return super().__len__()

    def get_subtree_by_path(self, p: tuple[int, ...]) -> RootedPlaneTree:
        """Given a path `p`, returns the corresponding subtree.

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
    def is_leaf(self) -> bool:
        """Returns `True` if the RootedPlaneTree is a leaf, `False` otherwise.

        A `RootedPlaneTree` is a leaf if and only if it contains no children.
        """
        return self.degree == 0

    def is_rooted_plane_tree_equivalent_to(self, t: FlexibleRootedPlaneTree) -> bool:
        """Returns `True` if this :class:`RootedPlaneTree` is connective-equivalent to :class:`RootedPlaneTree` `t`.

        Formal definition 1:
        A rooted-plane-tree `t` is connective-equivalent to a rooted-plane-tree `u` if and only if
         - degree(t) = degree(u).
         - and immediate sub-rooted-plane-tree t_i of t is-rooted-plane-tree-equivalent
           to immediate sub-rooted-plane-tree u_i of u with 0 <= i < degree(t) - 1.

        Formal definition 2:
        A rooted-plane-tree `t` is connective-equivalent to a rooted-plane-tree `u` if and only if
        the unsorted-inverted-integer AHU of `t` = the unsorted-inverted-integer AHU of `u`.

        :param t: A rooted-plane-tree.
        :return:
        """
        t: RootedPlaneTree = data_validate_rooted_plane_tree(t)
        t_i: RootedPlaneTree
        u_i: RootedPlaneTree
        return self.degree == t.degree and all(t_i.is_rooted_plane_tree_equivalent_to(u_i) for t_i, u_i in
                                               zip(t.iterate_immediate_subtrees(), self.iterate_immediate_subtrees()))
        # Equivalent implementation:
        # return t.ahu_unsorted_inverted_integer == self.ahu_unsorted_inverted_integer

    def iterate_immediate_subtrees(self) -> typing.Generator[RootedPlaneTree, None, None]:
        """Generator function that iterates the immediate subtrees of this :class:`RootedPlaneTree`.
        following the canonical vertex ordering.

        :yields: RootedPlaneTree - a subtree.
        :return: None
        """
        yield from super().__iter__()

    def iterate_subtrees(self) -> typing.Generator[RootedPlaneTree, None, None]:
        """Generator function that iterates recursively the subtrees of this :class:`RootedPlaneTree`.
        using the depth-first / canonical vertex ordering algorithm.

        :yields: RootedPlaneTree - a subtree.
        :return: None
        """
        yield self  # Yield the initial rooted-plane-tree itself.
        for child in self.immediate_subtrees:  # Recursively yield subtrees from the immediate subtrees.
            yield from child.iterate_subtrees()

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
        """Returns a multiline string representation of this `RootedPlaneTree`.

        May be useful to get a quick visual understanding of the tree structure.

        Sample:
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
        """Returns the size of this `RootedPlaneTree`.

        Definition: the size of a rooted plan tree is the total number of vertices in the graph."""
        return 1 + sum(child.size for child in self.immediate_subtrees)

    @property
    def substitute_subtree(self, m: dict[FlexibleRootedPlaneTree, FlexibleRootedPlaneTree]) -> RootedPlaneTree:
        raise NotImplementedError('TO BE IMPLEMENTED')

    @property
    def subtrees(self) -> tuple[RootedPlaneTree, ...]:
        """The tuple of subtrees ordered by the depth-first / canonical vertex ordering algorithm.

        :return: the tuple of the subtrees.
        """
        if self._subtrees is None:
            self._subtrees = tuple(self.iterate_subtrees())
        return self._subtrees

    def to_list(self) -> list:
        """Returns a Python `list` of equivalent structure. This is useful to manipulate formulas because
        lists are mutable."""
        return list(self.immediate_subtrees)


FlexibleRootedPlaneTree = typing.Union[
    RootedPlaneTree, tuple[RootedPlaneTree, ...], collections.abc.Iterator, collections.abc.Generator, None]

TupleTree: typing.TypeAlias = typing.Union[int, tuple["TupleTree", ...]]
"""A `TupleTree` is a tree of tuples whose leafs are empty empty tuples.

It allows to express RootedPlaneTree using python tuple syntax, e.g.: ( (), (), ( (), (), ), )

"""
