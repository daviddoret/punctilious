"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import log
import typesetting as ts
import fl1


# TODO: See Lawler, John. “Notation, Logical (See: Notation, Mathematical),” n.d. https://websites.umich.edu/~jlawler/IELL-LogicalNotation.pdf.
#   For a good synthesis on notation conventions for propositional logic.


class Flavors:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Flavors, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        # negation
        self._connective_negation_tilde: ts.Flavor = ts.flavors.register(name="pl1.connective.negation.tilde")
        self._connective_negation_not: ts.Flavor = ts.flavors.register(name="pl1.connective.negation.not",
            predecessor=self._connective_negation_tilde)  # define default preference.

    @property
    def connective_negation_not(self) -> ts.Flavor:
        return self._connective_negation_not

    @property
    def connective_negation_tilde(self) -> ts.Flavor:
        return self._connective_negation_tilde


flavors = Flavors()


class Tags:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Tags, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conditional = ts.tags.register(name="pl1.connective.conditional", predecessor=fl1.tags.connective)
        self._negation = ts.tags.register(name="pl1.connective.negation", predecessor=fl1.tags.connective)
        self._propositional_variable = ts.tags.register(name="pl1.propositional_variable",
            predecessor=fl1.tags.formal_object)

    @property
    def conditional(self) -> ts.Tag:
        return self._conditional

    @property
    def negation(self) -> ts.Tag:
        return self._negation

    @property
    def propositional_variable(self) -> ts.Tag:
        return self._propositional_variable


tags = Tags()


class MetaVariable(fl1.FormalObject):
    def __init__(self):
        super().__init__()


class MetaVariableCollection(fl1.FormalLanguageCollection):
    """An accretor for meta-variables."""

    def __init__(self, formal_language: fl1.FormalLanguage):
        super().__init__(formal_language=formal_language)


class MetaLanguage(fl1.FormalLanguage):
    """The meta-language of PL1."""

    def __init__(self):
        super().__init__()
        self._variables: MetaVariableCollection = MetaVariableCollection(formal_language=self)
        super()._add_class(x=self._variables)
        self.lock()

    @property
    def variables(self) -> MetaVariableCollection:
        """The class of meta-variables in the meta-language of PL1."""
        return self._variables


class PropositionalVariable(fl1.AtomicFormula):
    def __init__(self, formal_language_collection: fl1.FormalLanguageCollection):
        super().__init__(formal_language_collection=formal_language_collection)
        self.tag(tag=tags.propositional_variable)


class PropositionalVariableCollection(fl1.FormalLanguageCollection):
    def __init__(self, formal_language: PL1):
        super().__init__(formal_language=formal_language)

    def declare_proposition_variable(self) -> PropositionalVariable:
        """Declare a new propositional-variable in PL1."""
        p: PropositionalVariable = PropositionalVariable(formal_language_collection=self)
        super()._add_formal_object(x=p)
        return p


class ConnectiveClass(fl1.ConnectiveCollection):
    """A specialized ConnectiveClass for PL1 containing all PL1 connectors, and that is locked."""

    def __init__(self, formal_language: PL1):
        super().__init__(formal_language=formal_language)
        # exhaustive declaration of PL1 connectives.
        self._conditional: fl1.BinaryConnective = self.declare_binary_connective()
        self._conditional.tag(tag=tags.conditional)
        self._negation: fl1.UnaryConnective = self.declare_unary_connective()
        self._negation.tag(tag=tags.negation)
        self.lock()

    @property
    def conditional(self) -> fl1.BinaryConnective:
        """The conditional binary connective."""
        return self._conditional

    @property
    def negation(self) -> fl1.UnaryConnective:
        """The negation unary connective."""
        return self._negation


class CompoundFormulaClass(fl1.CompoundFormulaCollection):
    """A specialized class for PL1 containing all PL1 free formulas, and that is initially not locked."""

    def __init__(self, formal_language: PL1):
        self._pl1: PL1 = formal_language
        super().__init__(formal_language=formal_language)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: fl1.FormalObject) -> fl1.UnaryFormula:
        """Declare a well-formed unary formula in PL1.

        IMPORTANT: This method assures that only well-formed unary formulas are declared in PL1.

        :param connective:
        :param term:
        :return:
        """
        if connective not in self.pl1.connectives:
            log.error("connective is not a pl1 connective.")
        if not self.pl1.is_well_formed_formula(phi=term):
            log.error("term is not a pl1 well-formed-formula.")
        return super().declare_unary_formula(connective=connective, term=term)

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: fl1.FormalObject,
        term_2: fl1.FormalObject) -> fl1.BinaryFormula:
        """Declare a well-formed binary formula in PL1.

        IMPORTANT: This method assures that only well-formed binary formulas are declared in PL1.

        :param connective:
        :param term_1:
        :param term_2:
        :return:
        """
        if connective not in self.pl1.connectives:
            log.error("connective is not a pl1 connective.")
        if not self.pl1.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1 well-formed-formula.")
        if not self.pl1.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1 well-formed-formula.")
        return super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    @property
    def pl1(self) -> PL1:
        return self._pl1


class PL1ML(fl1.FormalLanguage):
    """Propositional Logic 1 Meta Language."""

    def __init__(self):
        super().__init__()
        self._meta_variables: MetaVariableCollection = MetaVariableCollection(formal_language=self)
        super()._add_class(x=self._meta_variables)
        self.lock()

    def is_well_formed_formula(self, phi: fl1.FormalObject) -> bool:
        """Return True if phi is a well-formed-formula on PL1, False otherwise."""
        # TODO: Implement this, i.e. extends PL1 vocabulary to include meta-variables.
        return True

    @property
    def meta_variables(self) -> MetaVariableCollection:
        """The collection of propositional variables declared in PL1."""
        return self._meta_variables


class PL1(fl1.FormalLanguage):
    """Propositional Logic 1."""

    def __init__(self):
        super().__init__()
        # Meta-language
        self._meta_language: PL1ML = PL1ML()
        # Object classes
        self._connectives: ConnectiveClass = ConnectiveClass(formal_language=self)
        super()._add_class(x=self._connectives)
        self._compound_formulas: CompoundFormulaClass = CompoundFormulaClass(formal_language=self)
        super()._add_class(x=self._compound_formulas)
        self._propositional_variables: PropositionalVariableCollection = PropositionalVariableCollection(
            formal_language=self)
        super()._add_class(x=self._propositional_variables)
        self.lock()

    @property
    def connectives(self) -> ConnectiveClass:
        """The collection of connectives in PL1."""
        return self._connectives

    @property
    def compound_formulas(self) -> CompoundFormulaClass:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def is_well_formed_formula(self, phi: fl1.FormalObject) -> bool:
        """Return True if phi is a well-formed-formula on PL1, False otherwise."""
        if phi in self.propositional_variables:
            # if phi is a PL1 propositional-variable, then it is a well-formed formula.
            return True
        elif phi in self.compound_formulas:
            # if phi is a PL1 formula, then it is a well-formed-formula,
            # because declaration as an element of pl1 formula-class requires validation.
            return True
        else:
            # otherwise, return False, i.e.: phi is not a well-formed-formula.
            return False

    @property
    def meta_language(self) -> PL1ML:
        """The meta-language of PL1."""
        return self._meta_language

    @property
    def propositional_variables(self) -> PropositionalVariableCollection:
        """The collection of declared propositional variables declared in PL1."""
        return self._propositional_variables


log.debug(f"Module {__name__}: loaded.")
