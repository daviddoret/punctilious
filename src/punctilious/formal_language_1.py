"""This module defines some generic classes to facilitate the design of formal-languages."""

from __future__ import annotations

import abc
import typing
import threading

import log
import typesetting as ts


class FormalLanguagePreference(ts.Preference):
    def __init__(self, item: str, value: typing.Optional[FormalLanguage]):
        super().__init__(item=item)
        self._value: FormalLanguage = value
        self._reset_value: FormalLanguage = value

    @property
    def value(self) -> typing.Optional[FormalLanguage]:
        return self._value

    @value.setter
    def value(self, formal_language: typing.Optional[FormalLanguage]):
        value_before: typing.Optional[FormalLanguage] = self.value
        self._value = formal_language
        super()._on_change(value_before=value_before, value_after=formal_language)

    def reset(self) -> None:
        self._value = self._reset_value


class Preferences:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Preferences, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        self._internal_set: typing.Union[set[None], set[ts.Preference, ...]] = set()
        super().__init__()
        section: str = "formal_language_1"
        self._formal_language = FormalLanguagePreference(item="formal_language", value=None)
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


preferences: Preferences = Preferences()


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


class TypesettingClass(ts.TC):
    """A collection of typesetting-classes."""
    FL1_FORMAL_OBJECT = ts.TC(ts.TypesettingClass.TS_TYPESETTABLE)
    FL1_CONNECTIVE = ts.TC(FL1_FORMAL_OBJECT)
    FL1_FIXED_ARITY_CONNECTIVE = ts.TC(FL1_CONNECTIVE)
    FL1_UNARY_CONNECTIVE = ts.TC(FL1_FIXED_ARITY_CONNECTIVE)
    FL1_BINARY_CONNECTIVE = ts.TC(FL1_FIXED_ARITY_CONNECTIVE)
    FL1_VARIABLE_ARITY_CONNECTIVE = ts.TC(FL1_CONNECTIVE)
    FL1_FORMULA = ts.TC(FL1_FORMAL_OBJECT)
    FL1_ATOMIC_FORMULA = ts.TC(FL1_FORMULA)
    FL1_COMPOUND_FORMULA = ts.TC(FL1_FORMULA)
    FL1_FIXED_ARITY_FORMULA = ts.TC(FL1_COMPOUND_FORMULA)
    FL1_UNARY_FORMULA = ts.TC(FL1_FIXED_ARITY_FORMULA)
    FL1_BINARY_FORMULA = ts.TC(FL1_FIXED_ARITY_FORMULA)
    FL1_VARIABLE_ARITY_FORMULA = ts.TC(FL1_COMPOUND_FORMULA)
    FL1_INFERENCE_RULE = ts.TC(FL1_FORMAL_OBJECT)
    FL1_FORMAL_LANGUAGE_COLLECTION = ts.TC(FL1_FORMAL_OBJECT)
    FL1_CONNECTIVE_COLLECTION = ts.TC(FL1_FORMAL_LANGUAGE_COLLECTION)
    FL1_INFERENCE_RULE_COLLECTION = ts.TC(FL1_FORMAL_LANGUAGE_COLLECTION)
    FL1_COMPOUND_FORMULA_COLLECTION = ts.TC(FL1_FORMAL_LANGUAGE_COLLECTION)
    FL1_FORMAL_LANGUAGE = ts.TC(FL1_FORMAL_OBJECT)
    FL1_META_LANGUAGE = ts.TC(FL1_FORMAL_LANGUAGE)
    FL1_AXIOM = ts.TC(FL1_FORMULA)


ts.TC.load_elements(cls=TypesettingClass)


class FormalObject(ts.Typesettable):
    """A formal-object is an object that is manipulated as part of a formal-system.
    """

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None,
                 default_rep: typing.Optional[ts.Representation] = None):
        self._formal_language_lock = threading.Lock()
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_FORMAL_OBJECT)
        if default_rep is None:
            default_rep = ts.representations.symbolic_representation
        super().__init__(tc=tc, default_rep=default_rep)
        self._formal_language_collection = c
        if c is not None:
            c.add_element(x=self)

    def __repr__(self):
        return super().to_string(representation=ts.representations.symbolic_representation)

    def __str__(self):
        return super().to_string(representation=ts.representations.symbolic_representation)

    @property
    def bound_to_formal_language(self):
        """A formal-object is bound to a formal-language l if and only if
         it is an element of one of the primary collections c1, c2, ..., cn
         that constitute the formal-language l := (c1, c2, ..., cn).

         Return True if this formal-object is bound (i.e. an element of) a formal-language, False otherwise."""
        return self._formal_language_collection is not None

    def bind_to_formal_language(self, c: FormalLanguageCollection):
        """If the formal-object is not yet bound to a formal-language,
        binds it to the formal-language that is the parent of formal-language collection.
        As a result, the .formal_language property of the formal-object is set,
        and the formal-object is made an element of the formal-language collection c."""
        if self.bound_to_formal_language:
            log.error(
                msg="Attempt to bind to a formal-language a formal-object that is already bound to a formal-language.",
                slf=self, c=c)
        else:
            with self._formal_language_lock:
                # implement the cross reference.
                self._formal_language_collection = c  # set the property
                c.add_element(x=self)  # add the element

    @property
    def formal_language(self) -> typing.Optional[FormalLanguage]:
        """If the formal-object is an element of a formal-language, return the formal-language. None otherwise."""
        if self.formal_language_collection is None:
            return None
        else:
            return self.formal_language_collection.formal_language

    @property
    def formal_language_collection(self) -> typing.Optional[FormalLanguageCollection]:
        """If the formal-object is an element of a formal-language, return the formal-language primary collection of which it is an element. None otherwise.

        Discussion:
        By definition, a formal-language is a tuple T := (C1, C2, ..., Cn) where Ci denote exclusive collections. This property return Ci such
        that the formal-object is an element of Ci in T.

        Question: Must C1, C2, ..., Cn be exclusive collections for all future formal-languages?
        """
        return self._formal_language_collection


class FormalLanguageCollection(FormalObject, abc.ABC):
    """A FormalLanguage is defined as a tuple of collections. The FormalLanguageCollection python-class is designed to
    facilitate navigation between the formal-language, its classes, and their class elements."""

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TC] = None,
                 default_rep: typing.Optional[ts.Representation] = None):
        self._is_locked: bool = False
        self._protected_set: set[FormalObject] = set()
        self._formal_language: FormalLanguage = formal_language
        if tc is None:
            tc = TypesettingClass.FL1_FORMAL_OBJECT
        elif not tc.is_subclass_of(tc=TypesettingClass.FL1_FORMAL_OBJECT):
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

    def add_element(self, x: FormalObject) -> FormalObject:
        """Add an element to this collection."""
        if self.is_locked:
            log.error(msg='This collection is locked.', slf=self, x=x)
        elif x.formal_language_collection is not self:
            log.error(
                msg='The primary formal-language-collection property of the element is not consistent with this formal-language collection. As a result, the formal-object cannot be added to the collection.',
                slf=self, x=x)
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

    def __init__(self, axioms: typing.Optional[AxiomCollection] = None, set_as_default: bool = False,
                 tc: typing.Optional[ts.TC] = None):
        """

        :param set_as_default: if True, the formal-language is set as the current default formal-language
            for the interpretation of formulas for which the formal-language is not expressly specified.
        :param tc:
        """
        if tc is None:
            tc = TypesettingClass.FL1_FORMAL_LANGUAGE
        elif not tc.is_subclass_of(tc=TypesettingClass.FL1_FORMAL_LANGUAGE):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        super().__init__(tc=tc, default_rep=ts.representations.symbolic_representation)
        if axioms is None:
            axioms: AxiomCollection = AxiomCollection(formal_language=self)
        elif axioms.formal_language is not self:
            log.error(
                msg="The formal-language property of the axioms collection passed as an argument to FormalLanguage.__init__() is not the formal-language being initialized.",
                slf=self, axioms=axioms, axioms_formal_language=axioms.formal_language)
        self._axioms = axioms
        self._is_locked: bool = False
        self._container: set = set()
        if set_as_default:
            # set the newly declared formal-language as the default language,
            # for the interpretation of formulas for which the formal-language
            # is not expressly specified.
            preferences.formal_language.value = self

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

    @abc.abstractmethod
    def declare_binary_formula(self, connective: Connective, term_1: Formula, term_2: Formula) -> BinaryFormula:
        """Abstract method that declare a well-formed binary formula in the formal-language."""
        log.error(msg="calling an abstract method.")

    @abc.abstractmethod
    def declare_unary_formula(self, connective: Connective, term: Formula) -> UnaryFormula:
        """Abstract method that declare a well-formed unary formula in the formal-language."""
        log.error(msg="calling an abstract method.")

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
        self.declare_typesetting_class_element(typesetting_class=TypesettingClass.FL1_META_LANGUAGE)

    @property
    def formal_language(self) -> FormalLanguage:
        return self._formal_language


class Connective(FormalObject):
    """A connective is a formal-object that may be used as a connective to build compound-formulas in a
    formal-language."""

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_CONNECTIVE)
        super().__init__(c=c, tc=tc)


class InferenceRule(FormalObject):
    """An inference-rule is a formal-object that allows to infer / derive new statements in a formal-language."""

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_INFERENCE_RULE)
        super().__init__(c=c, tc=tc)


class VariableArityConnective(Connective):
    """A variable-arity connective, aka n-ary connective, is a connective whose arity is not predefined / fixed
    when the connective is declared, but determined when compound-formulas based on that connective are declared."""

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_VARIABLE_ARITY_CONNECTIVE)
        super().__init__(c=c, tc=tc)


class FixedArityConnective(Connective):
    """A fixed-arity connective is a connective whose arity is fixed and determined during the declaration of the
    connective itself."""

    def __init__(self, arity_as_int: int, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        self._arity_as_int = arity_as_int
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_FIXED_ARITY_CONNECTIVE)
        super().__init__(c=c, tc=tc)

    @property
    def arity_as_int(self) -> int:
        return self._arity_as_int


class UnaryConnective(FixedArityConnective):
    """A unary connective is a connective whose arity is fixed and equal to 1."""

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_UNARY_CONNECTIVE)
        super().__init__(arity_as_int=1, c=c, tc=tc)

    def __or__(self, other):
        """Support for prefix formula (* x)."""
        if isinstance(other, Formula):
            return other.formal_language.declare_unary_formula(connective=self, term=other)
        else:
            log.error(msg="No interpretation found for python-pseudo-math entry.", slf=self, other=other)


class BinaryConnective(FixedArityConnective):
    """A binary connective is a connective whose arity is fixed and equal to 2."""

    def __init__(self, c: typing.Optional[FormalLanguageCollection] = None,
                 tc: typing.Optional[ts.TC] = None):
        tc: ts.TC = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_BINARY_CONNECTIVE)
        super().__init__(arity_as_int=2, c=c, tc=tc)


class ConnectiveCollection(FormalLanguageCollection):
    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_CONNECTIVE_COLLECTION)
        super().__init__(formal_language=formal_language, tc=tc)

    def declare_unary_connective(self, tc: typing.Optional[ts.TC]) -> UnaryConnective:
        x: UnaryConnective = UnaryConnective(c=self, tc=tc)
        return x

    def declare_binary_connective(self, tc: typing.Optional[ts.TC]) -> BinaryConnective:
        x: BinaryConnective = BinaryConnective(c=self, tc=tc)
        return x


class InferenceRuleCollection(FormalLanguageCollection):
    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_INFERENCE_RULE_COLLECTION)
        super().__init__(formal_language=formal_language, tc=tc)

    def declare_inference_rule(self, tc: typing.Optional[ts.TC]) -> InferenceRule:
        x: InferenceRule = InferenceRule(c=self, tc=tc)
        return x


class CompoundFormulaCollection(FormalLanguageCollection):

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TC] = None,
                 default_rep: typing.Optional[ts.Representation] = None):
        if tc is None:
            tc = TypesettingClass.FL1_FORMAL_OBJECT
        elif not tc.is_subclass_of(tc=TypesettingClass.FL1_FORMAL_OBJECT):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        # if default_rep is None:
        #     default_rep = ts.representations.symbolic_representation
        super().__init__(formal_language=formal_language, tc=tc, default_rep=default_rep)

    def declare_unary_formula(self, connective: UnaryConnective, term: Formula,
                              tc: typing.Optional[ts.TC] = None) -> UnaryFormula:
        x: UnaryFormula = UnaryFormula(c=self, connective=connective, term=term, tc=tc)
        return x

    def declare_binary_formula(self, connective: BinaryConnective, term_1: Formula, term_2: Formula,
                               tc: typing.Optional[ts.TC] = None) -> BinaryFormula:
        x: BinaryFormula = BinaryFormula(c=self, connective=connective, term_1=term_1, term_2=term_2, tc=tc)
        return x


class Formula(FormalObject):
    """A formula is a formal-object that may be used as an atomic-formula, or a composite-formula term, in some formal-language."""

    def __init__(self, c: FormalLanguageCollection,
                 tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_FORMULA)
        super().__init__(c=c, tc=tc)

    def __or__(self, other=object):
        """Hack to provide support for pseudo-infix notation, as in: p | implies | q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and gluing all this together with the InfixPartialFormula class.
        """
        if not isinstance(other, InfixPartialFormula):
            if isinstance(self, UnaryConnective) and isinstance(other, Formula):
                # for the time being, connectives are not formula,
                # making this particular condition impossible.
                # but this will need to change in the future,
                # in order to support rich meta-languages where
                # connectives are atomic formulas.
                return self.formal_language.declare_unary_formula(connective=self, term=other)
            elif isinstance(self, Formula) and isinstance(other, UnaryConnective):
                return self.formal_language.declare_unary_formula(connective=self, term=other)
            elif isinstance(self, Formula) and isinstance(other, BinaryConnective):
                # This is a partial infix formula.
                return InfixPartialFormula(term_1=self, partial_connective=other)
            else:
                log.error(msg="No interpretation found for python-pseudo-math", slf=self, other=other)
        else:
            # other was already converted to InfixPartialFormula.
            return self.formal_language.declare_binary_formula(connective=other.connective, term_1=self,
                                                               term_2=other.partial_term)

    @property
    def formal_language(self) -> FormalLanguage:
        """The formal-language of which this formula is an element.

        Note: return type is more specific than FormalObject.formal_language, where the property is optional."""
        return super().formal_language

    @property
    def formal_language_collection(self) -> FormalLanguageCollection:
        """The primary formal-language collection of which this formula is an element.

        Note: return type is more specific than FormalObject.formal_language_collection, where the property is optional."""
        return super().formal_language_collection

    def iterate_leaf_formulas(self) -> typing.Generator[AtomicFormula, None, None]:
        """Iterate through the formula-tree and return its ordered leaf elements (i.e.: its atomic-formulas). The order is reproducible: formula terms are read from left to right, depth-first."""
        if isinstance(self, AtomicFormula):
            yield self
        elif isinstance(self, CompoundFormula):
            for term in self.terms:
                yield from term.iterate_leaf_formulas()
        elif isinstance(self, Axiom):
            # unpack the axiom formula
            yield from self.phi.iterate_formulas()
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
    def __init__(self, c: FormalLanguageCollection, tc: typing.Optional[ts.TC]):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_ATOMIC_FORMULA)
        super().__init__(c=c, tc=tc)


class CompoundFormula(Formula):
    """A compound-formula is a formal-object and a tree-structure of atomic-formulas and compound-formulas."""

    def __init__(self, c: FormalLanguageCollection, connective: Connective,
                 terms: typing.Tuple[Formula, ...], tc: typing.Optional[ts.TC]):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_COMPOUND_FORMULA)
        if isinstance(connective, FixedArityConnective):
            if connective.arity_as_int != len(terms):
                log.error(msg='The number of arguments is not equal to the arity of the fixed-arity-connective.')
        elif isinstance(connective, VariableArityConnective):
            pass
        else:
            log.error(msg='Unsupported connective python class.')
        self._connective: Connective = connective
        self._terms: typing.Tuple[Formula, ...] = terms
        super().__init__(c=c, tc=tc)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.formal_language, TypesettingClass.FL1_COMPOUND_FORMULA, self.connective, self.terms,))

    @property
    def arity_as_int(self) -> int:
        # This is also valid for both variable- and fixed-arity connectives.
        return len(self.terms)

    @property
    def connective(self) -> Connective:
        return self._connective

    @property
    def terms(self) -> typing.Tuple[Formula, ...]:
        return self._terms


class FixedArityFormula(CompoundFormula):
    """A fixed-arity-formula is a formula with a fixed-arity connective."""

    def __init__(self, c: FormalLanguageCollection, connective: FixedArityConnective,
                 terms: typing.Tuple[Formula, ...], tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_FIXED_ARITY_FORMULA)
        super().__init__(c=c, connective=connective, terms=terms,
                         tc=tc)


class UnaryFormula(FixedArityFormula):
    """A unary-formula is a formula with a fixed unary connective."""

    def __init__(self, c: FormalLanguageCollection, connective: UnaryConnective, term: Formula,
                 tc: typing.Optional[ts.TC]):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_UNARY_FORMULA)
        super().__init__(c=c, connective=connective, terms=(term,),
                         tc=tc)

    @property
    def term(self) -> Formula:
        return self.terms[0]


class BinaryFormula(FixedArityFormula):
    """A binary-formula is a formula with a fixed binary connective."""

    def __init__(self, c: FormalLanguageCollection, connective: BinaryConnective,
                 term_1: Formula, term_2: Formula, tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_BINARY_FORMULA)
        super().__init__(c=c, connective=connective,
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
        super().__init__(formal_language=formal_language, typesetting_class=TypesettingClass.FL1_META_LANGUAGE)


def generate_unique_values(generator):
    """Utility function that yields only unique values from a generator."""
    observed_values = set()
    for value in generator():
        if value not in observed_values:
            observed_values.add(value)
            yield value


class Axiom(Formula):
    """An axiom is a formal-object that contains a formula assumed as valid in the parent formal-language."""

    def __init__(self, c: AxiomCollection, phi: Formula,
                 tc: typing.Optional[ts.TC]):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.FL1_AXIOM)
        self._phi: Formula = phi
        super().__init__(c=c, tc=tc)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.formal_language, TypesettingClass.FL1_AXIOM, self.phi,))

    @property
    def phi(self) -> Formula:
        return self._phi


class AxiomCollection(FormalLanguageCollection):

    def __init__(self, formal_language: FormalLanguage, tc: typing.Optional[ts.TC] = None,
                 default_rep: typing.Optional[ts.Representation] = None):
        if tc is None:
            tc = TypesettingClass.FL1_FORMAL_OBJECT
        elif not tc.is_subclass_of(tc=TypesettingClass.FL1_FORMAL_OBJECT):
            log.error(msg='inconsistent typesetting class', slf=self, tc=tc)
        # if default_rep is None:
        #     default_rep = ts.representations.symbolic_representation
        super().__init__(formal_language=formal_language, tc=tc, default_rep=default_rep)

    def postulate_axiom(self, axiom: Axiom):
        self.add_element(x=axiom)


class InfixPartialFormula:
    """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
    This is accomplished by re-purposing the | operator,
    overloading the __or__() method that is called when | is used,
    and glueing all this together with the InfixPartialFormula class.
    """

    def __init__(self, term_1: Formula, partial_connective):
        self.formal_language = preferences.formal_language.value  # formulas in python-math are interpreted in the default formal-language.
        self.partial_term = term_1
        self.partial_connective = partial_connective

    def __or__(self, term_2: Formula = None):
        """Hack to provide support for pseudo-infix notation, as in: p |implies| q.
        This is accomplished by re-purposing the | operator,
        overloading the __or__() method that is called when | is used,
        and glueing all this together with the InfixPartialFormula class.
        """
        partial_connective = self.partial_connective
        partial_term = self.partial_term
        return self.formal_language.declare_binary_formula(partial_connective, partial_term, term_2)

    def __str__(self):
        return f'InfixPartialFormula(partial_term = {self.partial_term}, partial_connective = {self.partial_connective})'


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
