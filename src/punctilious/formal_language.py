# special features
from __future__ import annotations

import typing
# external packages
import uuid

import const
import representation_foundation as rf


def ensure_uid(o: uuid.UUID) -> uuid.UUID:
    """Performs data validation on a presumed uid `o`.

    :param o:
    :return:
    """
    if o is None:
        raise ValueError('A uid cannot be None.')
    elif not isinstance(o, uuid.UUID):
        raise ValueError('A uid cannot be of a different type than `uuid.UUID`.')
    else:
        return o


def ensure_pointer(o: int) -> int:
    """Performs data validation on a presumed pointer `o`.

    :param o:
    :return:
    """
    if o is None:
        raise ValueError('A pointer cannot be None.')
    elif not isinstance(o, int):
        raise ValueError('A pointer cannot be of a different type than `int`.')
    elif o < 0:
        raise ValueError('A pointer cannot be negative.')
    else:
        return o


def ensure_formula_pointer(o: int) -> int:
    """Performs data validation on a presumed formula-pointer `o`.
    Convert `o` for FormulaPoint implicitly if necessary.
    """
    if o is None:
        raise ValueError('A formula-pointer cannot be None.')
    elif not isinstance(o, FormulaPointer):
        raise ValueError('A formula-point cannot be of a different type than `FormulaPointer`.')
    else:
        return o


def ensure_formula_structure(o: FormulaStructure, fix_tuple_with_structure: bool = True) -> FormulaStructure:
    """Performs data validation on a presumed Structure `o`.

    :param o:
    :param fix_tuple_with_structure:
    :return:
    """
    if o is None:
        raise ValueError('A structure cannot be None.')
    elif not isinstance(o, FormulaStructure):
        if fix_tuple_with_structure and isinstance(o, tuple) and len(o) == 2:
            # implicit conversion of equivalent tuple into structure.
            structure = FormulaStructure(root=o[0], sub_structures=o[1])
            return structure
        raise ValueError('A structure cannot be of a different type than `Structure`.')
    else:
        return o


def ensure_sub_structures(o: tuple[FormulaStructure, ...], fix_none_with_empty: bool = True,
                          fix_tuple_with_structure: bool = True) -> tuple[FormulaStructure, ...]:
    """Performs data validation on a presumed tuple of Structure `o`.

    :param o:
    :param fix_none_with_empty:
    :param fix_tuple_with_structure:
    :return:
    """
    if o is None:
        if fix_none_with_empty:
            return tuple()
        else:
            raise ValueError('A tuple of structures cannot be None.')
    elif not isinstance(o, tuple):
        raise ValueError('A tuple of structures cannot be of a different type than `tuple`.')
    elif not all(isinstance(structure, FormulaStructure) for structure in o):
        if fix_tuple_with_structure:
            # implicit conversion of equivalent tuples into structures.
            structures = tuple(ensure_formula_structure(o=structure) for structure in o)
            return structures
        raise ValueError('A tuple of structures cannot be of a different type than `Structure`.')
    else:
        return o


def compute_structure_hash(root: int, sub_structures: tuple[FormulaStructure, ...] = tuple()):
    """Given its components, returns the hash of a `Structure`.
    """
    root = ensure_pointer(root)
    sub_structures = ensure_sub_structures(sub_structures, fix_none_with_empty=True, fix_tuple_with_structure=True)
    return hash((const.formula_structure_hash_prime, FormulaStructure, root, sub_structures,))


_formula_structures: dict[int, FormulaStructure] = {}
_formula_pointers: dict[int, FormulaPointer] = {}


class FormulaPointer(int):
    """A `FormulaPointer` is a natural number (whose first element is mapped to 0),
    that is used to build formula-structures."""

    def __hash__(self):
        return compute_pointer_hash(self)

    def __new__(cls, n: int) -> FormulaPointer:
        global _formula_pointers
        if not isinstance(n, int):
            raise ValueError('`i` must be of type `int`.')
        formula_pointer_hash: int = compute_pointer_hash(n)
        if formula_pointer_hash in _formula_pointers:
            return _formula_pointers[formula_pointer_hash]
        elif isinstance(n, FormulaPointer):
            return n
        else:
            formula_pointer = super(FormulaPointer, cls).__new__(cls, n)
            _formula_pointers[formula_pointer_hash] = formula_pointer
            return formula_pointer


def compute_pointer_hash(i: int):
    return hash((const.formula_pointer_hash_prime, FormulaPointer, i))


class FormulaStructure(tuple):
    """A `FormulaStructure` is an abstract formula structure, independent of connectors.

    """

    def __hash__(self):
        return compute_structure_hash(root=self.root, sub_structures=self.sub_structures)

    def __init__(self, root: int, sub_structures: tuple[FormulaStructure, ...] = tuple()):
        global _formula_structures
        super(FormulaStructure, self).__init__()
        # `is_canonical` is cached, because this property will be pervasively necessary.
        is_canonical, _ = self.check_canonicity()
        self._is_canonical: bool = is_canonical
        pointers = [self.root]
        for sub_structure in self.sub_structures:
            for pointer in sub_structure.pointers:
                if pointer not in pointers:
                    pointers.append(pointer)
        pointers = sorted(pointers)
        self._pointers: tuple[int, ...] = tuple(pointers)
        structure_hash: int = compute_structure_hash(root=root, sub_structures=sub_structures)
        _formula_structures[structure_hash] = self

    def __new__(cls, root: int, sub_structures: tuple[FormulaStructure, ...] = tuple()):
        global _formula_structures
        root: int = ensure_pointer(root)
        sub_structures: tuple[FormulaStructure, ...] = ensure_sub_structures(o=sub_structures, fix_none_with_empty=True)
        structure_hash: int = compute_structure_hash(root=root, sub_structures=sub_structures)
        if structure_hash in _formula_structures:
            return _formula_structures[structure_hash]
        else:
            structure = super(FormulaStructure, cls).__new__(cls, (root, sub_structures,))
            return structure

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
        for sub_structure in self.sub_structures:
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

        A formula is well-formed only if its structure is canonical.

        :return:
        """
        return self._is_canonical

    @property
    def is_leaf(self) -> bool:
        """Returns `True` if the structure is a leaf, `False` otherwise.

        A structure is a leaf if and only if it contains no sub-structures.
        """
        return len(self.sub_structures) == 0

    @property
    def pointers(self) -> tuple[int, ...]:
        """Returns

        :return:
        """
        return self._pointers

    @property
    def pointers_count(self):
        """Returns the number of distinct counters in the structure.
        """
        return len(self.pointers)

    @property
    def root(self) -> int:
        """The root pointer of the structure.

        :return:
        """
        return self[0]

    @property
    def sub_structures(self) -> tuple[FormulaStructure]:
        """The tuple of sub-structures contained in this structure.

        :return:
        """
        return self[1]


_connectors: dict[int, Connector] = {}


def compute_connector_hash(uid: uuid.UUID):
    """Given its components, returns the hash of a `Connector`.
    """
    uid = ensure_uid(uid)
    return hash((const.connector_hash_prime, Connector, uid,))


class Connector(rf.Representable):
    """A `Connector` is a formula symbolic component."""

    def __call__(self, *args):
        """Return a formula with this connector as the root connector, and the arguments as its arguments."""
        pass

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return compute_connector_hash(uid=self.uid)

    def __init__(self, uid: uuid.UUID | None = None, representation_function: rf.RepresentationFunction | None = None):
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
        return hash(self) != hash(other)

    @property
    def uid(self) -> uuid.UUID:
        return self._uid


def ensure_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
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


class Formula(tuple, rf.Representable):
    """A `Formula` is a pair (C, S) where:
     - C is a non-empty, finite and ordered set of connectors.
     - S is a formula structure.
    """

    def __init__(self, connectors: tuple[Connector, ...], structure: FormulaStructure,
                 representation_function: rf.RepresentationFunction | None = None):
        super(Formula, self).__init__()
        rf.Representable.__init__(self=self, representation_function=representation_function)

    def __new__(cls, connectors: tuple[Connector, ...], structure: FormulaStructure):
        connectors = ensure_unicity(connectors, raise_error_on_duplicate=True)
        if len(connectors) == 0:
            raise ValueError('The formula `connectors` are empty.')
        elif len(connectors) != structure.pointers_count:
            raise ValueError('The length of `connectors` is not equal to the number of connectors in the `structure`.')
        formula: tuple[tuple[Connector, ...], FormulaStructure] = (connectors, structure,)
        return super(Formula, cls).__new__(cls, formula)

    @property
    def connectors(self) -> tuple[Connector, ...]:
        return self[0]

    @property
    def structure(self) -> FormulaStructure:
        return self[1]


pass
