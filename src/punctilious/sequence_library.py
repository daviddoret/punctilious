from __future__ import annotations
import itertools
import typing
import collections
import util

# punctilious libraries
import connective


# Data validation functions

def data_validate_restricted_growth_function_sequence(
        o: FlexibleRestrictedGrowthFunctionSequence) -> RestrictedGrowthFunctionSequence:
    """Data validates `o` against type `RestrictedGrowthFunctionSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a `RestrictedGrowthFunctionSequence`.
    :return:
    """
    if isinstance(o, RestrictedGrowthFunctionSequence):
        return o
    if isinstance(o, NaturalNumberSequence):
        # Raises an exception if this is not an RGF-sequence
        return RestrictedGrowthFunctionSequence(*o)
    if isinstance(o, collections.abc.Iterable):
        # Raises an exception if this is not an RGF-sequence
        return RestrictedGrowthFunctionSequence(*o)
    if isinstance(o, collections.abc.Generator):
        # Raises an exception if this is not an RGF-sequence
        return RestrictedGrowthFunctionSequence(*o)
    raise util.PunctiliousException('RestrictedGrowthFunctionSequence data validation failure', o=o)


def data_validate_restricted_growth_function_sequence_elements(
        o: FlexibleRestrictedGrowthFunctionSequence,
        raise_exception: bool = True) -> tuple[bool, FlexibleRestrictedGrowthFunctionSequence]:
    """Coerces `o` :class:`RestrictedGrowthFunctionSequence` type.

    :param o:
    :param raise_exception: Whether an exception is raised if coercion is fails.
    :return: a tuple (b, o) where `b == True` if coercion was successful and `o` is the coerced object, `False` and `None` otherwise.
    """
    if isinstance(o, RestrictedGrowthFunctionSequence):
        # data validation is assured by the class logic.
        return True, o
    elif isinstance(o, NaturalNumberSequence):
        try:
            # Raise an exception if the sequence is not an RGF-sequence
            o: RestrictedGrowthFunctionSequence = RestrictedGrowthFunctionSequence(*o)
            return True, o
        except util.PunctiliousException:
            return False, o
    elif isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o = tuple(int(n) for n in o)
        if o[0] != 0:
            if raise_exception:
                raise util.PunctiliousException("The first element `x` of the RGF sequence `s` is not equal to 0.",
                                                x=o[0], s=o)
            else:
                return False, None
        for i, n in enumerate(o):
            if i < 0:
                if raise_exception:
                    raise util.PunctiliousException(
                        "The i-th element `n` of the natural numbers sequence `s` is less than 0.",
                        i=i, n=n, s=o)
                else:
                    return False, None
            if i > 0 and n > max(o[0:i]) + 1:
                if raise_exception:
                    raise util.PunctiliousException(
                        "The i-th element `n` of the RGF sequence `s` is greater than max(s[0:i]) + 1.",
                        i=i, n=n, s=o)
                else:
                    return False, None
        return True, o
    if raise_exception:
        raise util.PunctiliousException("Non-supported input.", o=o)
    else:
        return False, None


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
        return concatenate_flexible_natural_numbers_sequences(self, s)

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
            s: NaturalNumberSequence = data_validate_natural_numbers_sequence(s)
            return self.is_natural_numbers_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((NaturalNumberSequence, *self.elements,))

    def __init__(self, *s):
        super(NaturalNumberSequence, self).__init__()

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
            s: NaturalNumberSequence = data_validate_natural_numbers_sequence(s)
            return not self.is_natural_numbers_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        s: tuple[int] = data_validate_natural_numbers_sequence_elements(s)
        s: tuple[int] = super(NaturalNumberSequence, cls).__new__(cls, s)
        s: tuple[int] = retrieve_natural_numbers_sequence_from_cache(s)
        return s

    def concatenate_with(self, *s: FlexibleNaturalNumbersSequence) -> NaturalNumberSequence:
        """Concatenates this :class:`NaturalNumberSequence` with :class:`NaturalNumberSequence` `s`,
        or an iterable / generator of multiple :class:`NaturalNumberSequence` elements.

        Shortcuts:
        s1 + s2
        sum(s1, s2, ..., sn)

        :param s:
        :return:
        """
        return concatenate_flexible_natural_numbers_sequences(self, *s)

    def convert_to_restricted_growth_function_sequence(self):
        """Converts this :class:`NaturalNumberSequence` object to type :class:`RestrictedGrowthFunctionSequence`,
        or raise an exception if the sequence is not an RGF sequence.

        :return:
        """
        return RestrictedGrowthFunctionSequence(*self)

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this :class:`NaturalNumberSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

    @property
    def is_restricted_growth_function_sequence(self) -> bool:
        """`True` if this natural numbers sequence is also an RGF sequence, `False` otherwise.
        """
        b: bool
        b, _ = data_validate_restricted_growth_function_sequence_elements(self)
        return b

    @property
    def is_natural_numbers_sequence(self) -> bool:
        return True

    def is_natural_numbers_sequence_equivalent_to(self, s: FlexibleNaturalNumbersSequence):
        """

        Formal definition:
        Two natural numbers-sequences s and t are natural-numbers-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: NaturalNumberSequence = data_validate_natural_numbers_sequence(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)

    @property
    def max_value(self) -> int:
        """The `max_value` of a `NaturalNumberSequence` is the maximum value of its elements."""
        return max(self)


class RestrictedGrowthFunctionSequence(NaturalNumberSequence):
    """A finite (computable) sequence of values starting at 0 whose maximal value increase is restricted.

    Acronym: RGFS

    Formal Definition:
    A :class:`RestrictedGrowthFunctionSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_i) such that:
        - n_0 = 0
        - n_j <= 1 + max(n_0, n_1, ..., n_(j-1)) for 0 < j <= i

    Note:
    Often RGF sequences have an initial value of 1 in the literature. We choose 0 here for consistency
    with the design choice of using 0-based indexes as the default indexing. In practice, 0-based indexes
    were a natural choice for Python implementation.


    """

    def __add__(self, other):
        """Concatenates the current :class:`RestrictedGrowthFunctionSequence` with another one.

        Note:
            This enables the usage of the python sum function, e.g.: sum(s1, s2, ...).

        :param other:
        :return:
        """
        return concatenate_flexible_restricted_growth_function_sequences(self, other)

    def __eq__(self, s):
        """Returns `False` if `s` cannot be interpreted as a :class:`RestrictedGrowthFunctionSequence`,
        returns `True` if `s` is connective-sequence-equivalent to this :class:`RestrictedGrowthFunctionSequence`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            s: RestrictedGrowthFunctionSequence = data_validate_restricted_growth_function_sequence(s)
            return self.is_restricted_growth_function_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((RestrictedGrowthFunctionSequence, *self.elements,))

    def __init__(self, *s):
        super(RestrictedGrowthFunctionSequence, self).__init__()

    def __ne__(self, s):
        """Returns `False` if `c` cannot be interpreted as a :class:`RestrictedGrowthFunctionSequence`,
        returns `True` if `c` is not connective-sequence-equivalent to this :class:`RestrictedGrowthFunctionSequence`,
        returns `False` otherwise.

         Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
       """
        try:
            b: bool
            s: RestrictedGrowthFunctionSequence = data_validate_restricted_growth_function_sequence(s)
            return not self.is_restricted_growth_function_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        b: bool
        s: tuple[int]
        b, s = data_validate_restricted_growth_function_sequence_elements(s, raise_exception=True)
        s: tuple[int] = super(RestrictedGrowthFunctionSequence, cls).__new__(cls, *s)
        s: tuple[int] = retrieve_restricted_growth_function_sequence_from_cache(s)
        return s

    def concatenate_with(self, *s: FlexibleRestrictedGrowthFunctionSequence) -> RestrictedGrowthFunctionSequence:
        """Concatenates the current :class:`RestrictedGrowthFunctionSequence` with another one,
        or an iterable of multiple ones.

        Shortcuts:
        s1 + s2
        sum(s1, s2, ..., sn)

        :param s:
        :return:
        """
        return concatenate_flexible_restricted_growth_function_sequences(self, *s)

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this :class:`RestrictedGrowthFunctionSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

    @property
    def is_restricted_growth_function_sequence(self) -> bool:
        return True

    @property
    def is_natural_numbers_sequence(self) -> bool:
        return True

    def is_restricted_growth_function_sequence_equivalent_to(self, s: FlexibleRestrictedGrowthFunctionSequence):
        """

        Formal definition:
        Two RGF-sequences s and t are RGF-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: RestrictedGrowthFunctionSequence = data_validate_restricted_growth_function_sequence(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)

    @property
    def max_value(self) -> int:
        """The `max_value` of a :class:`RestrictedGrowthFunctionSequence` is the maximum value of its elements."""
        return max(self)

    def convert_to_natural_numbers_sequence(self):
        """Converts this :class:`RestrictedGrowthFunctionSequence` object to an :class:`NaturalNumberSequence`.

        :return:
        """
        return NaturalNumberSequence(*self)


def apply_canonical_labeling(s: NaturalNumberSequence) -> RestrictedGrowthFunctionSequence:
    """Convert the :class:`NaturalNumberSequence` `s` into a :class:`RestrictedGrowthFunctionSequence` `t`,
    by applying canonical labeling.

    Definition - Canonical Labeling:
    The canonical-labeling of an natural-numbers-sequence S is an RFG-sequence T such that:
     - the value of the first element of S is mapped to 0
     - whenever a new value x appears in S, it is mapped to max(t0, t1, ..., ti) + 1 where i is the index
       position of x in S

    Examples:
    (3,5,2,1) --> (0,1,2,3)
    (3,5,3,1,5,2) --> (0,1,0,2,1,3)


    :param s:
    :return: A canonical-labeling of `s`
    """
    mapping: dict[int, int] = dict()
    mapped_value: int = 0
    n: int
    for n in s:
        if n not in mapping.keys():
            mapping[n] = mapped_value
            mapped_value += 1
    s2 = tuple(mapping[n] for n in s)
    return RestrictedGrowthFunctionSequence(*s2)


def concatenate_flexible_restricted_growth_function_sequences(*s: tuple[
    FlexibleRestrictedGrowthFunctionSequence, ...]) -> RestrictedGrowthFunctionSequence:
    """Concatenates :class:`RestrictedGrowthFunctionSequence` elements.

    :param s:
    :return:
    """
    t: tuple[FlexibleRestrictedGrowthFunctionSequence] = tuple(itertools.chain.from_iterable(s))
    return RestrictedGrowthFunctionSequence(*t)


def data_validate_natural_numbers_sequence(
        o: FlexibleNaturalNumbersSequence) -> NaturalNumberSequence:
    """Data validates `o` against type :class:`NaturalNumberSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a :class:`NaturalNumberSequence`.
    :return:
    """
    if isinstance(o, NaturalNumberSequence):
        return o
    if isinstance(o, RestrictedGrowthFunctionSequence):
        # This raises an exception if the sequence is not an RGF-sequence.
        return NaturalNumberSequence(*o)
    if isinstance(o, collections.abc.Iterable):
        # This raises an exception if the sequence is not an RGF-sequence.
        return NaturalNumberSequence(*o)
    if isinstance(o, collections.abc.Generator):
        # This raises an exception if the sequence is not an RGF-sequence.
        return NaturalNumberSequence(*o)
    raise util.PunctiliousException('NaturalNumberSequence data validation failure', o=o)


def data_validate_natural_numbers_sequence_elements(
        o: FlexibleNaturalNumbersSequence) -> FlexibleNaturalNumbersSequence:
    if isinstance(o, NaturalNumberSequence):
        # data validation is assured by the class logic.
        return o
    if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o = tuple(int(n) for n in o)
        for i, n in enumerate(o):
            if i < 0:
                raise util.PunctiliousException(
                    "The i-th element `n` of the natural numbers sequence `s` is less than 0.",
                    i=i, n=n, s=o)
        return o
    raise util.PunctiliousException("Non-supported input.", o=o)


def retrieve_natural_numbers_sequence_from_cache(i: NaturalNumberSequence):
    """cache mechanism assuring that unique natural-numbers-sequences are only instantiated once."""
    global _natural_numbers_sequence_cache
    if hash(i) in _natural_numbers_sequence_cache.keys():
        return _natural_numbers_sequence_cache[hash(i)]
    else:
        _natural_numbers_sequence_cache[hash(i)] = i
        return i


def concatenate_flexible_natural_numbers_sequences(*s: tuple[
    FlexibleNaturalNumbersSequence, ...]) -> NaturalNumberSequence:
    """Concatenates :class:`NaturalNumberSequence` elements.

    :param s:
    :return:
    """
    t: tuple[FlexibleNaturalNumbersSequence] = tuple(itertools.chain.from_iterable(s))
    return NaturalNumberSequence(*t)


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
        o: tuple[connective.Connective, ...] = tuple(connective.data_validate_connective(n) for n in o)
        return o
    raise util.PunctiliousException('ConnectiveSequence elements data validation failure', o=o)


def retrieve_connective_sequence_from_cache(i: ConnectiveSequence):
    """cache mechanism assuring that unique connective sequences are only instantiated once."""
    global _connective_sequence_cache
    if hash(i) in _connective_sequence_cache.keys():
        return _connective_sequence_cache[hash(i)]
    else:
        _connective_sequence_cache[hash(i)] = i
        return i


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
        s: tuple[connective.Connective, ...] = data_validate_connective_sequence_elements(s)
        if len(s) < 1:
            raise util.PunctiliousException('The length of a ConnectiveSequence must be strictly greater than ')
        s: tuple[connective.Connective] = super(ConnectiveSequence, cls).__new__(cls, s)
        s: tuple[connective.Connective] = retrieve_connective_sequence_from_cache(s)
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
    ConnectiveSequence, tuple[connective.Connective, ...], collections.abc.Iterator, collections.abc.Generator, None]
FlexibleRestrictedGrowthFunctionSequence = typing.Union[
    RestrictedGrowthFunctionSequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]
FlexibleNaturalNumbersSequence = typing.Union[
    NaturalNumberSequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]

# Aliases

CS = ConnectiveSequence  # An alias for ConnectiveSequence.
RGFS = RestrictedGrowthFunctionSequence  # An alias for RestrictedGrowthFunctionSequence
US = NaturalNumberSequence  # An alias for NaturalNumberSequence

# Cache management

_connective_sequence_cache: dict[
    int, ConnectiveSequence] = {}  # cache for ConnectiveSequence elements.
_restricted_growth_function_sequence_cache: dict[
    int, RestrictedGrowthFunctionSequence] = dict()  # cache for RestrictedGrowthFunctionSequence elements.
_natural_numbers_sequence_cache: dict[
    int, NaturalNumberSequence] = dict()  # cache for NaturalNumberSequence.


def retrieve_restricted_growth_function_sequence_from_cache(i: RestrictedGrowthFunctionSequence):
    """cache mechanism assuring that unique RGFS are only instantiated once."""
    global _restricted_growth_function_sequence_cache
    if hash(i) in _restricted_growth_function_sequence_cache.keys():
        return _restricted_growth_function_sequence_cache[hash(i)]
    else:
        _restricted_growth_function_sequence_cache[hash(i)] = i
        return i
