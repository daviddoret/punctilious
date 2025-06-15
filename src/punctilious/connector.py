from __future__ import annotations
import typing
import collections
import uuid

# package modules
import util

_connector_cache: dict[uuid.UUID, Connector] = {}  # cache mechanism assuring connectors unicity


def data_validate_connector(
        o: FlexibleConnector) -> Connector:
    if isinstance(o, Connector):
        return o
    if isinstance(o, uuid.UUID):
        return Connector(uid=o)
    raise util.PunctiliousException('Connector data validation failure', o=o)


def retrieve_connector_from_cache(uid: uuid.UUID) -> Connector | None:
    """cache mechanism assuring the unicity of connectors."""
    global _connector_cache
    uid: uuid.UUID = util.data_validate_uid(uid)
    if uid in _connector_cache.keys():
        return _connector_cache[uid]
    else:
        return None


def add_connector_to_cache(o: FlexibleConnector) -> Connector | None:
    """cache mechanism assuring the unicity of connectors."""
    global _connector_cache
    o: Connector = data_validate_connector(o)
    if not o.uid in _connector_cache.keys():
        _connector_cache[o.uid] = o
    else:
        existing = _connector_cache[o.uid]
        if o is not existing:
            raise util.PunctiliousException('`Connector`unicity conflict')


class Connector(tuple):
    """A `Connector` is an abstract symbol that may be assigned various (human-readable) representations,
    and that is recognized as a distinctive semantic unit.
    """

    def __hash__(self):
        return hash((Connector, self.uid,))

    def __init__(self, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        pass

    def __new__(cls, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        if uid is None:
            uid: uuid.UUID = uuid.uuid4()

        uid: uuid.UUID = util.data_validate_uid(uid)
        cached = retrieve_connector_from_cache(uid)
        if cached is not None:
            return cached
        else:
            phi = super(Connector, cls).__new__(cls, (uid, fallback_string_representation,))
            add_connector_to_cache(phi)
            return phi

    def __repr__(self):
        return self.get_string_representation()

    def __str__(self):
        return self.get_string_representation()

    @property
    def fallback_string_representation(self) -> str:
        """The `fallback_string_representation` of a `Connector` is a string representation
        that is always available, and will be used as a fallback value when no solution
        can be found to return a string representation matching user preferences.

        `fallback_string_representation` is an immutable property.

        By convention, the `fallback_string_representation`:
         - use a safe subset of Unicode characters that should render properly on any computer system.
         - can be naturally used in mathematical expressions or formulas.
         - use English words separated by dashes (in such a way as to constitute a single word for natural
           representation in mathematical expressions or formulas).
         - be as unambiguous as possible while not being too verbose or lengthy.

        :return: A string representation of the connector.
        """
        return tuple.__getitem__(self, 1)

    def get_string_representation(self, **user_preferences) -> str:
        """Returns the string representation of the `Connector` that best matches `user_preferences`.

        :param user_preferences:
        :return:
        """
        return self.fallback_string_representation

    @property
    def uid(self) -> uuid.UUID:
        """

        `uid` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 0)

    def yield_string_representation(self, **user_preferences) -> typing.Generator[str, None, None]:
        """Generates the string representation of the `Connector` that best matches `user_preferences`.

        :param user_preferences:
        :return:
        """
        yield self.fallback_string_representation


FlexibleConnector = typing.Union[
    Connector, uuid.UUID]
