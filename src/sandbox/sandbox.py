class Parent:

    def __init__(self, identifier: str):
        self.identifier = identifier

    @property
    def parent_hash(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self.identifier,))

    @property
    def parent_class(self):
        return self.__class__


class Child(Parent):

    def __init__(self, identifier: str):
        super().__init__(identifier=identifier)

    @property
    def child_hash(self):
        # hash only spans the properties that uniquely identify the object.
        return hash((self.__class__, self.identifier,))

    @property
    def child_class(self):
        return self.__class__


parent_a = Parent('a')
parent_b = Parent('b')
child_a = Child('a')
child_b = Child('b')

pass
