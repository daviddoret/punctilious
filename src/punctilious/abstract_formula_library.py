from __future__ import annotations
import typing
import collections
# import itertools

# package modules
import punctilious.util as util
import punctilious.rooted_plane_tree_library as rpt
import punctilious.natural_number_0_sequence_library as nn0sl
import punctilious.binary_relation_library as brl
import punctilious.natural_number_0_pair_library as nn0pl
import punctilious.ternary_boolean_library as tbl


class IsEqualTo(brl.BinaryRelation):
    r"""The abstract formulas equipped with the standard equality order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{F}, = )`.

    """

    # mathematical properties
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = False
    _is_irreflexive: bool | None = False
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = False
    _is_reflexive: bool | None = True
    _is_strongly_connected: bool | None = False
    _is_symmetric: bool | None = True
    _is_transitive: bool | None = True

    @util.readonly_class_property
    def is_antisymmetric(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object.
        :param y: A Python object.
        :return: `True` or `False`.
        """
        x: AbstractFormula = AbstractFormula.from_any(x)
        y: AbstractFormula = AbstractFormula.from_any(y)
        return x.is_canonical_abstract_formula_equivalent_to(y)


class IsStrictlyLessThan(brl.BinaryRelation):
    r"""The abstract formulas equipped with the standard strictly less-than order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{F}_0, < )`.

    """

    @classmethod
    def rank(cls, x: object) -> int:
        r"""Returns the rank of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A Python object interpretable as a (0-based) natural number.
        :return: An integer.
        """
        x: AbstractFormula = AbstractFormula.from_any(x)
        n1: int = x.rooted_plane_tree.rank()
        n2: int = x.natural_number_sequence.rank()
        p: nn0pl.NaturalNumber0Pair = nn0pl.NaturalNumber0Pair(n1, n2)
        n3: int = p.rank()
        return n3

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object interpretable as a (0-based) natural number.
        :param y: A Python object interpretable as a (0-based) natural number.
        :return: `True` or `False`.
        """
        x: AbstractFormula = AbstractFormula.from_any(x)
        y: AbstractFormula = AbstractFormula.from_any(y)
        n1: int = x.rank()
        n2: int = x.rank()
        return n1 < n2

    @classmethod
    def successor(cls, x: object) -> object:
        r"""Returns the successor of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A Python object interpretable as a (0-based) natural number.
        :return: The successor of `x`.
        """
        x: AbstractFormula = AbstractFormula.from_any(x)
        n: int = cls.rank(x)
        n += 1
        y: AbstractFormula = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> AbstractFormula:
        r"""Returns the (0-based) natural number of `x` such that its rank in :math:`( \mathbb{N}_0, < ) = n`.

        :param n: A positive integer.
        :return: A (0-based) natural number.
        """
        n = int(n)
        if n < 0:
            raise util.PunctiliousException("`n` must be a positive integer.", n=n)
        p = nn0pl.cantor_pairing_order.unrank(n)
        n1 = p.x
        n2 = p.y
        t = rpt.RootedPlaneTree.from_rank(n1)
        s = nn0sl.NaturalNumber0Sequence.from_rank(n2)
        f = AbstractFormula(t=t, s=s)
        return f


# Classes

class AbstractFormula(brl.RelationalElement, tuple):
    r"""A :class:`AbstractFormula` is a tuple `(T, S)` such that:
     - `T` is a rooted-plane-tree,
     - `S` is a sequence of (0-based) natural numbers.

    """

    def __eq__(self, phi) -> bool:
        r"""Returns `True` if this abstract-formula is equal to abstract-formula `phi`, `False` otherwise.

        See :attr:`AbstractFormula.is_equal_to` for a definition of abstract-formula equality.

        :param phi: An abstract-formula.
        :return: `True` if this abstract-formula is equal to abstract-formula `phi`, `False` otherwise.
        """
        return self.is_equal_to(phi)

    def __hash__(self):
        return self._compute_hash(self)

    def __init__(self, t: rpt.FlexibleRootedPlaneTree, s: nn0sl.FlexibleNaturalNumber0Sequence):
        super(AbstractFormula, self).__init__()
        self._canonical_abstract_formula: AbstractFormula | None = None
        self._immediate_subformulas_are_unique: AbstractFormula | None = None
        self._immediate_sub_formulas: tuple[AbstractFormula, ...] | None = None
        self._is_abstract_map: bool | None = None
        self._is_abstract_inference_rule: bool | None = None
        self._sub_formulas: tuple[AbstractFormula, ...] | None = None

    def __new__(cls, t: rpt.FlexibleRootedPlaneTree, s: nn0sl.FlexibleNaturalNumber0Sequence):
        t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_any(t)
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence.from_any(s)
        if t.size != s.length:
            raise util.PunctiliousException(
                f"`AbstractFormula` data validation error. The size of the `RootedPlaneGraph` is not equal to the length of the `UnrestrictedSequence`.",
                t_size=t.size, s_length=s.length, t=t, s=s)
        phi = super(AbstractFormula, cls).__new__(cls, (t, s))
        phi = cls._from_cache(phi)
        return phi

    def __repr__(self):
        return self.represent_as_function()

    def __str__(self):
        return self.represent_as_function()

    _cache: dict[int, AbstractFormula] = dict()  # Cache mechanism.

    _HASH_SEED: int = 11651462149556646224  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @property
    def abstract_inference_rule_conclusion(self) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-inference-rule, returns its conclusion.

        See :attr:`AbstractFormula.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the conclusion of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_sub_formulas[2]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-inference-rule.")

    @property
    def abstract_inference_rule_premises(self) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-inference-rule, returns its premises.

        See :attr:`AbstractFormula.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the premises of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_sub_formulas[1]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-inference-rule.")

    @property
    def abstract_inference_rule_variables(self) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-inference-rule, returns its variables.

        See :attr:`AbstractFormula.is_abstract_inference_rule` for a detailed description of abstract-inference-rules.

        :return: the variables of this inference-rule.
        """
        if self.is_abstract_inference_rule:
            return self.immediate_sub_formulas[0]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-inference-rule.")

    @property
    def abstract_map_preimage_sequence(self) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-map, returns its preimage sequence.

        See :attr:`AbstractFormula.is_abstract_map` for a detailed description of abstract-maps.

        :return: the preimage sequence of this map.
        """
        if self.is_abstract_map:
            return self.immediate_sub_formulas[0]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-map.")

    @property
    def abstract_map_image_sequence(self) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-map, returns its image sequence.

        See :attr:`AbstractFormula.is_abstract_map` for a detailed description of abstract-maps.

        :return: the image sequence of this map.
        """
        if self.is_abstract_map:
            return self.immediate_sub_formulas[1]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-map.")

    def derive_abstract_inference_rule(self, p: FlexibleAbstractFormula) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-inference-rule, derives a theorem
        from the finite (computable) sequence of premises `p`.

        See :attr:`AbstractFormula.is_abstract_inference_rule` for a detailed description of abstract-inference-rule.

        :param p: a finite (computable) sequence of premises, in the order expected by the inference-rule.
        :return: the theorem derived from this abstract-inference-rule, given premises `p`.
        """
        p: AbstractFormula = AbstractFormula.from_any(p)
        if self.is_abstract_inference_rule:
            if p.arity != self.abstract_inference_rule_premises.arity:
                raise util.PunctiliousException("The number of input premises is not equal to the number"
                                                " of premises expected by the inference-rule.",
                                                input_premises=p,
                                                expected_premises=self.abstract_inference_rule_premises,
                                                inference_rule=self)
            v: dict[AbstractFormula, AbstractFormula | None]  # A mapping for variable values

            i: AbstractFormula  # An input premise
            e: AbstractFormula  # An expected premise
            for i, e in zip(p.iterate_immediate_sub_formulas(), self.abstract_inference_rule_premises):
                ok, v = _compute_abstract_inference_rule_variables(v, i, e)
                if not ok:
                    pass
                else:
                    pass






        # TODO: IMPLEMENT INFERENCE-RULE LOGIC
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-inference-rule.")

    def get_abstract_map_value(self, phi: FlexibleAbstractFormula) -> AbstractFormula:
        r"""If this abstract-formula is an abstract-map, returns the image `phi` under this map.

        See :attr:`AbstractFormula.is_abstract_map` for a detailed description of abstract-maps.

        :param phi: a preimage element.
        :return: the image of `phi` under this map.
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        if self.is_abstract_map:
            i: int = self.abstract_map_preimage_sequence.get_immediate_subformula_index(phi)
            return self.abstract_map_image_sequence.immediate_sub_formulas[i]
        else:
            raise util.PunctiliousException("This abstract-formula is not an abstract-map.")

    @property
    def is_abstract_map(self) -> bool:
        r"""Returns `True` if this abstract-formula is an abstract-map, `False` otherwise.

        Intuitive definition: abstract-map
        ______________________________________

        Intuitively, an abstract-map is an abstract-formula that is structurally
         equivalent to a finite map.

        Formal definition: abstract-map
        _________________________________

        A finite (computable) abstract-map :math:`M` is a tuple :math:`(P, I)` where:

        - :math:`P` is a finite sequence of unique elements denoted as the preimage,
        - :math:`I` is a finite sequence of unique elements denoted as the image,
        - :math:`|P| = |I|`.

        Formal definition: abstract-map
        ___________________________________

        An abstract-formula is an abstract-map if and only if:

        - its arity equals 2,
        - the arity of its first immediate subformula equals the arity of its second immediate subformula,
        - the immediate subformulas of its first immediate subformula are unique.

        Note
        _____

        The following properties and methods are available when an abstract-formula is an abstract-map:

        - :attr:`AbstractFormula.abstract_map_preimage`
        - :attr:`AbstractFormula.abstract_map_image`
        - :meth:`AbstractFormula.get_abstract_map_value`

        :return: `True` if this abstract-formula is an abstract-map, `False` otherwise.

        """
        if self._is_abstract_map is None:
            self._is_abstract_map = \
                self.arity == 2 and \
                self.immediate_sub_formulas[0].arity == self.immediate_sub_formulas[1].arity and \
                self.immediate_sub_formulas[0].immediate_subformulas_are_unique
        return self._is_abstract_map

    @property
    def is_abstract_inference_rule(self) -> bool:
        r"""Returns `True` if this abstract-formula is an abstract-inference-rule, `False` otherwise.

        Intuitive definition: abstract-inference-rule
        ___________________________________________________

        Intuitively, an abstract-inference-rule is an abstract-formula that is structurally
         equivalent to an inference rule.

        Formal definition: abstract-inference-rule
        ______________________________________________

        An abstract-inference-rule :math:`I` is a tuple :math:`(V, P, C)` where:

        - :math:`V` is a finite sequence of unique elements denoted as the variables,
        - :math:`P` is a finite sequence of unique elements denoted as the premises,
        - :math:`C` is denoted as the conclusion.

        Formal definition: abstract-inference-rule
        _______________________________________________

        An abstract-formula is an abstract-inference-rule if and only if:

         - its arity equals 3.

        Note
        _____

        The following complementary properties and methods are available when an abstract-formula is an abstract-map:

        - :attr:`abstract_inference_rule_variables`
        - :attr:`abstract_inference_rule_premises`
        - :attr:`abstract_inference_rule_conclusion`
        - :meth:`derive_abstract_inference_rule`

        :return: `True` if this abstract-formula is an abstract-inference-rule, `False` otherwise.

        """
        if self._is_abstract_inference_rule is None:
            self._is_abstract_inference_rule = \
                self.arity == 3
        return self._is_abstract_inference_rule

    @classmethod
    def _compute_hash(cls, o: AbstractFormula) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with an abstract-formula.
        :return: The hash of the abstract-formula that is structurally equivalent to `o`.
        """
        return hash((AbstractFormula, cls._HASH_SEED, o.rooted_plane_tree, o.natural_number_sequence,))

    @classmethod
    def _from_cache(cls, o: FlexibleAbstractFormula):
        r"""Cache mechanism used in the constructor."""
        hash_value: int = AbstractFormula._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    @classmethod
    def abstract_map_from_preimage_and_image(
            cls,
            n: int,
            p: FlexibleAbstractFormula,
            i: FlexibleAbstractFormula) -> AbstractFormula:
        r"""Declares a new abstract-map.

        :param n: The main-element of the abstract-map.
        :param p: The preimage of the abstract-map.
        :param i: The image of the abstract-map.
        :return: The resulting abstract-map.
        """
        return AbstractFormula.from_immediate_sub_formulas(n=n, s=(p, i,))

    @property
    def arity(self) -> int:
        r"""The :attr:`AbstractFormula.arity` is the number of immediate sub-formulas it contains.

        :return:
        """
        return len(self.immediate_sub_formulas)

    @property
    def canonical_abstract_formula(self) -> AbstractFormula:
        r"""The canonical-abstract-formula of this abstract-formula.

        Definition: the canonical-abstract-formula `phi` of an abstract-formula `psi`
        is a formula such that:

        - their rooted-plane-tree are rooted-plane-tree-equivalent,
        - the natural-number-sequence of `phi` is the canonical-naturel-number-sequence
           of the natural-number-sequence of `psi`

        :return: The canonical-abstract-formula of this abstract-formula.
        """
        if self.is_canonical:
            return self
        elif self._canonical_abstract_formula is not None:
            return self._canonical_abstract_formula
        else:
            self._canonical_abstract_formula: AbstractFormula = AbstractFormula(
                t=self.rooted_plane_tree,
                s=self.natural_number_sequence.to_restricted_growth_function_sequence)
            return self._canonical_abstract_formula

    @property
    def formula_degree(self) -> int:
        r"""The `formula_degree` of an :class:`AbstractFormula` is the number of non-leaf nodes it contains.

        This definition is derived from (Mancosu et al., 2021, p. 18).

        Attention point: do not confuse `tree_size` and `formula_degree`.

        :return:
        """
        i: int = 0
        t: rpt.RootedPlaneTree
        for t in self.rooted_plane_tree.iterate_subtrees():
            if t.degree > 0:
                i += 1
        return i

    @classmethod
    def from_any(
            cls,
            o: FlexibleAbstractFormula) -> AbstractFormula:
        if isinstance(o, AbstractFormula):
            return o
        if isinstance(o, collections.abc.Iterable):
            return AbstractFormula(*o)
        if isinstance(o, collections.abc.Generator):
            return AbstractFormula(*o)
        raise util.PunctiliousException("`AbstractFormula` data validation failure. `o` is of unknown type.",
                                        type_of_o=type(o), o=o)

    @classmethod
    def from_immediate_sub_formulas(
            cls,
            n: int | None,
            s: tuple[FlexibleAbstractFormula, ...] | None) -> AbstractFormula:
        r"""Given a root natural number n,
        and a tuple of abstract-formulas s,
        declares a new formula 𝜓 := n(s_0, s_1, ..., s_n) where s_i is an element of s.

        :param n:
        :param s:
        :return:
        """
        if n is None:
            n: int = 0
        if s is None:
            s: tuple[AbstractFormula, ...] = ()
        s: tuple[AbstractFormula, ...] = tuple(
            AbstractFormula.from_any(o=phi) for phi in s)
        # Retrieves the children trees
        t: tuple[rpt.RootedPlaneTree, ...] = tuple(phi.rooted_plane_tree for phi in s)
        # Declare the new parent tree
        t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_immediate_subtrees(*t)
        # Declare the natural-number-sequence by appending n to the concatenation of the
        # children natural-number-sequences.
        u: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(n) + nn0sl.concatenate_natural_number_sequences(
            *(phi.natural_number_sequence for phi in s))
        phi: AbstractFormula = AbstractFormula(t=t, s=u)
        return phi

    @classmethod
    def from_tree_of_integer_tuple_pairs(cls, p) -> AbstractFormula:
        r"""Declares an abstract-formula object from a tree of integer/tuple pairs.

        Use case
        ___________

        Tree of integer/tuple pairs is a natural pythonic data structure to express abstract formulas.

        Definition
        ------------

        A tree of integer/tuple pairs `T` defined as:

        .. math::

            T := (n, T\prime)

        where:

        - :math:`n` is a natural number
        - :math:`\prime` is (possibly empty) tuple of trees of integer/tuple pairs.

        Sample
        --------

        The tree of integer/tuple pairs:
        (0, ((1,(),),(0,((2,(),),(1,(),),),),(2,(),),),)

        ...maps to the abstract-formula:
        0(1,0(2,1),2)

        :param p: A tree of integer/tuple pairs.
        :return: an abstract-formula.

        """

        t, s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=p)
        t: rpt.RootedPlaneTree = rpt.RootedPlaneTree.from_tuple_tree(t)
        s: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*s)
        phi: AbstractFormula = AbstractFormula(t, s)
        return phi

    def get_immediate_subformula_index(self, phi: FlexibleAbstractFormula):
        r"""Returns the 0-based index position of `phi` in this abstract-formula immediate subformulas.

        Prerequisites:

        - the immediate subformulas of this abstract-formula are unique, cf. :attr:`AbstractFormula.immediate_subformulas_are_unique`,
        - `phi` is an immediate subformula of this abstract-formula.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        if not self.immediate_subformulas_are_unique:
            raise util.PunctiliousException('The immediate subformulas of this abstract-formula are not unique.',
                                            this_formula=self, phi=phi)
        if not phi in self.immediate_sub_formulas:
            raise util.PunctiliousException('`phi` is not an immediate subformulas of this abstract-formula.',
                                            this_formula=self, phi=phi)

        return self.immediate_sub_formulas.index(phi)

    def get_sub_formula_by_path(self, p: tuple[int, ...]) -> AbstractFormula:
        r"""Given a path `p`, returns the corresponding sub-formula.

        Definition - sub-formula path:
        A sub-formula path is a finite sequence of natural numbers >= 0, of length > 0,
        that gives the index position of the sub-formulas, following the depth-first algorithm,
        starting with 0 meaning the original tree.

        It follows that for any formula `phi`, the path (0) returns the formula itself.

        :param p:
        :return:
        """
        p: tuple[int, ...] = tuple(int(n) for n in p)
        if p[0] != 0:
            raise util.PunctiliousException("The first element of the path is not equal to 0.", p0=p[0], p=p,
                                            phi=self)
        if p == (0,):
            return self
        else:
            phi: AbstractFormula = self
            for i in range(1, len(p)):
                j = p[i]
                if 0 < j >= phi.tree_degree:
                    raise util.PunctiliousException(
                        "The n-th element of the path is negative or greater than the number of"
                        " immediate sub-formulas in phi.", n_index=i, n_value=j,
                        phi=phi)
                phi: AbstractFormula = phi.immediate_sub_formulas[j]
            return phi

    @property
    def immediate_sub_formulas(self) -> tuple[AbstractFormula, ...]:
        r"""The `immediate_sub_formulas` of an :class:`AbstractFormula` `phi` is the tuple of :class:`AbstractFormula` elements
        that are the immediate children formulas of `phi` in the formula tree, or equivalently the formulas
        of degree 0 in `phi`.

        The term `immediate sub-formula` is used by (Mancosu 2021, p. 17-18).

        See also:

        - :attr:`AbstractFormula.sub_formulas`

        References:

        - Mancosu 2021.

        :return:
        """
        if self._immediate_sub_formulas is None:
            sub_formulas = list()
            for phi in self.iterate_immediate_sub_formulas():
                sub_formulas.append(phi)
            self._immediate_sub_formulas = tuple(sub_formulas)
        return self._immediate_sub_formulas

    @property
    def immediate_subformulas_are_unique(self) -> bool:
        r"""Returns `True` if all immediate subformulas contained in this :class:`AbstractFormula`
        are unique.

        Trivial case:
        If the :class:`AbstractFormula` is a leaf, i.e. it contains no immediate subformulas,
        then all of its immediate subformulas are unique.

        :return:
        """
        if self._immediate_subformulas_are_unique is None:
            unique_values: set[AbstractFormula] = set()
            psi: AbstractFormula
            for psi in self.iterate_immediate_sub_formulas():
                if psi in unique_values:
                    self._immediate_subformulas_are_unique = False
                unique_values.add(psi)
            self._immediate_subformulas_are_unique = True
        return self._immediate_subformulas_are_unique

    def is_abstract_formula_equivalent_to(self, phi: AbstractFormula):
        r"""Returns `True` if this :class:`AbstractFormula` is abstract-formula-equivalent
        to :class:`AbstractFormula` `phi`.

        Formal definition:
        Two abstract-formulas phi and psi are abstract-formula-equivalent if and only if:

        - the rooted-plane-tree of phi is rooted-plane-tree-equivalent to the rooted-plane-tree of psi,
        - the natural-numbers-sequence of phi is natural-numbers-sequence-equivalent to the natural-numbers-sequence of psi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        return self.rooted_plane_tree.is_rooted_plane_tree_equivalent_to(
            phi.rooted_plane_tree) and self.natural_number_sequence.is_natural_number_0_sequence_equivalent_to(
            phi.natural_number_sequence)

    def is_abstract_formula_equivalent_to_with_variables(self, phi: AbstractFormula,
                                                         v: AbstractFormula) -> bool:
        r"""Returns `True` if this abstract-formula is abstract-formula-equivalent to abstract-formula `phi`,
        after substitution of variables with assigned values in this abstract-formula,
        according to variables and assigned values in abstract-map `v`.

        :param phi: An abstract-formula.
        :param v: An abstract-map whose preimage is denoted as the variables, and image as the assigned values.
        :return: `True` if formulas are equivalent given above conditions, `False` otherwise.
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        v: AbstractFormula = AbstractFormula.from_any(v)
        if not v.is_abstract_map:
            raise util.PunctiliousException("`v` is not an abstract-map", v=v, phi=phi, this_abstract_formula=self)
        psi: AbstractFormula = self.substitute_sub_formulas_with_map(m=v)
        return psi.is_abstract_formula_equivalent_to(phi)

    @property
    def is_canonical(self) -> bool:
        r"""Returns `True` if this abstract-formula is in canonical form.

        Definition:
        An abstract-formula `phi` is `canonical` if and only if
        its natural-number-sequence is a restricted-growth-function-sequence.

        :return: `True` if this abstract-formula is in canonical form, `False` otherwise.
        """
        return self.natural_number_sequence.is_restricted_growth_function_sequence

    def is_canonical_abstract_formula_equivalent_to(self, phi: AbstractFormula):
        r"""Returns `True` if this :class:`AbstractFormula` is canonical-abstract-formula-equivalent
        to :class:`AbstractFormula` `phi`.

        Formal definition:
        Two abstract-formulas phi and psi are canonical-abstract-formula-equivalent if and only if:

        - the canonical-abstract-formula of phi is abstract-formula-equivalent
          to the canonical-abstract-formula of psi.

        Intuitive definition:
        Two formulas are canonical-abstract-formula-equivalent if they have the same "structure".

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        return self.canonical_abstract_formula.is_abstract_formula_equivalent_to(
            phi.canonical_abstract_formula)

    def is_equal_to(self, phi: FlexibleAbstractFormula):
        r"""Under :class:`AbstractFormula` canonical ordering,
        returns `True` if the current :class:`AbstractFormula` is equal to `phi`,
        `False` otherwise.

        See :attr:`AbstractFormula.is_less_than` for a definition of abstract-formula canonical-ordering.

        :param phi: A :class:`AbstractFormula`.
        :return: `True` if the current :class:`AbstractFormula` is equal to `s`, `False` otherwise.
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        return self.is_abstract_formula_equivalent_to(phi)

    def is_less_than(self, phi: FlexibleAbstractFormula) -> bool:
        r"""Under :class:`AbstractFormula` canonical ordering,
        returns `True` if the current :class:`AbstractFormula` is less than `phi`,
        `False` otherwise.

        Definition: canonical ordering of abstract-formula, denoted :math:`\prec`,
        is defined as rooted-plane-tree-first, natural-number-sequence second.

        :param phi: A :class:`AbstractFormula`.
        :return: `True` if the current :class:`AbstractFormula` is equal to `phi`, `False` otherwise.
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        if self.is_abstract_formula_equivalent_to(phi):
            return False
        elif self.rooted_plane_tree.is_less_than_under_o1(phi.rooted_plane_tree):
            return True
        elif phi.rooted_plane_tree.is_less_than_under_o1(self.rooted_plane_tree):
            return False
        elif self.natural_number_sequence.is_strictly_less_than(phi.natural_number_sequence):
            return True
        elif phi.natural_number_sequence.is_strictly_less_than(self.natural_number_sequence):
            return False
        raise util.PunctiliousException("Unreachable condition")

    def is_immediate_sub_formula_of(self, phi: AbstractFormula):
        r"""Returns `True` if this :class:`AbstractFormula` is an immediate sub-formula of :class:`AbstractFormula` phi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        psi: AbstractFormula
        for psi in phi.iterate_immediate_sub_formulas():
            if self.is_abstract_formula_equivalent_to(psi):
                return True
        return False

    def is_immediate_super_formula_of(self, phi: AbstractFormula):
        r"""Returns `True` if :class:`AbstractFormula` phi is an immediate super-formula of this :class:`AbstractFormula`.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        return phi.is_immediate_sub_formula_of(self)

    @property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this abstract-formula is increasing, `False` otherwise.

        Definition - increasing abstract-formula:
        An abstract-formula is increasing
        or increasing under canonical order,
        if its immediate subformulas are ordered.

        Definition - increasing abstract-formula:
        An abstract-formula :math:`\phi = c(\psi_0, \psi1, \cdots, \psi_l)` is increasing,
        or increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} \ge \psi_i`.

        :return: `True` if this abstract-formula is increasing, `False` otherwise.
        """
        return all(
            self.immediate_sub_formulas[i + 1] >= self.immediate_sub_formulas[i] for i in range(0, self.arity - 1))

    @property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this abstract-formula is strictly increasing, `False` otherwise.

        Definition - strictly increasing abstract-formula:
        An abstract-formula is strictly increasing
        or strictly increasing under canonical order,
        if its immediate subformulas are strictly ordered.

        Definition - strictly increasing abstract-formula:
        An abstract-formula :math:`\phi = c(\psi_0, \psi1, \cdots, \psi_l)` is strictly increasing,
        or strictly increasing under canonical order,
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, \psi_{i + 1} > \psi_i`.

        :return: `True` if this abstract-formula is strictly increasing, `False` otherwise.
        """
        return all(
            self.immediate_sub_formulas[i + 1] > self.immediate_sub_formulas[i] for i in range(0, self.arity - 1))

    def is_sub_formula_of(self, phi: AbstractFormula):
        r"""Returns `True` if this :class:`AbstractFormula` is a sub-formula of :class:`AbstractFormula` phi.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        psi: AbstractFormula
        for psi in phi.iterate_sub_formulas():
            if self.is_abstract_formula_equivalent_to(psi):
                return True
        return False

    def is_super_formula_of(self, phi: AbstractFormula):
        r"""Returns `True` if :class:`AbstractFormula` phi is a sub-formula of this :class:`AbstractFormula`.

        :param phi:
        :return:
        """
        phi: AbstractFormula = AbstractFormula.from_any(phi)
        return phi.is_sub_formula_of(self)

    def iterate_immediate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        r"""Iterates the immediate sub-formulas of the :class:`AbstractFormula`.

        See :attr:`AbstractFormula.immediate_sub_formulas` for a definition of the term `immediate sub-formula`.

        :return: A generator of :class:`AbstractFormula`.
        """
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_immediate_subtrees(),
                                              self.iterate_immediate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    def iterate_immediate_sub_sequences(self) -> typing.Generator[
        nn0sl.NaturalNumber0Sequence, None, None]:
        r"""Iterates the immediate (children) sub-:class:`UnrestrictedSequence` of this :class:`AbstractFormula`.

        Note:

        A sub-sequence of an abstract-formula is determined by:

        - 1) the parent rgf sequence,
        - and 2) the rooted plane tree.
        """
        i: int = 1  # remove the root
        child_tree: rpt.RootedPlaneTree
        for child_tree in self.rooted_plane_tree.iterate_immediate_subtrees():
            # retrieve the sub-sequence that is mapped to this child RPT
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + child_tree.size]
            sub_sequence: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*sub_sequence)
            # yield this child RGF sequence
            yield sub_sequence
            # truncate the remaining sequence
            i += child_tree.size

    def iterate_sub_sequences(self) -> collections.abc.Generator[nn0sl.NaturalNumber0Sequence, None, None]:
        i: int
        sub_tree: rpt.RootedPlaneTree
        for i, sub_tree in enumerate(self.rooted_plane_tree.iterate_subtrees()):
            # retrieves the sub-sequence in the sequence
            sub_sequence: tuple[int, ...] = self.natural_number_sequence[i:i + sub_tree.size]
            sub_sequence: nn0sl.NaturalNumber0Sequence = nn0sl.NaturalNumber0Sequence(*sub_sequence)
            # yield the child RGF sequence
            yield sub_sequence

    def iterate_sub_formulas(self) -> collections.abc.Generator[AbstractFormula, None, None]:
        r"""Iterates the sub-formulas of the :class:`AbstractFormula` using the `depth-first, ascending nodes` algorithm.

        See :attr:`AbstractFormula.sub_formulas` for a definition of the term `sub-formula`.

        :return:
        """
        child_tree: rpt.RootedPlaneTree
        child_sequence: nn0sl.NaturalNumber0Sequence
        for child_tree, child_sequence in zip(self.rooted_plane_tree.iterate_subtrees(),
                                              self.iterate_sub_sequences()):
            sub_formula = AbstractFormula(child_tree, child_sequence)
            yield sub_formula

    @property
    def main_element(self) -> int:
        r"""The `main_element` of an :class:`AbstractFormula` is the first element of its
        attr:`AbstractFormula.natural_numbers_sequence`, that corresponds to the root
        node of the attr:`AbstractFormula.rooted_plane_tree`.

        The term `main element` was coined in reference to the term `main connective`
         (cf. Mancosu 2021, p. 17), because abstract-formulas are composed of sequences,
         and thus `main connective` is reserved for "concrete" formulas.

        References:

        - Mancosu 2021

        :return: 1
        """
        return self.natural_number_sequence[0]

    @property
    def natural_number_sequence(self) -> nn0sl.NaturalNumber0Sequence:
        r"""Returns the :class:`NaturalNumberSequence` component of this :class:`AbstractFormula`.

        Shortcut: self.s.

        :return:
        """
        return super().__getitem__(1)

    def represent_as_function(self, connectives: tuple | None = None) -> str:
        r"""Returns a string representation of the :class:`AbstractFormula` using function notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.natural_numbers_sequence` .

        :param connectives: A tuple of connectives of length equal to the length of the :attr:`AbstractFormula.natural_numbers_sequence` . Default: `None`.

        :return:

        """
        if connectives is None:
            connectives = self.natural_number_sequence
        else:
            if len(connectives) != len(self.natural_number_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the abstract-formula's natural-number-sequence.",
                    connectives_length=len(connectives),
                    natural_number_sequence_length=self.natural_number_sequence.length,
                    connectives=connectives,
                    natural_number_sequence=self.natural_number_sequence,
                    abstract_formula=self
                )
        return self.rooted_plane_tree.represent_as_function(
            connectives=connectives)

    def represent_as_map_extension(self, connectives: tuple | None = None) -> str:
        r"""Returns a string representation of the :class:`AbstractFormula` using map notation.

        By default, connectives are represented by their respective values
        in the :attr:`AbstractFormula.natural_numbers_sequence`.

        :param connectives: A tuple of connectives of length equal to the length of the :attr:`AbstractFormula.natural_numbers_sequence`. Default: `None`.

        :return: A string representation of this abstract-formula.

        """
        if connectives is None:
            connectives = self.natural_number_sequence
        else:
            if len(connectives) != len(self.natural_number_sequence):
                raise util.PunctiliousException(
                    "The length of the connectives tuple is not equal to the length "
                    "of the abstract-formula's natural-number-sequence.",
                    connectives_length=len(connectives),
                    natural_number_sequence_length=self.natural_number_sequence.length,
                    connectives=connectives,
                    natural_number_sequence=self.natural_number_sequence,
                    abstract_formula=self
                )
        output = f"{{ "
        first = True
        for i, preimage, j, image in zip(
                range(1, 1 + self.abstract_map_preimage_sequence.arity),
                self.abstract_map_preimage_sequence.immediate_sub_formulas,
                range(1 + self.abstract_map_preimage_sequence.arity,
                      1 + 2 * self.abstract_map_preimage_sequence.arity),
                self.abstract_map_image_sequence.immediate_sub_formulas):
            if not first:
                output = f"{output}, "
            output = f"{output}{preimage} ⟼ {image}"
            first = False
        output = f"{output} }}"

        return output

    @property
    def rooted_plane_tree(self) -> rpt.RootedPlaneTree:
        r"""The :class:`RootedPlaneTree` component of this :class:`AbstractFormula`.

        Shortcut: self.t.

        """
        return super().__getitem__(0)

    @property
    def s(self) -> nn0sl.NaturalNumber0Sequence:
        r"""A shortcut for self.natural_numbers_sequence.

        """
        return self.natural_number_sequence

    @property
    def sequence_max_value(self) -> int:
        r"""The `sequence_max_value` of an :class:`AbstractFormula` is the `max_value` of its `natural_numbers_sequence`.

        """
        return self.natural_number_sequence.max_value

    @property
    def sub_formulas(self) -> tuple[AbstractFormula, ...]:
        r"""The `sub_formulas` of an :class:`AbstractFormula` `phi` is the tuple of :class:`AbstractFormula` elements that are present
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
            sub_formulas: list[AbstractFormula] = list()
            for sub_formula in self.iterate_sub_formulas():
                sub_formulas.append(sub_formula)
            self._sub_formulas = tuple(sub_formulas)
        return self._sub_formulas

    def substitute_sub_formulas_with_map(self, m: FlexibleAbstractFormula) -> AbstractFormula:
        r"""Returns a new abstract-formula similar to the current abstract-formula,
         except that its subformulas present in the map `m` preimage,
         are substituted with their corresponding images,
         giving priority to the substitution of superformulas over subformulas.

        :param m: An abstract-map.
        :return: A substituted formula.

        """
        m: AbstractFormula = AbstractFormula.from_any(m)
        if not m.is_abstract_map:
            raise util.PunctiliousException("`m` is not an abstract-map.", m=m, this_abstract_formula=self)
        if self in m.abstract_map_preimage_sequence.immediate_sub_formulas:
            # This formula must be substituted according to the substitution map.
            return m.get_abstract_map_value(self)
        else:
            # Pursue substitution recursively.
            phi: AbstractFormula
            s: tuple[AbstractFormula, ...] = tuple(phi.substitute_sub_formulas_with_map(m=m) for phi in
                                                   self.iterate_immediate_sub_formulas())
            return AbstractFormula.from_immediate_sub_formulas(n=self.main_element, s=s)

    @property
    def t(self) -> rpt.RootedPlaneTree:
        r"""A shortcut for self.rooted_plane_tree."""
        return self.rooted_plane_tree

    @property
    def tree_degree(self) -> int:
        r"""The `tree_degree` of an :class:`AbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_degree` and `formula_degree`.
        """
        return self.rooted_plane_tree.degree

    @property
    def tree_size(self) -> int:
        r"""The `tree_size` of an :class:`AbstractFormula` is the number of vertices in its `RootedPlaneTree`.

        Attention point: do not confuse `tree_size` and `formula_degree`.
        """
        return self.rooted_plane_tree.size


# Transformation functions


def extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p):
    r"""Given a tree of integer/tuple pairs, extracts:

     - its tree of tuples,
     - and its sequence of integers,

    following the depth-first ascending-nodes algorithm.

    :param p: the tree of integer/tuple pairs

    :return: a pair (T, S) where T is a tree of tuples, and S is a sequence of integers.
    """
    if len(p) != 2:
        raise util.PunctiliousException('The length of the pair is not equal to 2.', len_t=len(p), t=p)
    i: int = p[0]
    children = p[1]
    if len(children) == 0:
        # this is a leaf
        return (), (i,)
    else:
        t: list = []
        s: tuple[int, ...] = (i,)
        for sub_p in children:
            sub_t, sub_s = extract_tree_of_tuples_and_sequence_from_tree_of_integer_tuple_pairs(p=sub_p)
            t.append(sub_t)
            s += sub_s
        t: tuple[tuple, ...] = tuple(t)
        return t, s


# Flexible types to facilitate data validation

FlexibleAbstractFormula = typing.Union[
    AbstractFormula, tuple[
        rpt.FlexibleRootedPlaneTree, nn0sl.FlexibleNaturalNumber0Sequence], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

AF = AbstractFormula  # An alias for AbstractFormula
