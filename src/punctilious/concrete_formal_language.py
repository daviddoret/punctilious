# special features
from __future__ import annotations

import typing
import collections.abc
# external packages
import uuid

import util
import const
import abstract_formal_language as afl
import representation_foundation as rf

_connectors: dict[int, Connector] = {}


def compute_connector_hash(uid: uuid.UUID):
    """Given its components, returns the hash of a `Connector`.
    """
    uid = util.data_validate_uid(uid)
    return hash((const.connector_hash_prime, Connector, uid,))


class Connector(rf.Representable):
    """A `Connector` is a formula symbolic component."""

    def __call__(self, *args):
        """Return a formula with this connector as the root connector, and the arguments as its arguments."""
        pass

    def __eq__(self, other):
        return self.is_connector_equivalent_to(other)

    def __hash__(self):
        return compute_connector_hash(uid=self.uid)

    def __init__(self, uid: uuid.UUID | None = None, representation_function: rf.Presenter | None = None):
        # Assignment of self._uid was already done in __new__,
        # to manage the situation where uid was passed as None,
        # and __new__ created a new one.
        # In consequence, do not implement: self._uid = uid
        super(Connector, self).__init__(representation_function=representation_function)

    def __new__(cls, uid: uuid.UUID | None = None):
        global _connectors
        if uid is None:
            # Assigns automatically a new pseudo-random uid.
            uid: uuid.UUID = uuid.uuid4()
        instance_hash: int = compute_connector_hash(uid=uid)
        if instance_hash in _connectors:
            # Reuses the connector from the cache.
            return _connectors[instance_hash]
        else:
            # Initiates a new connector.
            instance: Connector = super(Connector, cls).__new__(cls)
            # The uid cannot be assigned from __init__,
            # because if it was None, __new__ would create a new one,
            # and the new one is not passed to __init__.
            # In consequence, execute the assignment directly in __new__:
            instance._uid = uid
            # Store the connector in the cache.
            _connectors[instance_hash] = instance
            return instance

    def __ne__(self, other):
        return not (self.is_connector_equivalent_to(other))

    def is_connector_equivalent_to(self, other: FlexibleConnector):
        """Returns `True` if and only if this `Connector` is connector-equivalent to `other`.

        Two `Connector` objects are connector-equivalent if they are the same object in all circumstances."""
        other: Connector = data_validate_connector(other)
        return hash(self) == hash(other)

    @property
    def uid(self) -> uuid.UUID:
        return self._uid


def data_validate_connector(o: FlexibleConnector) -> Connector:
    """Ensures `o` is of type `Connector`. Uses implicit conversion if possible.

    :param o:
    :return:
    """
    if isinstance(o, Connector):
        return o
    else:
        raise ValueError('`o` is not implicitly convertible to `Connector`.')


class ConnectorOrderedSet(tuple):
    """A finite, computable, ordered set of connectors."""

    def __new__(cls, connectors: tuple[Connector, ...]):
        connectors: tuple = util.data_validate_unicity(connectors, raise_error_on_duplicate=True)
        connector_ordered_set: tuple[Connector, ...] = tuple(data_validate_connector(c) for c in connectors)
        return super(ConnectorOrderedSet, cls).__new__(cls, connector_ordered_set)


class Formula(tuple, rf.Representable):
    """A `Formula` is a pair (C, S) where:
     - C is a non-empty, finite and ordered set of connectors of size n.
     - S is a formula-structure, such that:
        - all connector-index in S are < n.
        - all index positions in C are present in S (possibly in a sub-terms).

    `Formula` is mutable because it is `Representable`.
    """

    def __init__(self, connectors: tuple[Connector, ...], structure: afl.FormulaStructure,
                 representation_function: rf.Presenter | None = None):
        super(Formula, self).__init__()
        rf.Representable.__init__(self=self, representation_function=representation_function)

    def __new__(cls, connectors: tuple[Connector, ...], structure: afl.FormulaStructure):
        connectors = util.data_validate_unicity(connectors, raise_error_on_duplicate=True)
        if len(connectors) == 0:
            raise ValueError('The formula `connectors` are empty.')
        elif len(connectors) != structure.connector_indexes_count:
            raise ValueError('The length of `connectors` is not equal to the number of connectors in the `structure`.')
        formula: tuple[tuple[Connector, ...], afl.FormulaStructure] = (connectors, structure,)
        return super(Formula, cls).__new__(cls, formula)

    @property
    def connectors(self) -> tuple[Connector, ...]:
        return self[0]

    @property
    def structure(self) -> afl.FormulaStructure:
        return self[1]


FlexibleConnector = typing.Union[Connector,]

pass
