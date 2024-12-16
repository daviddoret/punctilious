import abc
import collections.abc
import re
import uuid
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


class Identifier(tuple):
    """An immutable globally unique identifier composed of a UUID and a slug.
    """

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Returns a hash for the identifier.

        Only the uuid component is taken into consideration because the slug could be modified.

        :return:
        """
        return hash((self.__class__, self[1],))

    def __init__(self, slug: FlexibleSlug, uuid: FlexibleUUID):
        """Initializes a new identifier.

        :param slug: A slug.
        :param uuid: A UUID.
        """
        super().__init__()

    def __new__(cls, slug: FlexibleSlug, uuid: FlexibleUUID):
        global _index
        slug = ensure_slug(slug)
        uuid = ensure_uuid(uuid)
        t = (slug, uuid,)
        new_identifier = super().__new__(cls, t)
        if new_identifier in _index.keys():
            raise ValueError(f'Identifier already exists: {new_identifier}')
        return

    def __repr__(self):
        """An unambiguous technical representation of the identifier.

        :return:
        """
        return f'{self.unambiguous_reference} identifier'

    def __str__(self):
        """A friendly representation of the identifier.

        :return:
        """
        return f'{self.friendly_reference} identifier'

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


FlexibleIdentifier = typing.Union[Identifier]


def ensure_identifier(o: FlexibleIdentifier) -> Identifier:
    """Assure `o` is of type Identifier, or implicitly convert `o` to Identifier, or raise an error if this fails.
    """
    if isinstance(o, Identifier):
        return o
    if isinstance(o, collections.abc.Mapping):
        slug: FlexibleSlug = o['slug']
        uuid: FlexibleUUID = o['uuid']
        return Identifier(slug=slug, uuid=uuid)
    if isinstance(o, collections.abc.Iterable) and len(o) == 2:
        slug: FlexibleSlug = o[0]
        uuid: FlexibleUUID = o[1]
        return Identifier(slug=slug, uuid=uuid)
    if isinstance(o, str):
        # IMPROVEMENT: Add support for string representations.
        raise NotImplementedError(f'Identifier string representation not supported: {o} ({type(o)})')
    else:
        raise ValueError(f'Invalid identifier: {o} ({type(o)})')


class Identifiable(abc.ABC):

    @property
    @abc.abstractmethod
    def identifier(self) -> Identifier:
        raise NotImplementedError('This is an abstract property.')


_index: dict[uuid.UUID, tuple[Identifier, Identifiable | None] | None] = {}


def check_identifier_uniqueness(o: Identifiable):
    """Checks that the identifier of an object is unique."""
    global _index
    existing_identifiable: Identifiable | None = get_identifiable(identifier=o.identifier, raise_not_found_error=False)
    if existing_identifiable is None:
        # stores the new object in the index
        _index[o.identifier.uuid] = (o.identifier, o,)
    else:
        if o is not existing_identifiable:
            raise ValueError(
                f'Duplicate object identifiers: new object: {o} ({o.identifier}) ({type(o)}), existing object: {existing} ({existing.identifier}) ({type(existing)})')


def get_identifiable(identifier: FlexibleIdentifier, raise_not_found_error: bool = False) -> Identifiable | None:
    """Returns an identifiable from an identifier.
    Returns None or raises an error if the identifiable is not found.
    """
    global _index
    identifier = ensure_identifier(identifier)
    existing_identifiable: Identifiable | None = None
    if identifier.uuid in _index.keys():
        t: tuple[Identifier, Identifiable | None] | None = _index[identifier.uuid]
        if t is None:
            # The identifier was not present in the index,
            # add it to the index even though we don't know what the identifiable is.
            t = (identifier, None,)
            _index[identifier.uuid] = t
        existing_identifiable = t[1]
    if existing_identifiable is None and raise_not_found_error:
        raise KeyError(f'Identifier not found: {identifier}')
    return existing_identifiable
