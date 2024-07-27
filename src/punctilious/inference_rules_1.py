# import typing
import sys

import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
import connectives_standard_library_1 as cls1

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
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            p=(
                cls1.is_a_proposition(phi),
                cls1.is_a_proposition(psi),
                phi,
                psi,),
            c=phi | cls1.land | psi,
            v=(phi, psi,)),
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
    simplification_1_rule: as1.TransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        p=(
            cls1.is_a_proposition(phi),
            cls1.is_a_proposition(psi),
            phi | cls1.land | psi,),
        c=phi,
        v=(phi, psi,))
simplification_1_axiom: as1.InferenceRule = as1.InferenceRule(
    f=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    simplification_2_rule: as1.TransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        p=(
            cls1.is_a_proposition(phi),
            cls1.is_a_proposition(psi),
            phi | cls1.land | psi,),
        c=psi,
        v=(phi, psi,))
simplification_2_axiom: as1.InferenceRule = as1.InferenceRule(
    f=simplification_2_rule)

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
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            p=(
                cls1.is_a_proposition(phi),
                cls1.is_a_proposition(psi),
                phi | cls1.implies | psi,
                phi),
            c=psi,
            v=(phi, psi,)),
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


def extend_theory_with_inference_rules_1(t: as1.FlexibleTheory) -> as1.Theory:
    """Extends a theory with:
     - the catalog of foundational inference-rules found in inference-rules-1.
     - TODO: add some theory-specific heuristics?

    """
    global conjunction_introduction, simplification_1_axiom, simplification_2_axiom, modus_ponens
    t: as1.Theory = as1.coerce_theory(t=t)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=conjunction_introduction)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=simplification_1_axiom)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=simplification_2_axiom)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=modus_ponens)
    return t
