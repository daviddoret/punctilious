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


class FormulaIterationNavigator:
    def __init__(self):
        self.is_start = True
        self.is_move_down = False
        self.is_move_right = False
        self.is_move_up = False
        self.is_end = False
        self.rooted_plane_tree_depth = 1
        self.rooted_plane_tree_children_index = 1
        self.restricted_growth_function_sequence_index = 1

    def __str__(self):
        if self.is_start:
            return "S"
        elif self.is_move_down:
            return "D"
        elif self.is_move_up:
            return "U"
        elif self.is_move_right:
            return "R"
        elif self.is_end:
            return "E"
        else:
            raise util.PunctiliousException('ooops')

    def move_down(self):
        self.is_start = False
        self.is_move_down = True
        self.is_move_right = False
        self.is_move_up = False
        self.is_end = False
        self.rooted_plane_tree_children_index = None
        self.rooted_plane_tree_depth += 1

    def move_right(self, i: int):
        """

        :param i: The rooted_plane_tree_children_index.
        :return:
        """
        self.is_start = False
        self.is_move_down = False
        self.is_move_right = True
        self.is_move_up = False
        self.is_end = False
        self.rooted_plane_tree_children_index = i
        self.restricted_growth_function_sequence_index += 1

    def move_up(self):
        self.is_start = False
        self.is_move_down = False
        self.is_move_right = False
        self.is_move_up = True
        self.is_end = False
        self.rooted_plane_tree_children_index = None
        self.rooted_plane_tree_depth -= 1

    def end(self):
        self.is_start = False
        self.is_move_down = False
        self.is_move_right = False
        self.is_move_up = False
        self.is_end = True
        self.rooted_plane_tree_children_index = None


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
                t=t, s=s)
        phi = super(AbstractFormula, cls).__new__(cls, (t, s))
        phi = retrieve_abstract_formula_from_cache(phi)
        return phi

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

    def iterate_formula_components_depth_first_ascending(self):
        nav = FormulaIterationNavigator()
        yield nav
        if self.rooted_plane_tree.degree > 0:
            nav.move_down()
            yield nav
            for i in range(0, self.rooted_plane_tree.degree):
                nav.move_right(i)
                yield nav
            nav.move_up()
            yield nav
        nav.end()
        yield nav

    def to_default_representation(self) -> str:
        """"""
        output = ""
        for nav in self.iterate_formula_components_depth_first_ascending():
            if nav.is_start:
                output += str(self.restricted_growth_function_sequence[nav.restricted_growth_function_sequence_index])
            elif nav.is_move_down:
                output += "("
            elif nav.is_move_right:
                if nav.rooted_plane_tree_children_index > 1:
                    output += ", "
                output += str(self.restricted_growth_function_sequence[nav.restricted_growth_function_sequence_index])
            elif nav.is_move_up:
                output += ")"
        return output


FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, rgf.FlexibleRestrictedGrowthFunctionSequence], collections.abc.Iterator, collections.abc.Generator, None]
