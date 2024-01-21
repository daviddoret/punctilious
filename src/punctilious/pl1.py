"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import fl1 as fl
import log
import pl1_typesetting
from fl1 import FormalObject


class MetaVariable(fl.FormalObject):
    def __init__(self):
        super().__init__()


class MetaVariableClass(fl.FormalLanguageClass):
    """An accretor for meta-variables."""

    def __init__(self, formal_language: fl.FormalLanguage):
        super().__init__(formal_language=formal_language)


class MetaLanguage(fl.FormalLanguage):
    """The meta-language of PL1."""

    def __init__(self):
        super().__init__()
        self._variables: MetaVariableClass = MetaVariableClass(formal_language=self)
        super()._add_class(x=self._variables)
        self.lock()

    @property
    def variables(self) -> MetaVariableClass:
        """The class of meta-variables in the meta-language of PL1."""
        return self._variables


class PropositionalVariable(fl.FormalObject):
    def __init__(self):
        super().__init__()


class PropositionalVariableClass(fl.FormalLanguageClass):
    def __init__(self, formal_language: PL1):
        super().__init__(formal_language=formal_language)

    def declare_proposition_variable(self) -> PropositionalVariable:
        """Declare a new propositional-variable in PL1."""
        p: PropositionalVariable = PropositionalVariable()
        super()._add_formal_object(x=p)
        return p


class ConnectiveClass(fl.ConnectiveClass):
    """A specialized ConnectiveClass for PL1 containing all PL1 connectors, and that is locked."""

    def __init__(self, formal_language: PL1):
        super().__init__(formal_language=formal_language)
        # exhaustive declaration of PL1 connectives.
        self._material_implication: fl.BinaryConnective = self.declare_binary_connective()
        self._material_implication.tag(pl1_typesetting.connective_material_implication)
        self._negation: fl.UnaryConnective = self.declare_unary_connective()
        self._negation.tag(pl1_typesetting.connective_negation)
        self.lock()

    @property
    def material_implication(self) -> fl.BinaryConnective:
        """The material implication binary connective."""
        return self._material_implication

    @property
    def negation(self) -> fl.UnaryConnective:
        """The negation unary connective."""
        return self._negation


class FormulaClass(fl.FormulaClass):
    """A specialized class for PL1 containing all PL1 free formulas, and that is initially not locked."""

    def __init__(self, formal_language: PL1):
        self._pl1 = formal_language
        super().__init__(formal_language=formal_language)

    def declare_unary_formula(self, connective: fl.UnaryConnective, term: FormalObject) -> fl.UnaryFormula:
        if connective not in self.pl1.connectives:
            log.error("connective is not a pl1-connective.")
        if not self.pl1.is_well_formed_formula(phi=term):
            log.error("term is not a pl1-well-formed-formula.")
        return super().declare_unary_formula(connective=connective, term=term)

    def declare_binary_formula(self, connective: fl.BinaryConnective, term_1: FormalObject, term_2: FormalObject) -> (
        fl.BinaryFormula):
        if connective not in self.pl1.connectives:
            log.error("connective is not a pl1-connective.")
        if not self.pl1.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1-well-formed-formula.")
        if not self.pl1.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1-well-formed-formula.")
        return super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    @property
    def pl1(self) -> PL1:
        return self._pl1


class PL1(fl.FormalLanguage):
    """Propositional Logic 1."""

    def __init__(self):
        super().__init__()
        self._connectives: ConnectiveClass = ConnectiveClass(formal_language=self)
        super()._add_class(x=self._connectives)
        self._formulas: FormulaClass = FormulaClass(formal_language=self)
        super()._add_class(x=self._formulas)
        self._propositional_variables: PropositionalVariableClass = PropositionalVariableClass(formal_language=self)
        super()._add_class(x=self._propositional_variables)
        self.lock()

    @property
    def connectives(self) -> ConnectiveClass:
        """The collection of connectives in PL1."""
        return self._connectives

    @property
    def formulas(self) -> FormulaClass:
        """The collection of formulas in PL1."""
        return self._formulas

    def is_well_formed_formula(self, phi: fl.FormalObject) -> bool:
        """Return True if phi is a well-formed-formula on PL1, False otherwise."""
        if phi in self.propositional_variables:
            # if phi is a PL1 propositional-variable, then it is a well-formed formula.
            return True
        elif phi in self.formulas:
            # if phi is a PL1 formula, then it is a well-formed-formula,
            # because declaration as an element of pl1 formula-class requires validation.
            return True
        else:
            # otherwise, return False, i.e.: phi is not a well-formed-formula.
            return False

    @property
    def propositional_variables(self) -> PropositionalVariableClass:
        """The collection of propositional variables declared in PL1."""
        return self._propositional_variables


log.debug(f"Module {__name__}: loaded.")
