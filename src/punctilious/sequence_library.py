from __future__ import annotations
import itertools
import typing
import collections
import util

# punctilious libraries
import connective_library as cl


# Data validation functions


def data_validate_natural_number_sequence(
        o: FlexibleNaturalNumberSequence) -> NaturalNumberSequence:
    """Data validates `o` against type :class:`NaturalNumberSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a :class:`NaturalNumberSequence`.
    :return:
    """
    if isinstance(o, NaturalNumberSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        # This raises an exception if the sequence is not an RGF-sequence.
        return NaturalNumberSequence(*o)
    if isinstance(o, collections.abc.Generator):
        # This raises an exception if the sequence is not an RGF-sequence.
        return NaturalNumberSequence(*o)
    raise util.PunctiliousException('NaturalNumberSequence data validation failure', o=o)


def data_validate_natural_number_sequence_elements(
        o: FlexibleNaturalNumberSequence, raise_exception_on_validation_failure: bool = True) -> tuple[
    bool, FlexibleNaturalNumberSequence | None]:
    """Validates `o` against type :class:`NaturalNumberSequence`,
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


def data_validate_connective_sequence(
        o: FlexibleConnectiveSequence) -> ConnectiveSequence:
    """Data validates `o` against type `ConnectiveSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a `ConnectiveSequence`.
    :return:
    """
    if isinstance(o, ConnectiveSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        return ConnectiveSequence(*o)
    if isinstance(o, collections.abc.Generator):
        return ConnectiveSequence(*o)
    raise util.PunctiliousException('ConnectiveSequence data validation failure', o=o)


def data_validate_connective_sequence_elements(
        o: FlexibleConnectiveSequence) -> FlexibleConnectiveSequence:
    if isinstance(o, ConnectiveSequence):
        # data validation is assured by the class logic.
        return o
    if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o: tuple[cl.Connective, ...] = tuple(cl.data_validate_connective(n) for n in o)
        return o
    raise util.PunctiliousException('ConnectiveSequence elements data validation failure', o=o)


# General functions

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
        return concatenate_natural_number_sequences(self, s)

    def __eq__(self, s):
        """Returns `False` if `s` cannot be interpreted as a :class:`NaturalNumberSequence`,
        returns `True` if `s` is connective-sequence-equivalent to this :class:`NaturalNumberSequence`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            s: NaturalNumberSequence = data_validate_natural_number_sequence(s)
            return self.is_natural_number_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((NaturalNumberSequence, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumberSequence, self).__init__()
        self._image: tuple[int, ...] | None = None
        self._is_restricted_growth_function_sequence: bool | None = None
        self._canonical_natural_number_sequence: NaturalNumberSequence | None = None

    def __ne__(self, s):
        """Returns `False` if `c` cannot be interpreted as a :class:`NaturalNumberSequence`,
        returns `True` if `c` is not connective-sequence-equivalent to this :class:`NaturalNumberSequence`,
        returns `False` otherwise.

         Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
       """
        try:
            s: NaturalNumberSequence = data_validate_natural_number_sequence(s)
            return not self.is_natural_number_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        v: bool
        s: tuple[int] | None
        r: bool
        v, s = data_validate_natural_number_sequence_elements(s, raise_exception_on_validation_failure=True)
        s: tuple[int] = super(NaturalNumberSequence, cls).__new__(cls, s)
        s: tuple[int] = retrieve_natural_numbers_sequence_from_cache(s)
        return s

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
        """Concatenates this :class:`NaturalNumberSequence` with :class:`NaturalNumberSequence` `s`,
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

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this :class:`NaturalNumberSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

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
        s: NaturalNumberSequence = data_validate_natural_number_sequence(s)
        return self.canonical_natural_number_sequence.is_natural_number_sequence_equivalent_to(s)

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
                if i > 0 and n > max(self[0:i]) + 1:
                    self._is_restricted_growth_function_sequence: bool = False
                    return self._is_restricted_growth_function_sequence
            self._is_restricted_growth_function_sequence: bool = True
            return self._is_restricted_growth_function_sequence

    @property
    def is_natural_number_sequence(self) -> bool:
        """

        Notation:
        :math:`\mathbb{N}\text{-sequence}(S)

        :return:
        """
        return True

    def is_natural_number_sequence_equivalent_to(self, s: FlexibleNaturalNumberSequence):
        """

        Notation:
        :math:`S ~_{\mathbb{N}\text{-sequence}} T`

        Formal definition:
        Two natural numbers-sequences s and t are natural-numbers-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: NaturalNumberSequence = data_validate_natural_number_sequence(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

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
        """Given a :class:`NaturalNumberSequence` :math:`S`,
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

    def __eq__(self, s):
        """Returns `False` if `s` cannot be interpreted as a :class:`ConnectiveSequence`,
        returns `True` if `s` is connective-sequence-equivalent to this :class:`ConnectiveSequence`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            s: ConnectiveSequence = data_validate_connective_sequence(s)
            return self.is_connective_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((ConnectiveSequence, *self.elements,))

    def __init__(self, *s):
        super(ConnectiveSequence, self).__init__()

    def __ne__(self, s):
        """Returns `False` if `c` cannot be interpreted as a :class:`ConnectiveSequence`,
        returns `True` if `c` is not connective-sequence-equivalent to this :class:`ConnectiveSequence`,
        returns `False` otherwise.

         Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
       """
        try:
            s: ConnectiveSequence = data_validate_connective_sequence(s)
            return not self.is_connective_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        s: tuple[cl.Connective, ...] = data_validate_connective_sequence_elements(s)
        if len(s) < 1:
            raise util.PunctiliousException('The length of a ConnectiveSequence must be strictly greater than ')
        s: tuple[cl.Connective] = super(ConnectiveSequence, cls).__new__(cls, s)
        s: tuple[cl.Connective] = retrieve_connective_sequence_from_cache(s)
        return s

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this `ConnectiveSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

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
        s: ConnectiveSequence = data_validate_connective_sequence(s)
        return all(i == j for i, j in zip(self, s))

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
US = NaturalNumberSequence  # An alias for NaturalNumberSequence

# Cache management

_connective_sequence_cache: dict[
    int, ConnectiveSequence] = {}  # cache for ConnectiveSequence elements.
_natural_numbers_sequence_cache: dict[
    int, NaturalNumberSequence] = dict()  # cache for NaturalNumberSequence.


def retrieve_natural_numbers_sequence_from_cache(i: NaturalNumberSequence):
    """cache mechanism assuring that unique natural-numbers-sequences are only instantiated once."""
    global _natural_numbers_sequence_cache
    if hash(i) in _natural_numbers_sequence_cache.keys():
        return _natural_numbers_sequence_cache[hash(i)]
    else:
        _natural_numbers_sequence_cache[hash(i)] = i
        return i


def retrieve_connective_sequence_from_cache(i: ConnectiveSequence):
    """cache mechanism assuring that unique connective sequences are only instantiated once."""
    global _connective_sequence_cache
    if hash(i) in _connective_sequence_cache.keys():
        return _connective_sequence_cache[hash(i)]
    else:
        _connective_sequence_cache[hash(i)] = i
        return i
