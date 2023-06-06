"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, serif_bold
from core import Axiom, configuration, Definition, FailedVerificationException, Formula, DirectAxiomInference, \
    DirectDefinitionInference, FreeVariable, \
    Note, note_categories, Relation, InconsistencyWarning, \
    SimpleObjct, SymbolicObjct, statement_categories, Theory, UniverseOfDiscourse
from foundation_system_1 import foundation_system_1, ft, u

print('Punctilious package: initialized.')
