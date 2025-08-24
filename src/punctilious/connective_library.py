from __future__ import annotations
import typing
import collections
import functools

# third party packages
import uuid

# package modules
import punctilious.util as util
import punctilious.ternary_boolean_library as tbl
import punctilious.binary_relation_library as brl


# import punctilious.rooted_plane_tree_library as rptl
# import punctilious.natural_number_0_sequence_library as nn0sl


# Binary relation classes

class IsEqualTo(brl.BinaryRelation):
    r"""The connective class equipped with the standard equality order relation.

    Mathematical definition
    -------------------------

    :math:`( \mathbb{F}, = )`.

    """

    @util.readonly_class_property
    def is_antisymmetric(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A Python object.
        :param y: A Python object.
        :return: `True` or `False`.
        """
        x: Connective = Connective.from_any(x)
        y: Connective = Connective.from_any(y)
        return x.is_connective_equivalent_to(y)


class GuidOrder(brl.BinaryRelation):
    r"""The connective class equipped with the standard strictly less-than order relation.

    Definition
    ------------

    Canonical ordering of connective elements, denoted :math:`\prec`,
    is based on the 128-bit integer value of their respective UUID component,
    which is the default implementation of __lt__ in the uuid package.

    Note
    ------

    The canonical ordering of connective-sequence being dependent on the connectives UUIDs,
    the resulting ordering may appear random to the human reader.

    """

    @util.readonly_class_property
    def is_order_isomorphic_with_n_strictly_less_than(cls) -> tbl.TernaryBoolean:
        r"""

        Proof
        ------

        TODO: Provide proof here.

        """
        return tbl.TernaryBoolean.TRUE

    @util.readonly_class_property
    def least_element(cls) -> Connective:
        """By design, we declare the least connective with GUID `00000000-0000-0000-0000-000000000000`.

        :return: The least connective.
        """
        return Connective(
            fallback_string_representation="Least connective element",
            uid=uuid.UUID("00000000-0000-0000-0000-000000000000")
        )

    @classmethod
    def rank(cls, x: object) -> int:
        r"""Returns the rank of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A connective `x`.
        :return: The rank of `x`.
        """
        x: Connective = Connective.from_any(x)
        return x.uid.int

    @classmethod
    def relates(cls, x: object, y: object) -> bool:
        r"""Returns `True` if :math:`xRy`, `False` otherwise.

        :param x: A connective.
        :param y: A connective.
        :return: `True` or `False`.
        """
        x: Connective = Connective.from_any(x)
        y: Connective = Connective.from_any(y)
        n1: int = x.rank
        n2: int = y.rank
        return n1 < n2

    @classmethod
    def successor(cls, x: object) -> object:
        r"""Returns the successor of `x` in :math:`( \mathbb{N}_0, < )`.

        :param x: A Python object interpretable as a (0-based) natural number.
        :return: The successor of `x`.
        """
        x: Connective = Connective.from_any(x)
        n: int = cls.rank(x)
        n += 1
        y: Connective = cls.unrank(n)
        return y

    @classmethod
    def unrank(cls, n: int) -> Connective:
        r"""Returns the connective `x` such that :math:`rank(x) = n`.

        :param n: A (0-based) natural number.
        :return: A connective.
        """
        n = int(n)
        if n < 0:
            raise util.PunctiliousException("`n` must be a positive integer.", n=n)
        return Connective(fallback_string_representation="# Anonymous connector", uid=uuid.UUID(int=n))


class Connective(brl.ClassWithOrder, tuple):
    """A `Connective` is an abstract symbol that may be assigned various (human-readable) representations,
    and that is recognized as a distinctive semantic unit.

    References:
     - Mancosu 2021, definition 2.1, p. 14, p. 15.
    """

    def __hash__(self):
        return self.compute_hash(self)

    def __init__(self, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        pass

    def __new__(cls, fallback_string_representation: str, uid: uuid.UUID | str | None = None):
        if uid is None:
            uid: uuid.UUID = uuid.uuid4()

        uid: uuid.UUID = util.data_validate_uid(uid)

        c = super(Connective, cls).__new__(cls, (uid, fallback_string_representation,))
        return c

    def __repr__(self):
        return self.get_string_representation()

    def __str__(self):
        return self.get_string_representation()

    _HASH_SEED: int = 11417641604436932830  # A static random seed to reduce collision risk, originally generated by random.getrandbits(64).

    @classmethod
    def compute_hash(cls, o: Connective) -> int:
        """Exposes the hashing logic as a static method.

        :param o: An object that is structurally compatible with a connective.
        :return: The hash of the connective that is structurally equivalent to `o`.
        """
        return hash((Connective, cls._HASH_SEED, o.uid,))

    @functools.cached_property
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

    @classmethod
    def from_any(cls, o: FlexibleConnective) -> Connective:
        """Declares a connective from a Python object that can be interpreted as a connective.

        Note:
            This method is redundant with the default constructor.

        :param o: a Python object that can be interpreted as a connective.
        :return: a connective.
        """
        if isinstance(o, Connective):
            return o
        if isinstance(o, collections.abc.Iterable):
            return Connective(*o)
        if isinstance(o, collections.abc.Generator):
            return Connective(*o)
        raise util.PunctiliousException('Connective data validation failure', o=o)

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
        c: Connective = Connective.from_any(c)
        return c.uid == self.uid

    @util.readonly_class_property
    def is_equal_to_relation(self) -> typing.Type[brl.BinaryRelation]:
        return IsEqualTo

    @util.readonly_class_property
    def is_strictly_less_than_relation(self) -> typing.Type[brl.BinaryRelation]:
        return GuidOrder

    @functools.cached_property
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
    Connective, tuple[uuid.UUID, str],]

connective_least_element: Connective = GuidOrder.least_element
