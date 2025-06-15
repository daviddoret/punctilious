from __future__ import annotations
import typing
import collections

# package modules
import util
import connective
import rooted_plane_tree as rpt
import restricted_growth_function as rgf


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
    def formula_degree(self) -> int:
        """The `formula_degree` of an `AbstractFormula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rpt.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_depth_first_ascending():
            if t.degree > 0:
                i += 1
        return i

    @property
    def immediate_sub_formulas(self) -> tuple[AbstractFormula, ...]:
        """The `immediate_sub_formulas` of an `AbstractFormula` `phi` is the tuple of `AbstractFormulas` that are the
        immediate children formulas of `phi` in the formula tree, or equivalently the formulas of degree 0 in `phi`.

        The term `immediate sub-formula` is used by (Mancosu 2021, definition 2.4, p. 18).

        See also:
        - :attr:`AbstractFormula.sub_formulas`

        References:
        - Mancosu 2021.

        :return:
        """
        if self._sub_formulas is None:
            sub_formulas = list()
            for sub_formula in self.iterate_immediate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`AbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`AbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_direct_ascending(),
                                              self.iterate_immediate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_immediate_sub_sequences(self) -> typing.Generator[rgf.RestrictedGrowthFunctionSequence, None, None]:
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

    def iterate_sub_sequences(self) -> \
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

    def iterate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        """Iterates the sub-formulas of the `AbstractFormula` using the `depth-first, ascending nodes` algorithm.

        See :attr:`AbstractFormula.sub_formulas` for a definition of the term `sub-formula`.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: rgf.RestrictedGrowthFunctionSequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_depth_first_ascending(),
                                              self.iterate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    @property
    def main_sequence_element(self) -> int:
        """The `main_sequence_element` of an `AbstractFormula` is the first element of the
        attr:`AbstractFormula.restricted_growth_function_sequence`, that corresponds to the root
        node of the attr:`AbstractFormula.rooted_plane_tree`.

        By the definition of restricted growth function, the `main_sequence_element` is
        always equal to 1.

        The term `main_sequence_element` was designed in reference to the term `main connective`,
        cf. Mancosu 2021, p. 17.

        References:
         - Mancosu 2021

        :return: 1
        """
        return self.restricted_growth_function_sequence[0]

    def represent_as_indexed_function(self) -> str:
        """Returns a string representation of the `AbstractFormula` using function notation,
        and the corresponding values of the `RestrictedGrowthFunctionSequence` as function names.
        """
        return self.rooted_plane_tree.represent_as_indexed_function(sequence=self.restricted_growth_function_sequence)

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
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of an `AbstractFormula` is the `max_value` of its `restricted_growth_function_sequence`."""
        return self.restricted_growth_function_sequence.max_value

    @property
    def sub_formulas(self) -> tuple[AbstractFormula, ...]:
        """The `sub_formulas` of an `AbstractFormula` `phi` is the tuple of `AbstractFormulas` that are present
        in the formula tree of `phi`, including `phi` itself.

        Formal definition:
         - If phi is an atomic formula, the sub-formulas of phi is the tuple (phi).
         - If phi is a non-atomic formula, the sub-formulas of phi is the tuple
           composed of phi, and all sub-formulas of the immediate sub-formulas of phi,
           in ascending order.
        - Nothing else is a sub-formula.

        This definition is a generalization of the term `formula` defined by (Mancosu 2021, definition 2.2, p. 14)
        for propositional-logic.

        See also:
        - :attr:`AbstractFormula.immediate_sub_formulas`

        References:
        - Mancosu 2021.

        :return: A tuple of the sub-formulas.
        """
        if self._sub_formulas is None:
            sub_formulas = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    @property
    def t(self) -> rpt.RootedPlaneTree:
        """A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @property
    def tree_size(self) -> int:
        """The `tree_size` of an `AbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, rgf.FlexibleRestrictedGrowthFunctionSequence], collections.abc.Iterator, collections.abc.Generator, None]
