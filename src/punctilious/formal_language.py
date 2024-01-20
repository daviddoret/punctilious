"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing
import typesetting
import log


class FormalObject(typesetting.TypesettableObject):
    """A formal-object is an object that is manipulated as part of a formal-system.

    A formal-object may be declared as an atomic-formula in a formal-language. Then, it can be viewed as a formula
    composed of a 0-arity connective and no terms.
    """

    def __init__(self):
        super().__init__()


class FormalClass(FormalObject, abc.ABC):
    """A formal-class is a formal-object for which a has-element relation is defined."""

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def has_element(self, x: FormalObject) -> bool:
        """Return True if x is an element of the formal-class."""
        log.error(msg='Abstract method.')


class FormalPythonClass(FormalClass):
    """A formal-python-class is a formal-class that is linked to a python-class,
    where the python-class is interpreted as the definition of the formal-class,
    with all instances of the python-class interpreted as members of the formal-class,
    and nothing else."""

    def __init__(self, python_class: type):
        super().__init__()
        self._python_class = python_class

    def has_element(self, x: FormalObject) -> bool:
        """Return True if x is an element of the formal-class."""
        return isinstance(x, self.python_class)

    @property
    def python_class(self) -> type:
        return self._python_class


class AccretorTuple(FormalObject, abc.ABC):
    """An accretor-tuple is generic collection that allows the addition of elements of a certain python-type,
    but not their removal."""

    def __init__(self, valid_python_types: typing.Optional[tuple[type, ...]]):
        self._is_locked = False
        self._container = set()
        self._valid_python_types: typing.Optional[tuple[type], ...] = valid_python_types
        super().__init__()

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def add(self, element: object):
        if self._is_locked:
            log.error(msg='Trying to call add() on a locked Accretor.')
        if self._valid_python_types is not None and not (any(isinstance(element, t) for t in self.valid_python_types)):
            log.error(msg='Invalid python-type when adding element to accretor.')
        self._container.add(element)

    def lock(self):
        """Forbid the further addition of elements in the accretor."""
        self._is_locked = True

    def remove(self, element: object):
        raise Exception('The Accretor class forbids the removal of elements.')

    @property
    def valid_python_types(self) -> typing.Optional[tuple[type], ...]:
        return self._valid_python_types


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build compound-formulas in a
    formal-language."""

    def __init__(self):
        super().__init__()


class VariableArityConnective(Connective):
    """A variable-arity connective, aka n-ary connective, is a connective whose arity is not predefined / fixed
    when the connective is declared, but determined when compound-formulas based on that connective are declared."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__()

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective whose arity is fixed and determined during the declaration of the
    connective itself."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__()

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class UnaryConnective(FixedArityConnective):
    """A unary connective is a connective whose arity is fixed and equal to 1."""

    def __init__(self):
        super().__init__(arity_as_int=1)


class BinaryConnective(FixedArityConnective):
    """A binary connective is a connective whose arity is fixed and equal to 2."""

    def __init__(self):
        super().__init__(arity_as_int=2)


class CompoundFormula(FormalObject):
    """A compound-formula is a formal-object and a tree-structure of atomic-formulas and compound-formulas."""

    def __init__(self, connective: Connective, terms: typing.Tuple[FormalObject]):
        if isinstance(connective, FixedArityConnective):
            if connective.arity_as_int != len(terms):
                log.error(msg='The number of arguments is not equal to the arity of the fixed-arity-connective.')
        elif isinstance(connective, VariableArityConnective):
            pass
        else:
            log.error(msg='Unsupported connective python class.')
        self._connective = connective
        self._terms = terms
        super().__init__()

    @property
    def arity_as_int(self) -> int:
        # This is also valid for both variable- and fixed-arity connectives.
        return len(self.terms)

    @property
    def connective(self) -> Connective:
        return self._connective

    @property
    def terms(self) -> typing.Tuple[FormalObject]:
        return self._terms


class FixedArityFormula(CompoundFormula):
    """A fixed-arity-formula is a formula with a fixed-arity connective."""

    def __init__(self, connective: FixedArityConnective, terms: typing.Tuple[FormalObject]):
        super().__init__(connective=connective, terms=terms)


class UnaryFormula(FixedArityFormula):
    """A unary-formula is a formula with a fixed unary connective."""

    def __init__(self, connective: UnaryConnective, term: FormalObject):
        super().__init__(connective=connective, terms=(term,))

    @property
    def term(self) -> FormalObject:
        return self.terms[0]


class BinaryFormula(FixedArityFormula):
    """A binary-formula is a formula with a fixed binary connective."""

    def __init__(self, connective: BinaryConnective, term_1: FormalObject, term_2: FormalObject):
        super().__init__(connective=connective, terms=(term_1, term_2,))

    @property
    def term_1(self) -> FormalObject:
        return self.terms[0]

    @property
    def term_2(self) -> FormalObject:
        return self.terms[1]


class FormalLanguage(AccretorTuple):
    """A formal language is defined as an accretor-tuple of formal-objects."""

    def __init__(self):
        super().__init__(valid_python_types=(FormalObject,))


class FormalClassAccretorTuple(AccretorTuple):
    def __init__(self):
        super().__init__(valid_python_types=(FormalClass,))


class MetaLanguageClassAccretor(FormalClassAccretorTuple):
    def __init__(self):
        super().__init__()
        self._connective_class: FormalPythonClass = FormalPythonClass(python_class=Connective)
        self.add(element=self._connective_class)
        self._formal_object_class: FormalPythonClass = FormalPythonClass(python_class=FormalObject)
        self.add(element=self._formal_object_class)

    @property
    def connective_class(self) -> FormalPythonClass:
        """The class of all connectives."""
        return self._connective_class

    @property
    def formal_object_class(self) -> FormalPythonClass:
        """The class of all formal-objects."""
        return self._formal_object_class


class MetaLanguage(FormalLanguage):
    """The basic punctilious meta-language implements some punctilious fundamental classes,
    and may be extended to define meta-languages with complementary classes."""

    def __init__(self):
        super().__init__()
        self._formal_classes: MetaLanguageClassAccretor = MetaLanguageClassAccretor()
        self.add(element=self._formal_classes)

    @property
    def formal_classes(self) -> MetaLanguageClassAccretor:
        return self._formal_classes
