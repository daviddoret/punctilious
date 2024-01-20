"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing
import typesetting
import log


class FormalObject(typesetting.TypesettableObject):
    """A formal-object is an object that is manipulated as part of a formal-system.
    """

    def __init__(self):
        super().__init__()


class FormalLanguageClass(FormalObject, abc.ABC):
    """A FormalLanguage is defined as a tuple of class. The FormalLanguageClass python-class is designed to
    facilitate navigation between the formal-language, its classes, and their class elements."""

    def __init__(self, formal_language: FormalLanguage):
        self._is_locked: bool = False
        self._container: set[FormalObject] = set()
        self._formal_language: FormalLanguage = formal_language
        super().__init__()

    def __contains__(self, x: FormalObject) -> bool:
        """Allows the in operator."""
        return x in self._container

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def _add_formal_object(self, x: FormalObject) -> None:
        """This is a protected method, it is only intended to be called from inherited classes."""
        if self.is_locked:
            log.error(msg='This class is locked.')
        else:
            self._container.add(x)

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def lock(self):
        """Forbid the further addition of elements in the accretor."""
        self._is_locked = True


class FormalLanguage(FormalObject, abc.ABC):
    """A formal language is defined as an accretor-tuple of accretor-tuples."""

    def __init__(self):
        self._is_locked: bool = False
        self._container: set = set()
        super().__init__()

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def _add_class(self, x: FormalLanguageClass) -> None:
        """This is a protected method, it is only intended to be called from inherited classes."""
        if self.is_locked:
            log.error(msg='This formal-language is locked.')
        else:
            self._container.add(x)

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def lock(self):
        """Forbid the further addition of elements in the accretor."""
        self._is_locked = True


class MetaLanguage(FormalLanguage):
    """A meta-language is a formal-language that is linked to another formal-language and denoted as the
    meta-language of that formal-language."""

    def __init__(self, formal_language: FormalLanguage):
        super().__init__()
        self._formal_language = formal_language

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build compound-formulas in a
    formal-language."""

    def __init__(self):
        super().__init__()


# _connective_class: FormalPythonClass = FormalPythonClass(python_class=Connective)


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


class ConnectiveClass(FormalLanguageClass):
    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)

    def declare_unary_connective(self) -> UnaryConnective:
        x: UnaryConnective = UnaryConnective()
        self._add_formal_object(x=x)
        return x

    def declare_binary_connective(self) -> BinaryConnective:
        x: BinaryConnective = BinaryConnective()
        self._add_formal_object(x=x)
        return x


class FormulaClass(FormalLanguageClass):
    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)

    def declare_unary_formula(self, connective: UnaryConnective, term: FormalObject) -> UnaryFormula:
        x: UnaryFormula = UnaryFormula(connective=connective, term=term)
        self._add_formal_object(x=x)
        return x

    def declare_binary_formula(self, connective: BinaryConnective, term_1: FormalObject, term_2: FormalObject) -> (
        BinaryFormula):
        x: BinaryFormula = BinaryFormula(connective=connective, term_1=term_1, term_2=term_2)
        self._add_formal_object(x=x)
        return x


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


class ML1(FormalLanguageClass, abc.ABC):
    """ML1 is a rather minimalist meta-language designed to facilite the construction of formal-languages."""

    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)
