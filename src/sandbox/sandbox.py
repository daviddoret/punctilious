import abc
import typing

x = (1, 2, 3,)
print(type(x).__name__)
print(id(x))
y = tuple(x)
print(type(y).__name__)
print(id(y))
