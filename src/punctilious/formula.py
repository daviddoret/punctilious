from __future__ import annotations
import typing
import collections

# package modules
import util
import connective
import abstract_formula as af
import connective_sequence as cs


def data_validate_formula(
        o: FlexibleFormula) -> Formula:
    if isinstance(o, Formula):
        return o
    if isinstance(o, collections.abc.Iterable):
        return Formula(*o)
    if isinstance(o, collections.abc.Generator):
        return Formula(*o)
    raise util.PunctiliousException('Formula data validation failure', o=o)


_formula_cache = dict()  # cache mechanism assuring that unique  formulas are only instantiated once.


def retrieve_formula_from_cache(o: FlexibleFormula):
    """cache mechanism assuring that unique  formulas are only instantiated once."""
    global _formula_cache
    o: Formula = data_validate_formula(o)
    if hash(o) in _formula_cache.keys():
        return _formula_cache[hash(o)]
    else:
        _formula_cache[hash(o)] = o
        return o


class Formula(tuple):
    """A `Formula` is a pair (S, ϕ) where:
     - S is a sequence of connectives of length n,
     - ϕ is an abstract formula of tree-size n.
    """

    def __init__(self, s: cs.FlexibleConnectiveSequence, phi: af.FlexibleAbstractFormula):
        super(Formula, self).__init__()
        self._connectives = None

    def __new__(cls, s: cs.FlexibleConnectiveSequence, phi: af.FlexibleAbstractFormula):
        s: cs.ConnectiveSequence = cs.data_validate_connective_sequence(s)
        phi: af.AbstractFormula = af.data_validate_abstract_formula(phi)
        if s.length != phi.sequence_max_value:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` is not equal to the `sequence_max_value` of its `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (s, phi,))
        psi = retrieve_formula_from_cache(psi)
        return psi

    @property
    def abstract_formula(self) -> af.AbstractFormula:
        """

        `abstract_formula` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 1)

    @property
    def connective_sequence(self) -> cs.ConnectiveSequence:
        """

        `connective_sequence` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 0)

    @property
    def connectives(self) -> tuple[connective.Connective, ...]:
        """The `connectives` of a `Formula` `phi` is the tuple of `Connective` elements in the formula tree,
        following the depth-first, ascending-nodes algorithm.

        :return:
        """
        if self._connectives is None:
            connectives = list()
            for c in self.iterate_connectives():
                connectives.append(c)
            self._connectives = tuple(connectives)
        return self._connectives

    @property
    def formula_degree(self) -> int:
        """The `formula_degree` of a `Formula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al, 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        return self.abstract_formula.formula_degree

    def iterate_connectives(self) -> collections.abc.Generator[connective.Connective, None, None]:
        """Iterate the `Formula` connectives, following the depth-first, ascending-nodes algorithm.

        :return: None
        """
        i: int
        c: connective.Connective
        for i in self.abstract_formula.restricted_growth_function_sequence:
            yield self.connective_sequence[i - 1]

    @property
    def main_connective(self) -> connective.Connective:
        """The `main_connective` of a :class:`Formula` `phi` is the :class:`Connective` that corresponds
        to the root node of the formula tree.

        The term `main connective` is defined by Mancosu 2021, p. 17 in the context of propositional logic.

        References:
         - Mancosu 2021

        :return: a :class:`Connective`
        """
        return self.connectives[0]

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of a `Formula` is the `sequence_max_value` of its `abstract_formula`."""
        return self.abstract_formula.sequence_max_value

    @property
    def tree_size(self) -> int:
        """The `tree_size` of a `Formula` is the number of vertices in the `RootedPlaneTree` of its `abstract_formula`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.abstract_formula.tree_size


FlexibleFormula = typing.Union[
    Formula, tuple[
        cs.FlexibleConnectiveSequence, af.FlexibleAbstractFormula], collections.abc.Iterator, collections.abc.Generator, None]
