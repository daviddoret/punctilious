"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing

import log
import typesetting as ts


# Treatments

class Treatments:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Treatments, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._symbolic_representation = ts.Treatment(name="symbolic-representation")
        self._common_language = ts.Treatment(name="common-language")

    @property
    def common_language(self) -> ts.Treatment:
        """The common-language representation used in free text."""
        return self._common_language

    @property
    def symbolic_representation(self) -> ts.Treatment:
        """The formal representation used in formulas."""
        return self._symbolic_representation


treatments: Treatments = Treatments()


class Flavors:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Flavors, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        # formulas
        self._formula_function_call: ts.Flavor = ts.flavors.register(name="fl1.formula.function_call")
        self._formula_prefix_no_parenthesis: ts.Flavor = ts.flavors.register(name="fl1.formula.prefix_no_parenthesis",
            predecessor=self.formula_function_call)
        self._formula_infix: ts.Flavor = ts.flavors.register(name="fl1.formula.infix",
            predecessor=self._formula_function_call)

    @property
    def formula_function_call(self) -> ts.Flavor:
        """Typeset formulas with function notation, e.g.: f(x), g(x ,y), h(x ,y ,z), etc."""
        return self._formula_function_call

    @property
    def formula_prefix_no_parenthesis(self) -> ts.Flavor:
        """Typeset unary formulas with prefix notation and without parenthesis, e.g.: fx"""
        return self._formula_prefix_no_parenthesis

    @property
    def formula_infix(self) -> ts.Flavor:
        """Typeset binary formulas with infix notation, e.g.: x f y"""
        return self._formula_infix


flavors: Flavors = Flavors()


# TAGS

class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._formal_object = ts.tags.register(name="fl1.formal_object")
        self._formula = ts.tags.register(name="fl1.formula", predecessor=self._formal_object)
        self._atomic_formula = ts.tags.register(name="fl1.atomic_formula", predecessor=self._formula)
        self._compound_formula = ts.tags.register(name="fl1.compound_formula", predecessor=self._formula)
        self._connective = ts.tags.register(name="fl1.connective")
        self._variable_arity_connective = ts.tags.register(name="fl1.variable_arity_connective",
            predecessor=self._connective)
        self._fixed_arity_connective = ts.tags.register(name="fl1.fixed_arity_connective", predecessor=self._connective)
        self._binary_connective = ts.tags.register(name="fl1.binary_connective",
            predecessor=self._fixed_arity_connective)
        self._unary_connective = ts.tags.register(name="fl1.unary_connective", predecessor=self._fixed_arity_connective)
        self._fixed_arity_formula = ts.tags.register(name="fl1.fixed_arity_formula", predecessor=self._formal_object)
        self._binary_formula = ts.tags.register(name="fl1.binary_formula", predecessor=self._fixed_arity_formula)
        self._unary_formula = ts.tags.register(name="fl1.unary_formula", predecessor=self._fixed_arity_formula)
        self._formal_language_collection = ts.tags.register(name="fl1.formal_language_collection",
            predecessor=self._formal_object)
        self._compound_formula_collection = ts.tags.register(name="fl1.compound_formula_collection",
            predecessor=self._formal_language_collection)
        self._connective_collection = ts.tags.register(name="fl1.connective_collection",
            predecessor=self._formal_language_collection)
        self._formal_language = ts.tags.register(name="fl1.formal_language")
        self._meta_language = ts.tags.register(name="fl1.meta_language")
        self._ml1 = ts.tags.register(name="fl1.ml1")

    @property
    def atomic_formula(self) -> ts.Tag:
        return self._atomic_formula

    @property
    def binary_connective(self) -> ts.Tag:
        return self._binary_connective

    @property
    def binary_formula(self) -> ts.Tag:
        return (self._binary_formula)

    @property
    def compound_formula(self) -> ts.Tag:
        return self._compound_formula

    @property
    def compound_formula_collection(self) -> ts.Tag:
        return self._compound_formula_collection

    @property
    def connective(self) -> ts.Tag:
        return self._connective

    @property
    def connective_collection(self) -> ts.Tag:
        return self._connective_collection

    @property
    def fixed_arity_connective(self) -> ts.Tag:
        return self._fixed_arity_connective

    @property
    def fixed_arity_formula(self) -> ts.Tag:
        return self._fixed_arity_formula

    @property
    def formal_language(self) -> ts.Tag:
        return self._formal_language

    @property
    def formal_language_collection(self) -> ts.Tag:
        return self._formal_language_collection

    @property
    def formal_object(self) -> ts.Tag:
        return self._formal_object

    @property
    def formula(self) -> ts.Tag:
        return self._formula

    @property
    def meta_language(self) -> ts.Tag:
        return self._meta_language

    @property
    def ml1(self) -> ts.Tag:
        return self._ml1

    @property
    def unary_connective(self) -> ts.Tag:
        return self._unary_connective

    @property
    def unary_formula(self) -> ts.Tag:
        return self._unary_formula

    @property
    def variable_arity_connective(self) -> ts.Tag:
        return self._variable_arity_connective


tags = Tags()


class FormalObject(ts.Typesettable):
    """A formal-object is an object that is manipulated as part of a formal-system.
    """

    def __init__(self):
        super().__init__(
            default_treatment=treatments.symbolic_representation)  # Make the formal-object  # typesettable.
        self.tag(tag=tags.formal_object)

    def __repr__(self):
        return super().to_string(protocol=ts.protocols.unicode_limited, treatment=treatments.symbolic_representation)

    def __str__(self):
        return super().to_string(protocol=ts.protocols.unicode_limited, treatment=treatments.symbolic_representation)


class FormalLanguageCollection(FormalObject, abc.ABC):
    """A FormalLanguage is defined as a tuple of collections. The FormalLanguageCollection python-class is designed to
    facilitate navigation between the formal-language, its classes, and their class elements."""

    def __init__(self, formal_language: FormalLanguage):
        self._is_locked: bool = False
        self._protected_set: set[FormalObject] = set()
        self._formal_language: FormalLanguage = formal_language
        super().__init__()
        self.tag(tag=tags.formal_language_collection)

    def __contains__(self, x: FormalObject) -> bool:
        """Allows the in operator."""
        return x in self._protected_set

    def __iter__(self):
        return iter(self._protected_set)

    def __len__(self):
        return len(self._protected_set)

    def _add_formal_object(self, x: FormalObject) -> FormalObject:
        """This is a protected method, it is only intended to be called from inherited classes."""
        if self.is_locked:
            log.error(msg='This class is locked.')
        else:
            if x in self._protected_set:
                x_prime: FormalObject = next(
                    iter(x_already_present for x_already_present in self._protected_set if x_already_present == x))
                if id(x) != id(x_prime):
                    log.debug(
                        msg=f"FormalObject '{x}' (python id: {id(x)}) is already present in this FormalLanguageClass as '{x_prime}' (python id: {id(x_prime)}). The existing object is reused and the new object is discarded.")
                    # Substitute x_prime for x
                    x = x_prime
            else:
                self._protected_set.add(x)
            return x

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
        self.tag(tag=tags.formal_language)

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def _add_class(self, x: FormalLanguageCollection) -> None:
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
        self.tag(tag=tags.meta_language)

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build compound-formulas in a
    formal-language."""

    def __init__(self):
        super().__init__()
        self.tag(tag=tags.connective)


# _connective_class: FormalPythonClass = FormalPythonClass(python_class=Connective)


class VariableArityConnective(Connective):
    """A variable-arity connective, aka n-ary connective, is a connective whose arity is not predefined / fixed
    when the connective is declared, but determined when compound-formulas based on that connective are declared."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__()
        self.tag(tag=tags.variable_arity_connective)

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective whose arity is fixed and determined during the declaration of the
    connective itself."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__()
        self.tag(tag=tags.fixed_arity_connective)

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class UnaryConnective(FixedArityConnective):
    """A unary connective is a connective whose arity is fixed and equal to 1."""

    def __init__(self):
        super().__init__(arity_as_int=1)
        self.tag(tag=tags.unary_connective)


class BinaryConnective(FixedArityConnective):
    """A binary connective is a connective whose arity is fixed and equal to 2."""

    def __init__(self):
        super().__init__(arity_as_int=2)
        self.tag(tag=tags.binary_connective)


class ConnectiveCollection(FormalLanguageCollection):
    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)
        self.tag(tag=tags.connective_collection)

    def declare_unary_connective(self) -> UnaryConnective:
        x: UnaryConnective = UnaryConnective()
        self._add_formal_object(x=x)
        return x

    def declare_binary_connective(self) -> BinaryConnective:
        x: BinaryConnective = BinaryConnective()
        self._add_formal_object(x=x)
        return x


class CompoundFormulaCollection(FormalLanguageCollection):
    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)
        self.tag(tag=tags.compound_formula_collection)

    def declare_unary_formula(self, connective: UnaryConnective, term: FormalObject) -> UnaryFormula:
        x: UnaryFormula = UnaryFormula(formal_language_collection=self, connective=connective, term=term)
        x = self._add_formal_object(x=x)
        return x

    def declare_binary_formula(self, connective: BinaryConnective, term_1: FormalObject, term_2: FormalObject) -> (
        BinaryFormula):
        x: BinaryFormula = BinaryFormula(formal_language_collection=self, connective=connective, term_1=term_1,
            term_2=term_2)
        x = self._add_formal_object(x=x)
        return x


class Formula(FormalObject):
    def __init__(self):
        super().__init__()
        self.tag(tag=tags.formula)


class AtomicFormula(FormalObject):
    def __init__(self, formal_language: FormalLanguage):
        self._formal_language = formal_language
        super().__init__()
        self.tag(tag=tags.atomic_formula)

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language


class CompoundFormula(Formula):
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
        self.tag(tag=tags.compound_formula)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.connective, self.terms,))

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

    def __init__(self, connective: FixedArityConnective, terms: typing.Tuple[FormalObject, ...]):
        super().__init__(connective=connective, terms=terms)
        self.tag(tag=tags.fixed_arity_formula)


class UnaryFormula(FixedArityFormula):
    """A unary-formula is a formula with a fixed unary connective."""

    def __init__(self, connective: UnaryConnective, term: FormalObject):
        super().__init__(connective=connective, terms=(term,))
        self.tag(tag=tags.unary_formula)

    @property
    def term(self) -> FormalObject:
        return self.terms[0]


class BinaryFormula(FixedArityFormula):
    """A binary-formula is a formula with a fixed binary connective."""

    def __init__(self, connective: BinaryConnective, term_1: FormalObject, term_2: FormalObject):
        super().__init__(connective=connective, terms=(term_1, term_2,))
        self.tag(tag=tags.binary_formula)

    @property
    def term_1(self) -> FormalObject:
        return self.terms[0]

    @property
    def term_2(self) -> FormalObject:
        return self.terms[1]


class ML1(FormalLanguageCollection, abc.ABC):
    """ML1 is a rather minimalist meta-language designed to facilite the construction of formal-languages."""

    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language)
        self.tag(tag=tags.ml1)


def iterate_formula_elements(phi: FormalObject):
    """Iterate through formulas, returning the compound-formula objects, their connectives, and terms, recursively. The order is reproducible: formula terms are read from left to right, depth-first."""
    yield phi
    if isinstance(phi, CompoundFormula):
        phi: CompoundFormula
        yield phi.connective
        for term in phi.terms:
            yield term


def generate_unique_values(generator):
    """Utility function that yields only unique values from a generator."""
    observed_values = set()
    for value in generator():
        if value not in observed_values:
            observed_values.add(value)
            yield value


def substitute_formula_elements_from_map(phi, map):
    # TODO: Implement
    pass


log.debug(f"Module {__name__}: loaded.")
