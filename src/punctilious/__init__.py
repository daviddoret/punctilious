"""Punctilious: punctilious/__init__.py

"""
__version__ = "1.0.10"

from punctilious.plaintext import force_plaintext, Plaintext, unidecode
from punctilious.repm import monospace, prnt, serif_bold
from punctilious.core import (AbsorptionDeclaration, AbsorptionInclusion, Article, AxiomDeclaration, AxiomInclusion,
    AxiomInterpretationDeclaration, AxiomInterpretationInclusion, BiconditionalElimination1Declaration,
    BiconditionalElimination1Inclusion, BiconditionalElimination2Declaration, BiconditionalElimination2Inclusion,
    BiconditionalIntroductionDeclaration, BiconditionalIntroductionInclusion, BoundVariable, ClassDeclaration,
    classes_OBSOLETE, ComposableBlockSequence, ComposableText, configuration, ConjunctionElimination1Declaration,
    ConjunctionElimination1Inclusion, ConjunctionElimination2Declaration, ConjunctionElimination2Inclusion,
    ConjunctionIntroductionDeclaration, ConjunctionIntroductionInclusion, consistency_values, ConstantDeclaration,
    ConstantDeclarationDict, ConstructiveDilemmaDeclaration, ConstructiveDilemmaInclusion, create_universe_of_discourse,
    DashedName, DefinitionInclusion, DefinitionInterpretationDeclaration, DefinitionInterpretationInclusion, \
    DestructiveDilemmaDeclaration, DestructiveDilemmaInclusion, DisjunctionIntroduction1Declaration, \
    DisjunctionIntroduction1Inclusion, DisjunctionIntroduction2Declaration, DisjunctionIntroduction2Inclusion,
    DisjunctiveResolutionDeclaration, DisjunctiveResolutionInclusion, DisjunctiveSyllogism1Declaration, \
    DisjunctiveSyllogism1Inclusion, DisjunctiveSyllogism2Declaration, DisjunctiveSyllogism2Inclusion,
    DoubleNegationEliminationDeclaration, DoubleNegationEliminationInclusion, DoubleNegationIntroductionDeclaration, \
    DoubleNegationIntroductionInclusion, Encoding, encodings, EqualityCommutativityDeclaration, \
    EqualityCommutativityInclusion, EqualTermsSubstitutionDeclaration, EqualTermsSubstitutionInclusion, ErrorCode,
    error_codes, FormulaAccretor, formula_alpha_contains, get_formula_unique_variable_ordered_set, PunctiliousException,
    CompoundFormula, FreeVariable, Header, Hypothesis, HypotheticalSyllogismDeclaration, HypotheticalSyllogismInclusion,
    InconsistencyIntroduction1Declaration, InconsistencyIntroduction1Inclusion, InconsistencyIntroduction2Declaration,
    InconsistencyIntroduction2Inclusion, InconsistencyIntroduction3Declaration, InconsistencyIntroduction3Inclusion,
    InconsistencyWarning, InferenceRuleDeclaration, InferenceRuleDeclarationAccretor, InferenceRuleInclusion,
    InferenceRuleInclusionCollection, InferredStatement, is_alpha_equivalent_to, is_alpha_equivalent_to_iterable,
    is_in_class_OBSOLETE, iterate_formula_data_model_components, is_declaratively_member_of_class,
    is_derivably_member_of_class, ModusPonensDeclaration, ModusPonensInclusion, ModusTollensDeclaration,
    ModusTollensInclusion, NameSet, NoteInclusion, Paragraph, paragraph_headers, ParagraphHeader, prioritize_value,
    ProofByContradiction1Declaration, ProofByContradiction1Inclusion, ProofByContradiction2Declaration,
    ProofByContradiction2Inclusion, ProofByRefutation1Declaration, ProofByRefutation1Inclusion,
    ProofByRefutation2Declaration, ProofByRefutation2Inclusion, PunctiliousException, QuasiQuotation, Connective,
    rep_two_columns_proof_item, SansSerifBold, SansSerifNormal, ScriptNormal, SerifBoldItalic, SerifItalic, SerifNormal,
    SimpleObjct, SimpleObjctDict, Statement, StyledText, Subscript, subscriptify, SymbolicObject, text_styles,
    TextStyle, Formula, TheoryDerivation, TheoryPackage, UniverseOfDiscourse, Variable, VariableSubstitutionDeclaration,
    VariableSubstitutionInclusion, verify, verify_formula, verify_formula_statement, verify_universe_of_discourse)

# from foundation_system_1 import foundation_system_1, ft, u

from punctilious.locale_en_us import locale_en_us

# Configure the default locale
configuration.locale = locale_en_us

print(
    'Welcome to punctilious. The library documentation is available here: https://punctilious.readthedocs.io/en/latest/')
