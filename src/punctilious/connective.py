from __future__ import annotations
import typing
import uuid

# package modules
import util

_connective_cache: dict[uuid.UUID, Connective] = {}  # cache mechanism assuring connectives unicity


def data_validate_connective(
        o: FlexibleConnective) -> Connective:
    if isinstance(o, Connective):
        return o
    if isinstance(o, uuid.UUID):
        return Connective(uid=o)
    raise util.PunctiliousException('Connective data validation failure', o=o)


def retrieve_connective_from_cache(uid: uuid.UUID) -> Connective | None:
    """cache mechanism assuring the unicity of connectives."""
    global _connective_cache
    uid: uuid.UUID = util.data_validate_uid(uid)
    if uid in _connective_cache.keys():
        return _connective_cache[uid]
    else:
        return None


def add_connective_to_cache(o: FlexibleConnective) -> Connective | None:
    """cache mechanism assuring the unicity of connectives."""
    global _connective_cache
    o: Connective = data_validate_connective(o)
    if not o.uid in _connective_cache.keys():
        _connective_cache[o.uid] = o
    else:
        existing = _connective_cache[o.uid]
        if o is not existing:
            raise util.PunctiliousException('`Connective`unicity conflict')


class Connective(tuple):
    """A `Connective` is an abstract symbol that may be assigned various (human-readable) representations,
    and that is recognized as a distinctive semantic unit.

    References:
     - Mancosu 2021, definition 2.1, p. 14, p. 15.
    """

    def __eq__(self, c):
        """Returns `False` if `c` cannot be interpreted as a :class:`Connective`,
        returns `True` if `c` is connective-equivalent to this :class:`Connective`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            c: Connective = data_validate_connective(c)
            return self.is_connective_equivalent_to(c)
        except util.PunctiliousException:
            return False

    def __hash__(self):
        return hash((Connective, self.uid,))

    def __init__(self, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        pass

    def __ne__(self, c):
        """Returns `False` if `c` cannot be interpreted as a :class:`Connective`,
        returns `True` if `c` is not connective-equivalent to this :class:`Connective`,
        returns `False` otherwise.

        Note:
            The python equality operator may be misleading because it can be called
            whatever the type of the second object, and formally speaking equality with objects
            of a distinct type is not defined. For this reason, the following
            paradox is possible: `not(x == y) and not(x != y)`.
            To avoid any ambiguity, use the more accurate is-equivalent method.
        """
        try:
            c: Connective = data_validate_connective(c)
            return not self.is_connective_equivalent_to(c)
        except util.PunctiliousException:
            return False

    def __new__(cls, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        if uid is None:
            uid: uuid.UUID = uuid.uuid4()

        uid: uuid.UUID = util.data_validate_uid(uid)
        cached = retrieve_connective_from_cache(uid)
        if cached is not None:
            return cached
        else:
            phi = super(Connective, cls).__new__(cls, (uid, fallback_string_representation,))
            add_connective_to_cache(phi)
            return phi

    def __repr__(self):
        return self.get_string_representation()

    def __str__(self):
        return self.get_string_representation()

    @property
    def fallback_string_representation(self) -> str:
        """The `fallback_string_representation` of a `Connective` is a string representation
        that is always available, and will be used as a fallback value when no solution
        can be found to return a string representation matching user preferences.

        `fallback_string_representation` is an immutable property.

        By convention, the `fallback_string_representation`:
         - use a safe subset of Unicode characters that should render properly on any computer system.
         - can be naturally used in mathematical expressions or formulas.
         - use English words separated by dashes (in such a way as to constitute a single word for natural
           representation in mathematical expressions or formulas).
         - be as unambiguous as possible while not being too verbose or lengthy.

        :return: A string representation of the connective.
        """
        return tuple.__getitem__(self, 1)

    def get_string_representation(self, **user_preferences) -> str:
        """Returns the string representation of the `Connective` that best matches `user_preferences`.

        :param user_preferences:
        :return:
        """
        return self.fallback_string_representation

    def is_connective_equivalent_to(self, c: FlexibleConnective):
        """Returns `True` if this :class:`Connective` is connective-equivalent to :class:`Connective` `c`.

        Formal definition:
        A connective `c` is connective-equivalent to a connective `d` if and only if this is the same
        symbol, or equivalently they are indistinguishable.

        Note:
        connective-equivalence is a syntactic property, i.e. it is related to an abstract symbol,
        and it is not related to the diverse and sometimes ambiguous ways a connective may be represented.

        Implementation:
        As a proxy for the concept of an abstract symbol, we use the :attr:`Connective.uid` property.

        :param c:
        :return:
        """
        c: Connective = data_validate_connective(c)
        return c.uid == self.uid

    @property
    def uid(self) -> uuid.UUID:
        """

        `uid` is an immutable property.


        :return:
        """
        return tuple.__getitem__(self, 0)

    def yield_string_representation(self, **user_preferences) -> typing.Generator[str, None, None]:
        """Generates the string representation of the `Connective` that best matches `user_preferences`.

        :param user_preferences:
        :return:
        """
        yield self.fallback_string_representation


FlexibleConnective = typing.Union[
    Connective, uuid.UUID]
