"""Punctilious: punctilious/__init__.py

"""
__version__ = "1.0.2"

from punctilious.plaintext import force_plaintext, Plaintext
from punctilious.repm import monospace, prnt, serif_bold
from punctilious.core import Article, AxiomDeclaration, AxiomInclusion, ComposableBlockSequence, \
    classes, configuration, consistency_values, DashedName, create_universe_of_discourse, \
    DefinitionInclusion, Encoding, encodings, FailedVerificationException, Formula, FreeVariable, \
    Header, Hypothesis, InconsistencyWarning, interpret_formula, interpret_statement_formula, \
    is_in_class, InferredStatement, NoteInclusion, Paragraph, ParagraphHeader, paragraph_headers, \
    prioritize_value, QuasiQuotation, Relation, rep_two_columns_proof_item, ScriptNormal, \
    SansSerifBold, SansSerifNormal, SerifBoldItalic, SerifItalic, SerifNormal, SimpleObjct, \
    Statement, Subscript, subscriptify, paragraph_headers, ComposableText, NameSet, SymbolicObject, \
    TextStyle, text_styles, TheoreticalObject, TheoryElaborationSequence, TheoryPackage, \
    paragraph_headers, UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

from punctilious.locale_en_us import locale_en_us

# Configure the default locale
configuration.locale = locale_en_us

print(
    'Welcome to punctilious. The library documentation is available here: https://punctilious.readthedocs.io/en/latest/')
