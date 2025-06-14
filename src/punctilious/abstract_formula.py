from __future__ import annotations
import typing
import collections

# package modules
import util
import rooted_plane_tree as rpt
import restricted_growth_function as rgf


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


def retrieve_abstract_formula_from_cache(o: FlexibleAbstractFormula):
    """cache mechanism assuring that unique abstract formulas are only instantiated once."""
    global _abstract_formula_cache
    o: AbstractFormula = data_validate_abstract_formula(o)
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

    def __repr__(self):
        return self.represent_as_indexed_function()

    def __str__(self):
        return self.represent_as_indexed_function()

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

    def iterate_sequences_direct_ascending(self) -> typing.Generator[rgf.RestrictedGrowthFunctionSequence, None, None]:
        """Iterates the direct child RGF sequences of this `AbstractFormula`.

        Note: the child rgf sequences are determined by 1) the parent rgf sequence,
        and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rpt.RootedPlaneTree
        # truncated_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[1:]
        for child_tree in self.rooted_plane_tree.iterate_direct_ascending():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[i:i + child_tree.size]
            # transform the sequence into an RGF sequence, restarting from initial value 1
            sub_sequence: rgf.RestrictedGrowthFunctionSequence = rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
                sub_sequence)
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_sequences_depth_first_ascending(self) -> \
            collections.abc.Generator[rgf.RestrictedGrowthFunctionSequence, None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_depth_first_ascending()):
            # retrieves the sub-sequence in the root RGF sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.restricted_growth_function_sequence[i:i + sub_tree.size]
            # converts ths sub-sequence to an RGF sequence, which modifies all values to start with 1.
            sub_sequence: rgf.RestrictedGrowthFunctionSequence = rgf.convert_arbitrary_sequence_to_restricted_growth_function_sequence(
                sub_sequence)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_formulas_depth_first_ascending(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the recursive sub-formulas of the `AbstractFormula`,
        including the `AbstractFormula` itself.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: rgf.RestrictedGrowthFunctionSequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_depth_first_ascending(),
                                              self.iterate_sequences_depth_first_ascending()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_sub_formulas_direct(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the direct sub-formulas of the `AbstractFormula`.

        :return:
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_direct_ascending(),
                                              self.iterate_sequences_direct_ascending()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def represent_as_indexed_function(self) -> str:
        """Returns a string representation of the `AbstractFormula` using function notation,
        and the corresponding values of the `RestrictedGrowthFunctionSequence` as function names.
        """
        return self.rooted_plane_tree.represent_as_indexed_function(sequence=self.restricted_growth_function_sequence)


FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, rgf.FlexibleRestrictedGrowthFunctionSequence], collections.abc.Iterator, collections.abc.Generator, None]
