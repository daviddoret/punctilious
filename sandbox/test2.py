import dataclasses
import enum
import typing


@enum.unique
class HierarchicalEnum(enum.Enum):

    def __init__(self, *args):
        local_name = args[0]
        self.local_name = local_name
        parent_tuple = args[1]
        self.parent_tuple = parent_tuple
        hierarchical_name = self.local_name
        while parent_tuple is not None:
            parent_name = parent_tuple[0]
            hierarchical_name = f"{hierarchical_name}.{parent_name}"
            parent_tuple = parent_tuple[1]
        self.hierarchical_name = hierarchical_name


class H1(HierarchicalEnum):
    FORMAL_OBJECT = "FORMAL_OBJECT", None
    FORMULA = "FORMULA", FORMAL_OBJECT
    BINARY_FORMULA = "BINARY_FORMULA", FORMULA


class H2(HierarchicalEnum):
    FORMAL_OBJECT = "FORMAL_OBJECT", None
    FORMULA = "FORMULA", FORMAL_OBJECT
    BINARY_FORMULA = "BINARY_FORMULA", FORMULA


print(H1.FORMAL_OBJECT)
print(H1.FORMULA)
print(H1.FORMULA.parent_tuple)
print(H1.BINARY_FORMULA.hierarchical_name)

print(H1.FORMULA == H2.BINARY_FORMULA)
print(H1.BINARY_FORMULA == H2.BINARY_FORMULA)
print(H1.BINARY_FORMULA == H1.BINARY_FORMULA)

print('hello')

pass
