# import typing
import sys

import presentation_layer_1 as pl1
from connectives_standard_library_1 import *

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')
_state = dict() if not hasattr(_current_module, '_state') else getattr(_current_module, '_state')


def _set_state(key: str, value: object):
    """An internal utility function to store module state and avoid
    issues with global variables being re-instantiated if modules are re-loaded."""
    global _state
    if key in _state.items():
        value = _state.get(key)
    else:
        _state[key] = value
    return value


# Basic inference rules

with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    conjunction_introduction: as1.InferenceRule = as1.InferenceRule(
        t=as1.let_x_be_a_natural_transformation(
            premises=(
                phi | is_a | proposition,
                psi | is_a | proposition,
                phi,
                psi,),
            conclusion=phi | land | psi,
            variables=(phi, psi,)),
        ref_ts=pl1.Monospace(text='CI'))
    """The conjunction-introduction inference rule.
    
    Abbreviation: CI
    
    Aka:
     - Adjunction
     
    Premises:
     1. phi is-a proposition
     2. psi is-a proposition
     3. phi
     4. psi
     
    Conclusion: phi ∧ psi

    References:
     - https://en.wikipedia.org/wiki/List_of_rules_of_inference
    """

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   phi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    simplification_1_rule: as1.NaturalTransformation = as1.let_x_be_a_natural_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=phi,
        variables=(phi, psi,))
simplification_1_axiom: as1.InferenceRule = as1.InferenceRule(
    t=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    simplification_2_rule: as1.NaturalTransformation = as1.let_x_be_a_natural_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=psi,
        variables=(phi, psi,))
simplification_2_axiom: as1.InferenceRule = as1.InferenceRule(
    t=simplification_2_rule)

# Modus ponens inference rule:
#   phi --> psi
#   phi
#   ___________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_ts='P') as phi, as1.let_x_be_a_variable(formula_ts='Q') as psi:
    modus_ponens: as1.InferenceRule = as1.InferenceRule(
        t=as1.let_x_be_a_natural_transformation(
            premises=(
                phi | is_a | proposition,
                psi | is_a | proposition,
                phi | implies | psi,
                phi),
            conclusion=psi,
            variables=(phi, psi,)),
        ref_ts=pl1.Monospace(text='MP'))
    """The modus-ponens inference-rule.
    
    Abbreviation: MP
    
    Premises:
     1. phi | is_a | proposition,
     2. psi | is_a | proposition,
     3. phi | implies | psi,
     4. phi
    
    Conclusion: psi
    
    Variables: phi, psi
    """

axiomatization = as1.Axiomatization(d=(
    conjunction_introduction,
    simplification_1_axiom,
    simplification_2_axiom,
    modus_ponens,))
