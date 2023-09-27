import typing
from typing import Optional, Union

# MyArg = collections.namedtuple('MyArg', ['x', 'y'])
super_type = Optional[Union[int, float, str]]


class MyArg(typing.NamedTuple):
    x: super_type
    y: int


MyArg2 = typing.NamedTuple('MyArg2', )

t = MyArg(x=1, y=2)
print(t)
print(type(t))
print(type(MyArg))
