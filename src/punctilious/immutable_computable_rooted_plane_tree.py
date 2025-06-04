from __future__ import annotations
import typing
import collections
import util
from punctilious.immutable_computable_rooted_plane_tree_full_data_model import RootedPlaneTree


def data_validate_rooted_plane_tree(o: FlexibleRootedPlaneTree) -> RootedPlaneTree:
    if isinstance(o, RootedPlaneTree):
        return o
    if isinstance(o, collections.abc.Iterable):
        return RootedPlaneTree(*o)
    if isinstance(o, collections.abc.Generator):
        return RootedPlaneTree(*o)
    raise util.PunctiliousException('FlexibleRootedPlaneTree data validation failure', o=o)


_rooted_plane_tree_index = dict()  # cache mechanism assuring that unique rpts are only instantiated once.


def retrieve_rooted_plane_tree_from_cache(rpt: FlexibleRootedPlaneTree):
    """cache mechanism assuring that unique rpts are only instantiated once."""
    global _rooted_plane_tree_index
    if hash(rpt) in _rooted_plane_tree_index.keys():
        return _rooted_plane_tree_index[hash(rpt)]
    else:
        _rooted_plane_tree_index[hash(rpt)] = rpt
        return rpt


class RootedPlaneTree(tuple):
    """A `RootedPlaneTree` is an implementation of an immutable and computable rooted plane tree,
    aka rooted ordered tree.

    Reminder:
    Theorem 3.11 A graph G is a tree if and only if every two vertices of G are connected by a unique path.
    Chartrand, Lesniak, and Zhang, Graphs & Digraphs: Sixth Edition, p. 65.

    """

    def __init__(self, *children: FlexibleRootedPlaneTree):
        # children: RootedPlaneTreeTerms = data_validate_formula_structure_terms(children)
        super(RootedPlaneTree, self).__init__()

    def __new__(cls, *children: FlexibleRootedPlaneTree):
        children: tuple[RootedPlaneTree, ...] = tuple(
            data_validate_rooted_plane_tree(child) for child in children)
        rpt = super(RootedPlaneTree, cls).__new__(cls, children)
        # cache mechanism assuring that unique rpts are only instantiated once.
        rpt = retrieve_rooted_plane_tree_from_cache(rpt)
        return rpt

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
        """The child rooted plane trees that compose this `RootedPlaneTree`.

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

    def to_multiline_string_vertical_tree_representation(self, prefix="", is_root=True, is_first=True, is_last=True):
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
        output = ""
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
        # suffix = "" if self.is_leaf else "┓"
        # connector = "┗" if is_last else "┣"
        if is_root:
            output = output
        elif is_first:
            output = output
        else:
            output = "\n" + prefix + output
        # Update the prefix for child levels
        if is_root:
            new_prefix = prefix + " "
        elif is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + " ┃  "

        child_count = len(self.children)
        for i, child in enumerate(self.children):
            is_first_child = (i == 0)
            is_last_child = (i == child_count - 1)
            output = output + child.to_multiline_string_vertical_tree_representation(new_prefix, False, is_first_child,
                                                                                     is_last_child)

        return output


FlexibleRootedPlaneTree = typing.Union[
    RootedPlaneTree, tuple[RootedPlaneTree], collections.abc.Iterator, collections.abc.Generator, None]
