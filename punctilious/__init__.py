"""Punctilious: punctilious/__init__.py

"""

print('Punctilious package (punctilious/__init__.py)')
from repm import monospace, serif_bold
from core import FailedVerificationException, Formula, DirectAxiomInference, \
    DirectDefinitionInference, FreeVariable, \
    Axiom, Definition, Note, Relation, \
    SimpleObjct, SymbolicObjct, Theory, UniverseOfDiscourse
from foundation_system_1 import ft, u

print('Punctilious package: initialized.')
