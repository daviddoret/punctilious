"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, prnt, serif_bold
from core import \
    AxiomDeclaration, AxiomInclusion, \
    classes, configuration, consistency_values, \
    DashedName, DefinitionInclusion, DirectDefinitionInference, \
    FailedVerificationException, Formula, FreeVariable, \
    is_in_class, \
    Note, note_categories, InconsistencyWarning, \
    ObjctHeader, \
    Relation, \
    SimpleObjct, Symbol, SymbolicObjct, statement_categories, \
    TheoreticalObjct, TheoryElaborationSequence, \
    UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
