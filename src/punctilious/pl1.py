"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import log
import pl1
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


class Clazzes:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Clazzes, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conditional = ts.clazzes.register(name="pl1.connective.conditional", predecessor=fl1.clazzes.connective)
        self._meta_variable = ts.clazzes.register(name="pl1ml.meta_variable", predecessor=fl1.clazzes.formula)
        self._negation = ts.clazzes.register(name="pl1.connective.negation", predecessor=fl1.clazzes.connective)
        self._propositional_formula = ts.clazzes.register(name="pl1.propositional_formula",
            predecessor=fl1.clazzes.formula)
        self._propositional_unary_formula = ts.clazzes.register(name="pl1.propositional_unary_formula",
            predecessor=fl1.clazzes.unary_formula)
        self._propositional_binary_formula = ts.clazzes.register(name="pl1.propositional_binary_formula",
            predecessor=fl1.clazzes.binary_formula)
        self._propositional_variable = ts.clazzes.register(name="pl1.propositional_variable",
            predecessor=fl1.clazzes.formal_object)

    @property
    def conditional(self) -> ts.Clazz:
        return self._conditional

    @property
    def meta_variable(self) -> ts.Clazz:
        return self._meta_variable

    @property
    def negation(self) -> ts.Clazz:
        return self._negation

    @property
    def propositional_formula(self) -> ts.Clazz:
        return self._propositional_formula

    @property
    def propositional_unary_formula(self) -> ts.Clazz:
        return self._propositional_unary_formula

    @property
    def propositional_binary_formula(self) -> ts.Clazz:
        return self._propositional_binary_formula

    @property
    def propositional_variable(self) -> ts.Clazz:
        return self._propositional_variable


clazzes = Clazzes()


class MetaVariable(fl1.AtomicFormula):
    def __init__(self, formal_language_collection: fl1.FormalLanguageCollection):
        super().__init__(formal_language_collection=formal_language_collection)
        self.declare_clazz_element(clazz=clazzes.meta_variable)


class MetaVariableCollection(fl1.FormalLanguageCollection):
    """An accretor for meta-variables."""

    def __init__(self, formal_language: fl1.FormalLanguage):
        super().__init__(formal_language=formal_language)

    def declare_meta_variable(self) -> MetaVariable:
        """Declare a new meta-variable in PL1ML."""
        mv: MetaVariable = MetaVariable(formal_language_collection=self)
        super()._add_formal_object(x=mv)
        return mv


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
        self.declare_clazz_element(clazz=clazzes.propositional_variable)


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
        self._conditional.declare_clazz_element(clazz=clazzes.conditional)
        self._negation: fl1.UnaryConnective = self.declare_unary_connective()
        self._negation.declare_clazz_element(clazz=clazzes.negation)
        self.lock()

    @property
    def conditional(self) -> fl1.BinaryConnective:
        """The conditional binary connective."""
        return self._conditional

    @property
    def negation(self) -> fl1.UnaryConnective:
        """The negation unary connective."""
        return self._negation


class PL1CompoundFormulaCollection(fl1.CompoundFormulaCollection):
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
        phi: fl1.UnaryFormula = super().declare_unary_formula(connective=connective, term=term)
        phi.declare_clazz_element(clazz=clazzes.propositional_formula)
        phi.declare_clazz_element(clazz=clazzes.propositional_unary_formula)
        return phi

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
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)
        phi.declare_clazz_element(clazz=clazzes.propositional_formula)
        phi.declare_clazz_element(clazz=clazzes.propositional_binary_formula)
        return phi

    @property
    def pl1(self) -> PL1:
        return self._pl1


class PL1MLCompoundFormulaCollection(fl1.CompoundFormulaCollection):
    """A specialized class for PL1 meta-language containing all PL1 meta-language free formulas, and that is initially
    not locked."""

    def __init__(self, pl1ml: PL1ML):
        self._pl1ml: PL1ML = pl1ml
        super().__init__(formal_language=pl1ml)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: fl1.Formula) -> fl1.UnaryFormula:
        """Declare a well-formed unary formula in PL1.

        IMPORTANT: This method assures that only well-formed unary formulas are declared in PL1.

        :param connective:
        :param term:
        :return:
        """
        if connective not in self.pl1ml.pl1:
            log.error("connective is not a pl1 meta-language connective.")
        if not self.pl1ml.is_well_formed_formula(phi=term):
            log.error("term is not a pl1 meta-language well-formed-formula.")
        phi: fl1.UnaryFormula = super().declare_unary_formula(connective=connective, term=term)
        phi.declare_clazz_element(clazz=clazzes.propositional_formula)
        phi.declare_clazz_element(clazz=clazzes.propositional_unary_formula)
        return phi

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: fl1.FormalObject,
        term_2: fl1.FormalObject) -> fl1.BinaryFormula:
        """Declare a well-formed binary formula in PL1.

        IMPORTANT: This method assures that only well-formed binary formulas are declared in PL1.

        :param connective:
        :param term_1:
        :param term_2:
        :return:
        """
        if connective not in self.pl1ml.pl1.connectives:
            log.error("connective is not a pl1 meta-language connective.")
        if not self.pl1ml.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1 meta-language well-formed-formula.")
        if not self.pl1ml.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1 meta-language well-formed-formula.")
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)
        phi.declare_clazz_element(clazz=clazzes.propositional_formula)
        phi.declare_clazz_element(clazz=clazzes.propositional_binary_formula)
        return phi

    @property
    def pl1ml(self) -> PL1M1:
        return self._pl1ml


class PL1ML(fl1.FormalLanguage):
    """Propositional Logic 1 Meta Language."""

    def __init__(self, pl1: PL1):
        super().__init__()
        self._pl1: PL1 = pl1
        # Language tuples
        self._meta_variables: MetaVariableCollection = MetaVariableCollection(formal_language=self)
        super()._add_class(x=self._meta_variables)
        self._compound_formulas: PL1MLCompoundFormulaCollection = PL1MLCompoundFormulaCollection(pl1ml=self)
        super()._add_class(x=self._compound_formulas)
        # self._propositional_variables: PropositionalVariableCollection = PropositionalVariableCollection(
        #    formal_language=self)
        # super()._add_class(x=self._propositional_variables)
        self.lock()

    @property
    def compound_formulas(self) -> PL1MLCompoundFormulaCollection:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def get_meta_variable_tuple(self, phi: fl1.Formula) -> tuple[MetaVariable]:
        return tuple(p for p in phi.iterate_leaf_formulas() if p in self.meta_variables)

    def is_well_formed_formula(self, phi: fl1.Formula) -> bool:
        """Return True if phi is a well-formed-formula in PL1ML, False otherwise."""
        if phi in self.meta_variables:
            # if phi is a PL1ML meta-variable, then it is a well-formed formula.
            return True
        elif self.pl1.is_well_formed_formula(phi=phi):
            # if phi is a well-formed formula in the PL1 sub-language, then it is a well-formed-formula,
            return True
        elif phi in self.compound_formulas:
            # if phi is a well-formed formula in the PL1ML sub-language, then it is a well-formed-formula,
            return True
        else:
            # otherwise, return False, i.e.: phi is not a well-formed-formula.
            return False

    @property
    def meta_variables(self) -> MetaVariableCollection:
        """The collection of propositional variables declared in PL1."""
        return self._meta_variables

    @property
    def pl1(self) -> PL1:
        """The collection of propositional variables declared in PL1."""
        return self._pl1

    def substitute_meta_variables(self, phi: fl1.Formula, m: dict[fl1.Formula, fl1.Formula]) -> fl1.Formula:
        """Given a map of formal-objects m, mapping all meta-variables in phi with well-formed-formulas from PL1,
        replaces all meta-variable occurrences in phi with their mapped PL1 formulas,
        and return the corresponding well-formed PL1 formula."""
        # DATA VALIDATION
        # TODO: DATA-VALIDATION: check that all meta-variables are covered by the map to raise a more meaningful
        #  exception.
        # TODO: OPTIMIZATION: don't do data-validation multiple times because of recursion.
        if not self.is_well_formed_formula(phi):
            log.error(msg='phi is not a well-formed formula in the PL1 meta-language')
        for mv, psi in m.items():
            if mv not in self.meta_variables:
                log.error(msg='map key element is not a meta-variable in the PL1 meta-language')
            if not self.is_well_formed_formula(phi=psi):
                log.error(msg='map formula element is not a meta-variable in the PL1 meta-language')
        if phi in m.keys():
            # direct substitution
            return m[phi]
        elif phi.is_an_element_of_clazz(c=pl1.clazzes.propositional_variable):
            return phi
        elif phi.is_an_element_of_clazz(c=fl1.clazzes.unary_formula):
            phi: fl1.UnaryFormula
            connective: fl1.Connective = phi.connective
            connective: fl1.UnaryConnective
            term: fl1.Formula = self.substitute_meta_variables(phi=phi.term, m=m)
            psi = self.pl1.compound_formulas.declare_unary_formula(connective=connective, term=term)
            return psi
        elif phi.is_an_element_of_clazz(c=fl1.clazzes.binary_formula):
            phi: fl1.BinaryFormula
            connective: fl1.Connective = phi.connective
            connective: fl1.BinaryConnective
            term_1: fl1.Formula = self.substitute_meta_variables(phi=phi.term_1, m=m)
            term_2: fl1.Formula = self.substitute_meta_variables(phi=phi.term_2, m=m)
            psi = self.pl1.compound_formulas.declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)
            return psi
        else:
            log.error(msg='unsupported class.')


class PL1(fl1.FormalLanguage):
    """Propositional Logic 1."""

    def __init__(self):
        super().__init__()
        # Meta-language
        self._meta_language: PL1ML = PL1ML(pl1=self)
        # Object classes
        self._connectives: ConnectiveClass = ConnectiveClass(formal_language=self)
        super()._add_class(x=self._connectives)
        self._compound_formulas: PL1CompoundFormulaCollection = PL1CompoundFormulaCollection(formal_language=self)
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
    def compound_formulas(self) -> PL1CompoundFormulaCollection:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def is_well_formed_formula(self, phi: fl1.Formula) -> bool:
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

    def get_propositional_variable_tuple(self, phi: fl1.Formula) -> tuple[PropositionalVariable]:
        return tuple(p for p in phi.iterate_leaf_formulas() if p in self.propositional_variables)

    @property
    def meta_language(self) -> PL1ML:
        """The meta-language of PL1."""
        return self._meta_language

    @property
    def propositional_variables(self) -> PropositionalVariableCollection:
        """The collection of declared propositional variables declared in PL1."""
        return self._propositional_variables


log.debug(f"Module {__name__}: loaded.")
