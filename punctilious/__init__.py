"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, prnt, serif_bold
from core import \
    AxiomDeclaration, AxiomInclusion, \
    ComposableBlockSequence, \
    classes, configuration, consistency_values, \
    DashedName, declare_universe_of_discourse, DefinitionInclusion, DirectDefinitionInference, \
    Encoding, encodings, \
    FailedVerificationException, Formula, FreeVariable, \
    InconsistencyWarning, is_in_class, \
    NoteInclusion, \
    Paragraph, \
    QuasiQuotation, \
    Relation, rep_two_columns_proof_item, \
    ScriptNormal, SansSerifBold, SansSerifNormal, SerifNormal, SimpleObjct, \
    Subscript, subscriptify, \
    title_categories, ComposableText, NameSet, SymbolicObject, \
    TextStyle, text_styles, TheoreticalObject, \
    TheoryElaborationSequence, TheoryPackage, \
    title_categories, \
    UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

from locale_en_us import locale_en_us

# Configure the default locale
configuration.locale = locale_en_us

print('Punctilious package: initialized.')
