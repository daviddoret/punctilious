import abc
import collections.abc
import re
import uuid as uuid_pkg
import typing


class Slug(str):
    """A slug is an identifier that uses lowercase alphanumeric ASCII characters with words
    delimited with underscores."""

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.__class__, super().__str__(),))

    def __init__(self, slug: str):
        super().__init__()

    def __new__(cls, slug: str):
        pattern = r"^[a-zA-Z][a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*[a-zA-Z0-9]$"
        if not bool(re.fullmatch(pattern, slug)):
            raise ValueError(f'Invalid slug: "{slug}".')
        return super().__new__(cls, slug)

    def __repr__(self):
        return f'"{str(super().__str__())}" slug'

    def __str__(self):
        return str(super().__str__())


class SlugsDictionary(dict):
    """A typed dictionary of slugs.

    """

    def __init__(self):
        super().__init__()

    def __setitem__(self, slug, value):
        slug = ensure_slug(o=slug)
        if slug in self:
            raise KeyError(f"Key '{slug}' already exists.")
        super().__setitem__(slug, value)


FlexibleSlug = typing.Union[Slug, str]


def ensure_slug(o: FlexibleSlug) -> Slug:
    """Assure `o` is of type Slug, or implicitly convert `o` to Slug, or raise an error if this fails.
    """
    if isinstance(o, Slug):
        return o
    elif isinstance(o, str):
        i: str
        return Slug(o)
    else:
        raise ValueError(f'Invalid slug {o}')


FlexibleUUID = typing.Union[uuid_pkg.UUID, str]


def ensure_uuid(o: FlexibleUUID) -> uuid_pkg.UUID:
    """Assure `o` is of type uuid_pkg.UUID, or implicitly convert `o` to uuid_pkg.UUID, or raise an error if this fails.
    """
    if isinstance(o, uuid_pkg.UUID):
        return o
    elif isinstance(o, str):
        return uuid_pkg.UUID(o)
    else:
        raise ValueError(f'Invalid uuid {o}')


class UniqueIdentifier(tuple):
    """An immutable globally unique identifier composed of a UUID and a friendly slug.
    """

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Returns a hash for the identifier.

        Only the uuid component is taken into consideration because the slug could be modified.

        :return:
        """
        return hash((UniqueIdentifier, self[1],))

    def __init__(self, slug: FlexibleSlug, uuid: FlexibleUUID, raises_error_if_exists: bool = False):
        """Initializes a new identifier.

        :param slug: A slug.
        :param uuid: A UUID.
        """
        global _unique_identifier_index
        super().__init__()
        uuid = ensure_uuid(uuid)
        if uuid not in _unique_identifier_index.keys():
            _unique_identifier_index[uuid] = self

    def __new__(cls, slug: FlexibleSlug, uuid: FlexibleUUID, raises_error_if_exists: bool = False):
        global _unique_identifier_index
        slug = ensure_slug(slug)
        uuid = ensure_uuid(uuid)
        if uuid in _unique_identifier_index.keys():
            if raises_error_if_exists:
                raise ValueError(f'UniqueIdentifier already exists. Uuid: {uuid}.')
            else:
                # Reuse existing identifier.
                existing_identifier: UniqueIdentifier = _unique_identifier_index[uuid]
                if slug != existing_identifier.slug:
                    raise ValueError(
                        f'UniqueIdentifier has inconsistent slug. New slug: `{slug}`, existing slug: `{existing_identifier.slug}`, uuid: {uuid}')
                else:
                    # Return existing identifier.
                    return existing_identifier
        else:
            # Instantiates a new UniqueIdentifier.
            t = (slug, uuid,)
            uid = super().__new__(cls, t)
            return uid

    def __repr__(self):
        """An unambiguous technical representation of the identifier.

        :return:
        """
        return f'{self.unambiguous_reference} UniqueIdentifier'

    def __str__(self):
        """A friendly representation of the identifier.

        :return:
        """
        return f'{self.friendly_reference} UniqueIdentifier'

    @property
    def friendly_reference(self) -> str:
        """Returns a friendly reference to the identifier (i.e. its slug). This reference may not be unique."""
        return str(self.slug)

    @property
    def slug(self) -> Slug:
        return self[0]

    @property
    def unambiguous_reference(self) -> str:
        """Returns an unambiguous reference to the identifier. This reference is unique."""
        return f'{str(self.slug)} ({str(self.uuid)})'

    @property
    def uuid(self) -> uuid_pkg.UUID:
        return self[1]


FlexibleUniqueIdentifier = typing.Union[UniqueIdentifier, collections.abc.Mapping, collections.abc.Iterable]


def ensure_unique_identifier(o: FlexibleUniqueIdentifier) -> UniqueIdentifier:
    """Assure `o` is of type Identifier, or implicitly convert `o` to Identifier, or raise an error if this fails.
    """
    if isinstance(o, UniqueIdentifier):
        return o
    if isinstance(o, collections.abc.Mapping):
        slug: FlexibleSlug = o['slug']
        uuid: FlexibleUUID = o['uuid']
        return UniqueIdentifier(slug=slug, uuid=uuid)
    if isinstance(o, collections.abc.Iterable) and len(o) == 2:
        slug: FlexibleSlug = o[0]
        uuid: FlexibleUUID = o[1]
        return UniqueIdentifier(slug=slug, uuid=uuid)
    if isinstance(o, str):
        # IMPROVEMENT: Add support for string representations.
        raise NotImplementedError(f'Identifier string representation not supported: {o} ({type(o)})')
    else:
        raise ValueError(f'Invalid identifier: {o} ({type(o)})')


class UniqueIdentifiable(abc.ABC):
    """A UniqueIdentifiable is an object:
     - that is uniquely identified by a UniqueIdentifier,
     - that when loaded is indexed in a central index to assure it has no duplicate,
     - that may have some immutable properties,
     - that may have some mutable properties.

    """

    def __hash__(self):
        """

        :return:
        """
        return hash((UniqueIdentifiable, self.uid,))

    def __init__(self, uid: FlexibleUniqueIdentifier):
        """
        
        Raises an error if a UniqueIdentifiable with the same UniqueIdentifier already exists.
        
        :param uid: 
        """""
        # Add the identifier to the global index
        global _unique_identifiable_index
        uid: UniqueIdentifier = ensure_unique_identifier(uid)
        self._uid = uid
        if uid.uuid not in _unique_identifiable_index.keys():
            _unique_identifiable_index[uid.uuid] = self
        else:
            raise ValueError(f"UniqueIdentifiable with UniqueIdentifier '{uid}' already exists.")
        super().__init__()

    @property
    def uid(self) -> UniqueIdentifier:
        return self._uid


_unique_identifier_index: dict[uuid_pkg.UUID, UniqueIdentifier | None] = {}
_unique_identifiable_index: dict[uuid_pkg.UUID, UniqueIdentifiable | None] = {}


def get_unique_identifiable(uid: FlexibleUniqueIdentifier | None,
                            uuid: FlexibleUUID | None = None) -> UniqueIdentifiable | None:
    """Returns the existing UniqueIdentifiable with the given uid or UUID if it exists.
    Returns None otherwise.

    :param uid: The UniqueIdentifier of the UniqueIdentifiable to return.
    :param uuid: Alternatively, the UUID of the UniqueIdentifiable to return.
    :return: The UniqueIdentifiable or None if it does not exist.
    """
    global _unique_identifiable_index
    if uid is None and uuid is None:
        raise ValueError('Either uid or uuid must be provided.')
    if uid is not None:
        uid = ensure_unique_identifier(uid)
        uuid = uid.uuid
    uuid: uuid_pkg.UUID = ensure_uuid(uuid)
    if uuid in _unique_identifiable_index.keys():
        return _unique_identifiable_index[uuid]
    else:
        return None
