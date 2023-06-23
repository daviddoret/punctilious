"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, prnt, serif_bold
from core import \
    AxiomDeclaration, AxiomInclusion, \
    configuration, \
    DashedName, DefinitionInclusion, DirectDefinitionInference, \
    FailedVerificationException, Formula, FreeVariable, \
    consistency_values, \
    Note, note_categories, InconsistencyWarning, \
    ObjctHeader, \
    Relation, \
    SimpleObjct, Symbol, SymbolicObjct, statement_categories, \
    TheoreticalObjct, TheoryElaborationSequence, \
    UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
