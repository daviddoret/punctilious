from __future__ import annotations

import enum
import typing


class HierarchicalEnumItemValue:
    def __init__(self, parent: typing.Optional[HierarchicalEnumItemValue]):
        self.name: typing.Optional[str] = None
        self.parent: typing.Optional[HierarchicalEnumItemValue] = parent
        self.hierarchical_name: typing.Optional[str] = None

    def __eq__(self, other):
        if isinstance(other, HierarchicalEnumItemValue):
            return hash(self) == hash(other)
        else:
            return False

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return self.hierarchical_name

    def __str__(self):
        return self.hierarchical_name


HEIV: typing.Type = HierarchicalEnumItemValue


class HierarchicalEnum:

    @staticmethod
    def load_elements(cls: type):
        """Fulfill the name and hierarchical_name attributes of enum elements."""
        # update name properties
        for attribute_name in dir(cls):
            if not callable(getattr(cls, attribute_name)) and not attribute_name.startswith("__"):
                attribute_value = getattr(cls, attribute_name)
                if isinstance(attribute_value, HierarchicalEnumItemValue):
                    attribute_value.name = attribute_name
        # update hierarchical-name properties
        for attribute_name in dir(cls):
            if not callable(getattr(cls, attribute_name)) and not attribute_name.startswith("__"):
                attribute_value = getattr(cls, attribute_name)
                if isinstance(attribute_value, HierarchicalEnumItemValue):
                    hierarchical_name: str = attribute_name
                    current_item: typing.Optional[HierarchicalEnumItemValue] = attribute_value.parent
                    while current_item is not None:
                        parent_name = current_item.name
                        hierarchical_name = f"{hierarchical_name}.{parent_name}"
                        current_item = current_item.parent
                    attribute_value.hierarchical_name = hierarchical_name


HE: typing.Type = HierarchicalEnum


class H1(HierarchicalEnum):
    FORMAL_OBJECT = HEIV(None)
    FORMULA = HEIV(FORMAL_OBJECT)
    BINARY_FORMULA = HEIV(FORMULA)


HierarchicalEnum.load_elements(H1)


class H2(HierarchicalEnum):
    FORMAL_OBJECT = HEIV(None)
    FORMULA = HEIV(FORMAL_OBJECT)
    BINARY_FORMULA = HEIV(FORMULA)


HierarchicalEnum.load_elements(H2)

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
