from __future__ import annotations

import connector
import typing
import collections
import util


def data_validate_connector_sequence(
        o: FlexibleConnectorSequence) -> ConnectorSequence:
    """Data validates `o` against type `ConnectorSequence`,
    applying implicit conversion as necessary.

    :param o: An object that may be interpreted as a `ConnectorSequence`.
    :return:
    """
    if isinstance(o, ConnectorSequence):
        return o
    if isinstance(o, collections.abc.Iterable):
        return ConnectorSequence(*o)
    if isinstance(o, collections.abc.Generator):
        return ConnectorSequence(*o)
    raise util.PunctiliousException('ConnectorSequence data validation failure', o=o)


def data_validate_connector_sequence_elements(
        o: FlexibleConnectorSequence) -> FlexibleConnectorSequence:
    if isinstance(o, ConnectorSequence):
        # data validation is assured by the class logic.
        return o
    if isinstance(o, collections.abc.Iterable) or isinstance(o, collections.abc.Generator):
        o = tuple(o)
        o: tuple[connector.Connector, ...] = tuple(connector.data_validate_connector(n) for n in o)
        return o
    raise util.PunctiliousException('ConnectorSequence elements data validation failure', o=o)


_connector_sequence_cache: dict[
    int, ConnectorSequence] = {}  # cache mechanism assuring that unique rpts are only instantiated once.


def retrieve_connector_sequence_from_cache(i: ConnectorSequence):
    """cache mechanism assuring that unique connector sequences are only instantiated once."""
    global _connector_sequence_cache
    if hash(i) in _connector_sequence_cache.keys():
        return _connector_sequence_cache[hash(i)]
    else:
        _connector_sequence_cache[hash(i)] = i
        return i


class ConnectorSequence(tuple):
    """A finite (computable) sequence of at least 1 connectors.

    """

    def __init__(self, *s):
        super(ConnectorSequence, self).__init__()

    def __new__(cls, *s):
        s: tuple[connector.Connector, ...] = data_validate_connector_sequence_elements(s)
        if len(s) < 1:
            raise util.PunctiliousException('The length of a ConnectorSequence must be strictly greater than ')
        s: tuple[connector.Connector] = super(ConnectorSequence, cls).__new__(cls, s)
        s: tuple[connector.Connector] = retrieve_connector_sequence_from_cache(s)
        return s

    @property
    def length(self) -> int:
        """The `length` of a finite sequence is the number of elements in the sequence."""
        return len(self)


FlexibleConnectorSequence = typing.Union[
    ConnectorSequence, tuple[connector.Connector, ...], collections.abc.Iterator, collections.abc.Generator, None]
