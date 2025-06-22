from __future__ import annotations
import itertools
import typing
import collections
import util


def data_validate_restricted_growth_function_sequence(
        o: FlexibleRestrictedGrowthFunctionSequence) -> RestrictedGrowthFunctionSequence:
    """Data validates `o` against type `RestrictedGrowthFunctionSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a `RestrictedGrowthFunctionSequence`.
    :return:
    """
    if isinstance(o, RestrictedGrowthFunctionSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        return RestrictedGrowthFunctionSequence(*o)
    if isinstance(o, collections.abc.Generator):
        return RestrictedGrowthFunctionSequence(*o)
    raise util.PunctiliousException('RestrictedGrowthFunctionSequence data validation failure', o=o)


def data_validate_restricted_growth_function_sequence_elements(
        o: FlexibleRestrictedGrowthFunctionSequence) -> FlexibleRestrictedGrowthFunctionSequence:
    if isinstance(o, RestrictedGrowthFunctionSequence):
        # data validation is assured by the class logic.
        return o
    if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o = tuple(int(n) for n in o)
        if o[0] != 0:
            raise util.PunctiliousException("The first element `x` of the RGF sequence `s` is not equal to 0.",
                                            x=o[0], s=o)
        for i, n in enumerate(o):
            if i > 0 and n > max(o[0:i]) + 1:
                raise util.PunctiliousException(
                    "The i-th element `n` of the RGF sequence `s` is greater than max(s[0:i]) + 1.",
                    i=i, n=n, s=o)
        return o
    raise util.PunctiliousException("Non-supported input.", o=o)


_restricted_growth_function_sequence_cache = dict()  # cache mechanism assuring that unique RGFS are only instantiated once.


def retrieve_restricted_growth_function_sequence_from_cache(i: RestrictedGrowthFunctionSequence):
    """cache mechanism assuring that unique RGFS are only instantiated once."""
    global _restricted_growth_function_sequence_cache
    if hash(i) in _restricted_growth_function_sequence_cache.keys():
        return _restricted_growth_function_sequence_cache[hash(i)]
    else:
        _restricted_growth_function_sequence_cache[hash(i)] = i
        return i


class RestrictedGrowthFunctionSequence(tuple):
    """A finite (computable) sequence of values starting at 0 whose maximal value increase is restricted.

    Acronym: RGFS

    Formal Definition:
    A :class:`RestrictedGrowthFunctionSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_i) such that:
        - n_0 = 0
        - with j > 0, n_j <= 1 + max(n_0, n_1, ..., n_(j-1))

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
            s: RestrictedGrowthFunctionSequence = data_validate_restricted_growth_function_sequence(s)
            return not self.is_restricted_growth_function_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        s: tuple[int] = data_validate_restricted_growth_function_sequence_elements(s)
        s: tuple[int] = super(RestrictedGrowthFunctionSequence, cls).__new__(cls, s)
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
        """The `max_value` of a `RestrictedGrowthFunctionSequence` is the maximum value of its elements."""
        return max(self)


def convert_arbitrary_sequence_to_restricted_growth_function_sequence(s: tuple[int, ...]):
    """Convert any finite sequence into a `RestrictedGrowthFunctionSequence`,
    by substituting natural numbers based on their order of appearance in the sequence.

    Examples:
    (3,5,2,1) --> (1,2,3,4)
    (3,5,3,1,5,2) --> (1,2,1,3,2,4)


    :param s:
    :return:
    """
    mapping = dict()
    mapped_value = 0
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


FlexibleRestrictedGrowthFunctionSequence = typing.Union[
    RestrictedGrowthFunctionSequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]
