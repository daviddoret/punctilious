# import punctilious as pu

from abc import ABC


class ITopLevel(ABC):  # Abstract base class
    pass


class ISecondLevel(ITopLevel, ABC):  # Also an abstract base class
    pass


class HelloWorld(ITopLevel):  # Concrete class
    pass


x = HelloWorld()

pass
