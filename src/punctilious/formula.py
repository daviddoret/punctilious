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
    """A `Formula` is a pair (ϕ, S) where:
     - ϕ is an abstract formula of tree-size n.
     - S is a sequence of connectives of length n.
    """

    def __init__(self, phi: af.FlexibleAbstractFormula, s: cs.FlexibleConnectiveSequence):
        super(Formula, self).__init__()
        self._connectives = None
        self._immediate_sub_formulas = None
        self._sub_formulas = None

    def __new__(cls, phi: af.FlexibleAbstractFormula, s: cs.FlexibleConnectiveSequence):
        s: cs.ConnectiveSequence = cs.data_validate_connective_sequence(s)
        phi: af.AbstractFormula = af.data_validate_abstract_formula(phi)
        if s.length != phi.sequence_max_value + 1:
            raise util.PunctiliousException(
                f"`Formula` data validation error. The length of the `ConnectiveSequence` is not equal to the `sequence_max_value` of its `abstract_formula`.",
                s_length=s.length, phi_tree_size=phi.tree_size, s=s, phi=phi)
        psi = super(Formula, cls).__new__(cls, (s, phi,))
        psi = retrieve_formula_from_cache(psi)
        return psi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

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

    def get_connective_by_sequence_element(self, i: int) -> connective.Connective:
        return self.connective_sequence[i]

    @property
    def immediate_sub_formulas(self) -> tuple[Formula, ...]:
        """The `immediate_sub_formulas` of a `Formula` `phi` is the tuple of `Formula` elements that are the
        immediate children formulas of `phi` in the formula tree, or equivalently the formulas of degree 0 in `phi`.

        The term `immediate sub-formula` is used by (Mancosu 2021, p. 17-18) in the context of propositional logic.

        See also:
        - :attr:`Formula.sub_formulas`

        References:
        - Mancosu 2021.

        :return:
        """
        if self._sub_formulas is None:
            sub_formulas: list[Formula] = list()
            for sub_formula in self.iterate_immediate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def iterate_connectives(self) -> collections.abc.Generator[connective.Connective, None, None]:
        """Iterate the `Formula` connectives, following the depth-first, ascending-nodes algorithm.

        :return: None
        """
        i: int
        c: connective.Connective
        for i in self.abstract_formula.restricted_growth_function_sequence:
            yield self.get_connective_by_sequence_element(i)

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        """Iterates the immediate sub-formulas of the :class:`Formula`.

        See :attr:`Formula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`Formula`.
        """
        for phi, s in zip(self.abstract_formula.iterate_immediate_sub_formulas(),
                          self.abstract_formula.iterate_immediate_sub_sequences()):
            t: tuple[connective.Connective, ...] = tuple(
                self.get_connective_by_sequence_element(i) for i in s)
            yield Formula(phi, t)

    def iterate_sub_formulas(self) -> collections.abc.Generator[Formula, None, None]:
        raise NotImplementedError()

    @property
    def main_connective(self) -> connective.Connective:
        """The `main_connective` of a :class:`Formula` `phi` is the :class:`Connective` that corresponds
        to the root node of the formula tree.

        By definition of a :class:`Formula` as a pair (phi, S) where S is sequence of connectives,
        the `main_connective` is the first element of S.

        The term `main connective` is defined by Mancosu 2021, p. 17 in the context of propositional logic.

        References:
         - Mancosu 2021

        :return: a :class:`Connective`
        """
        return self.connective_sequence[0]

    def represent_as_function(self) -> str:
        """Returns a string representation of the `Formula` using function notation.
        """
        # TODO: TEST THIS
        return self.abstract_formula.represent_as_function(connectives=self.connective_sequence)

    @property
    def sequence_max_value(self) -> int:
        """The `sequence_max_value` of a `Formula` is the `sequence_max_value` of its `abstract_formula`."""
        return self.abstract_formula.sequence_max_value

    @property
    def sub_formulas(self) -> tuple[Formula, ...]:
        """The `sub_formulas` of an `Formula` `phi` is the tuple of `Formula` elements that are present
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
        - :attr:`Formula.immediate_sub_formulas`

        References:
        - Mancosu 2021.

        :return: A tuple of the sub-formulas.
        """
        if self._sub_formulas is None:
            sub_formulas: list[Formula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    @property
    def tree_size(self) -> int:
        """The `tree_size` of a `Formula` is the number of vertices in the `RootedPlaneTree` of its `abstract_formula`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.abstract_formula.tree_size


FlexibleFormula = typing.Union[
    Formula, tuple[
        cs.FlexibleConnectiveSequence, af.FlexibleAbstractFormula], collections.abc.Iterator, collections.abc.Generator, None]
