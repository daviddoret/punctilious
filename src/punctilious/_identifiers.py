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


class Identifier(tuple):

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        # The hash only takes the uuid into account.
        # The slug may potentially be modified.
        return hash((self.__class__, self[1],))

    def __init__(self, slug: FlexibleSlug, uuid: FlexibleUUID):
        """A globally unique identifier composed of a UUID and a slug.

        :param i: A uuid.
        :param p: A package slug.
        :param s: An object slug.
        """
        super().__init__()

    def __new__(cls, slug: FlexibleSlug, uuid: FlexibleUUID):
        slug = ensure_slug(slug)
        uuid = ensure_uuid(uuid)
        t = (slug, uuid,)
        return super().__new__(cls, t)

    def __repr__(self):
        """An unambiguous technical representation of the identifier.

        :return:
        """
        return f'"{self[1]}" ({self[1]}) identifier'

    def __str__(self):
        """A friendly representation of the identifier.

        :return:
        """
        return f'{self[0]}.{self[1]}'

    @property
    def slug(self) -> Slug:
        return self[0]

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
        raise NotImplementedError(f'Invalid identifier {o} ({type(o)})')
    else:
        raise ValueError(f'Invalid identifier {o} ({type(o)})')


class Identifiable(abc.ABC):

    @property
    @abc.abstractmethod
    def identifier(self) -> Identifier:
        raise NotImplementedError('This is an abstract property.')


_index: dict[Identifier, Identifiable] = {}


def check_identifier_uniqueness(o: Identifiable):
    global _index
    if o.identifier not in _index.keys():
        # stores the new object in the index
        _index[o.identifier] = o
    else:
        # retrieve the existing object from the index
        existing = _index[o.identifier]
        if not o is existing:
            raise ValueError(
                f'Duplicate object identifiers: new object: {o} ({o.identifier}) ({type(o)}), existing object: {existing} ({existing.identifier}) ({type(existing)})')


def get_from_identifier(identifier: FlexibleIdentifier) -> Identifiable:
    global _index
    identifier = ensure_identifier(identifier)
    if identifier in _index.keys():
        return _index[identifier]
    else:
        raise KeyError(f'Identifier not found: {identifier}')
