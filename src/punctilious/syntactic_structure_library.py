r"""

"""
from __future__ import annotations

import typing

import functools

import labeled_rooted_plane_tree_library as lrptl


class SyntacticStructure:
    r"""A syntactic structure.

    Definition
    ------------

    A `syntactic structure` is an LRPT,
    possibly satisfying a set of defined constraints,
    that represents a mathematical object,
    but that is independent of the actual symbols used to represent it.

    """

    def __init__(self, lrpt: lrptl.FlexibleLabeledRootedPlaneTree):
        self._labeled_rooted_plane_tree = lrpt

    @classmethod
    def from_any(
            cls,
            o: FlexibleSyntacticStructure) -> SyntacticStructure:
        if isinstance(o, SyntacticStructure):
            return o
        elif isinstance(o, lrptl.LabeledRootedPlaneTree):
            return SyntacticStructure(o)
        else:
            lrpt: lrptl.LabeledRootedPlaneTree = lrptl.LabeledRootedPlaneTree.from_any(o)
            return SyntacticStructure(lrpt)

    @classmethod
    def is_well_formed(
            cls,
            o: lrptl.FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Check if the given LRPT object `o` is well-formed according to this syntactic structure.

        If `True`, :meth:`SyntacticStructure.from_any` can be safely called on `o`.

        :param o: An LRPT.
        :return:
        """
        o: lrptl.LabeledRootedPlaneTree = lrptl.LabeledRootedPlaneTree.from_any(o)
        return True

    @property
    def labeled_rooted_plane_tree(self) -> lrptl.LabeledRootedPlaneTree:
        return self._labeled_rooted_plane_tree


class AbstractOrderedSet(SyntacticStructure):
    r"""An abstract ordered set.

    Definition
    ------------

    An `abstract ordered set` is a syntactic structure that models a finite (computable) ordered set defined by extension.

    Given LRPT :math:`T` with sub-LRPTs :math:`t_0, t_1, \cdots, t_n`,
    its `abstract ordered set` is the ordered set :math:`(s_0, s_1, \cdots, s_m)`
    where :math:`s_i` denotes the :math:`i`-th *unique* immediate sub-LRPTs of :math:`T`, preserving order.

    Sample
    --------
    Given :math:`T = 0(3, 1, 1, 1, 2)`, the corresponding abstract ordered set is :math:`(3, 1, 2)`.

    Note
    ------

    The main element of the LRPT is not an information of the abstract ordered set, i.e.: it is dropped.

    Note
    -----------

    Every LRPT is an abstract ordered set.

    Note
    ----------

    Every LRPT of degree 0 is the empty ordered set.

    """

    def __init__(self, lrpt: lrptl.FlexibleLabeledRootedPlaneTree):
        super().__init__(lrpt)

    @functools.cached_property
    def cardinality(self) -> int:
        r"""Returns the cardinality of this abstract ordered set.

        Note
        ______

        This is equal to the number of unique immediate sub-LRPTs
        in the LRPT of this syntactic structure.

        This is equivalent to the degree of the LRPT
        if its immediate sub-LRPTs are unique.

        :return: an integer.
        """
        return len(self.elements)

    @functools.cached_property
    def elements(self) -> tuple[lrptl.LabeledRootedPlaneTree, ...]:
        r"""Returns the elements of this abstract ordered set.

        Note
        ______

        This is equivalent to the unique and immediate subtrees of the LRPT, preserving order.

        :return: The elements of the ordered set, in order.
        """
        unique_elements: tuple[lrptl.LabeledRootedPlaneTree, ...] = ()
        for sub_lrpt in self.labeled_rooted_plane_tree.iterate_immediate_subtrees():
            if sub_lrpt not in unique_elements:
                unique_elements = unique_elements + (sub_lrpt,)
        return unique_elements

    def has_element(self, x: lrptl.FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if `x` is an element of this set, `False` otherwise.

        :param x: An object.
        :return: `True` or `False`
        """
        return self._labeled_rooted_plane_tree.has_immediate_subtree(x)

    def is_abstract_ordered_set_equivalent_to(self, x: FlexibleSyntacticStructure) -> bool:
        r"""Check if this syntactic structure is abstract ordered set equivalent to `x`.

        Definition:

        :param x: A syntactic structure.
        :return: `True` or `False`.
        """

        # direct conversion to abstract set is possible because abstract ordered sets have no constraints.
        x: AbstractOrderedSet = AbstractOrderedSet.from_any(x)

        # direct comparison of elements is possible because order is considered.
        return self.elements == x.elements


class AbstractSet(SyntacticStructure):
    r"""An abstract set.

    Definition
    ------------

    An `abstract set` is a syntactic structure that models a finite (computable) set defined by extension.

    Given any LRPT :math:`T`,
    its `abstract set` is the set :math:`{t_0, t_1, \cdots, t_n}`
    where :math:`t_i` denotes the immediate sub-LRPTs of :math:`T`.

    Note
    ------

    The main element of the LRPT is not an information of the abstract set, i.e.: it is dropped.

    The order of immediate sub-LRPTs in the LRPT is not an information of the abstract set, i.e.: it is dropped.

    Note
    -----------

    Every LRPT is an abstract set.

    Note
    ----------

    Every LRPT of degree 0 is the empty set.

    """

    def __init__(self, lrpt: lrptl.FlexibleLabeledRootedPlaneTree):
        super().__init__(lrpt)

    @functools.cached_property
    def cardinality(self) -> int:
        r"""Returns the cardinality of this abstract set.

        Note
        ______

        This is equal to the number of unique immediate sub-LRPTs
        in the LRPT of this syntactic structure.

        This is equivalent to the degree of the LRPT
        if its immediate sub-LRPTs are unique.

        :return: an integer.
        """
        return len(self.elements)

    @functools.cached_property
    def elements(self) -> tuple[lrptl.LabeledRootedPlaneTree, ...]:
        r"""Returns the elements of this abstract set.

        Note
        ______

        This is equivalent to the unique and immediate subtrees of the LRPT.

        Note
        ------

        Even though sets are not ordered, by convention the elements of an abstract set
        are ordered by LRPT canonical order, facilitating equivalence checking.

        :return: The elements of the set.
        """
        unique_elements: tuple[lrptl.LabeledRootedPlaneTree, ...] = ()
        for sub_lrpt in self.labeled_rooted_plane_tree.iterate_immediate_subtrees():
            if sub_lrpt not in unique_elements:
                unique_elements = unique_elements + (sub_lrpt,)
        # by convention, returns the elements in canonical lrpt order
        unique_elements = tuple(sorted(unique_elements))
        return unique_elements

    def has_element(self, x: lrptl.FlexibleLabeledRootedPlaneTree) -> bool:
        r"""Returns `True` if `x` is an element of this set, `False` otherwise.

        :param x: An object.
        :return: `True` or `False`
        """
        return self._labeled_rooted_plane_tree.has_immediate_subtree(x)

    def is_abstract_set_equivalent_to(self, x: FlexibleSyntacticStructure) -> bool:
        r"""Check if this syntactic structure is abstract set equivalent `x`.

        Definition:

        :param x: A syntactic structure.
        :return: `True` or `False`.
        """

        # direct conversion to abstract set is possible because abstract sets have no constraints.
        x: AbstractSet = AbstractSet.from_any(x)

        # direct comparison of elements is possible because they are canonically ordered by convention.
        return self.elements == x.elements


# Flexible types to facilitate data validation

FlexibleSyntacticStructure = typing.Union[
    SyntacticStructure, lrptl.FlexibleLabeledRootedPlaneTree]

# Aliases

AOS = AbstractOrderedSet  # An alias for :class:`AbstractOrderedSet`.
AS = AbstractSet  # An alias for :class:`AbstractSet`.
SR = SyntacticStructure  # An alias for :class:`SyntacticStructure`.
