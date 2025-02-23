# special features
from __future__ import annotations

import typing
# external packages
import uuid


class Structure(tuple):
    """A `Structure` is an abstract formula structure, independent of connectors.

    """

    def __init__(self, root: int, sub_structures: tuple[Structure, ...] = tuple()):
        super(Structure, self).__init__()
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

    def __new__(cls, root: int, sub_structures: tuple[Structure, ...] = tuple()):
        if root < 0:
            raise ValueError('The value of a pointer cannot be negative.')
        structure: tuple[root, sub_structures] = (root, sub_structures,)
        return super(Structure, cls).__new__(cls, structure)

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
    def sub_structures(self) -> tuple[Structure]:
        """The tuple of sub-structures contained in this structure.

        :return:
        """
        return self[1]


class Connector:
    """A `Connector` is a formula symbolic component."""

    def __call__(self, *args):
        """Return a formula with this connector as the root connector, and the arguments as its arguments."""
        pass

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((type(self), self.uid))

    def __init__(self, uid: uuid.UUID | None = None):
        if uid is None:
            # Assigns automatically a new uid
            uid: uuid.UUID = uuid.uuid4()
        self._uid = uid
        super(Connector, self).__init__()

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __repr__(self):
        return f'{self.uid}'

    def __str__(self):
        return f'{self.uid}'

    @property
    def uid(self) -> uuid.UUID:
        return self._uid


def ensure_unicity(elements: typing.Iterable, raise_error_on_duplicate: bool = True) -> tuple:
    """Returns a

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


class Formula(tuple):
    """A `Formula` is a pair (C, S) where:
     - C is a finite and ordered set of connectors.
     - S is a formula structure.
    """

    def __init__(self, connectors: tuple[Connector, ...], structure: Structure):
        super(Formula, self).__init__()

    def __new__(cls, connectors: tuple[Connector, ...], structure: Structure):
        connectors = ensure_unicity(connectors, raise_error_on_duplicate=True)
        if len(connectors) != structure.pointers_count:
            raise ValueError('The length of `connectors` is not equal to the number of connectors in the `structure`.')
        formula: tuple[tuple[Connector, ...], Structure] = (connectors, structure,)
        return super(Formula, cls).__new__(cls, formula)


pass
