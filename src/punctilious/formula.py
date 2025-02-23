# special features
from __future__ import annotations

_pointers: list[Pointer] = list()


class Pointer(int):

    def __init__(self, index):
        super().__init__()

    def __new__(cls, index: int):
        return super().__new__(cls, index)

    def __str__(self):
        return f'p{super().__str__()}'


_p0 = Pointer(0)


class Structure(tuple):

    def __init__(self, root: Pointer, sub_structures: tuple[Structure] = tuple()):
        super().__init__()
        # `is_canonical` is cached, because this property will be pervasively necessary.
        is_canonical, _ = self.check_canonicity()
        self._is_canonical: bool = is_canonical

    def __new__(cls, root: Pointer, sub_structures: tuple[Structure] = tuple()):
        structure: tuple[root, sub_structures] = (root, sub_structures,)
        return super().__new__(cls, structure)

    def check_canonicity(self, max_pointer: Pointer | None = None) -> tuple[bool, Pointer | None]:
        if max_pointer is None:
            if self.root != 0:
                # this is a root structure, but its pointer is not p0.
                return False, None
            else:
                max_pointer: Pointer = self.root
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
    def is_leaf(self) -> bool:
        """Returns `True` if the structure is a leaf, `False` otherwise.

        A structure is a leaf if and only if it contains no sub-structures."""
        return len(self.sub_structures) == 0

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
    def root(self) -> Pointer:
        return self[0]

    @property
    def sub_structures(self) -> tuple[Structure]:
        return self[1]


pass
