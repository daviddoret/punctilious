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

    def __ne__(self, other):
        return not (self == other)

    def __new__(cls, slug: str):
        pattern = r'^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$'
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

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        """Returns a hash for the identifier.

        Only the uuid component is taken into consideration because the slug could be modified.
        In consequence, a UniqueIdentifier has the same hash as its UUID.

        :return:
        """
        return hash(self[1])

    def __init__(self, slug: FlexibleSlug, uuid: FlexibleUUID):
        """Initializes a new identifier.

        :param slug: A slug.
        :param uuid: A UUID.
        """
        # global _unique_identifier_index
        super().__init__()
        uuid = ensure_uuid(uuid)
        # _unique_identifier_index[uuid] = self

    def __new__(cls, slug: FlexibleSlug, uuid: FlexibleUUID):
        # global _unique_identifier_index
        slug = ensure_slug(slug)
        uuid = ensure_uuid(uuid)
        # if uuid in _unique_identifier_index.keys():
        #    raise ValueError(f'UniqueIdentifier already exists. Uuid: {uuid}.')
        # else:
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
    if isinstance(o, tuple) and len(o) == 2:
        slug: FlexibleSlug = o[0]
        uuid: FlexibleUUID = o[1]
        return UniqueIdentifier(slug=slug, uuid=uuid)
    if isinstance(o, str):
        # IMPROVEMENT: Add support for string representations.
        raise NotImplementedError(f'Identifier string representation not supported: {o} ({type(o)})')
    else:
        raise ValueError(f'Invalid identifier: {o} ({type(o)})')


def load_unique_identifier(o: typing.Mapping) -> UniqueIdentifier:
    """Returns the corresponding UniqueIdentifier if it exists,
    or instantiates, indexes, and returns a new one otherwise.

    :param o: A dictionary representing the unique identifier.
    :return:
    """
    uuid: uuid_pkg.UUID = ensure_uuid(o['uuid'])
    slug: Slug = ensure_slug(o['slug'])
    if uuid in _unique_identifier_index.keys():
        # The unique identifier already exists.
        uid: UniqueIdentifier = _unique_identifier_index[uuid]
        if uid.slug != slug:
            raise ValueError(f'Inconsistent slugs')
        return uid
    else:
        # The unique identifier does not exist.
        # __new__ will re-check it does not exist.
        # __init__ will add it to the index.
        uid: UniqueIdentifier = UniqueIdentifier(slug=slug, uuid=uuid)
        return uid


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
        if uid.uuid in _unique_identifiable_index.keys():
            raise ValueError(f"UniqueIdentifiable with UniqueIdentifier '{uid}' already exists.")
        _unique_identifiable_index[uid.uuid] = self
        super().__init__()

    @property
    def uid(self) -> UniqueIdentifier:
        return self._uid


# _unique_identifier_index: dict[uuid_pkg.UUID, UniqueIdentifier | None] = {}
_unique_identifiable_index: dict[uuid_pkg.UUID, UniqueIdentifiable | None] = {}


def create_uid(slug: FlexibleSlug) -> UniqueIdentifier:
    """Creates a new UniqueIdentifier.

    :param slug: A slug.
    :return: A new UniqueIdentifier.
    """
    uuid: uuid_pkg.UUID = uuid_pkg.uuid4()
    return UniqueIdentifier(slug=slug, uuid=uuid)


def load_unique_identifiable(o: typing.Mapping) -> UniqueIdentifiable | None:
    """Returns the existing UniqueIdentifiable if it exists.
    Returns None otherwise.

    :param o: A dictionary representing the unique identifiable.
    :return: The UniqueIdentifiable or None if it does not exist.
    """
    global _unique_identifiable_index
    uid = ensure_unique_identifier(o['uid'])
    return _unique_identifiable_index.get(uid.uuid, None)
