from __future__ import annotations
import itertools
import typing
import collections
import functools

# punctilious libraries
import punctilious.util as util
import punctilious.binary_relation_library as brl
import punctilious.natural_number_0_library as nn0l
import punctilious.prime_number_library as pnl
import punctilious.ternary_boolean_library as tbl
import punctilious.special_values_library as spl


# Relation orders

class LexicographicOrder(brl.BinaryRelation):
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

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.FALSE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
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


class LengthFirstLexicographicSecondOrder(brl.BinaryRelation):
    r"""The length-first-lexicographic-second order of (0-based) natural numbers.

    Mathematical definition
    -------------------------

    Let :math:`S = (s_0, s_1, \ldots, s_m)` and :math:`T = (t_0, t_1, \ldots, t_n)`
    be two finite sequences of (1-based) natural numbers with :math:`s_i, t_j \in \mathbb{N}^+`.

    We say that :math:`S \prec T` under sum-lexicographic-order if and only if:

    :math:`|{S}| < |{T}|`

    or:

    :math:`|{S}| = |{T}| \land \exists k \leq \min(m,n)` such that :math:`s_i = t_i` for all :math:`i < k` and :math:`s_k < t_k`

    or:

    :math:`|{S}| = |{T}| \land m < n` and :math:`s_i = t_i` for all :math:`i = 1, \ldots, m`

    Note
    ------

    In the context of labeled rooted plane trees,
    "length-first" orders may look better suited to design orders of labeled rooted plane trees,
    because labeled rooted plane trees require the linkage of two orders:

    - rooted plane trees,
    - sequences of (0-based) natural numbers.

    In effect, for a labeled rooted plane tree to be well-formed,
    the size of the rooted plane trees must be equal
    to the length of the (0-based) natural number sequence.

    But the problem with length-first orders is that they are not well-founded,
    as by definition they have infinite chains, such as:
    (0),(1),(2),(3),...

    In effect, as there are countably infinite sequences of size n,
    length-first orders cannot be well-founded.

    See also
    ----------

    - :class:`LexicographicOrder`


    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def rank(cls, x: object) -> int | typing.Literal[spl.SpecialValues.NOT_AVAILABLE]:
        # TODO: IMPLEMENT THIS
        pass

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
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

    @classmethod
    def unrank(cls, n: int) -> object:
        pass
    # TODO: IMPLEMENT THIS


class SumFirstLexicographicSecondOrder(brl.BinaryRelation):
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

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        if x.is_equal_to(y):
            return False
        elif sum(x) < sum(y):
            return True
        elif sum(y) < sum(x):
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


class GodelNumberEncodingOrder(brl.BinaryRelation):
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

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.FALSE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x = NaturalNumber0Sequence.from_any(x)
        if x == cls.least_element:
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

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: object) -> object:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return cls.least_element
        else:
            f = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Sequence(*s)


class RefinedGodelNumberOrder(brl.BinaryRelation):
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

    :math:`\mathrm{rank}(S) = p_0^{s_0} \cdot p_1^{s_1} \ldots p_n^{s_n}

    Note
    ------

    The Gödel-number-encoding order has the following disadvantages:

    - it grows very fast,
    - unranking requires factorization (but not so hard because primes are taken in sequence).

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 should be mapped to the empty sequence ().
        1 should be mapped to sequence (0).

        :param x:
        :return:
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        if x == cls.least_element:
            return 0
        else:
            n: int = 1
            p: int = 1
            i: int
            exponent: int
            for i, exponent in enumerate(x):
                p = pnl.get_next_prime(p)
                if i == len(x) - 1:
                    # this is the last factor
                    # Increment it to undo the encoding hack for leading zeroes.
                    exponent += 1
                factor: int = p ** exponent
                n = n * factor
            return n - 1

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: object) -> object:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> object:
        n = int(n)
        n += 1  # Makes the ranks 0-based.
        if n == 1:
            return cls.least_element
        else:
            f: tuple[int, ...] = pnl.factorize(n)
            # Decrement the last element by 1.
            # This hack makes leading zeroes meaningful.
            s = util.decrement_last_element(f)
            return NaturalNumber0Sequence(*s)


class CombinedIntegerWithSentinelOrder(brl.BinaryRelation):
    r"""The combined integer with sentinel order of (0-based) natural number sequence.

    See also
    ---------

    - :func:`util.combine_nbit_ints_with_sentinel`.
    - :func:`util.split_nbit_ints_with_sentinel`.

    Note
    ------

    The problem with the Gödel number approach is that it grows extremely fast.
    If we accept as a constraint that sequence elements have maximum = 2^n,
    such as 2^32, or 2^64 as is usual on many computer systems,
    then we can combine integer values using fixed-length bit representations.
    And to solve the problem of leading zeroes, we append a sentinel value of 1.

    """

    _max_bits_constraints: int = 32

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        """

        The least element is the empty sequence.

        :return:
        """
        return NaturalNumber0Sequence()

    @classmethod
    def rank(cls, x: object) -> int:
        """

        0 is mapped to the empty sequence ().
        1 is mapped to sequence (0).

        :param x:
        :return:
        """
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        return util.combine_fixed_length_ints_with_sentinel(i=x, b=cls._max_bits_constraints)

    @classmethod
    def relates(cls, x: FlexibleNaturalNumber0Sequence, y: FlexibleNaturalNumber0Sequence) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        n: int = cls.rank(x)
        m: int = cls.rank(y)
        return n < m

    @classmethod
    def successor(cls, x: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        n = cls.rank(x)
        n += 1
        y = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> NaturalNumber0Sequence:
        n = int(n)
        s: tuple[int, ...] = util.split_fixed_length_ints_with_sentinel(i=n, b=cls._max_bits_constraints)
        s: NaturalNumber0Sequence = NaturalNumber0Sequence(*s)
        return s


class IsEqualTo(brl.BinaryRelation):
    r"""The equality binary-relation for 0-based natural numbers.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{N}_0, = )`.

    """

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        y: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(y)
        return x.is_natural_number_0_sequence_equivalent_to(y)


# General functions

def concatenate_natural_number_0_sequences(*s: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
    """Concatenates a collection of :class:`NaturalNumberSequence` elements, preserving order.

    :param s:
    :return:
    """
    s: tuple[int] = tuple(itertools.chain.from_iterable(
        t for t in s))
    return NaturalNumber0Sequence(*s)


# Classes


class NaturalNumber0Sequence(brl.OrderIsomorphicToNaturalNumber0AndStrictlyLessThanStructure, tuple):
    """A finite (computable) sequence of (0-based) natural numbers.

    Definition:
    An :class:`NaturalNumberSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_j) such that:
        - n_i >= 0 for 0 <= i <= j

    """

    def __add__(self, s):
        """Concatenates this :class:`NaturalNumberSequence` with another :class:`NaturalNumberSequence` `s`.
        Or performs a scalar addition if s is an integer.

        Note:
            This enables the usage of the python sum function, e.g.: sum(s0, s1, ...).

        :param s:
        :return:
        """
        if isinstance(s, int):
            return self.scalar_addition(n=s)
        elif isinstance(s, typing.Iterable):
            return concatenate_natural_number_0_sequences(self, s)
        else:
            raise util.PunctiliousException("Unsupported type.")

    def __hash__(self):
        return hash((NaturalNumber0Sequence, NaturalNumber0Sequence._HASH_SEED, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumber0Sequence, self).__init__()

    def __new__(cls, *s):
        v: bool
        s: tuple[int] | None
        r: bool
        v, s = cls.data_validate_elements(s, raise_exception_on_validation_failure=True)
        s: tuple[int] = super(NaturalNumber0Sequence, cls).__new__(cls, s)
        s: tuple[int] = cls._from_cache(s)
        return s

    _HASH_SEED: int = 6807878777699371138  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    _cache: dict[
        int, NaturalNumber0Sequence] = dict()  # cache for NaturalNumberSequence.

    @classmethod
    def _compute_hash(cls, o: FlexibleNaturalNumber0Sequence) -> int:
        r"""Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a natural-number-sequence.
        :return: The hash of the natural-number-sequence that is structurally equivalent to `o`.
        """
        return hash((NaturalNumber0Sequence, cls._HASH_SEED, o.elements,))

    @classmethod
    def _from_cache(cls, o: FlexibleNaturalNumber0Sequence):
        r"""Cache mechanism used in the constructor."""
        hash_value: int = NaturalNumber0Sequence._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    def concatenate_with(self, x) -> NaturalNumber0Sequence:
        x: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(x)
        return concatenate_natural_number_0_sequences(self, x, )

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return RefinedGodelNumberOrder

    @util.readonly_class_property
    def least_element(cls) -> NaturalNumber0Sequence:
        return cls.is_strictly_less_than_relation.least_element

    @functools.cached_property
    def restricted_growth_function_sequence(self) -> NaturalNumber0Sequence:
        r"""Converts the natural-number-sequence `s` into a restricted-growth-function-sequence `t`,
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
        else:
            mapping: dict[int, int] = dict()
            mapped_value: int = 0
            n: int
            for n in self:
                if n not in mapping.keys():
                    mapping[n] = mapped_value
                    mapped_value += 1
            s: tuple[int, ...] = tuple(mapping[n] for n in self)
            return NaturalNumber0Sequence(*s)

    def concatenate_with(self, *s: FlexibleNaturalNumber0Sequence) -> NaturalNumber0Sequence:
        r"""Concatenates this :class:`NaturalNumberSequence` with :class:`NaturalNumberSequence` `s`,
        or an iterable / generator of multiple :class:`NaturalNumberSequence` elements.

        Notation:
        :math:`S \mathbin{+\!\!+} T`

        Shortcuts:
        s1 + s2
        sum(s1, s2, ..., sn)

        :param s:
        :return:
        """
        return concatenate_natural_number_0_sequences(self, *s)

    @classmethod
    def data_validate_elements(
            cls,
            o: FlexibleNaturalNumber0Sequence, raise_exception_on_validation_failure: bool = True) -> \
            tuple[bool, FlexibleNaturalNumber0Sequence | None]:
        r"""Validates `o` as a collection of (0-based) natural number elements,
        applying implicit conversion as necessary.

        :param o: An object that may be interpreted as a :class:`NaturalNumberSequence`.
        :param raise_exception_on_validation_failure: Raises an exception if data validation fails.
        :return: a tuple (v, s) where v is True if data validation was successful, False otherwise,
            and s is the resulting natural-number sequence, or None if data validation failed.
        """
        if isinstance(o, NaturalNumber0Sequence):
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
        r"""Returns a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.

        :return: a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.
        """
        return tuple(super().__iter__())

    @classmethod
    def from_any(cls, o: object) -> NaturalNumber0Sequence:
        r"""Declares a natural-number-sequence from a Python object that can be interpreted as a natural-number-sequence.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a natural-number-sequence.
        :return: a natural-number-sequence.
        """
        if isinstance(o, NaturalNumber0Sequence):
            return o
        if isinstance(o, collections.abc.Iterable):
            return NaturalNumber0Sequence(*o)
        if isinstance(o, collections.abc.Generator):
            return NaturalNumber0Sequence(*o)
        raise util.PunctiliousException('NaturalNumberSequence data validation failure', o=o)

    @property
    def im(self) -> tuple[int, ...]:
        r"""A shortcut for :attr:`NaturalNumberSequence.image`."""
        return self.image

    @functools.cached_property
    def image(self) -> tuple[int, ...]:
        r"""The :attr:`NaturalNumberSequence.image` is the set of values contained in the sequence,
        returned as a tuple of ascending and unique values.

        Notation:
        :math:`Im(S)`

        Note: a Python tuple is returned instead of a Python set. This is a design choice
            to force working with immutable objects.

        Note: the values are returned in ascending order.

        Shortcut: :attr:`NaturalNumberSequence.im`

        Definition:
            S := { s_0, s_1, ..., s_n }
            Im(S) := { s_i | 0 <= i <= n }

        :return: an ordered tuple of integers.
        """
        s: set[int] = set()
        for n in self.elements:
            s.add(n)
        s: tuple[int, ...] = tuple(s)
        s: tuple[int, ...] = tuple(sorted(s))
        return s

    @functools.cached_property
    def image_cardinality(self) -> int:
        r"""The :attr:`NaturalNumberSequence.image_cardinality` is the cardinality
         of the :attr:`NaturalNumberSequence.image`, i.e. the number of distinct values it contains.

        Notation:
        :math:`|Im(S)|`

        :return:
        """
        return len(self.image)

    def is_restricted_growth_function_equivalent_to(self, s) -> bool:
        r"""`True` if this natural number sequence canonical-natural-number-sequence-equivalent
        to the natural-number-sequence `s`, `False` otherwise.

        Notation:
        :math:`S ~_{canonical} T`

        Formal Definition:
        Two natural-number-sequences `s` and `t` are canonical-natural-number-sequence-equivalent
        if and only if their canonical-natural-number-sequence are natural-number-sequence-equivalent.

        """
        s: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(s)
        return self.restricted_growth_function_sequence.is_natural_number_0_sequence_equivalent_to(s)

    @functools.cached_property
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

    @functools.cached_property
    def is_natural_number_sequence(self) -> bool:
        r"""

        Notation:
        :math:`\mathbb{N}\text{-sequence}(S)

        :return:
        """
        return True

    def is_natural_number_0_sequence_equivalent_to(self, s: FlexibleNaturalNumber0Sequence):
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
        s: NaturalNumber0Sequence = NaturalNumber0Sequence.from_any(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @functools.cached_property
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
        for i, n in enumerate(self):
            if i == 0 and n >= 1:
                return False
            if i > 0 and n > max(self.elements[0:i]) + 1:
                return False
        return True

    @functools.cached_property
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

    @functools.cached_property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence.

        Notation:
        :math:`|S|`

        """
        return len(self)

    @functools.cached_property
    def max_value(self) -> int:
        """The `max_value` of a `NaturalNumberSequence` is the maximum value of its elements.

        Notation:
        :math:`max(S)`

        """
        return max(self)

    def scalar_addition(self, n: int):
        r"""Given a :class:`NaturalNumberSequence` :math:`S`,
        and a natural number :math:`n`,
        return a :class:`NaturalNumberSequence` :math:`T` defined as
        :math:`(t_0 + n, t_1 + n, \cdots, t_i)`.

        :param n:
        :return:
        """
        t: tuple[int, ...] = tuple(x + n for x in self.elements)
        return NaturalNumber0Sequence(*t)


# Flexible types to facilitate data validation

FlexibleNaturalNumber0Sequence = typing.Union[
    NaturalNumber0Sequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases and well-known objects

NN0S = NaturalNumber0Sequence  # An alias for NaturalNumberSequence
trivial_sequence = NaturalNumber0Sequence()  # An alias for the empty sequence ().
empty_sequence = NaturalNumber0Sequence()  # The empty sequence ().
is_equal_to = IsEqualTo  # The is-equal-to binary relation.
refined_godel_number_order = RefinedGodelNumberOrder
lexicographic_order = LexicographicOrder
length_first_lexicographic_second_order = LengthFirstLexicographicSecondOrder
sum_first_lexicographic_second_order = SumFirstLexicographicSecondOrder
godel_number_order = GodelNumberEncodingOrder
combined_integer_with_sentinel_order = CombinedIntegerWithSentinelOrder
