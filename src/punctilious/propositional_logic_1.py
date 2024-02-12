"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import typing

import log
import typesetting as ts
import formal_language_1 as fl1
from formal_language_1 import Connective, Formula, BinaryFormula


# TODO: See Lawler, John. “Notation, Logical (See: Notation, Mathematical),” n.d. https://websites.umich.edu/~jlawler/IELL-LogicalNotation.pdf.
#   For a good synthesis on notation conventions for propositional logic.


class TypesettingClasses:
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(TypesettingClasses, cls).__new__(cls)
        return cls._singleton

    def __init__(self):
        super().__init__()
        self._conjunction = ts.typesetting_classes.register(name="pl1.connective.conjunction",
                                                            superclass=fl1.typesetting_classes.binary_connective)
        self._disjunction = ts.typesetting_classes.register(name="pl1.connective.disjunction",
                                                            superclass=fl1.typesetting_classes.binary_connective)
        self._modus_ponens = ts.typesetting_classes.register(name="pl1.inference_rule.modus_ponens",
                                                             superclass=fl1.typesetting_classes.inference_rule)
        self._material_implication = ts.typesetting_classes.register(name="pl1.connective.material_implication",
                                                                     superclass=fl1.typesetting_classes.binary_connective)
        self._connective_collection = ts.typesetting_classes.register(name="pl1.connective_collection",
                                                                      superclass=fl1.typesetting_classes.connective_collection)
        self._meta_variable = ts.typesetting_classes.register(name="meta_language.meta_variable",
                                                              superclass=fl1.typesetting_classes.atomic_formula)
        self._negation = ts.typesetting_classes.register(name="pl1.connective.negation",
                                                         superclass=fl1.typesetting_classes.unary_connective)
        self._pl1ml = ts.typesetting_classes.register(name="pl1ml", superclass=fl1.typesetting_classes.formal_language)
        self._pl1 = ts.typesetting_classes.register(name="pl1", superclass=fl1.typesetting_classes.formal_language)
        # pl1ml is an extension of pl1, all formulas in pl1 are valid in pl1ml + metavariables.
        self._pl1ml_formula = ts.typesetting_classes.register(name="meta_language.formula",
                                                              superclass=fl1.typesetting_classes.formula)
        self._pl1ml_unary_formula = ts.typesetting_classes.register(name="meta_language.unary_formula",
                                                                    superclass=fl1.typesetting_classes.unary_formula)
        self._pl1ml_binary_formula = ts.typesetting_classes.register(name="meta_language.binary_formula",
                                                                     superclass=fl1.typesetting_classes.binary_formula)
        # pl1 is a more specialized class.
        self._pl1_formula = ts.typesetting_classes.register(name="pl1.propositional_formula",
                                                            superclass=self._pl1ml_formula)
        self._pl1_unary_formula = ts.typesetting_classes.register(name="pl1.propositional_unary_formula",
                                                                  superclass=self._pl1ml_unary_formula)
        self._pl1_binary_formula = ts.typesetting_classes.register(name="pl1.propositional_binary_formula",
                                                                   superclass=self._pl1ml_binary_formula)
        self._pl1_variable = ts.typesetting_classes.register(name="pl1.propositional_variable",
                                                             superclass=fl1.typesetting_classes.atomic_formula)

    @property
    def conjunction(self) -> ts.TypesettingClass:
        return self._conjunction

    @property
    def disjunction(self) -> ts.TypesettingClass:
        return self._disjunction

    @property
    def material_implication(self) -> ts.TypesettingClass:
        return self._material_implication

    @property
    def connective_collection(self) -> ts.TypesettingClass:
        return self._connective_collection

    @property
    def meta_variable(self) -> ts.TypesettingClass:
        return self._meta_variable

    @property
    def negation(self) -> ts.TypesettingClass:
        return self._negation

    @property
    def logical_calculi(self) -> ts.TypesettingClass:
        return self._pl1

    @property
    def modus_ponens(self) -> ts.TypesettingClass:
        return self._modus_ponens

    @property
    def pl1ml(self) -> ts.TypesettingClass:
        return self._pl1ml

    @property
    def pl1_formula(self) -> ts.TypesettingClass:
        return self._pl1_formula

    @property
    def pl1_unary_formula(self) -> ts.TypesettingClass:
        return self._pl1_unary_formula

    @property
    def pl1_binary_formula(self) -> ts.TypesettingClass:
        return self._pl1_binary_formula

    @property
    def pl1_variable(self) -> ts.TypesettingClass:
        return self._pl1_variable

    @property
    def pl1ml_formula(self) -> ts.TypesettingClass:
        return self._pl1ml_formula

    @property
    def pl1ml_unary_formula(self) -> ts.TypesettingClass:
        return self._pl1ml_unary_formula

    @property
    def pl1ml_binary_formula(self) -> ts.TypesettingClass:
        return self._pl1ml_binary_formula


typesetting_classes = TypesettingClasses()


class MetaVariable(fl1.AtomicFormula):

    def __init__(self, c: fl1.FormalLanguageCollection,
                 tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.meta_variable)
        super().__init__(c=c, tc=tc)


class MetaVariableCollection(fl1.FormalLanguageCollection):
    """An accretor for meta-variables."""

    def __init__(self, formal_language: fl1.FormalLanguage):
        super().__init__(formal_language=formal_language)

    def declare_meta_variable(self) -> MetaVariable:
        """Declare a new meta-variable in PL1ML."""
        mv: MetaVariable = MetaVariable(c=self)
        super().add_element(x=mv)
        return mv


class PropositionalVariable(fl1.AtomicFormula):

    def __init__(self, c: fl1.FormalLanguageCollection,
                 tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.pl1_variable)
        super().__init__(c=c, tc=tc)


class PropositionalVariableCollection(fl1.FormalLanguageCollection):
    def __init__(self, formal_language: PropositionalLogic):
        super().__init__(formal_language=formal_language)

    def declare_proposition_variable(self) -> PropositionalVariable:
        """Declare a new propositional-variable."""
        p: PropositionalVariable = PropositionalVariable(c=self)
        super().add_element(x=p)
        return p

    def declare_proposition_variables(self, n: int) -> tuple[PropositionalVariable, ...]:
        """Declare n new propositional variables."""
        return tuple(self.declare_proposition_variable() for _ in range(n))


class ConnectiveCollection(fl1.ConnectiveCollection):
    """A specialized ConnectiveCollection for PL1 containing all PL1 connectors, and that is locked."""

    def __init__(self, formal_language: PropositionalLogic, tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.connective_collection)
        super().__init__(formal_language=formal_language, tc=tc)
        # exhaustive declaration of PL1 connectives.
        self._conjunction: fl1.BinaryConnective = self.declare_binary_connective(tc=typesetting_classes.conjunction)
        self._disjunction: fl1.BinaryConnective = self.declare_binary_connective(tc=typesetting_classes.disjunction)
        self._material_implication: fl1.BinaryConnective = self.declare_binary_connective(
            tc=typesetting_classes.material_implication)
        self._negation: fl1.UnaryConnective = self.declare_unary_connective(tc=typesetting_classes.negation)
        self.lock()

    @property
    def conjunction(self) -> fl1.BinaryConnective:
        """The conjunction binary connective."""
        return self._conjunction

    @property
    def disjunction(self) -> fl1.BinaryConnective:
        """The disjunction binary connective."""
        return self._disjunction

    @property
    def material_implication(self) -> fl1.BinaryConnective:
        """The material-implication binary connective."""
        return self._material_implication

    @property
    def negation(self) -> fl1.UnaryConnective:
        """The negation unary connective."""
        return self._negation


class PropositionalLogicCompoundFormulaCollection(fl1.CompoundFormulaCollection):
    """A specialized class for PL1 containing all PL1 free formulas, and that is initially not locked."""

    def __init__(self, formal_language: PropositionalLogic):
        self._propositional_logic: PropositionalLogic = formal_language
        super().__init__(formal_language=formal_language)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: fl1.Formula) -> fl1.UnaryFormula:
        """Declare a well-formed unary formula in PL1.

        IMPORTANT: This method assures that only well-formed unary formulas are declared in PL1.

        :param connective:
        :param term:
        :return:
        """
        # TODO: push this logic to the generic fl1 super class.
        if connective not in self.propositional_logic.connectives:
            log.error("connective is not a pl1 connective.")
        if not self.propositional_logic.is_well_formed_formula(phi=term):
            log.error("term is not a pl1 well-formed-formula.")
        tc: ts.TypesettingClass = typesetting_classes.pl1_unary_formula
        phi: fl1.UnaryFormula = super().declare_unary_formula(connective=connective, term=term, tc=tc)
        return phi

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: fl1.Formula,
                               term_2: fl1.Formula) -> fl1.BinaryFormula:
        """Declare a well-formed binary formula in PL1.

        IMPORTANT: This method assures that only well-formed binary formulas are declared in PL1.

        :param connective:
        :param term_1:
        :param term_2:
        :return:
        """
        if connective not in self.propositional_logic.connectives:
            log.error("connective is not a pl1 connective.", pl1=self.pl1, connective=connective)
        if not self.propositional_logic.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1 well-formed-formula.", pl1=self.pl1, phi=term_1)
        if not self.propositional_logic.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1 well-formed-formula.", pl1=self.pl1, phi=term_2)
        tc: ts.TypesettingClass = typesetting_classes.pl1_binary_formula
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2,
                                                                tc=tc)
        return phi

    @property
    def propositional_logic(self) -> PropositionalLogic:
        return self._propositional_logic


class ModusPonens(fl1.InferenceRule):
    def __init__(self, c: fl1.FormalLanguageCollection,
                 tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.meta_variable)
        super().__init__(c=c, tc=tc)

    def derive_formula(self):
        pass

    def derive_statement(self):
        pass


class PropositionalLogicInferenceRuleCollection(fl1.InferenceRuleCollection):
    """A specialized class for PL1 containing inference-rules, and that is initially locked."""

    def __init__(self, propositional_logic: PropositionalLogic):
        self._propositional_logic: PropositionalLogic = propositional_logic
        super().__init__(formal_language=propositional_logic)
        self._modus_ponens = self.declare_inference_rule()

    def declare_inference_rule(self) -> fl1.InferenceRule:
        tc: ts.TypesettingClass = fl1.typesetting_classes.inference_rule
        phi: fl1.InferenceRule = super().declare_inference_rule(tc=tc)
        return phi


class MetaLanguageCompoundFormulaCollection(fl1.CompoundFormulaCollection):
    """A specialized class for PL1 meta-language containing all PL1 meta-language free formulas, and that is initially
    not locked."""

    def __init__(self, meta_language: MetaLanguage):
        self._meta_language: MetaLanguage = meta_language
        super().__init__(formal_language=meta_language)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: fl1.Formula) -> fl1.UnaryFormula:
        """Declare a well-formed unary formula in PL1.

        IMPORTANT: This method assures that only well-formed unary formulas are declared in PL1.

        :param connective:
        :param term:
        :return:
        """
        if connective not in self.meta_language.logical_calculi:
            log.error("connective is not a pl1 meta-language connective.")
        if not self.meta_language.is_well_formed_formula(phi=term):
            log.error("term is not a pl1 meta-language well-formed-formula.")
        tc: ts.TypesettingClass = typesetting_classes.pl1ml_unary_formula
        phi: fl1.UnaryFormula = super().declare_unary_formula(connective=connective, term=term, tc=tc)
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
        if connective not in self.meta_language.propositional_logic.connectives:
            log.error("connective is not a pl1 meta-language connective.")
        if not self.meta_language.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1 meta-language well-formed-formula.")
        if not self.meta_language.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1 meta-language well-formed-formula.")
        tc: ts.TypesettingClass = typesetting_classes.pl1ml_binary_formula
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2,
                                                                tc=tc)
        return phi

    @property
    def meta_language(self) -> MetaLanguage:
        return self._meta_language


class N0AxiomSchemaCollection(fl1.AxiomCollection):
    # TODO: N0AxiomSchemaCollection complete implementation.
    def __init__(self, meta_language: MetaLanguage):
        self._meta_language = meta_language
        super().__init__(formal_language=meta_language)
        implies: fl1.BinaryConnective = self.meta_language.propositional_logic.connectives.material_implication
        land: fl1.BinaryConnective = self.meta_language.propositional_logic.connectives.conjunction
        a = self.meta_language.meta_variables.declare_meta_variable()
        b = self.meta_language.meta_variables.declare_meta_variable()
        c = self.meta_language.meta_variables.declare_meta_variable()
        self._pl1 = fl1.Axiom(formal_language_collection=self, phi=a | implies | (a | land | a))
        super().declare_axiom(phi=pl1)

    @property
    def meta_language(self) -> MetaLanguage:
        return self._meta_language

    @property
    def pl1(self):
        return self._pl1


class MetaLanguage(fl1.FormalLanguage):
    """Propositional Logic 1 Meta Language."""

    def __init__(self, propositional_logic: PropositionalLogic):
        super().__init__()
        self._propositional_logic: PropositionalLogic = propositional_logic
        # Language tuples
        self._meta_variables: MetaVariableCollection = MetaVariableCollection(formal_language=self)
        super()._add_class(x=self._meta_variables)
        self._compound_formulas: MetaLanguageCompoundFormulaCollection = MetaLanguageCompoundFormulaCollection(
            meta_language=self)
        super()._add_class(x=self._compound_formulas)
        # self._propositional_variables: PropositionalVariableCollection = PropositionalVariableCollection(
        #    formal_language=self)
        # super()._add_class(x=self._propositional_variables)
        self.lock()

    @property
    def compound_formulas(self) -> MetaLanguageCompoundFormulaCollection:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: Formula,
                               term_2: Formula) -> BinaryFormula:
        return self.compound_formulas.declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    def declare_unary_formula(self, connective: fl1.BinaryConnective, term: Formula) -> BinaryFormula:
        return self.compound_formulas.declare_binary_formula(connective=connective, term=term)

    def get_meta_variable_tuple(self, phi: fl1.Formula) -> tuple[MetaVariable, ...]:
        return tuple(p for p in phi.iterate_leaf_formulas() if p in self.meta_variables)

    def get_propositional_variable_tuple(self, phi: fl1.Formula) -> tuple[PropositionalVariable, ...]:
        return self.propositional_logic.get_propositional_variable_tuple(phi=phi)

    def is_well_formed_formula(self, phi: fl1.Formula) -> bool:
        """Return True if phi is a well-formed-formula in meta-language, False otherwise."""
        if phi in self.meta_variables:
            # if phi is a meta-language meta-variable, then it is a well-formed formula.
            return True
        elif self.propositional_logic.is_well_formed_formula(phi=phi):
            # if phi is a well-formed formula in the PL1 sub-language, then it is a well-formed-formula,
            return True
        elif phi in self.compound_formulas:
            # if phi is a well-formed formula in the meta-language sub-language, then it is a well-formed-formula,
            return True
        else:
            # otherwise, return False, i.e.: phi is not a well-formed-formula.
            return False

    @property
    def meta_variables(self) -> MetaVariableCollection:
        """The collection of propositional variables declared in PL1."""
        return self._meta_variables

    @property
    def propositional_logic(self) -> PropositionalLogic:
        """The collection of propositional variables declared in PL1."""
        return self._propositional_logic

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
        elif phi.is_an_element_of_typesetting_class(c=typesetting_classes.pl1_variable):
            return phi
        elif phi.is_an_element_of_typesetting_class(c=fl1.typesetting_classes.unary_formula):
            phi: fl1.UnaryFormula
            connective: fl1.Connective = phi.connective
            connective: fl1.UnaryConnective
            term: fl1.Formula = self.substitute_meta_variables(phi=phi.term, m=m)
            psi = self.propositional_logic.compound_formulas.declare_unary_formula(connective=connective, term=term)
            return psi
        elif phi.is_an_element_of_typesetting_class(c=fl1.typesetting_classes.binary_formula):
            phi: fl1.BinaryFormula
            connective: fl1.Connective = phi.connective
            connective: fl1.BinaryConnective
            term_1: fl1.Formula = self.substitute_meta_variables(phi=phi.term_1, m=m)
            term_2: fl1.Formula = self.substitute_meta_variables(phi=phi.term_2, m=m)
            psi = self.propositional_logic.compound_formulas.declare_binary_formula(connective=connective,
                                                                                    term_1=term_1, term_2=term_2)
            return psi
        else:
            log.error(msg='unsupported class.')


class PropositionalLogic(fl1.FormalLanguage):
    """Propositional Logic 1."""

    def __init__(self, set_as_default: bool = False, tc: typing.Optional[ts.TypesettingClass] = None):
        tc = ts.validate_tc(tc=tc, superclass=typesetting_classes.logical_calculi)
        super().__init__(set_as_default=set_as_default, tc=tc)
        # Meta-language
        self._meta_language: MetaLanguage = MetaLanguage(propositional_logic=self)
        # Object classes
        self._connectives: ConnectiveCollection = ConnectiveCollection(formal_language=self)
        super()._add_class(x=self._connectives)
        self._inference_rules: PropositionalLogicInferenceRuleCollection = PropositionalLogicInferenceRuleCollection(
            propositional_logic=self)
        super()._add_class(x=self._inference_rules)
        self._compound_formulas: PropositionalLogicCompoundFormulaCollection = PropositionalLogicCompoundFormulaCollection(
            formal_language=self)
        super()._add_class(x=self._compound_formulas)
        self._propositional_variables: PropositionalVariableCollection = PropositionalVariableCollection(
            formal_language=self)
        super()._add_class(x=self._propositional_variables)
        self._axioms: fl1.AxiomCollection = fl1.AxiomCollection(formal_language=self)
        self.lock()

    @property
    def axioms(self) -> fl1.AxiomCollection:
        """The collection of axioms in PL1."""
        return self._axioms

    @property
    def connectives(self) -> ConnectiveCollection:
        """The collection of connectives in PL1."""
        return self._connectives

    @property
    def compound_formulas(self) -> PropositionalLogicCompoundFormulaCollection:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: Formula,
                               term_2: Formula) -> fl1.BinaryFormula:
        return self.compound_formulas.declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: Formula) -> fl1.UnaryFormula:
        return self.compound_formulas.declare_unary_formula(connective=connective, term=term)

    @property
    def inference_rules(self) -> PropositionalLogicInferenceRuleCollection:
        """The collection of inference-rules in PL1."""
        return self._inference_rules

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

    def get_propositional_variable_tuple(self, phi: fl1.Formula) -> tuple[PropositionalVariable, ...]:
        return tuple(p for p in phi.iterate_leaf_formulas() if p in self.propositional_variables)

    @property
    def meta_language(self) -> MetaLanguage:
        """The meta-language of PL1."""
        return self._meta_language

    @property
    def propositional_variables(self) -> PropositionalVariableCollection:
        """The collection of declared propositional variables declared in PL1."""
        return self._propositional_variables


log.debug(f"Module {__name__}: loaded.")
