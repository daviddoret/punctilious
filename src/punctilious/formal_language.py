# special features
from __future__ import annotations

import typing
# external packages
import uuid

import util
import const
import representation_foundation as rf


# TODO: FormulaStructureTerms caching does not function properly.
#   first, develop a test test_formula_structure to check if hashing functions properly.

def data_validate_uid(o: uuid.UUID) -> uuid.UUID:
    """Ensures `o` is of type `uuid.UUID`, using implicit conversion if necessary.

    :param o:
    :return:
    """
    if isinstance(o, uuid.UUID):
        return o
    elif isinstance(o, str):
        try:
            return uuid.UUID(o)
        except ValueError:
            raise util.PunctiliousException('`uuid.UUID` ensurance failure. `o` is not a string in valid UUID format.',
                                            o=o)
    else:
        raise util.PunctiliousException('`uuid.UUID` ensurance failure. `o` is not of a supported type.', o=o)


def data_validate_connector_index(o: int) -> ConnectorIndex:
    """Performs data validation on a presumed connector-index `o`.
    Convert `o` for FormulaPoint implicitly if necessary.
    """
    if isinstance(o, ConnectorIndex):
        return o
    elif isinstance(o, int):
        return ConnectorIndex(o)
    else:
        raise util.PunctiliousException('`ConnectorIndex` ensurance failure. `o` is not of a supported type.', o=o)


def ensure_connector_index_tuple(o: tuple) -> tuple[ConnectorIndex, ...]:
    """Ensure that a python-tuple `o` is composed of `ConnectorIndex` elements.
    Otherwise, implicitly convert its elements to `ConnectorIndex` and return a new tuple.

    :param o:
    :return:
    """
    return tuple(data_validate_connector_index(fp) for fp in o)


def data_validate_formula_structure(o: FlexibleFormulaStructure) -> FormulaStructure:
    """Performs data validation on a presumed Structure `o`.

    :param o:
    :param implicit_tuple_conversion: if `o` is a tuple
    :return:
    """
    if isinstance(o, FormulaStructure):
        return o
    elif isinstance(o, ConnectorIndex):
        # implicit conversion of ConnectorIndex `o` to FormulaStructure o().
        return FormulaStructure(o)
    elif isinstance(o, int):
        # implicit conversion of int `o` to FormulaStructure o().
        return FormulaStructure(o)
    elif isinstance(o, tuple) and len(o) == 2:
        # implicit conversion of tuple of length 2 `o` to FormulaStructure o0(*o1).
        structure = FormulaStructure(root=o[0], terms=o[1])
        return structure
    else:
        raise util.PunctiliousException('`FormulaStructure` ensurance failure. `o` is not of a supported type.', o=o)


def data_validate_terms(o: FlexibleTerms) -> FormulaStructureTerms:
    """Performs data validation on presumed Terms `o`.

    :param o:
    :return:
    """
    # Logic is implemented in Terms.__new__().
    return FormulaStructureTerms(o)


def compute_formula_structure_hash(root: FlexibleConnectorIndex, terms: FlexibleTerms = None):
    """Given its components, returns the hash of a `Structure`.
    """
    root = data_validate_connector_index(root)
    terms = data_validate_terms(terms)
    return hash((const.formula_structure_hash_prime, FormulaStructure, root, terms,))


def compute_formula_structure_terms_hash(terms: FlexibleTerms = None):
    if terms is None:
        terms = tuple()
    if not isinstance(terms, tuple):
        raise util.PunctiliousException('oops', terms=terms)
    # we cannot data_validate_terms as this leads to infinite loop.
    # terms = data_validate_terms(terms)
    # instead we explode the terms in the hash computation, as follows:
    return hash((const.formula_structure_terms_hash_prime, FormulaStructureTerms, *terms,))


_formula_structures: dict[int, FormulaStructure] = {}
_formula_structure_terms: dict[int, FormulaStructureTerms] = {}
_connector_indexes: dict[int, ConnectorIndex] = {}


class ConnectorIndex(int):
    """A `ConnectorIndex` is a model of natural number (whose first element is mapped to 0),
    that is used as a connector index to build formula-structures.

    """

    def __hash__(self):
        return compute_connector_index_hash(self)

    def __new__(cls, n: int) -> ConnectorIndex:
        global _connector_indexes
        if not isinstance(n, int):
            raise ValueError('`i` must be of type `int`.')
        connector_index_hash: int = compute_connector_index_hash(n)
        if connector_index_hash in _connector_indexes:
            return _connector_indexes[connector_index_hash]
        elif isinstance(n, ConnectorIndex):
            return n
        else:
            connector_index = super(ConnectorIndex, cls).__new__(cls, n)
            _connector_indexes[connector_index_hash] = connector_index
            return connector_index

    def __str__(self):
        return f'i{self.as_int()}'

    def as_int(self) -> int:
        return int(self)

    def is_connector_index_equivalent_to(self, connector_index: FlexibleConnectorIndex) -> bool:
        """Returns `True` if `self` is connector-index-equivalent to `other`.
        Raises an exception if `other` is not a `ConnectorIndex`."""
        connector_index: ConnectorIndex = data_validate_connector_index(connector_index)
        return self is connector_index or self.as_int() == connector_index.as_int()


def compute_connector_index_hash(i: int):
    if isinstance(i, ConnectorIndex):
        # To avoid infinite recursion with method __hash__ of ConnectorIndex.
        i: int = int(i)
    return hash((const.connector_index_hash_prime, ConnectorIndex, i))


class FormulaStructure(tuple):
    """A `FormulaStructure` is an abstract formula structure, independent of connectors.

    """

    def __hash__(self):
        return compute_formula_structure_hash(root=self.root, terms=self.terms)

    def __init__(self, root: FlexibleConnectorIndex, terms: FlexibleTerms = tuple()):
        global _formula_structures
        root: ConnectorIndex = data_validate_connector_index(root)
        terms: tuple[FormulaStructure, ...] = data_validate_terms(terms)
        super(FormulaStructure, self).__init__()
        # `is_canonical` is cached, because this property will be pervasively necessary.
        is_canonical, _ = self.check_canonicity()
        self._is_canonical: bool = is_canonical
        connector_indexes = [self.root]
        for term in self.terms:
            for ci in term.connector_indexes:
                if ci not in connector_indexes:
                    connector_indexes.append(ci)
        connector_indexes = sorted(connector_indexes)
        self._connector_indexes: tuple[ConnectorIndex, ...] = tuple(connector_indexes)
        structure_hash: int = compute_formula_structure_hash(root=root, terms=terms)
        _formula_structures[structure_hash] = self

    def __new__(cls, root: FlexibleConnectorIndex, terms: FlexibleTerms = tuple()):
        global _formula_structures
        root: ConnectorIndex = data_validate_connector_index(root)
        terms: tuple[FormulaStructure, ...] = data_validate_terms(o=terms)
        structure_hash: int = compute_formula_structure_hash(root=root, terms=terms)
        if structure_hash in _formula_structures:
            return _formula_structures[structure_hash]
        else:
            terms = super(FormulaStructure, cls).__new__(cls, (root, terms,))
            return terms

    def arity(self) -> int:
        """Returns the `arity` of the `FormulaStructure`.

        The `arity` of a `FormulaStructure` is the number of terms it contains.

        :return:
        """
        return len(self._connector_indexes)

    def check_canonicity(self, max_pointer: int | None = None) -> tuple[bool, int | None]:
        """Returns `True` if this structure participates in a canonical structure, `False` otherwise.

        :param max_pointer: The greatest pointer in precedent points.
        :return:
        """
        if max_pointer is None:
            if self.root != 0:
                # this is a root structure, but its pointer is not p0.
                return False, None
            else:
                max_pointer: int = self.root
        if self.root > max_pointer + 1:
            # this is not a root structure, but its pointer is too big.
            return False, None
        if self.root == max_pointer + 1:
            # this is the only authorized increment of max_pointer.
            max_pointer = self.root
        for sub_structure in self.terms:
            check, max_pointer = sub_structure.check_canonicity(max_pointer=max_pointer)
            if not check:
                return False, None
        return True, max_pointer

    @property
    def is_canonical(self) -> bool:
        """Returns `True` if this structure is a canonical, `False` otherwise.

        A structure is a canonical if and only if
        the pointers appearing in the structure,
        when read left-to-right, depth-first,
        are such that no pointer `p_i` ever appear in the structure
        unless i=0, or `p_(i-1)` already appeared in the structure.

        :return:
        """
        return self._is_canonical

    def is_formula_structure_equivalent_to(self, formula_structure: FlexibleFormulaStructure,
                                           implicit_tuple_conversion: bool = True) -> bool:
        """Two formula-structures a and b are formula-structure-equivalent if and only if
         - the root of a is connector-index equivalent to the root of b,
         - the arity of a is equal to the arity of b,
         - in order, every term of a is formula-structure-equivalent to the corresponding term of b.

        :param formula_structure:
        :param implicit_tuple_conversion:
        :return:
        """
        formula_structure: FormulaStructure = data_validate_formula_structure(formula_structure)
        if self is formula_structure:
            return True
        elif not (self.root.is_connector_index_equivalent_to(formula_structure.root)):
            return False
        elif not (self.arity() == formula_structure.arity()):
            return False
        elif not (
                all(fs1.is_formula_structure_equivalent_to(fs2) for fs1, fs2 in
                    zip(self.terms, formula_structure.terms))):
            return False
        return True

    @property
    def is_leaf(self) -> bool:
        """Returns `True` if the structure is a leaf, `False` otherwise.

        A structure is a leaf if and only if it contains no sub-terms.
        """
        return len(self.terms) == 0

    @property
    def connector_indexes(self) -> tuple[ConnectorIndex, ...]:
        """Returns

        :return:
        """
        return self._connector_indexes

    @property
    def connector_indexes_count(self):
        """Returns the number of distinct `ConnectorIndex` in the `FormulaStructure`.
        """
        return len(self.connector_indexes)

    @property
    def root(self) -> ConnectorIndex:
        """The `root` of the `FormulaStructure`.

        The `root` of a `FormulaStructure` is the topmost `ConnectorIndex` of the formula tree..

        :return:
        """
        return self[0]

    @property
    def terms(self) -> tuple[FormulaStructure]:
        """The tuple of terms (sub-structures) contained in this `FormulaStructure`.

        :return:
        """
        return self[1]


_connectors: dict[int, Connector] = {}


def compute_connector_hash(uid: uuid.UUID):
    """Given its components, returns the hash of a `Connector`.
    """
    uid = data_validate_uid(uid)
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


def data_validate_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
    """Given some `elements`, returns a tuple of unique elements.

    :param elements:
    :param raise_error_on_duplicate:
    :return:
    """
    unique_elements = []
    for element in elements:
        if element not in unique_elements:
            unique_elements.append(element)
        elif raise_error_on_duplicate:
            raise ValueError('Duplicate elements.')
    return tuple(unique_elements)


class FormulaStructureTerms(tuple):
    """Formula Structure Terms"""

    def __hash__(self):
        return compute_formula_structure_terms_hash(self)

    def __init__(self, terms: FlexibleTerms = None):
        terms_hash: int = compute_formula_structure_terms_hash(terms)
        if terms_hash not in _formula_structure_terms:
            _formula_structure_terms[terms_hash] = self

    def __new__(cls, terms: FlexibleTerms = None):
        global _formula_structure_terms
        if isinstance(terms, FormulaStructureTerms):
            return terms
        else:
            if terms is None:
                terms = tuple()
            if isinstance(terms, tuple):
                terms: tuple[FlexibleFormulaStructure, ...] = tuple(
                    data_validate_formula_structure(term) for term in terms)
                terms_hash: int = compute_formula_structure_terms_hash(terms)
                if terms_hash in _formula_structure_terms:
                    # reuse cache.
                    return _formula_structure_terms[terms_hash]
                else:
                    return super(FormulaStructureTerms, cls).__new__(cls, terms)
        raise util.PunctiliousException('Data validation error for `Terms` `o`.', terms=terms)


class ConnectorOrderedSet(tuple):
    """A finite, computable, ordered set of connectors."""

    def __new__(cls, connectors: tuple[Connector, ...]):
        connectors: tuple = data_validate_unicity(connectors, raise_error_on_duplicate=True)
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

    def __init__(self, connectors: tuple[Connector, ...], structure: FormulaStructure,
                 representation_function: rf.Presenter | None = None):
        super(Formula, self).__init__()
        rf.Representable.__init__(self=self, representation_function=representation_function)

    def __new__(cls, connectors: tuple[Connector, ...], structure: FormulaStructure):
        connectors = data_validate_unicity(connectors, raise_error_on_duplicate=True)
        if len(connectors) == 0:
            raise ValueError('The formula `connectors` are empty.')
        elif len(connectors) != structure.connector_indexes_count:
            raise ValueError('The length of `connectors` is not equal to the number of connectors in the `structure`.')
        formula: tuple[tuple[Connector, ...], FormulaStructure] = (connectors, structure,)
        return super(Formula, cls).__new__(cls, formula)

    @property
    def connectors(self) -> tuple[Connector, ...]:
        return self[0]

    @property
    def structure(self) -> FormulaStructure:
        return self[1]


FlexibleConnector = typing.Union[Connector,]
FlexibleConnectorIndex = typing.Union[ConnectorIndex, int,]
FlexibleFormulaStructure = typing.Union[FormulaStructure, tuple[ConnectorIndex, tuple,], ConnectorIndex, int]
FlexibleTerms = typing.Union[tuple[FlexibleFormulaStructure, ...], tuple[()], None]

pass
