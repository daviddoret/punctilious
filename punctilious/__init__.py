"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, serif_bold
from core import \
    Axiom, AxiomInclusion, \
    configuration, \
    DashedName, DefinitionEndorsement, DirectAxiomInference, DirectDefinitionInference, \
    FailedVerificationException, Formula, FreeVariable, \
    Note, note_categories, InconsistencyWarning, \
    ObjctHeader, \
    Relation, \
    SimpleObjct, Symbol, SymbolicObjct, statement_categories, \
    TheoryElaborationSequence, \
    UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
