"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing
import typesetting


class Accretor(set, abc.ABC):
    """A generic collection that allows the addition of elements of a certain python-type, but not their removal."""

    def __init__(self):
        self._container = set()
        super().__init__()

    def add(self, element: object):
        self._container.add(element)

    def remove(self, element: object):
        raise Exception('The Accretor class forbids the removal of elements.')


class FormalObject(typesetting.TypesettableObject):
    def __init__(self):
        super().__init__()


class AtomicObject(FormalObject):
    """An atomic-object is a formal-object that may be used as a leaf object to build formulas in a formal-language."""

    def __init__(self):
        super().__init__()


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build formulas in a formal-language."""

    def __init__(self):
        super().__init__()


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective whose arity is fixed and determined during initialization."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__()

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class Formula(FormalObject):
    """A formula is a tree"""

    def __init__(self, connective, *args):
        self._connective = connective
        if isinstance(connective, FixedArityConnective):
            if len(args) != connective.arity_as_int:
                raise Exception("OOOPS")
        self._args = args
        super().__init__()


class FormalLanguage(Accretor):
    def __init__(self):
        super().__init__()
