from __future__ import annotations

import connective
import typing
import collections
import util


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


_connective_sequence_cache: dict[
    int, ConnectiveSequence] = {}  # cache mechanism assuring that unique rpts are only instantiated once.


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

    def __hash__(self):
        return hash((ConnectiveSequence, *self,))

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


FlexibleConnectiveSequence = typing.Union[
    ConnectiveSequence, tuple[connective.Connective, ...], collections.abc.Iterator, collections.abc.Generator, None]
