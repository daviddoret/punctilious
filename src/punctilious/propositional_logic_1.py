"""This python module defines the PL1 formal-language."""

from __future__ import annotations

import abc
import typing

import log
import typesetting as ts
import formal_language_1 as fl1


# TODO: See Lawler, John. “Notation, Logical (See: Notation, Mathematical),” n.d. https://websites.umich.edu/~jlawler/IELL-LogicalNotation.pdf.
#   For a good synthesis on notation conventions for propositional logic.


class TypesettingClass(ts.TC):
    """A collection of typesetting-classes."""
    PL1_CONNECTIVE_CONJUNCTION = ts.TC(fl1.TypesettingClass.FL1_BINARY_CONNECTIVE)
    PL1_CONNECTIVE_DISJUNCTION = ts.TC(fl1.TypesettingClass.FL1_BINARY_CONNECTIVE)
    PL1_CONNECTIVE_MATERIAL_IMPLICATION = ts.TC(fl1.TypesettingClass.FL1_BINARY_CONNECTIVE)
    PL1_CONNECTIVE_NEGATION = ts.TC(fl1.TypesettingClass.FL1_UNARY_CONNECTIVE)
    PL1_INFERENCE_RULE_MODUS_PONENS = ts.TC(fl1.TypesettingClass.FL1_INFERENCE_RULE)
    PL1_CONNECTIVE_COLLECTION = ts.TC(fl1.TypesettingClass.FL1_CONNECTIVE_COLLECTION)
    PL1_INFERENCE_RULE_COLLECTION = ts.TC(fl1.TypesettingClass.FL1_INFERENCE_RULE_COLLECTION)
    PL1_COMPOUND_FORMULA_COLLECTION = ts.TC(fl1.TypesettingClass.FL1_COMPOUND_FORMULA_COLLECTION)
    PL1_ML_META_VARIABLE = ts.TC(fl1.TypesettingClass.FL1_ATOMIC_FORMULA)
    PL1_ML_META_LANGUAGE = ts.TC(fl1.TypesettingClass.FL1_META_LANGUAGE)
    PL1_ML_FORMULA = ts.TC(fl1.TypesettingClass.FL1_FORMULA)
    PL1_ML_UNARY_FORMULA = ts.TC(fl1.TypesettingClass.FL1_UNARY_FORMULA)
    PL1_ML_BINARY_FORMULA = ts.TC(fl1.TypesettingClass.FL1_BINARY_FORMULA)
    PL1_FORMULA = ts.TC(fl1.TypesettingClass.FL1_FORMULA)
    PL1_UNARY_FORMULA = ts.TC(fl1.TypesettingClass.FL1_UNARY_FORMULA)
    PL1_BINARY_FORMULA = ts.TC(fl1.TypesettingClass.FL1_BINARY_FORMULA)
    PL1_PROPOSITIONAL_VARIABLE = ts.TC(fl1.TypesettingClass.FL1_ATOMIC_FORMULA)
    PL1_AXIOM = ts.TC(fl1.TypesettingClass.FL1_AXIOM)
    PL1_AXIOM_PL1 = ts.TC(PL1_AXIOM)
    PL1_AXIOM_PL2 = ts.TC(PL1_AXIOM)
    PL1_PROPOSITIONAL_LOGIC_LANGUAGE = ts.TC(fl1.TypesettingClass.FL1_FORMAL_LANGUAGE)
    PL1_MINIMAL_PROPOSITIONAL_LOGIC_LANGUAGE = ts.TC(PL1_PROPOSITIONAL_LOGIC_LANGUAGE)


ts.TC.load_elements(cls=TypesettingClass)


class MetaVariable(fl1.AtomicFormula):

    def __init__(self, c: fl1.FormalLanguageCollection,
                 tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.PL1_ML_META_VARIABLE)
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
                 tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.PL1_PROPOSITIONAL_VARIABLE)
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

    def __init__(self, formal_language: PropositionalLogic, tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.PL1_CONNECTIVE_COLLECTION)
        super().__init__(formal_language=formal_language, tc=tc)
        # exhaustive declaration of PL1 connectives.
        self._conjunction: fl1.BinaryConnective = self.declare_binary_connective(
            tc=TypesettingClass.PL1_CONNECTIVE_CONJUNCTION)
        self._disjunction: fl1.BinaryConnective = self.declare_binary_connective(
            tc=TypesettingClass.PL1_CONNECTIVE_DISJUNCTION)
        self._material_implication: fl1.BinaryConnective = self.declare_binary_connective(
            tc=TypesettingClass.PL1_CONNECTIVE_MATERIAL_IMPLICATION)
        self._negation: fl1.UnaryConnective = self.declare_unary_connective(tc=TypesettingClass.PL1_CONNECTIVE_NEGATION)
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
        tc: ts.TC = TypesettingClass.PL1_UNARY_FORMULA
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
            log.error("connective is not a pl1 connective.", pl1=self.formal_language, connective=connective)
        if not self.propositional_logic.is_well_formed_formula(phi=term_1):
            log.error("term_1 is not a pl1 well-formed-formula.", pl1=self.formal_language, phi=term_1)
        if not self.propositional_logic.is_well_formed_formula(phi=term_2):
            log.error("term_2 is not a pl1 well-formed-formula.", pl1=self.formal_language, phi=term_2)
        tc: ts.TC = TypesettingClass.PL1_BINARY_FORMULA
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2,
                                                                tc=tc)
        return phi

    @property
    def propositional_logic(self) -> PropositionalLogic:
        return self._propositional_logic


class ModusPonens(fl1.InferenceRule):
    def __init__(self, c: fl1.FormalLanguageCollection,
                 tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.PL1_ML_META_VARIABLE)
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
        tc: ts.TC = fl1.TypesettingClass.FL1_INFERENCE_RULE
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
        tc: ts.TC = TypesettingClass.PL1_ML_UNARY_FORMULA
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
        tc: ts.TC = TypesettingClass.PL1_ML_BINARY_FORMULA
        phi: fl1.BinaryFormula = super().declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2,
                                                                tc=tc)
        return phi

    @property
    def meta_language(self) -> MetaLanguage:
        return self._meta_language


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

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: fl1.Formula,
                               term_2: fl1.Formula) -> fl1.BinaryFormula:
        return self.compound_formulas.declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    def declare_unary_formula(self, connective: fl1.BinaryConnective, term: fl1.Formula) -> fl1.BinaryFormula:
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
        elif phi.is_an_element_of_typesetting_class(tc=TypesettingClass.PL1_PROPOSITIONAL_VARIABLE):
            return phi
        elif phi.is_an_element_of_typesetting_class(tc=fl1.TypesettingClass.FL1_UNARY_FORMULA):
            phi: fl1.UnaryFormula
            connective: fl1.Connective = phi.connective
            connective: fl1.UnaryConnective
            term: fl1.Formula = self.substitute_meta_variables(phi=phi.term, m=m)
            psi = self.propositional_logic.compound_formulas.declare_unary_formula(connective=connective, term=term)
            return psi
        elif phi.is_an_element_of_typesetting_class(tc=fl1.TypesettingClass.FL1_BINARY_FORMULA):
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

    def __init__(self, set_as_default: bool = False,
                 tc: typing.Optional[ts.TC] = None):
        tc = ts.validate_tc(tc=tc, superclass=TypesettingClass.PL1_PROPOSITIONAL_LOGIC_LANGUAGE)
        self._meta_language: MetaLanguage = MetaLanguage(propositional_logic=self)
        super().__init__(set_as_default=set_as_default, tc=tc)
        self._inference_rules: PropositionalLogicInferenceRuleCollection = PropositionalLogicInferenceRuleCollection(
            propositional_logic=self)
        super()._add_class(x=self._inference_rules)
        self._compound_formulas: PropositionalLogicCompoundFormulaCollection = PropositionalLogicCompoundFormulaCollection(
            formal_language=self)
        super()._add_class(x=self._compound_formulas)
        self._propositional_variables: PropositionalVariableCollection = PropositionalVariableCollection(
            formal_language=self)
        super()._add_class(x=self._propositional_variables)
        self.lock()

    @property
    @abc.abstractmethod
    def axioms(self) -> fl1.AxiomCollection:
        """The collection of axioms in PL1."""
        log.error(msg='abstract method')

    @property
    @abc.abstractmethod
    def connectives(self) -> ConnectiveCollection:
        """The collection of connectives in PL1."""
        log.error(msg='abstract method')

    @property
    @abc.abstractmethod
    def compound_formulas(self) -> PropositionalLogicCompoundFormulaCollection:
        """The collection of declared compound formulas in PL1."""
        return self._compound_formulas

    def declare_binary_formula(self, connective: fl1.BinaryConnective, term_1: fl1.Formula,
                               term_2: fl1.Formula) -> fl1.BinaryFormula:
        return self.compound_formulas.declare_binary_formula(connective=connective, term_1=term_1, term_2=term_2)

    def declare_unary_formula(self, connective: fl1.UnaryConnective, term: fl1.Formula) -> fl1.UnaryFormula:
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


class MinimalistPropositionalLogicAxioms(fl1.AxiomCollection):
    def __init__(self, propositional_logic: PropositionalLogic):
        if isinstance(propositional_logic, PropositionalLogic):
            self._propositional_logic: PropositionalLogic = propositional_logic
        super().__init__(formal_language=propositional_logic)
        implies: fl1.BinaryConnective = self.propositional_logic.connectives.material_implication
        land: fl1.BinaryConnective = self.propositional_logic.connectives.conjunction
        a = self.propositional_logic.meta_language.meta_variables.declare_meta_variable()
        b = self.propositional_logic.meta_language.meta_variables.declare_meta_variable()
        c = self.propositional_logic.meta_language.meta_variables.declare_meta_variable()
        previous_default_formal_language = fl1.preferences.formal_language.value
        fl1.preferences.formal_language.value = self.propositional_logic.meta_language
        self._pl1 = fl1.Axiom(c=self, phi=a | implies | (a | land | a), tc=TypesettingClass.PL1_AXIOM_PL1)
        super().postulate_axiom(axiom=self._pl1)
        self._pl2 = fl1.Axiom(c=self, phi=(a | land | b) | implies | (b | land | a), tc=TypesettingClass.PL1_AXIOM_PL2)
        super().postulate_axiom(axiom=self._pl1)
        fl1.preferences.formal_language.value = previous_default_formal_language

    @property
    def propositional_logic(self) -> PropositionalLogic:
        return self._propositional_logic

    @property
    def pl1(self) -> fl1.Axiom:
        return self._pl1

    @property
    def pl2(self) -> fl1.Axiom:
        return self._pl2


class MinimalistPropositionalLogic(PropositionalLogic):

    def __init__(self, set_as_default: bool = True):
        super().__init__(set_as_default=set_as_default,
                         tc=TypesettingClass.PL1_MINIMAL_PROPOSITIONAL_LOGIC_LANGUAGE)
        self._connectives = ConnectiveCollection(formal_language=self)
        self._compound_formulas = PropositionalLogicCompoundFormulaCollection(formal_language=self)
        self._axioms: MinimalistPropositionalLogicAxioms = MinimalistPropositionalLogicAxioms(propositional_logic=self)

    @property
    def axioms(self) -> fl1.AxiomCollection:
        return self._axioms

    @property
    def connectives(self) -> ConnectiveCollection:
        return self._connectives

    @property
    def compound_formulas(self) -> PropositionalLogicCompoundFormulaCollection:
        return self._compound_formulas


log.debug(f"Module {__name__}: loaded.")
