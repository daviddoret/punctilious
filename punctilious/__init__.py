"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, prnt, serif_bold
from core import Article, AxiomDeclaration, AxiomInclusion, ComposableBlockSequence, classes, \
    configuration, consistency_values, DashedName, create_universe_of_discourse, \
    DefinitionInclusion, Encoding, encodings, FailedVerificationException, Formula, FreeVariable, \
    Header, InconsistencyWarning, interpret_formula, interpret_statement_formula, is_in_class, \
    InferredStatement, NoteInclusion, Paragraph, ParagraphHeader, paragraph_headers, \
    prioritize_value, QuasiQuotation, Relation, rep_two_columns_proof_item, ScriptNormal, \
    SansSerifBold, SansSerifNormal, SerifBoldItalic, SerifItalic, SerifNormal, SimpleObjct, \
    Statement, Subscript, subscriptify, paragraph_headers, ComposableText, NameSet, SymbolicObject, \
    TextStyle, text_styles, TheoreticalObject, TheoryElaborationSequence, TheoryPackage, \
    paragraph_headers, UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

from locale_en_us import locale_en_us

# Configure the default locale
configuration.locale = locale_en_us

print('Punctilious package: initialized.')
