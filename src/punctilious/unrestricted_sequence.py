from __future__ import annotations
import itertools
import typing
import collections
import util


def data_validate_unrestricted_sequence(
        o: FlexibleUnrestrictedSequence) -> UnrestrictedSequence:
    """Data validates `o` against type `UnrestrictedSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a `UnrestrictedSequence`.
    :return:
    """
    if isinstance(o, UnrestrictedSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        return UnrestrictedSequence(*o)
    if isinstance(o, collections.abc.Generator):
        return UnrestrictedSequence(*o)
    raise util.PunctiliousException('UnrestrictedSequence data validation failure', o=o)


def data_validate_unrestricted_sequence_elements(
        o: FlexibleUnrestrictedSequence) -> FlexibleUnrestrictedSequence:
    if isinstance(o, UnrestrictedSequence):
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


_unrestricted_sequence_cache = dict()  # cache mechanism assuring that unique RGFS are only instantiated once.


def retrieve_unrestricted_sequence_from_cache(i: UnrestrictedSequence):
    """cache mechanism assuring that unique RGFS are only instantiated once."""
    global _unrestricted_sequence_cache
    if hash(i) in _unrestricted_sequence_cache.keys():
        return _unrestricted_sequence_cache[hash(i)]
    else:
        _unrestricted_sequence_cache[hash(i)] = i
        return i


class UnrestrictedSequence(tuple):
    """A finite (computable) and arbitrary sequence of natural numbers.

    Definition:
    An :class:`UnrestrictedSequence` is a finite sequence of natural numbers (n_0, n_1, ..., n_j) such that:
        - n_i >= 0 for 0 <= i <= j

    """

    def __add__(self, other):
        """Concatenates the current :class:`UnrestrictedSequence` with another one.

        Note:
            This enables the usage of the python sum function, e.g.: sum(s1, s2, ...).

        :param other:
        :return:
        """
        return concatenate_flexible_unrestricted_sequences(self, other)

    def __eq__(self, s):
        """Returns `False` if `s` cannot be interpreted as a :class:`UnrestrictedSequence`,
        returns `True` if `s` is connective-sequence-equivalent to this :class:`UnrestrictedSequence`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            s: UnrestrictedSequence = data_validate_unrestricted_sequence(s)
            return self.is_unrestricted_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((UnrestrictedSequence, *self.elements,))

    def __init__(self, *s):
        super(UnrestrictedSequence, self).__init__()

    def __ne__(self, s):
        """Returns `False` if `c` cannot be interpreted as a :class:`UnrestrictedSequence`,
        returns `True` if `c` is not connective-sequence-equivalent to this :class:`UnrestrictedSequence`,
        returns `False` otherwise.

         Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
       """
        try:
            s: UnrestrictedSequence = data_validate_unrestricted_sequence(s)
            return not self.is_unrestricted_sequence_equivalent_to(s)
        except util.PunctiliousException:
            return False

    def __new__(cls, *s):
        s: tuple[int] = data_validate_unrestricted_sequence_elements(s)
        s: tuple[int] = super(UnrestrictedSequence, cls).__new__(cls, s)
        s: tuple[int] = retrieve_unrestricted_sequence_from_cache(s)
        return s

    def concatenate_with(self, *s: FlexibleUnrestrictedSequence) -> UnrestrictedSequence:
        """Concatenates the current :class:`UnrestrictedSequence` with another one,
        or an iterable of multiple ones.

        Shortcuts:
        s1 + s2
        sum(s1, s2, ..., sn)

        :param s:
        :return:
        """
        return concatenate_flexible_unrestricted_sequences(self, *s)

    @property
    def elements(self) -> tuple[int, ...]:
        """The elements that compose this :class:`UnrestrictedSequence`, in order.

        :return:
        """
        return tuple(super().__iter__())

    def is_unrestricted_sequence_equivalent_to(self, s: FlexibleUnrestrictedSequence):
        """

        Formal definition:
        Two RGF-sequences s and t are RGF-sequence-equivalent if and only if:
         - length(s) = length(t)
         - s_i = t_i for 0 <= i < length(s)

        :param s:
        :return:
        """
        s: UnrestrictedSequence = data_validate_unrestricted_sequence(s)
        return self.length == s.length and all(x == y for x, y in zip(self, s))

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)

    @property
    def max_value(self) -> int:
        """The `max_value` of a `UnrestrictedSequence` is the maximum value of its elements."""
        return max(self)


def convert_arbitrary_sequence_to_unrestricted_sequence(s: tuple[int, ...]):
    """Convert any finite sequence into a `UnrestrictedSequence`,
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
    return UnrestrictedSequence(*s2)


def concatenate_flexible_unrestricted_sequences(*s: tuple[
    FlexibleUnrestrictedSequence, ...]) -> UnrestrictedSequence:
    """Concatenates :class:`UnrestrictedSequence` elements.

    :param s:
    :return:
    """
    t: tuple[FlexibleUnrestrictedSequence] = tuple(itertools.chain.from_iterable(s))
    return UnrestrictedSequence(*t)


FlexibleUnrestrictedSequence = typing.Union[
    UnrestrictedSequence, tuple[int, ...], collections.abc.Iterator, collections.abc.Generator, None]
