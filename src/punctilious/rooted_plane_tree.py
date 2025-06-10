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


def convert_tuple_tree_to_rooted_plane_tree(t: TupleTree | None = None) -> RootedPlaneTree:
    """

    :param t:
    :return:
    """
    if t is None:
        return RootedPlaneTree()
    elif len(t) == 0:
        return RootedPlaneTree()
    else:
        children = tuple(convert_tuple_tree_to_rooted_plane_tree(u) for u in t)
        return RootedPlaneTree(*children)


class RootedPlaneTree(tuple):
    """The `RootedPlaneTree` class implements an immutable, finite (and computable) rooted plane tree,
    aka rooted ordered tree.

    Reminder:
    Theorem 3.11 A graph G is a tree if and only if every two vertices of G are connected by a unique path.
    Chartrand, Lesniak, and Zhang, Graphs & Digraphs: Sixth Edition, p. 65.

    """

    def __init__(self, *children: FlexibleRootedPlaneTree, tuple_tree: tuple[tuple] = None):
        """

        :param children: A tuple of FlexibleRootedPlaneTree instances.
        :param tuple_tree: A tuple tree structure.
        """
        # children: RootedPlaneTreeTerms = data_validate_formula_structure_terms(children)
        super(RootedPlaneTree, self).__init__()

    def __new__(cls, *children: FlexibleRootedPlaneTree, tuple_tree: TupleTree = None):
        if tuple_tree is not None:
            t = convert_tuple_tree_to_rooted_plane_tree(tuple_tree)
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
        child_encodings = [child.ahu_unsorted_string for child in self.children]
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
    def children(self) -> tuple[RootedPlaneTree, ...]:
        """The child rooted plane trees that compose this `RootedPlaneTree`.

        :return:
        """
        return tuple(super().__iter__())

    @property
    def degree(self) -> int:
        """The `degree` of a `RootedPlaneTree` is the number of immediate children it has.

        :return:
        """
        return super().__len__()

    @property
    def is_leaf(self) -> bool:
        """Returns `True` if the RootedPlaneTree is a leaf, `False` otherwise.

        A `RootedPlaneTree` is a leaf if and only if it contains no children.
        """
        return self.degree == 0

    def is_rooted_plane_tree_equivalent_to(self, x: FlexibleRootedPlaneTree) -> bool:
        x: RootedPlaneTree = data_validate_rooted_plane_tree(x)
        return x.ahu_unsorted_inverted_integer == self.ahu_unsorted_inverted_integer

    def iterate_children(self) -> typing.Generator[RootedPlaneTree, None, None]:
        """Generator function that iterates the direct children of the `RootedPlaneTree`.

        :return:
        """
        yield from super().__iter__()

    def iterate_depth_first_ascending(self) -> typing.Generator[RootedPlaneTree, None, None]:
        """Generator function that iterates the `RootedPlaneTree` using the depth-first, then ascending children
        algorithm.

        :return:
        """
        yield self
        for child in self.children:
            yield from child.iterate_depth_first_ascending()

    def represent_as_anonymous_function(self) -> str:
        output: str = "★"
        if not self.is_leaf:
            output += "("
        for i, child in enumerate(self.children):
            if i > 0:
                output += ", "
            output += child.represent_as_anonymous_function()
        if not self.is_leaf:
            output += ")"
        return output

    def represent_as_indexed_function(self, sequence: tuple[int]) -> str:
        output: str = str(sequence[0])
        if not self.is_leaf:
            output += "("
        for i, child in enumerate(self.children):
            if i > 0:
                output += ", "
            sub_sequence = sequence[1:]
            output += child.represent_as_indexed_function(sequence=sub_sequence)
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

        child_count: int = len(self.children)
        for i, child in enumerate(self.children):
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
                current_rooted_plane_tree = current_rooted_plane_tree.children[n - 1]
        return current_rooted_plane_tree

    @property
    def size(self):
        """Returns the size of this `RootedPlaneTree`.

        Definition: the size of a rooted plan tree is the total number of vertices in the graph."""
        return 1 + sum(child.size for child in self.children)

    def to_list(self) -> list:
        """Returns a Python `list` of equivalent structure. This is useful to manipulate formulas because
        lists are mutable."""
        return list(self.children)


FlexibleRootedPlaneTree = typing.Union[
    RootedPlaneTree, tuple[RootedPlaneTree], collections.abc.Iterator, collections.abc.Generator, None]

TupleTree: typing.TypeAlias = typing.Union[int, tuple["TupleTree", ...]]
