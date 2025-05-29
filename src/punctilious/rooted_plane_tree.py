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


class RootedPlaneTree(tuple):
    """A `RootedPlaneTree` is an implementation of an (immutable) rooted plane tree, aka rooted ordered tree.

    Reminder:
    Theorem 3.11 A graph G is a tree if and only if every two vertices of G are connected by a unique path.
    Chartrand, Lesniak, and Zhang, Graphs & Digraphs: Sixth Edition, p. 65.


    """

    def __init__(self, *children: FlexibleRootedPlaneTree):
        # children: RootedPlaneTreeTerms = data_validate_formula_structure_terms(children)
        super(RootedPlaneTree, self).__init__()

    def __new__(cls, *children: FlexibleRootedPlaneTree):
        children: tuple[RootedPlaneTree, ...] = tuple(data_validate_rooted_plane_tree(child) for child in children)
        return super(RootedPlaneTree, cls).__new__(cls, children)

    @property
    def ahu_unsorted_string(self) -> str:
        """Returns the AHU unsorted encoding of this `RootedPlaneTree`.

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
    def children(self) -> tuple[RootedPlaneTree]:
        """The tuple of terms (sub-structures) contained in this `RootedPlaneTree`.

        :return:
        """
        return self

    @property
    def degree(self) -> int:
        return len(self.children)

    @property
    def is_leaf(self) -> bool:
        """Returns `True` if the RootedPlaneTree is a leaf, `False` otherwise.

        A `RootedPlaneTree` is a leaf if and only if it contains no children.
        """
        return self.degree == 0

    def is_rooted_plane_tree_equivalent_to(self, x: FlexibleRootedPlaneTree) -> bool:
        x: RootedPlaneTree = data_validate_rooted_plane_tree(x)
        return x.ahu_unsorted_inverted_integer == self.ahu_unsorted_inverted_integer

    @property
    def size(self):
        """Returns the size of this `RootedPlaneTree`.

        Definition: the size of a rooted plan tree is the total number of vertices in the graph."""
        return 1 + sum(child.size for child in self.children)

    def to_list(self) -> list:
        """Returns a Python `list` of equivalent structure. This is useful to manipulate formulas because
        lists are mutable."""
        return list(self.children)


FlexibleRootedPlaneTree = typing.Union[RootedPlaneTree, collections.abc.Iterator, collections.abc.Generator, None]
