"""Punctilious: punctilious/__init__.py

"""
__version__ = "1.0.9"

from punctilious.plaintext import force_plaintext, Plaintext, unidecode
from punctilious.repm import monospace, prnt, serif_bold
from punctilious.core import AbsorptionDeclaration, AbsorptionInclusion, Article, AxiomDeclaration, \
    AxiomInclusion, BiconditionalElimination1Declaration, BiconditionalElimination1Inclusion, \
    BiconditionalElimination2Declaration, BiconditionalElimination2Inclusion, \
    BiconditionalIntroductionDeclaration, BiconditionalIntroductionInclusion, classes, \
    ComposableBlockSequence, ComposableText, configuration, ConjunctionElimination1Declaration, \
    ConjunctionElimination1Inclusion, ConjunctionElimination2Declaration, \
    ConjunctionElimination2Inclusion, ConjunctionIntroductionDeclaration, \
    ConjunctionIntroductionInclusion, consistency_values, create_universe_of_discourse, DashedName, \
    DefinitionInclusion, DisjunctionIntroduction1Declaration, DisjunctionIntroduction1Inclusion, \
    DisjunctionIntroduction2Declaration, DisjunctionIntroduction2Inclusion, \
    DoubleNegationEliminationDeclaration, DoubleNegationEliminationInclusion, \
    DoubleNegationIntroductionDeclaration, DoubleNegationIntroductionInclusion, Encoding, encodings, \
    EqualityCommutativityDeclaration, EqualityCommutativityInclusion, \
    EqualTermsSubstitutionDeclaration, EqualTermsSubstitutionInclusion, FailedVerificationException, \
    Formula, FreeVariable, Header, Hypothesis, InconsistencyIntroduction1Declaration, \
    InconsistencyIntroduction1Inclusion, InconsistencyIntroduction2Declaration, \
    InconsistencyIntroduction2Inclusion, InconsistencyIntroduction3Declaration, \
    InconsistencyIntroduction3Inclusion, InconsistencyWarning, InferenceRuleDeclaration, \
    InferenceRuleDeclarationCollection, InferenceRuleInclusion, InferenceRuleInclusionCollection, \
    InferredStatement, interpret_formula, interpret_statement_formula, is_in_class, \
    ModusPonensDeclaration, ModusPonensInclusion, NameSet, NoteInclusion, Paragraph, \
    paragraph_headers, ParagraphHeader, prioritize_value, ProofByContradiction1Declaration, \
    ProofByContradiction1Inclusion, ProofByContradiction2Declaration, \
    ProofByContradiction2Inclusion, ProofByRefutation1Declaration, ProofByRefutation1Inclusion, \
    ProofByRefutation2Declaration, ProofByRefutation2Inclusion, QuasiQuotation, Relation, \
    rep_two_columns_proof_item, SansSerifBold, SansSerifNormal, ScriptNormal, SerifBoldItalic, \
    SerifItalic, SerifNormal, SimpleObjct, SimpleObjctDict, Statement, Subscript, subscriptify, \
    SymbolicObject, text_styles, TextStyle, TheoreticalObject, TheoryElaborationSequence, Package, \
    UniverseOfDiscourse, VariableSubstitutionDeclaration, VariableSubstitutionInclusion

# from foundation_system_1 import foundation_system_1, ft, u

from punctilious.locale_en_us import locale_en_us

# Configure the default locale
configuration.locale = locale_en_us

print(
    'Welcome to punctilious. The library documentation is available here: https://punctilious.readthedocs.io/en/latest/')
