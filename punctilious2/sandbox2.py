
class Parent:
    pass

class Child(Parent):
    pass

x = Child()

print(isinstance(x, Parent))

print(type(x))

