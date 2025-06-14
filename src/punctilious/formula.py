from __future__ import annotations
import typing
import collections

# package modules
import util
import rooted_plane_tree as rpt
import restricted_growth_function as rgf
import abstract_formula as af


class Formula(tuple):
    """A `Formula` is a pair (C, ϕ) where:
     - C is a sequence of connectors of size n,
     - ϕ is an abstract formula of size n.
    """

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: rgf.FlexibleRestrictedGrowthFunctionSequence):
        super(Formula, self).__init__()
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
