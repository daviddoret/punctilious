from __future__ import annotations
import itertools
import typing
import collections

# punctilious libraries
import punctilious.util as util
import punctilious.binary_relation_library as orl
import punctilious.natural_number_0_library as nn0l
import punctilious.prime_number_library as pnl


# Relation orders


class LexicographicOrder(orl.BinaryRelation):
    r"""The lexicographic order of (0-based) natural numbers.

    Note
    -----

    The lexicographic order is not an isomorphism

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under lexicographic-order if and only if:

    :math:`\exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    Quotes
    -------

    "(Lexicographic order.) Let S be well-ordered by ≺, and for n > 0 let Tn
    be the set of all n-tuples (x1, x2, ..., xn) of elements xj in S.
    Define (x1, x2, ..., xn) ≺ (y1, y2, ..., yn) if there is some k, 1 ≤ k ≤ n,
    such that xj = yj for 1 ≤ j < k, but xk ≺ yk in S." [Knuth 1997, p. 20]

    "Here the relation (an, ..., a1) < (bn, ..., b1) denotes lexicographic ordering from left to right;
    that is, there is an index j such that ak = bk for n ≥ k > j, but aj < bj." [Knuth 1998, p. 6]

    Bibliography
    --------------

    - Knuth, Donald Ervin. The Art of Computer Programming - Volume 1 - Fundamental Algorithms - Third Edition. 1997.
    - Knuth, Donald Ervin. The Art of Computer Programming - Volume 3 - Sorting and Searching - Second Edition. 1998.


    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = True
    _is_irreflexive: bool | None = True
    _is_reflexive: bool | None = False
    _is_strongly_connected: bool | None = False
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        if x.is_equal_to(y):
            return False
        else:
            minimum_length: int = min(x.length, y.length)
            i: int
            for i in range(minimum_length):
                if x[i] < y[i]:
                    return True
                elif x[i] > y[i]:
                    return False
            # All compared elements are equal.
            if len(x) < len(y):
                # Shorter sequence is less
                return True
            else:
                return False


lexicographic_order = LexicographicOrder()


class SumFirstLexicographicSecondOrder(orl.BinaryRelation):
    r"""The sum-first-lexicographic-second order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under sum-lexicographic-order if and only if:

    :math:`\sum{S} < \sum{T}`

    or:

    :math:`\sum{S} = \sum{T} \land \exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`\sum{S} = \sum{T} \land m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    See also
    ----------

    - :class:`LexicographicOrder`


    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = True
    _is_irreflexive: bool | None = True
    _is_reflexive: bool | None = False
    _is_strongly_connected: bool | None = False
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        if x.is_equal_to(y):
            return False
        elif x.length < y.length:
            return True
        elif y.length < x.length:
            return False
        else:
            minimum_length: int = min(x.length, y.length)
            i: int
            for i in range(minimum_length):
                if x[i] < y[i]:
                    return True
                elif x[i] > y[i]:
                    return False
            # All compared elements are equal.
            if len(x) < len(y):
                # Shorter sequence is less
                return True
            else:
                return False


sum_first_lexicographic_second_order = SumFirstLexicographicSecondOrder()


class GodelNumberEncodingOrder(orl.BinaryRelation):
    r"""The Godel-number-encoding relation order of (0-based) natural number sequences.

    Mathematical definition - xRy
    -------------------------------

    Let :math:`x = (s_0, s_1, \ldots, s_n)`
    be a finite sequences with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`y = (t_0, t_1, \ldots, t_n)`
    be a finite sequences with :math:`t_i \in \mathbb{N}^+`.

    :math:`xRy` if and only if :math:`\mathrm{rank}(S) < \mathrm{rank}(T)`

    Mathematical definition - rank()
    ----------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequence with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`p_0, p_1, \ldots, p_n` be the first :math:`n` prime numbers in ascending order.

    :math:`\mathrm{rank}(S) = p_0^{s_0} \cdot p_1^{s_1} \ldots p_n^{s_n}`

    Note
    ------

    The Gödel-number-encoding order has the following disadvantages:

    - it is not bijective with the natural numbers,
    - it grows very fast,
    - unranking requires factorization (but easy in practice because primes are taken in sequence).

    Note
    -----

    :math:`rank((1)) = 2^1 = 2`

    :math:`rank((1,0)) = 2^1 * 3^0 = 2`

    It follows that the Gödel-number-encoding order is not injective.

    It follows that the Gödel-number-encoding order is not bijective.

    It follows that the Gödel-number-encoding order is not isomorphic to (N, <).

    See the :class:`RefinedGodelNumberEncodingOrder` for an improved version of
    the Gödel-number-encoding order that is isomorphic to (N, <).

    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = True
    _is_irreflexive: bool | None = True
    _is_order_isomorphic_to_n_strictly_less_than: bool | None = False
    _is_reflexive: bool | None = False
    _is_strongly_connected: bool | None = False
    _is_transitive: bool | None = True

    def rank(self, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x = NaturalNumber0Pair.from_any(x)
        if x == NaturalNumber0Pair():
            return 0
        else:
            n = 1
            p = 1
            for i, f in enumerate(x):
                p = pnl.get_next_prime(p)
                if i == len(x) - 1:
                    # this is the last factor
                    # Increment it to undo the encoding hack for leading zeroes.
                    f += 1
                n = n * p ** f
            return n - 1

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        n: int = self.rank(x)
        m: int = self.rank(y)
        return n < m

    def successor(self, x: object) -> object:
        n = self.rank(x)
        n += 1
        y = self.unrank(n)
        return y

    def unrank(self, n: int) -> object:
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return NaturalNumber0Pair()
        else:
            f = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Pair(*s)


godel_number_order = GodelNumberEncodingOrder()


class RefinedGodelNumberOrder(orl.BinaryRelation):
    r"""The refined Godel-number-encoding order of (0-based) natural number sequences.

    Mathematical definition - xRy
    -------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequences with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`T = (t_0, t_1, \ldots, t_n)`
    be a finite sequences with :math:`t_i \in \mathbb{N}^+`.

    :math:`S < T` if and only if :math:`\mathrm{rank}(S) < \mathrm{rank}(T)`

    Mathematical definition - rank()
    ----------------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_n)`
    be a finite sequence with :math:`s_i \in \mathbb{N}^+`.

    Let :math:`p_0, p_1, \ldots, p_n` be the first :math:`n` prime numbers in ascending order.

    :math:`\mathrm{rank}(S) = p_0^{s_0 - 1} \cdot p_1^{s_1 - 1} \ldots p_n^{s_n - 1}

    The :math:`- 1` in the ranking formula is necessary to make the function bijective
    when working with 1-based natural numbers.

    Note
    ------

    The Gödel-number-encoding order has the following disadvantages:

    - it grows very fast,
    - unranking requires factorization (but not so hard because primes are taken in sequence).

    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = True
    _is_irreflexive: bool | None = True
    _is_reflexive: bool | None = False
    _is_strongly_connected: bool | None = False
    _is_transitive: bool | None = True

    def rank(self, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x = NaturalNumber0Pair.from_any(x)
        if x == NaturalNumber0Pair():
            return 0
        else:
            n = 1
            p = 1
            for i, f in enumerate(x):
                p = pnl.get_next_prime(p)
                if i == len(x) - 1:
                    # this is the last factor
                    # Increment it to undo the encoding hack for leading zeroes.
                    f += 1
                n = n * p ** f
            return n - 1

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        n: int = self.rank(x)
        m: int = self.rank(y)
        return n < m

    def successor(self, x: object) -> object:
        n = self.rank(x)
        n += 1
        y = self.unrank(n)
        return y

    def unrank(self, n: int) -> object:
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return NaturalNumber0Pair()
        else:
            f = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Pair(*s)


refined_godel_number_order = RefinedGodelNumberOrder()


class CantorPairingOrder(orl.BinaryRelation):
    r"""The Cantor pairing order of (0-based) natural numbers.

    Bibliography
    --------------

    - https://en.wikipedia.org/wiki/Pairing_function
    - https://www.cantorsparadise.org/cantor-pairing-function-e213a8a89c2b/

    """

    # mathematical properties
    _is_antisymmetric: bool | None = None
    _is_asymmetric: bool | None = None
    _is_connected: bool | None = None
    _is_irreflexive: bool | None = None
    _is_reflexive: bool | None = None
    _is_strongly_connected: bool | None = None
    _is_transitive: bool | None = None

    def rank(self, x: object) -> int:
        """
            Cantor pairing function: maps two natural numbers to a unique natural number.
            π(x,y) = (x + y)(x + y + 1)/2 + y
            """
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        return ((x.x + x.y) * (x.x + x.y + 1)) // 2 + x.y

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        n: int = self.rank(x)
        m: int = self.rank(y)
        return n < m

    def successor(self, x: object) -> object:
        n = self.rank(x)
        n += 1
        y = self.unrank(n)
        return y

    def unrank(self, n: int) -> object:
        """
        Inverse of Cantor pairing function: maps a natural number back to a pair.
        """
        # Find the triangular root
        w = int(((8 * n + 1) ** 0.5 - 1) / 2)
        t = (w * (w + 1)) // 2
        y = n - t
        x = w - y
        return NaturalNumber0Pair(x, y)


cantor_pairing_order = CantorPairingOrder()


# TODO: Implement the Szudzik "more elegant" order
# http://szudzik.com/ElegantPairing.pdf


class IsEqualTo(orl.BinaryRelation):
    r"""The equality binary-relation for 0-based natural numbers.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_0, = )`.

    """

    # mathematical properties
    _is_antisymmetric: bool | None = True
    _is_asymmetric: bool | None = False
    _is_connected: bool | None = False
    _is_irreflexive: bool | None = False
    _is_reflexive: bool | None = True
    _is_strongly_connected: bool | None = False
    _is_symmetric: bool | None = True
    _is_transitive: bool | None = True

    def relates(self, x: object, y: object) -> bool:
        x: NaturalNumber0Pair = NaturalNumber0Pair.from_any(x)
        y: NaturalNumber0Pair = NaturalNumber0Pair.from_any(y)
        return x.is_natural_number_0_pair_equivalent_to(y)


is_equal_to = IsEqualTo()


# Classes


class NaturalNumber0Pair(orl.RelationalElement, tuple):
    """A pair of (0-based) natural numbers.

    """

    # Configuration of class properties (cf. Relatable).
    _is_equal_to: orl.BinaryRelation = is_equal_to
    _is_strictly_less_than: orl.BinaryRelation = cantor_pairing_order

    def __add__(self, s):
        """Performs a scalar addition if s is an integer.

        :param s:
        :return:
        """
        if isinstance(s, int):
            return self.scalar_addition(n=s)
        else:
            raise util.PunctiliousException("Unsupported type.")

    def __hash__(self):
        return hash((NaturalNumber0Pair, NaturalNumber0Pair._HASH_SEED, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumber0Pair, self).__init__()
        self._image: tuple[int, ...] | None = None
        self._is_restricted_growth_function_sequence: bool | None = None
        self._restricted_growth_function_sequence: NaturalNumber0Pair | None = None

    def __new__(cls, *s):
        v: bool
        s: tuple[int] | None
        r: bool
        v, s = cls.data_validate_elements(s, raise_exception_on_validation_failure=True)
        s: tuple[int] = super(NaturalNumber0Pair, cls).__new__(cls, s)
        s: tuple[int] = cls._from_cache(s)
        if len(s) != 2:
            raise util.PunctiliousException("A pair must contain strictly two elements.", s_length=len(s), s=s)
        return s

    _HASH_SEED: int = 6599904930401148556  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    _cache: dict[
        int, NaturalNumber0Pair] = dict()  # cache for NaturalNumber0Pair.

    @classmethod
    def _compute_hash(cls, o: FlexibleNaturalNumber0Pair) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a natural-number-0-pair.
        :return: The hash of the natural-number-0-pair that is structurally equivalent to `o`.
        """
        return hash((NaturalNumber0Pair, cls._HASH_SEED, o.elements,))

    @classmethod
    def _from_cache(cls, o: FlexibleNaturalNumber0Pair):
        r"""Cache mechanism used in the constructor."""
        hash_value: int = NaturalNumber0Pair._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    def to_restricted_growth_function_sequence(self) -> NaturalNumber0Pair:
        r"""Converts the natural-number-0-pair `s` into a restricted-growth-function-sequence `t`,
        by applying canonical labeling.

        Notation:
        :math:`canonical(S)`

        Definition - Canonical Labeling:
        The canonical-labeling of a natural-numbers-sequence S is an RFG-sequence T such that:
         - the value of the first element of S is mapped to 1
         - whenever a new value x appears in S, it is mapped to max(t0, t1, ..., ti) + 1 where i is the index
           position of x in S

        Examples:
        (3,5,2,1) --> (1,2,3,4)
        (3,5,3,1,5,2) --> (1,2,1,3,2,4)

        :return:
        """
        if self.is_restricted_growth_function_sequence:
            return self
        elif self._restricted_growth_function_sequence is not None:
            return self._restricted_growth_function_sequence
        else:
            mapping: dict[int, int] = dict()
            mapped_value: int = 0
            n: int
            for n in self:
                if n not in mapping.keys():
                    mapping[n] = mapped_value
                    mapped_value += 1
            s: tuple[int, ...] = tuple(mapping[n] for n in self)
            self._restricted_growth_function_sequence = NaturalNumber0Pair(*s)
            return self._restricted_growth_function_sequence

    @classmethod
    def data_validate_elements(
            cls,
            o: FlexibleNaturalNumber0Pair, raise_exception_on_validation_failure: bool = True) -> \
            tuple[bool, FlexibleNaturalNumber0Pair | None]:
        r"""Validates `o` as a collection of (0-based) natural number elements,
        applying implicit conversion as necessary.

        :param o: An object that may be interpreted as a :class:`NaturalNumber0Pair`.
        :param raise_exception_on_validation_failure: Raises an exception if data validation fails.
        :return: a tuple (v, s) where v is True if data validation was successful, False otherwise,
            and s is the resulting natural-number sequence, or None if data validation failed.
        """
        if isinstance(o, NaturalNumber0Pair):
            # data validation is assured by the class logic.
            return True, o
        if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
            o: tuple[nn0l.NaturalNumber0, ...] = tuple(nn0l.NaturalNumber0.from_any(n) for n in o)
            return True, o
        if raise_exception_on_validation_failure:
            raise util.PunctiliousException("The type of `o` is not supported.", o_type=type(o), o=o)
        else:
            return False, None

    @property
    def elements(self) -> tuple[int, ...]:
        r"""Returns a tuple of the elements that compose this :class:`NaturalNumber0Pair`, preserving order.

        :return: a tuple of the elements that compose this :class:`NaturalNumber0Pair`, preserving order.
        """
        return tuple(super().__iter__())

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber0Pair:
        r"""Declares a natural-number-0-pair from a Python object that can be interpreted as a natural-number-0-pair.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a natural-number-0-pair.
        :return: a natural-number-0-pair.
        """
        if isinstance(o, NaturalNumber0Pair):
            return o
        if isinstance(o, collections.abc.Iterable):
            return NaturalNumber0Pair(*o)
        if isinstance(o, collections.abc.Generator):
            return NaturalNumber0Pair(*o)
        raise util.PunctiliousException('NaturalNumber0Pair data validation failure', o=o)

    @property
    def im(self) -> tuple[int, ...]:
        r"""A shortcut for :attr:`NaturalNumber0Pair.image`."""
        return self.image

    @property
    def image(self) -> tuple[int, ...]:
        r"""The :attr:`NaturalNumber0Pair.image` is the set of values contained in the sequence,
        returned as a tuple of ascending and unique values.

        Notation:
        :math:`Im(S)`

        Note: a Python tuple is returned instead of a Python set. This is a design choice
            to force working with immutable objects.

        Note: the values are returned in ascending order.

        Shortcut: :attr:`NaturalNumber0Pair.im`

        Definition:
            S := { s_0, s_1, ..., s_n }
            Im(S) := { s_i | 0 <= i <= n }

        :return: an ordered tuple of integers.
        """
        if self._image is not None:
            return self._image
        else:
            s: set[int] = set()
            for n in self.elements:
                s.add(n)
            s: tuple[int, ...] = tuple(s)
            s: tuple[int, ...] = tuple(sorted(s))
            self._image = s
            return s

    @property
    def image_cardinality(self) -> int:
        r"""The :attr:`NaturalNumber0Pair.image_cardinality` is the cardinality
         of the :attr:`NaturalNumber0Pair.image`, i.e. the number of distinct values it contains.

        Notation:
        :math:`|Im(S)|`

        :return:
        """
        return len(self.image)

    def is_restricted_growth_function_sequence_equivalent_to(self, s) -> bool:
        r"""`True` if this natural number sequence RGF equivalent
        to the natural-number-0-pair `s`, `False` otherwise.

        Notation:
        :math:`S ~_{canonical} T`

        Formal Definition:
        Two natural-number-0-pairs `s` and `t` are canonical-natural-number-0-pair-equivalent
        if and only if their canonical-natural-number-0-pair are natural-number-0-pair-equivalent.

        """
        s: NaturalNumber0Pair = NaturalNumber0Pair.from_any(s)
        return self.to_restricted_growth_function_sequence().is_natural_number_0_pair_equivalent_to(s)

    @property
    def is_increasing(self) -> bool:
        r"""Returns `True` if this sequence is increasing, `False` otherwise.

        Definition - Increasing sequence:
        A sequence :math:`S = (n_0, n1, \cdots, n_l)` is increasing
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, n_{i + 1} \ge n_i`.

        References:
         - Adams, Malcolm R. “An Introduction to Mathematical Analysis,” 2007.

        :return: `True` if this sequence is increasing, `False` otherwise.
        """
        return all(self.elements[i + 1] >= self.elements[i] for i in range(0, self.length - 1))

    @property
    def is_natural_number_sequence(self) -> bool:
        r"""

        Notation:
        :math:`\mathbb{N}\text{-sequence}(S)

        :return:
        """
        return True

    def is_natural_number_0_pair_equivalent_to(self, s: FlexibleNaturalNumber0Pair):
        r"""

        Notation:
        :math:`S ~_{\mathbb{N}\text{-sequence}} T`

        Formal definition:
        Two natural numbers-sequences s and t are natural-numbers-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: NaturalNumber0Pair = NaturalNumber0Pair.from_any(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @property
    def is_restricted_growth_function_sequence(self) -> bool:
        """`True` if this natural numbers sequence is also an RGF sequence, `False` otherwise.

        Formal Definition:
        A restricted-growth-function-sequence is a finite (computable) sequence
        of natural numbers (n_0, n_1, ..., n_i) such that:
            - n_0 = 1
            - n_j <= 1 + max(n_0, n_1, ..., n_(j-1)) for 0 < j <= i

        Synonyms:
         - RGFS
         - RGF sequence

        Note:
        Often RGF sequences have an initial value of 1 in the literature. We choose 0 here for consistency
        with the design choice of using 0-based indexes as the default indexing method in Python.

        """
        if self._is_restricted_growth_function_sequence is not None:
            return self._is_restricted_growth_function_sequence
        else:
            for i, n in enumerate(self):
                if i == 0 and n > 1:
                    self._is_restricted_growth_function_sequence: bool = False
                    return self._is_restricted_growth_function_sequence
                if i > 0 and n > max(self.elements[0:i]) + 1:
                    self._is_restricted_growth_function_sequence: bool = False
                    return self._is_restricted_growth_function_sequence
            self._is_restricted_growth_function_sequence: bool = True
            return self._is_restricted_growth_function_sequence

    @property
    def is_strictly_increasing(self) -> bool:
        r"""Returns `True` if this sequence is strictly increasing, `False` otherwise.

        Definition - Strictly increasing sequence:
        A sequence :math:`S = (n_0, n1, \cdots, n_l)` is strictly increasing
        if and only if :math:`\forall i \in \{ 0, 1, \cdots, l - 1 \}, n_{i + 1} > n_i`.

        References:
         - Adams, Malcolm R. “An Introduction to Mathematical Analysis,” 2007.

        :return: `True` if this sequence is strictly increasing, `False` otherwise.
        """
        return all(self.elements[i + 1] > self.elements[i] for i in range(0, self.length - 1))

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence.

        Notation:
        :math:`|S|`

        """
        return len(self)

    @property
    def max_value(self) -> int:
        """The `max_value` of a `NaturalNumber0Pair` is the maximum value of its elements.

        Notation:
        :math:`max(S)`

        """
        return max(self)

    def scalar_addition(self, n: int):
        r"""Given a :class:`NaturalNumber0Pair` :math:`S`,
        and a natural number :math:`n`,
        return a :class:`NaturalNumber0Pair` :math:`T` defined as
        :math:`(t_0 + n, t_1 + n, \cdots, t_i)`.

        :param n:
        :return:
        """
        t: tuple[int, ...] = tuple(x + n for x in self.elements)
        return NaturalNumber0Pair(*t)

    @property
    def x(self) -> nn0l.NaturalNumber0:
        """Returns the first element of the pair.

        :return:
        """
        return self.elements[0]

    @property
    def y(self) -> nn0l.NaturalNumber0:
        """Returns the second element of the pair.

        :return:
        """
        return self.elements[1]


# Flexible types to facilitate data validation

FlexibleNaturalNumber0Pair = typing.Union[
    NaturalNumber0Pair, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

NN0S = NaturalNumber0Pair  # An alias for NaturalNumber0Pair
