from __future__ import annotations
import itertools
import typing
import collections

# punctilious libraries
import punctilious.util as util
import punctilious.connective_library as cl


# Data validation functions


# General functions

def get_sequences_of_natural_numbers_whose_sum_equals_n(n):
    """Returns the all combinations of natural numbers such that their sum equals `n`.

    :param n:
    :return:
    """
    if n < 1:
        raise util.PunctiliousException("Invalid parameter", n=n)
    elif n == 1:
        yield (1,)
    else:
        for first_number in range(n, 0, -1):
            if first_number == n:
                yield (first_number,)
            else:
                for s in get_sequences_of_natural_numbers_whose_sum_equals_n(n - first_number):
                    yield (first_number,) + s


def concatenate_natural_number_sequences(*s: FlexibleNaturalNumberSequence) -> NaturalNumberSequence:
    """Concatenates a collection of :class:`NaturalNumberSequence` elements, preserving order.

    :param s:
    :return:
    """
    s: tuple[int] = tuple(itertools.chain.from_iterable(
        t for t in s))
    return NaturalNumberSequence(*s)


# Classes


class NaturalNumberSequence(tuple):
    """A non-empty, finite (computable) sequence of natural numbers (0 based).

    Definition:
    An :class:`NaturalNumberSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_j) such that:
        - n_i >= 0 for 0 <= i <= j

    """

    def __add__(self, s):
        """Concatenates this :class:`NaturalNumberSequence` with another :class:`NaturalNumberSequence` `s`.

        Note:
            This enables the usage of the python sum function, e.g.: sum(s1, s2, ...).

        :param s:
        :return:
        """
        if isinstance(s, int):
            return self.scalar_addition(n=s)
        elif isinstance(s, typing.Iterable):
            return concatenate_natural_number_sequences(self, s)
        else:
            raise util.PunctiliousException("Unsupported type.")

    def __eq__(self, s) -> bool:
        """Returns `True` if this natural-number-sequence is equal to natural-number-sequence `s`, `False` otherwise.

        See :attr:`NaturalNumberSequence.is_equal_to` for a definition of natural-number-sequence equality.

        :param s: A natural-number-sequence.
        :return: `True` if this natural-number-sequence is equal to natural-number-sequence `s`, `False` otherwise.
        """
        return self.is_equal_to(s)

    def __hash__(self):
        return hash((NaturalNumberSequence, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumberSequence, self).__init__()
        self._image: tuple[int, ...] | None = None
        self._is_restricted_growth_function_sequence: bool | None = None
        self._canonical_natural_number_sequence: NaturalNumberSequence | None = None

    def __lt__(self, s) -> bool:
        """Returns `True` if this natural-number-sequence is less than formula `s`, `False` otherwise.

        See :attr:`NaturalNumberSequence.is_less_than` for a definition of natural-number-sequence canonical-ordering.

        """
        return self.is_less_than(s)

    def __new__(cls, *s):
        v: bool
        s: tuple[int] | None
        r: bool
        v, s = cls.data_validate_elements(s, raise_exception_on_validation_failure=True)
        s: tuple[int] = super(NaturalNumberSequence, cls).__new__(cls, s)
        s: tuple[int] = cls._from_cache(s)
        return s

    _cache: dict[
        int, NaturalNumberSequence] = dict()  # cache for NaturalNumberSequence.

    _HASH_SEED: int = 7537674779484982803  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def _compute_hash(cls, o: FlexibleNaturalNumberSequence) -> int:
        """Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a natural-number-sequence.
        :return: The hash of the natural-number-sequence that is structurally equivalent to `o`.
        """
        return hash((NaturalNumberSequence, cls._HASH_SEED, o.elements,))

    @classmethod
    def _from_cache(cls, o: FlexibleNaturalNumberSequence):
        """Cache mechanism used in the constructor."""
        hash_value: int = NaturalNumberSequence._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    @property
    def canonical_natural_number_sequence(self) -> NaturalNumberSequence:
        """Convert the :class:`NaturalNumberSequence` `s` into a restricted-growth-function-sequence `t`,
        by applying canonical labeling.

        Notation:
        :math:`canonical(S)`

        Definition - Canonical Labeling:
        The canonical-labeling of a natural-numbers-sequence S is an RFG-sequence T such that:
         - the value of the first element of S is mapped to 0
         - whenever a new value x appears in S, it is mapped to max(t0, t1, ..., ti) + 1 where i is the index
           position of x in S

        Examples:
        (3,5,2,1) --> (0,1,2,3)
        (3,5,3,1,5,2) --> (0,1,0,2,1,3)

        :return:
        """
        if self.is_restricted_growth_function_sequence:
            return self
        elif self._canonical_natural_number_sequence is not None:
            return self._canonical_natural_number_sequence
        else:
            mapping: dict[int, int] = dict()
            mapped_value: int = 0
            n: int
            for n in self:
                if n not in mapping.keys():
                    mapping[n] = mapped_value
                    mapped_value += 1
            s: tuple[int, ...] = tuple(mapping[n] for n in self)
            self._canonical_natural_number_sequence = NaturalNumberSequence(*s)
            return self._canonical_natural_number_sequence

    def concatenate_with(self, *s: FlexibleNaturalNumberSequence) -> NaturalNumberSequence:
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
        return concatenate_natural_number_sequences(self, *s)

    @classmethod
    def data_validate_elements(
            cls,
            o: FlexibleNaturalNumberSequence, raise_exception_on_validation_failure: bool = True) -> \
            tuple[bool, FlexibleNaturalNumberSequence | None]:
        """Validates `o` as a collection of natural number elements,
        applying implicit conversion as necessary.

        :param o: An object that may be interpreted as a :class:`NaturalNumberSequence`.
        :param raise_exception_on_validation_failure: Raises an exception if data validation fails.
        :return: a tuple (v, s) where v is True if data validation was successful, False otherwise,
            and s is the resulting natural-number sequence, or None if data validation failed.
        """
        if isinstance(o, NaturalNumberSequence):
            # data validation is assured by the class logic.
            return True, o
        if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
            v: bool = True
            o = tuple(o)
            if len(o) == 0:
                if raise_exception_on_validation_failure:
                    raise util.PunctiliousException(
                        "`o` is empty.", o=o)
                else:
                    v = False
            o = tuple(int(n) for n in o)
            if any(n for n in o if n < 0):
                if raise_exception_on_validation_failure:
                    raise util.PunctiliousException(
                        "Some element of `o` is less than 0.", o=o)
                else:
                    v = False
            return v, o if v else None
        if raise_exception_on_validation_failure:
            raise util.PunctiliousException("The type of `o` is not supported.", o_type=type(o), o=o)
        else:
            return False, None

    @property
    def elements(self) -> tuple[int, ...]:
        """Returns a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.

        :return: a tuple of the elements that compose this :class:`NaturalNumberSequence`, preserving order.
        """
        return tuple(super().__iter__())

    @classmethod
    def from_any(cls, o: FlexibleNaturalNumberSequence) -> NaturalNumberSequence:
        """Declares a natural-number-sequence from a Python object that can be interpreted as a natural-number-sequence.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a natural-number-sequence.
        :return: a natural-number-sequence.
        """
        if isinstance(o, NaturalNumberSequence):
            return o
        if isinstance(o, collections.abc.Iterable):
            return NaturalNumberSequence(*o)
        if isinstance(o, collections.abc.Generator):
            return NaturalNumberSequence(*o)
        raise util.PunctiliousException('NaturalNumberSequence data validation failure', o=o)

    @property
    def im(self) -> tuple[int, ...]:
        """A shortcut for :attr:`NaturalNumberSequence.image`."""
        return self.image

    @property
    def image(self) -> tuple[int, ...]:
        """The :attr:`NaturalNumberSequence.image` is the set of values contained in the sequence,
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
        """The :attr:`NaturalNumberSequence.image_cardinality` is the cardinality
         of the :attr:`NaturalNumberSequence.image`, i.e. the number of distinct values it contains.

        Notation:
        :math:`|Im(S)|`

        :return:
        """
        return len(self.image)

    def is_canonical_natural_number_sequence_equivalent(self, s) -> bool:
        """`True` if this natural number sequence canonical-natural-number-sequence-equivalent
        to the natural-number-sequence `s`, `False` otherwise.

        Notation:
        :math:`S ~_{canonical} T`

        Formal Definition:
        Two natural-number-sequences `s` and `t` are canonical-natural-number-sequence-equivalent
        if and only if their canonical-natural-number-sequence are natural-number-sequence-equivalent.

        """
        s: NaturalNumberSequence = NaturalNumberSequence.from_any(s)
        return self.canonical_natural_number_sequence.is_natural_number_sequence_equivalent_to(s)

    def is_equal_to(self, s: FlexibleNaturalNumberSequence):
        """Under :class:`NaturalNumberSequence` canonical ordering,
        returns `True` if the current :class:`NaturalNumberSequence` is equal to `s`,
        `False` otherwise.

        See :attr:`NaturalNumberSequence.is_less_than` for a definition of natural-number-sequence canonical-ordering.

        :param s: A :class:`NaturalNumberSequence`.
        :return: `True` if the current :class:`NaturalNumberSequence` is equal to `s`, `False` otherwise.
        """
        s: NaturalNumberSequence = NaturalNumberSequence.from_any(s)
        return self.is_natural_number_sequence_equivalent_to(s)

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

    def is_less_than(self, s: FlexibleNaturalNumberSequence) -> bool:
        r"""Under :class:`NaturalNumberSequence` canonical ordering,
        returns `True` if the current :class:`NaturalNumberSequence` is less than `s`,
        `False` otherwise.

        Definition: canonical ordering of natural-number-sequence, denoted :math:`\prec`,
        is defined as length-first, ascending-order second.

        :param s: A :class:`NaturalNumberSequence`.
        :return: `True` if the current :class:`NaturalNumberSequence` is equal to `s`, `False` otherwise.
        """
        s: NaturalNumberSequence = NaturalNumberSequence.from_any(s)
        if self.is_natural_number_sequence_equivalent_to(s):
            return False
        elif self.length < s.length:
            return True
        elif self.length > s.length:
            return False
        else:
            for n, m in zip(self.elements, s.elements):
                if n < m:
                    return True
                if n > m:
                    return False
        raise util.PunctiliousException("Unreachable condition")

    @property
    def is_natural_number_sequence(self) -> bool:
        r"""

        Notation:
        :math:`\mathbb{N}\text{-sequence}(S)

        :return:
        """
        return True

    def is_natural_number_sequence_equivalent_to(self, s: FlexibleNaturalNumberSequence):
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
        s: NaturalNumberSequence = NaturalNumberSequence.from_any(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @property
    def is_restricted_growth_function_sequence(self) -> bool:
        """`True` if this natural numbers sequence is also an RGF sequence, `False` otherwise.

        Formal Definition:
        A restricted-growth-function-sequence is a finite (computable) sequence
        of natural numbers (n_0, n_1, ..., n_i) such that:
            - n_0 = 0
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
                if i == 0 and n > 0:
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
        return NaturalNumberSequence(*t)


class ConnectiveSequence(tuple):
    """A finite (computable) sequence of at least 1 connectives.

    """

    def __eq__(self, s) -> bool:
        """Returns `True` if this connective-sequence is equal to connective-sequence `s`, `False` otherwise.

        See :attr:`ConnectiveSequence.is_equal_to` for a definition of connective-sequence equality.

        :param s: A connective-sequence.
        :return: `True` if this connective-sequence is equal to connective-sequence `s`, `False` otherwise.
        """
        return self.is_equal_to(s)

    def __hash__(self):
        return self._compute_hash(self)

    def __init__(self, *s):
        super(ConnectiveSequence, self).__init__()

    def __lt__(self, s) -> bool:
        """Returns `True` if this connective-sequence is less than formula `s`, `False` otherwise.

        See :attr:`ConnectiveSequence.is_less_than` for a definition of connective-sequence canonical-ordering.

        """
        return self.is_less_than(s)

    def __new__(cls, *s):
        v: bool
        s: tuple[cl.Connective, ...]
        v, s = cls.data_validate_elements(s)
        if len(s) < 1:
            raise util.PunctiliousException('The length of a ConnectiveSequence must be strictly greater than ')
        s: tuple[cl.Connective] = super(ConnectiveSequence, cls).__new__(cls, s)
        s: tuple[cl.Connective] = cls._from_cache(s)
        return s

    _cache: dict[
        int, ConnectiveSequence] = dict()  # cache for ConnectiveSequence.

    _HASH_SEED: int = 642062802475784292  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def _compute_hash(cls, o: FlexibleConnectiveSequence) -> int:
        """Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a natural-number-sequence.
        :return: The hash of the natural-number-sequence that is structurally equivalent to `o`.
        """
        return hash((ConnectiveSequence, cls._HASH_SEED, o.elements,))

    @classmethod
    def _from_cache(cls, o: FlexibleConnectiveSequence):
        """Cache mechanism used in the constructor."""
        hash_value: int = ConnectiveSequence._compute_hash(o)
        if hash_value in cls._cache.keys():
            return cls._cache[hash_value]
        else:
            cls._cache[hash_value] = o
            return o

    @classmethod
    def data_validate_elements(
            cls,
            o: FlexibleConnectiveSequence, raise_exception_on_validation_failure: bool = True) -> \
            tuple[bool, tuple[cl.Connective, ...] | None]:
        """Validates `o` as a collection of connective elements,
        applying implicit conversion as necessary.

        :param o: An collection of elements that may be interpreted as :class:`Connective`.
        :param raise_exception_on_validation_failure: Raises an exception if data validation fails.
        :return: a tuple (v, s) where v is True if data validation was successful, False otherwise,
            and s is a data-validated sequence of connective elements, or None if data validation failed.
        """
        if isinstance(o, ConnectiveSequence):
            # data validation is assured by the class logic.
            return True, o
        if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
            v: bool = True
            o = tuple(o)
            if len(o) == 0:
                if raise_exception_on_validation_failure:
                    raise util.PunctiliousException(
                        "`o` is empty.", o=o)
                else:
                    v = False
            c: cl.FlexibleConnective
            l: list[cl.Connective] = list()
            for c in o:
                try:
                    c: cl.Connective = cl.Connective.from_any(c)
                except util.PunctiliousException:
                    if raise_exception_on_validation_failure:
                        raise util.PunctiliousException(
                            "Some element `c` of `o` is not interpretable as a connective.", c=c, o=o)
                    else:
                        v = False
            return v, o if v else None
        if raise_exception_on_validation_failure:
            raise util.PunctiliousException("The type of `o` is not supported.", o_type=type(o), o=o)
        else:
            return False, None

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this `ConnectiveSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

    @classmethod
    def from_any(cls, o: FlexibleConnectiveSequence) -> ConnectiveSequence:
        """Declares a connective-sequence from a Python object that can be interpreted as a connective-sequence.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a connective-sequence.
        :return: a connective-sequence.
        """
        if isinstance(o, ConnectiveSequence):
            return o
        if isinstance(o, collections.abc.Iterable):
            return ConnectiveSequence(*o)
        if isinstance(o, collections.abc.Generator):
            return ConnectiveSequence(*o)
        raise util.PunctiliousException('Connective-sequence data validation failure', o=o)

    def is_connective_sequence_equivalent_to(self, s: FlexibleConnectiveSequence):
        """Returns `True` if this :class:`ConnectiveSequence` is connective-sequence-equivalent
        to :class:`ConnectiveSequence` `s`.

        Formal definition:
        A connective-sequence `s` is connective-sequence-equivalent to a connective-sequence `t` if and only if
         - the length of `t` = the length of `d`,
         - s_i is connective-equivalent to d_i for all i from 0 to length(`t`) - 1.

        :param s:
        :return:
        """
        s: ConnectiveSequence = ConnectiveSequence.from_any(s)
        return all(i == j for i, j in zip(self, s))

    def is_equal_to(self, c: FlexibleConnectiveSequence):
        """Under :class:`ConnectiveSequence` canonical ordering,
        returns `True` if the current :class:`ConnectiveSequence` is equal to `c`,
        `False` otherwise.

        See :attr:`ConnectiveSequence.is_less_than` for a definition of connective-sequence canonical-ordering.

        :param c: A :class:`ConnectiveSequence`.
        :return: `True` if the current :class:`ConnectiveSequence` is equal to `c`, `False` otherwise.
        """
        c: ConnectiveSequence = ConnectiveSequence.from_any(c)
        return self.is_connective_sequence_equivalent_to(c)

    def is_less_than(self, c: FlexibleConnectiveSequence) -> bool:
        r"""Under :class:`ConnectiveSequence` canonical ordering,
        returns `True` if the current :class:`ConnectiveSequence` is less than `c`,
        `False` otherwise.

        Definition: canonical ordering of natural-number-sequence, denoted :math:`\prec`,
        is defined as length-first, ascending-order second.

        Note:
        The canonical ordering of connective-sequence being dependent on the connectives UUIDs,
        the resulting ordering may appear random to the human reader.

        :param c: A :class:`ConnectiveSequence`.
        :return: `True` if the current :class:`ConnectiveSequence` is equal to `c`, `False` otherwise.
        """
        c: ConnectiveSequence = ConnectiveSequence.from_any(c)
        if self.is_connective_sequence_equivalent_to(c):
            return False
        elif self.length < c.length:
            return True
        elif self.length > c.length:
            return False
        else:
            for n, m in zip(self.elements, c.elements):
                if n < m:
                    return True
                if n > m:
                    return False
        raise util.PunctiliousException("Unreachable condition")

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)


# Flexible types to facilitate data validation

FlexibleConnectiveSequence = typing.Union[
    ConnectiveSequence, tuple[cl.Connective, ...], collections.abc.Iterator, collections.abc.Generator, None]
FlexibleNaturalNumberSequence = typing.Union[
    NaturalNumberSequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

CS = ConnectiveSequence  # An alias for ConnectiveSequence.
NNS = NaturalNumberSequence  # An alias for NaturalNumberSequence
