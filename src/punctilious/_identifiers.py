import re
import uuid
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


FlexibleUUID = typing.Union[uuid.UUID, str]


def ensure_uuid(o: str | uuid.UUID) -> uuid.UUID:
    """Assure `o` is of type uuid.UUID, or implicitly convert `o` to uuid.UUID, or raise an error if this fails.
    """
    if isinstance(o, uuid.UUID):
        return o
    elif isinstance(o, str):
        return uuid.UUID(o)
    else:
        raise ValueError(f'Invalid uuid {o}')


class Identifier(tuple):

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.__class__, self[0], self[1], self[2],))

    def __init__(self, i: FlexibleUUID, p: FlexibleSlug, s: FlexibleSlug):
        """A globally unique identifier composed of a UUID and a slug.

        :param i: A uuid.
        :param p: A package slug.
        :param s: An object slug.
        """
        super().__init__()

    def __new__(cls, i: FlexibleUUID, p: FlexibleSlug, s: FlexibleSlug):
        i = ensure_uuid(i)
        p = ensure_slug(p)
        s = ensure_slug(s)
        phi = (i, p, s,)
        return super().__new__(cls, phi)

    def __repr__(self):
        """An unambiguous technical representation of the identifier.

        :return:
        """
        return f'"{self[1]}.{self[2]}" ({self[0]}) identifier'

    def __str__(self):
        """A friendly representation of the identifier.

        :return:
        """
        return f'{self[0]}.{self[2]}'

    @property
    def package_slug(self) -> Slug:
        return self[1]

    @property
    def package_uuid(self) -> uuid.UUID:
        return self[0]

    @property
    def slug(self) -> Slug:
        return self[2]


FlexibleIdentifier = typing.Union[Identifier]


def ensure_identifier(o: Identifier | str) -> Identifier:
    """Assure `o` is of type Identifier, or implicitly convert `o` to Identifier, or raise an error if this fails.
    """
    if isinstance(o, Identifier):
        return o
    else:
        raise ValueError(f'Invalid identifier {o}')
