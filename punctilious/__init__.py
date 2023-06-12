"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, serif_bold
from core import \
    Axiom, AxiomPostulate, \
    configuration, \
    DashedName, DefinitionEndorsement, DirectAxiomInference, DirectDefinitionInference, \
    FailedVerificationException, Formula, FreeVariable, \
    ModusPonensStatement, ModusPonensInferenceRule, \
    Note, note_categories, InconsistencyWarning, \
    ObjctHeader, \
    Relation, \
    SimpleObjct, Symbol, SymbolicObjct, statement_categories, \
    TheoryElaboration, \
    UniverseOfDiscourse

# from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
