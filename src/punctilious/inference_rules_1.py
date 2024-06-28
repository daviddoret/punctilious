# import typing
import sys

import axiomatic_system_1 as as1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')
_state = dict() if not hasattr(_current_module, '_state') else getattr(_current_module, '_state')


def _set_state(key: str, value: object):
    """An internal utility function to store module state and avoid
    issues with global variables being re-instanciated if modules are re-loaded."""
    global _state
    if key in _state.items():
        value = _state.get(key)
    else:
        _state[key] = value
    return value


# Propositional logic vocabulary
is_a = as1._connectives.is_a
implies = as1._connectives.implies
land = as1._connectives.land
lnot = as1._connectives.lnot
proposition = as1._connectives.proposition
propositional_variable = as1._connectives.propositional_variable

# Basic inference rules

# Adjunction inference rule, aka conjunction introduction:
#   phi
#   psi
#   ________
#   phi ∧ psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_typesetter='phi') as phi, as1.let_x_be_a_variable(formula_typesetter='psi') as psi:
    adjunction_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi,
            psi,),
        conclusion=phi | land | psi,
        variables=(phi, psi,))
adjunction_axiom: as1.InferenceRule = as1.InferenceRule(transformation=adjunction_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   phi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_typesetter='phi') as phi, as1.let_x_be_a_variable(formula_typesetter='psi') as psi:
    simplification_1_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=phi,
        variables=(phi, psi,))
simplification_1_axiom: as1.InferenceRule = as1.InferenceRule(transformation=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_typesetter='phi') as phi, as1.let_x_be_a_variable(formula_typesetter='psi') as psi:
    simplification_2_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | land | psi,),
        conclusion=psi,
        variables=(phi, psi,))
simplification_2_axiom: as1.InferenceRule = as1.InferenceRule(transformation=simplification_2_rule)

# Modus ponens inference rule:
#   phi --> psi
#   phi
#   ___________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_typesetter='P') as phi, as1.let_x_be_a_variable(formula_typesetter='Q') as psi:
    modus_ponens_rule: as1.Transformation = as1.let_x_be_a_transformation(
        premises=(
            phi | is_a | proposition,
            psi | is_a | proposition,
            phi | implies | psi,
            phi),
        conclusion=psi,
        variables=(phi, psi,))
modus_ponens_axiom: as1.InferenceRule = as1.InferenceRule(transformation=modus_ponens_rule)
"""Premises:
 - phi | is_a | proposition,
 - psi | is_a | proposition,
 - phi | implies | psi,
 - phi

Conclusion: psi

Variables: phi, psi
"""

axiomatization = as1.Axiomatization(derivations=(
    adjunction_axiom,
    simplification_1_axiom,
    simplification_2_axiom,
    modus_ponens_axiom,))
