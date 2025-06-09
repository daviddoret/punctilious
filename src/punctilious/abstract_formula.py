from __future__ import annotations
import typing
import collections
import enum

# package modules
import util
import rooted_plane_tree as rpt
import restricted_growth_function as rgf
from punctilious.restricted_growth_function import RestrictedGrowthFunctionSequence
from punctilious.rooted_plane_tree import RootedPlaneTree


class AbstractFormulaIterationNavigator:
    def __init__(self, phi: FlexibleAbstractFormula):
        self._abstract_formula = data_validate_abstract_formula(phi)
        self._sequence_path: tuple[int, ...] = (1,)

    def __str__(self):
        return str(self.sequence_path)

    def iterate(self):
        pass

    @property
    def abstract_formula(self) -> AbstractFormula:
        return self._abstract_formula

    @property
    def sequence_path(self) -> tuple[int, ...]:
        return self._sequence_path


def data_validate_abstract_formula(
        o: FlexibleAbstractFormula) -> AbstractFormula:
    if isinstance(o, AbstractFormula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return AbstractFormula(*o)
    if isinstance(o, collections.abc.Generator):
        return AbstractFormula(*o)
    raise util.PunctiliousException('AbstractFormula data validation failure', o=o)


_abstract_formula_cache = dict()  # cache mechanism assuring that unique abstract formulas are only instantiated once.


def retrieve_abstract_formula_from_cache(o: AbstractFormula):
    """cache mechanism assuring that unique abstract formulas are only instantiated once."""
    global _abstract_formula_cache
    if hash(o) in _abstract_formula_cache.keys():
        return _abstract_formula_cache[hash(o)]
    else:
        _abstract_formula_cache[hash(o)] = o
        return o


class AbstractFormula(tuple):
    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: rgf.FlexibleRestrictedGrowthFunctionSequence):
        super(AbstractFormula, self).__init__()
        self._sub_formulas = None

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: rgf.FlexibleRestrictedGrowthFunctionSequence):
        t: rpt.RootedPlaneTree = rpt.data_validate_rooted_plane_tree(t)
        s: rgf.RestrictedGrowthFunctionSequence = rgf.data_validate_restricted_growth_function_sequence(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`AbstractFormula` data validation error. The size of the `RootedPlaneGraph` is not equal to the length of the `RestrictedGrowthFunctionSequence`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        phi = super(AbstractFormula, cls).__new__(cls, (t, s))
        phi = retrieve_abstract_formula_from_cache(phi)
        return phi

    # def __repr__(self):
    #    return self.to_default_representation()

    # def __str__(self):
    #    return self.to_default_representation()

    @property
    def restricted_growth_function_sequence(self) -> rgf.RestrictedGrowthFunctionSequence:
        """Shortcut: self.s.

        :return:
        """
        return self[1]

    @property
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        """Shortcut: self.t."""
        return self[0]

    @property
    def s(self) -> rgf.RestrictedGrowthFunctionSequence:
        """A shortcut for self.restricted_growth_function_sequence."""
        return self.restricted_growth_function_sequence

    @property
    def sub_formulas(self):
        if self._sub_formulas is None:
            sequence_index = 0
            sub_formulas = list()
            for sub_tree in self.rooted_plane_tree.children:
                sub_tree_size = sub_tree.size
                sub_sequence = self.restricted_growth_function_sequence[sequence_index:sequence_index + sub_tree_size]
                sub_formulas.append(AbstractFormula(t=sub_tree, s=sub_sequence))
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    @property
    def t(self) -> rpt.RootedPlaneTree:
        """A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    def iterate_child_sequences(self):
        """Iterates the direct child rgf sequences of this `AbstractFormula`.

        Note: the child rgf sequences are determined by 1) the parent rgf sequence,
        and 2) the rooted plane tree.
        """
        # remove the root
        truncated_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[1:]
        for child_tree in self.rooted_plane_tree.iterate_children():
            # retrieve the elements mapped to this child tree
            child_sequence: tuple[int, ...] = truncated_sequence[0:child_tree.size]
            # transform the sequence into an rgf sequence
            child_sequence: rgf.RestrictedGrowthFunctionSequence = rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
                child_sequence)
            # yield this child rgf sequence
            yield child_sequence
            # truncate the remaining sequence
            truncated_sequence = truncated_sequence[child_tree.size:]

    def iterate_sub_formulas_depth_first_ascending(self):
        yield self
        for child_tree, child_sequence in self.rooted_plane_tree.iterate_children(), self.iterate_child_sequences():
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield from sub_formula.iterate_sub_formulas_depth_first_ascending()

    def iterate_sub_formulas_direct_children(self):
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_children(),
                                              self.iterate_child_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def represent_as_indexed_function(self) -> str:
        """"""
        output = str(self.restricted_growth_function_sequence[0])
        if not self.rooted_plane_tree.is_leaf:
            output += "("
            output += ", ".join(
                sub_formula.represent_as_indexed_function() for sub_formula in
                self.iterate_sub_formulas_direct_children())
            output += ")"
        return output


FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, rgf.FlexibleRestrictedGrowthFunctionSequence], collections.abc.Iterator, collections.abc.Generator, None]
