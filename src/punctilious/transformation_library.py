from __future__ import annotations

import punctilious.util as util
import punctilious.rooted_plane_tree_library as rptl
import punctilious.natural_number_0_sequence_library as nn0s
import punctilious.labeled_rooted_plane_tree_library as afl


class AbstractOrderedSet(afl.LabeledRootedPlaneTree):
    r"""An abstract ordered set is a labeled rooted plane tree that has the structure of a finite (computable) ordered-set.

    Definition
    --------------

    A labeled rooted plane tree :math:`\phi` is an abstract-ordered-set if and only if:

    - its immediate sub-formulas are unique.

    N.B.: abstract-classes being structurally composed of a rooted-tree-plane,
      the immediate sub-formulas of a labeled rooted plane tree are necessarily ordered.

    Use case
    ------------

    The abstract-ordered-set is the preimage component of the abstract-map.

    """

    def __init__(self, phi: afl.FlexibleLabeledRootedPlaneTree, n: int, p: afl.FlexibleLabeledRootedPlaneTree,
                 i: afl.FlexibleLabeledRootedPlaneTree, t: rptl.FlexibleRootedPlaneTree,
                 s: nn0s.FlexibleNaturalNumber1Sequence):
        r"""

        :param n: The natural number of the map's root element.
        :param i: The image of the map.
        :param p: The preimage of the map.
        """
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_immediate_subtrees(
            p.rooted_plane_tree, i.rooted_plane_tree)
        s: nn0s.NaturalNumber1Sequence = nn0s.concatenate_natural_number_0_sequences((n,), p.natural_number_sequence,
                                                                                     i.natural_number_sequence)
        super(AbstractFormula, self).__init__(t=t, s=s)

    def __new__(cls, phi: afl.FlexibleLabeledRootedPlaneTree, n: int, p: afl.FlexibleLabeledRootedPlaneTree,
                i: afl.FlexibleLabeledRootedPlaneTree, t: rptl.FlexibleRootedPlaneTree,
                s: nn0s.FlexibleNaturalNumber1Sequence):
        if phi is None:

            # Alternative constructor based on the structural components of an abstract-ordered.set.
            n: int = int(n)
            p: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(p)
            i: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(i)
            if p.arity != i.arity:
                raise util.PunctiliousException(
                    f"`Formula` data validation error. The length of the preimage `p`"
                    f" is not equal to the length of image `i`.",
                    p_length=len(p), i_length=len(i), s=s, phi=phi)
            t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_immediate_subtrees(
                p.rooted_plane_tree, i.rooted_plane_tree)
            s: nn0s.NaturalNumber1Sequence = nn0s.concatenate_natural_number_0_sequences((n,),
                                                                                         p.natural_number_sequence,
                                                                                         i.natural_number_sequence)
            psi = super(AbstractMap, cls).__new__(cls, (t, s,))

        if not isinstance(phi, AbstractFormula):
            raise TypeError("Expected a Bar instance")
        phi.__class__ = cls  # Retype the object to Foo
        return phi

    @classmethod
    def from_labeled_rooted_plane_tree(cls, t: afl.FlexibleLabeledRootedPlaneTree):
        r"""Takes a labeled rooted plane tree structurally compatible with an abstract-ordered-set,
        and returns the same object typed as :class:`AbstractOrderedSet`.

        :param t:
        :return:
        """
        t: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(t)
        unique_values: set[afl.LabeledRootedPlaneTree] = set()
        u: afl.LabeledRootedPlaneTree
        for u in t:
            if u in unique_values:
                return False
            unique_values.add(u)
        return True
        # return cls(d['x'], d['y'])


class AbstractMap(afl.LabeledRootedPlaneTree):
    r"""An :class:`AbstractFormula` that has the structure of a finite (computable) map.

    Definition
    --------------

    A labeled rooted plane tree :math:`\phi` is an abstract-map if and only if:

    - its arity equals 2,
    - the arities of its immediate sub-formulas are equal.

    Properties
    ------------

    - pre-image: noted :math:`f^{-1}(\phi)`, the first immediate sub-formula of :math:`\phi`. Note that the pre-image is not a set, it is a sub-formula.
    - image: noted :math:`\operatorname{Im}(\phi)`, the second immediate sub-formula of :math:`\phi`. Note that the pre-image is not a set, it is a sub-formula.

    Definition
    -----------

    An abstract-map :math:`\phi` is canonical if and only if:

     - its pre-image is canonically ordered.

    Use case
    ------------

    If a labeled rooted plane tree :math:`\phi` is an abstract-map,
    then there is an algorithm that receives a labeled rooted plane tree :math:`\psi` as input,
    that if :math:`\psi` is an element of :math:`f^{-1}(\phi)`
    returns the element of :math:`\operatorname{Im}(\phi)` that is at the same index position.

    """

    def __init__(self, n: int, p: afl.FlexibleLabeledRootedPlaneTree, i: afl.FlexibleLabeledRootedPlaneTree):
        r"""

        :param n: The natural number of the root element of the map.
        :param i: The image of the map.
        :param p: The preimage of the map.
        """
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_immediate_subtrees(
            p.rooted_plane_tree, i.rooted_plane_tree)
        s: nn0s.NaturalNumber1Sequence = nn0s.concatenate_natural_number_0_sequences((n,), p.natural_number_sequence,
                                                                                     i.natural_number_sequence)
        super(AbstractMap, self).__init__(t=t, s=s)

    def __new__(cls, n: int, p: afl.FlexibleLabeledRootedPlaneTree, i: afl.FlexibleLabeledRootedPlaneTree):
        r"""

        :param n: The natural number of the root element of the map.
        :param i: The image of the map.
        :param p: The preimage of the map.
        """
        n: int = int(n)
        p: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(p)
        i: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(i)
        if p.arity != i.arity:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the preimage `p`"
                f" is not equal to the length of image `i`.",
                p_length=len(p), i_length=len(i), s=s, phi=phi)
        t: rptl.RootedPlaneTree = rptl.RootedPlaneTree.from_immediate_subtrees(
            p.rooted_plane_tree, i.rooted_plane_tree)
        s: nn0s.NaturalNumber1Sequence = nn0s.concatenate_natural_number_0_sequences((n,), p.natural_number_sequence,
                                                                                     i.natural_number_sequence)
        psi = super(AbstractMap, cls).__new__(cls, (t, s,))
        return psi

    @property
    def canonical_labeled_rooted_plane_tree(self) -> AbstractMap:
        paired = list(zip(self.pre, Bar))
        paired_sorted = sorted(paired)  # Sort by Foo (alphabetical)
        Foo_sorted, Bar_aligned = zip(*paired_sorted)

    @property
    def pre_image(self) -> afl.LabeledRootedPlaneTree:
        return self[0]

    @property
    def image(self) -> afl.LabeledRootedPlaneTree:
        return self[1]


class AbstractTransformation(afl.LabeledRootedPlaneTree):
    r"""An abstract transformation.

    A labeled rooted plane tree 0(phi, psi)
    where phi is denoted as the input, and psi is denoted as the output.

    A tuple (input, output).

    """

    def __init__(self, i: afl.FlexibleLabeledRootedPlaneTree, o: afl.FlexibleLabeledRootedPlaneTree):
        super(AbstractTransformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleLabeledRootedPlaneTree, o: afl.FlexibleLabeledRootedPlaneTree):
        i: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(i)
        o: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(o)
        phi: afl.LabeledRootedPlaneTree = phi.canonical_labeled_rooted_plane_tree  # Canonize the labeled rooted plane tree
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" labeled tree.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi


class AbstractTransformationBySubstitution(AbstractTransformation):
    r"""

    A tuple (input, output) where the input is composed of a tuple: (input, variables, substitution_values) to which correspond a unique output

    input: the formula that must be transformed

    variables: the unique placeholders of the formulas to be replaced, of length n, by convention, we will use atomic (leaf) formulas, in ascending order

    substitution: the unique substitution_values for the variables, of length n

    output: the transformed

    """

    def __init__(self, i: afl.FlexibleLabeledRootedPlaneTree, o: afl.FlexibleLabeledRootedPlaneTree):
        super(AbstractTransformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleLabeledRootedPlaneTree, v: afl.FlexibleLabeledRootedPlaneTree,
                s: afl.FlexibleLabeledRootedPlaneTree,
                o: afl.FlexibleLabeledRootedPlaneTree):
        i: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(i)
        o: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(o)
        phi: afl.LabeledRootedPlaneTree = phi.canonical_labeled_rooted_plane_tree  # Canonize the labeled rooted plane tree
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" labeled tree.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi


class TransformationBySubstitution:
    def __init__(self, i: afl.FlexibleLabeledRootedPlaneTree, v: afl.FlexibleLabeledRootedPlaneTree,
                 s: afl.FlexibleLabeledRootedPlaneTree,
                 o: afl.FlexibleLabeledRootedPlaneTree):
        super(Transformation, self).__init__(t=None, s=None)

    def __new__(cls, i: afl.FlexibleLabeledRootedPlaneTree, v: afl.FlexibleLabeledRootedPlaneTree,
                s: afl.FlexibleLabeledRootedPlaneTree,
                o: afl.FlexibleLabeledRootedPlaneTree):
        i: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(i)
        o: afl.LabeledRootedPlaneTree = afl.LabeledRootedPlaneTree.from_any(o)
        phi: afl.LabeledRootedPlaneTree = phi.canonical_labeled_rooted_plane_tree  # Canonize the labeled rooted plane tree
        if s.length != phi.natural_number_sequence.image_cardinality:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` `s`"
                f" is not equal to the `image_cardinality` of the `natural_number_sequence` of its"
                f" labeled tree.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (phi, s,))
        psi = retrieve_formula_from_cache(psi)
        return psi
