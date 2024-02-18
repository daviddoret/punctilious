import dataclasses
import enum


class Element:
    def __init__(self, name, superclass):
        self.name = name
        self.superclass = superclass

    def __hash__(self):
        return hash(id(self))


class MyEnum(enum.Enum):
    FORMAL_OBJECT = Element("FORMAL_OBJECT", None)
    FORMULA = Element("FORMULA", FORMAL_OBJECT)


print(MyEnum.FORMAL_OBJECT)
print(MyEnum.FORMULA)
print(MyEnum.FORMULA.value.superclass)
