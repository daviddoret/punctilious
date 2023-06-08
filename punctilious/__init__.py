"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, serif_bold
from core import Axiom, AxiomInclusion, configuration, DashedName, Definition, FailedVerificationException, \
    Formula, \
    DirectAxiomInference, \
    DirectDefinitionInference, FreeVariable, ObjctHeader, \
    Note, note_categories, Relation, InconsistencyWarning, \
    SimpleObjct, Symbol, SymbolicObjct, statement_categories, TheoryElaboration, UniverseOfDiscourse
from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
