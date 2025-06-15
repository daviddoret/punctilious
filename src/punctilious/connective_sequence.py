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

    def __init__(self, *s):
        super(ConnectiveSequence, self).__init__()

    def __new__(cls, *s):
        s: tuple[connective.Connective, ...] = data_validate_connective_sequence_elements(s)
        if len(s) < 1:
            raise util.PunctiliousException('The length of a ConnectiveSequence must be strictly greater than ')
        s: tuple[connective.Connective] = super(ConnectiveSequence, cls).__new__(cls, s)
        s: tuple[connective.Connective] = retrieve_connective_sequence_from_cache(s)
        return s

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)


FlexibleConnectiveSequence = typing.Union[
    ConnectiveSequence, tuple[connective.Connective, ...], collections.abc.Iterator, collections.abc.Generator, None]
