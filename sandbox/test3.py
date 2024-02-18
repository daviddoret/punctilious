import enum


class HierarchicalEnumItemValue:
    def __init__(self, name, parent):
        self.name = name
        self._value_ = self
        self.parent = parent

    def __repr__(self):
        return self.hierarchical_name

    def __str__(self):
        return self.name

    @property
    def hierarchical_name(self):
        hierarchical_name = self.name
        parent = self.parent
        while parent is not None:
            parent_name = parent[0]
            hierarchical_name = f"{hierarchical_name}.{parent_name}"
            parent = parent[1]
        return hierarchical_name


@enum.unique
class HierarchicalEnum(enum.Enum):

    def __new__(cls, *args):
        pass
        local_name = args[0]
        parent_tuple = args[1]
        parent_name = None if parent_tuple is None else parent_tuple[0]
        parent_element = None if parent_name is None else cls[parent_name]
        print(type(parent_element))
        obj = HierarchicalEnumItemValue(name=local_name, parent=parent_element)
        return obj

    @property
    def parent(self):
        if isinstance(self.value, HierarchicalEnumItemValue):
            return self.value.parent
        else:
            return None

    @property
    def hierarchical_name(self):
        pass
        if isinstance(self.value, HierarchicalEnumItemValue):
            return self.value.hierarchical_name
        else:
            return None


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
print(H1.FORMULA.parent)
print(H1.BINARY_FORMULA.hierarchical_name)
x = H1.BINARY_FORMULA.hierarchical_name
print(H1.FORMULA == H2.BINARY_FORMULA)
print(H1.BINARY_FORMULA == H2.BINARY_FORMULA)
print(H1.BINARY_FORMULA == H1.BINARY_FORMULA)

print('hello')

pass
