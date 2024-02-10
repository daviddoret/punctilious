"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing

import log
import typesetting as ts


# Representations

class Representations:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Representations, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()


representations: Representations = Representations()


# TAGS

class TypesettingClasses:
    """A collection of typesetting-classes."""
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(TypesettingClasses, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._formal_object = ts.typesetting_classes.register(name="fl1.formal_object",
            superclass=ts.typesetting_classes.typesettable)
        self._formula = ts.typesetting_classes.register(name="fl1.formula", superclass=self.formal_object)
        self._atomic_formula = ts.typesetting_classes.register(name="fl1.atomic_formula", superclass=self._formula)
        self._compound_formula = ts.typesetting_classes.register(name="fl1.compound_formula", superclass=self._formula)
        self._connective = ts.typesetting_classes.register(name="fl1.connective", superclass=self.formal_object)
        self._variable_arity_connective = ts.typesetting_classes.register(name="fl1.variable_arity_connective",
            superclass=self._connective)
        self._fixed_arity_connective = ts.typesetting_classes.register(name="fl1.fixed_arity_connective",
            superclass=self._connective)
        self._binary_connective = ts.typesetting_classes.register(name="fl1.binary_connective",
            superclass=self._fixed_arity_connective)
        self._unary_connective = ts.typesetting_classes.register(name="fl1.unary_connective",
            superclass=self._fixed_arity_connective)
        self._fixed_arity_formula = ts.typesetting_classes.register(name="fl1.fixed_arity_formula",
            superclass=self._compound_formula)
        self._binary_formula = ts.typesetting_classes.register(name="fl1.binary_formula",
            superclass=self._fixed_arity_formula)
        self._unary_formula = ts.typesetting_classes.register(name="fl1.unary_formula",
            superclass=self._fixed_arity_formula)
        self._formal_language_collection = ts.typesetting_classes.register(name="fl1.formal_language_collection",
            superclass=self._formal_object)
        self._compound_formula_collection = ts.typesetting_classes.register(name="fl1.compound_formula_collection",
            superclass=self._formal_language_collection)
        self._connective_collection = ts.typesetting_classes.register(name="fl1.connective_collection",
            superclass=self._formal_language_collection)
        self._formal_language = ts.typesetting_classes.register(name="fl1.formal_language",
            superclass=self.formal_object)
        self._meta_language = ts.typesetting_classes.register(name="fl1.meta_language", superclass=self.formal_language)
        self._ml1 = ts.typesetting_classes.register(name="fl1.ml1", superclass=self.formal_language)
        self._axiom = ts.typesetting_classes.register(name="fl1.axiom", superclass=self.formula)

    @property
    def atomic_formula(self) -> ts.TypesettingClass:
        return self._atomic_formula

    @property
    def axiom(self) -> ts.TypesettingClass:
        return self._axiom

    @property
    def binary_connective(self) -> ts.TypesettingClass:
        return self._binary_connective

    @property
    def binary_formula(self) -> ts.TypesettingClass:
        return (self._binary_formula)

    @property
    def compound_formula(self) -> ts.TypesettingClass:
        return self._compound_formula

    @property
    def compound_formula_collection(self) -> ts.TypesettingClass:
        return self._compound_formula_collection

    @property
    def connective(self) -> ts.TypesettingClass:
        return self._connective

    @property
    def connective_collection(self) -> ts.TypesettingClass:
        return self._connective_collection

    @property
    def fixed_arity_connective(self) -> ts.TypesettingClass:
        return self._fixed_arity_connective

    @property
    def fixed_arity_formula(self) -> ts.TypesettingClass:
        return self._fixed_arity_formula

    @property
    def formal_language(self) -> ts.TypesettingClass:
        return self._formal_language

    @property
    def formal_language_collection(self) -> ts.TypesettingClass:
        return self._formal_language_collection

    @property
    def formal_object(self) -> ts.TypesettingClass:
        return self._formal_object

    @property
    def formula(self) -> ts.TypesettingClass:
        return self._formula

    @property
    def meta_language(self) -> ts.TypesettingClass:
        return self._meta_language

    @property
    def ml1(self) -> ts.TypesettingClass:
        return self._ml1

    @property
    def unary_connective(self) -> ts.TypesettingClass:
        return self._unary_connective

    @property
    def unary_formula(self) -> ts.TypesettingClass:
        return self._unary_formula

    @property
    def variable_arity_connective(self) -> ts.TypesettingClass:
        return self._variable_arity_connective


typesetting_classes = TypesettingClasses()


class FormalObject(ts.Typesettable):
    """A formal-object is an object that is manipulated as part of a formal-system.
    """

    def __init__(self, tc: typing.Optional[ts.TypesettingClass] = None,
        default_rep: typing.Optional[ts.Representation] = None):
        if tc is None:
            tc = typesetting_classes.formal_object
        elif not tc.is_subclass_of(c=typesetting_classes.formal_object):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        if default_rep is None:
            default_rep = ts.representations.symbolic_representation
        super().__init__(tc=tc, default_rep=default_rep)

    def __repr__(self):
        return super().to_string(protocol=ts.protocols.unicode_limited,
            representation=ts.representations.symbolic_representation)

    def __str__(self):
        return super().to_string(protocol=ts.protocols.unicode_limited,
            representation=ts.representations.symbolic_representation)


class FormalLanguageCollection(FormalObject, abc.ABC):
    """A FormalLanguage is defined as a tuple of collections. The FormalLanguageCollection python-class is designed to
    facilitate navigation between the formal-language, its classes, and their class elements."""

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TypesettingClass] = None,
        default_rep: typing.Optional[ts.Representation] = None):
        self._is_locked: bool = False
        self._protected_set: set[FormalObject] = set()
        self._formal_language: FormalLanguage = formal_language
        if tc is None:
            tc = typesetting_classes.formal_object
        elif not tc.is_subclass_of(c=typesetting_classes.formal_object):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        # if default_rep is None:
        #     default_rep = ts.representations.symbolic_representation
        super().__init__(tc=tc, default_rep=default_rep)

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

    def __init__(self, tc: typing.Optional[TypesettingClass] = None):
        if tc is None:
            tc = typesetting_classes.formal_language
        elif not tc.is_subclass_of(c=typesetting_classes.formal_language):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(tc=tc, default_rep=ts.representations.symbolic_representation)
        self._is_locked: bool = False
        self._container: set = set()

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
        self.declare_typesetting_class_element(typesetting_class=typesetting_classes.meta_language)

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build compound-formulas in a
    formal-language."""

    def __init__(self, tc: typing.Optional[ts.TypesettingClass] = None):
        if tc is None:
            tc = typesetting_classes.connective
        elif not tc.is_subclass_of(c=typesetting_classes.connective):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(tc=tc)


# _connective_class: FormalPythonClass = FormalPythonClass(python_class=Connective)


class VariableArityConnective(Connective):
    """A variable-arity connective, aka n-ary connective, is a connective whose arity is not predefined / fixed
    when the connective is declared, but determined when compound-formulas based on that connective are declared."""

    def __init__(self, arity_as_int: int):
        self._arity_as_int = arity_as_int
        super().__init__(tc=typesetting_classes.variable_arity_connective)

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective whose arity is fixed and determined during the declaration of the
    connective itself."""

    def __init__(self, arity_as_int: int, tc: typing.Optional[ts.TypesettingClass] = None):
        self._arity_as_int = arity_as_int
        if tc is None:
            tc = typesetting_classes.fixed_arity_connective
        elif not tc.is_subclass_of(c=typesetting_classes.fixed_arity_connective):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(tc=tc)

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class UnaryConnective(FixedArityConnective):
    """A unary connective is a connective whose arity is fixed and equal to 1."""

    def __init__(self, tc: typing.Optional[ts.TypesettingClass] = None):
        if tc is None:
            tc = typesetting_classes.unary_connective
        elif not tc.is_subclass_of(c=typesetting_classes.unary_connective):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(arity_as_int=1, tc=tc)


class BinaryConnective(FixedArityConnective):
    """A binary connective is a connective whose arity is fixed and equal to 2."""

    def __init__(self, tc: typing.Optional[ts.TypesettingClass] = None):
        if tc is None:
            tc = typesetting_classes.binary_connective
        elif not tc.is_subclass_of(c=typesetting_classes.binary_connective):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(arity_as_int=2, tc=tc)


class ConnectiveCollection(FormalLanguageCollection):
    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.connective_collection)
        super().__init__(formal_language=formal_language, tc=tc)

    def declare_unary_connective(self, tc: typing.Optional[ts.TypesettingClass]) -> UnaryConnective:
        x: UnaryConnective = UnaryConnective(tc=tc)
        self._add_formal_object(x=x)
        return x

    def declare_binary_connective(self, tc: typing.Optional[ts.TypesettingClass]) -> BinaryConnective:
        x: BinaryConnective = BinaryConnective(tc=tc)
        self._add_formal_object(x=x)
        return x


class CompoundFormulaCollection(FormalLanguageCollection):

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TypesettingClass] = None,
        default_rep: typing.Optional[ts.Representation] = None):
        if tc is None:
            tc = typesetting_classes.formal_object
        elif not tc.is_subclass_of(c=typesetting_classes.formal_object):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        # if default_rep is None:
        #     default_rep = ts.representations.symbolic_representation
        super().__init__(formal_language=formal_language, tc=tc, default_rep=default_rep)

    def declare_unary_formula(self, connective: UnaryConnective, term: FormalObject,
        tc: typing.Optional[ts.TypesettingClass] = None) -> UnaryFormula:
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.unary_formula)
        x: UnaryFormula = UnaryFormula(formal_language_collection=self, connective=connective, term=term, tc=tc)
        x = self._add_formal_object(x=x)
        return x

    def declare_binary_formula(self, connective: BinaryConnective, term_1: FormalObject, term_2: FormalObject,
        tc: typing.Optional[ts.TypesettingClass] = None) -> BinaryFormula:
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.binary_formula)
        x: BinaryFormula = BinaryFormula(formal_language_collection=self, connective=connective, term_1=term_1,
            term_2=term_2, tc=tc)
        x = self._add_formal_object(x=x)
        return x


class Formula(FormalObject):
    """In FL1, a formula is necessarily linked to a formal-language via a collection."""

    def __init__(self, formal_language_collection: FormalLanguageCollection,
        tc: typing.Optional[ts.TypesettingClass] = None):
        self._formal_language_collection = formal_language_collection
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.formula)
        super().__init__(tc=tc)

    @property
    def formal_language(self) -> FormalLanguage:
        return self.formal_language_collection.formal_language

    @property
    def formal_language_collection(self) -> FormalLanguageCollection:
        return self._formal_language_collection

    def iterate_leaf_formulas(self) -> typing.Generator[AtomicFormula, None, None]:
        """Iterate through the formula-tree and return its ordered leaf elements (i.e.: its atomic-formulas). The order is reproducible: formula terms are read from left to right, depth-first."""
        if isinstance(self, AtomicFormula):
            yield self
        elif isinstance(self, CompoundFormula):
            for term in self.terms:
                yield from term.iterate_leaf_formulas()
        else:
            log.error(msg='Unsupported formula type.')

    def iterate_formulas(self) -> typing.Generator[Formula, None, None]:
        """Iterate through the formula-tree and return its ordered formulas components in canonical order.
        Canonical order: top-down, formula terms are read from left to right, depth-first."""
        yield self
        if isinstance(self, CompoundFormula):
            for term in self.terms:
                yield from term.iterate_formulas()

    def iterate_formulas_inverse(self) -> typing.Generator[Formula, None, None]:
        """Yields formula in reversed canonical order, """
        original_sequence: list[Formula] = list(self.iterate_formulas())
        for phi in reversed(original_sequence):
            yield phi

    def list_formulas(self, s: typing.Optional[set[fl1.Formula]] = None) -> set[fl1.Formula]:
        """List all unique formulas in the formula-tree.
        Let s' be the set of unique formula elements in the formula-tree, returns the set s received as a
        parameter, union s'.
        Note that parameter s is a mutable set, so s is transformed during the process.
        Algorithm: formula terms are read from left to right, depth-first."""
        if self not in s:
            s.add(self)
        if isinstance(self, CompoundFormula):
            for term in self.terms:
                term.list_formulas(s=s)
        return s


class AtomicFormula(Formula):
    def __init__(self, formal_language_collection: FormalLanguageCollection, tc: typing.Optional[ts.TypesettingClass]):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.atomic_formula)
        super().__init__(formal_language_collection=formal_language_collection, tc=tc)


class CompoundFormula(Formula):
    """A compound-formula is a formal-object and a tree-structure of atomic-formulas and compound-formulas."""

    def __init__(self, formal_language_collection: FormalLanguageCollection, connective: Connective,
        terms: typing.Tuple[Formula], tc: typing.Optional[ts.TypesettingClass]):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.compound_formula)
        if isinstance(connective, FixedArityConnective):
            if connective.arity_as_int != len(terms):
                log.error(msg='The number of arguments is not equal to the arity of the fixed-arity-connective.')
        elif isinstance(connective, VariableArityConnective):
            pass
        else:
            log.error(msg='Unsupported connective python class.')
        self._connective: Connective = connective
        self._terms: typing.Tuple[Formula] = terms
        super().__init__(formal_language_collection=formal_language_collection, tc=tc)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.formal_language, typesetting_classes.compound_formula, self.connective, self.terms,))

    @property
    def arity_as_int(self) -> int:
        # This is also valid for both variable- and fixed-arity connectives.
        return len(self.terms)

    @property
    def connective(self) -> Connective:
        return self._connective

    @property
    def terms(self) -> typing.Tuple[Formula]:
        return self._terms


class FixedArityFormula(CompoundFormula):
    """A fixed-arity-formula is a formula with a fixed-arity connective."""

    def __init__(self, formal_language_collection: FormalLanguageCollection, connective: FixedArityConnective,
        terms: typing.Tuple[Formula, ...], tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.fixed_arity_formula)
        super().__init__(formal_language_collection=formal_language_collection, connective=connective, terms=terms,
            tc=tc)


class UnaryFormula(FixedArityFormula):
    """A unary-formula is a formula with a fixed unary connective."""

    def __init__(self, formal_language_collection: FormalLanguageCollection, connective: UnaryConnective, term: Formula,
        tc: typing.Optional[ts.TypesettingClass]):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.unary_formula)
        super().__init__(formal_language_collection=formal_language_collection, connective=connective, terms=(term,),
            tc=tc)

    @property
    def term(self) -> Formula:
        return self.terms[0]


class BinaryFormula(FixedArityFormula):
    """A binary-formula is a formula with a fixed binary connective."""

    def __init__(self, formal_language_collection: FormalLanguageCollection, connective: BinaryConnective,
        term_1: Formula, term_2: Formula, tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.binary_formula)
        super().__init__(formal_language_collection=formal_language_collection, connective=connective,
            terms=(term_1, term_2,), tc=tc)

    @property
    def term_1(self) -> Formula:
        return self.terms[0]

    @property
    def term_2(self) -> Formula:
        return self.terms[1]


class ML1(FormalLanguageCollection, abc.ABC):
    """ML1 is a rather minimalist meta-language designed to facilite the construction of formal-languages."""

    def __init__(self, formal_language: FormalLanguage):
        super().__init__(formal_language=formal_language, typesetting_class=typesetting_classes.ml1)


def generate_unique_values(generator):
    """Utility function that yields only unique values from a generator."""
    observed_values = set()
    for value in generator():
        if value not in observed_values:
            observed_values.add(value)
            yield value


class Axiom(Formula):
    """An axiom is a formal-object that contains a formula assumed as valid in the parent formal-language."""

    def __init__(self, formal_language_collection: FormalLanguageCollection, phi: Formula,
        tc: typing.Optional[ts.TypesettingClass]):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.axiom)
        self._phi: Formula = phi
        super().__init__(formal_language_collection=formal_language_collection, tc=tc)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.formal_language, typesetting_classes.axiom, self.phi,))

    @property
    def phi(self) -> Formula:
        return self._phi


class AxiomCollection(FormalLanguageCollection):

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TypesettingClass] = None,
        default_rep: typing.Optional[ts.Representation] = None):
        if tc is None:
            tc = typesetting_classes.formal_object
        elif not tc.is_subclass_of(c=typesetting_classes.formal_object):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        # if default_rep is None:
        #     default_rep = ts.representations.symbolic_representation
        super().__init__(formal_language=formal_language, tc=tc, default_rep=default_rep)

    def declare_axiom(self, phi: Formula, tc: typing.Optional[ts.TypesettingClass] = None) -> Axiom:
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.axiom)
        x: Axiom = Axiom(formal_language_collection=self, phi=phi, tc=tc)
        x = self._add_formal_object(x=x)
        return x


class FormalLanguagePreference(ts.Preference):
    def __init__(self, item: str, formal_language: FormalLanguage):
        super().__init__(item=item)
        self._formal_language: FormalLanguage = formal_language
        self._reset_value: FormalLanguage = formal_language

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language

    @formal_language.setter
    def formal_language(self, formal_language: FormalLanguage):
        self._formal_language = formal_language

    def reset(self) -> None:
        self.formal_language = self._reset_value


class Preferences:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_set: typing.Union[set[ts.Preference, ...], set[None]] = set()
        super().__init__()
        self._formal_language = FormalLanguagePreference(item='formal language', formal_language=None)
        self._register(preference=self._formal_language)

    def _register(self, preference: ts.Preference) -> None:
        self._internal_set.add(preference)

    @property
    def formal_language(self) -> FormalLanguagePreference:
        """binary formula notation preference"""
        return self._formal_language

    def reset(self):
        for preference in self._internal_set:
            preference.reset()


log.debug(f"Module {__name__}: loaded.")
