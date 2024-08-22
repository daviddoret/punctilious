# import typing
import sys

import presentation_layer_1 as pl1
import axiomatic_system_1 as as1
import connectives_standard_library_1 as cls1

_current_module = sys.modules[__name__]
if __name__ == '__main__':
    raise ImportError(
        'This module does not support being directly executed as a script. Please use the import statement.')

# Basic inference rules

with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    conjunction_introduction: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
        f=as1.let_x_be_a_transformation_by_variable_substitution(
            i=(
                cls1.is_a_proposition(phi),
                cls1.is_a_proposition(psi),
                phi,
                psi,),
            o=phi | cls1.land | psi,
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
    simplification_1_rule: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        i=(
            cls1.is_a_proposition(phi),
            cls1.is_a_proposition(psi),
            phi | cls1.land | psi,),
        o=phi,
        v=(phi, psi,))
simplification_1_axiom: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
    f=simplification_1_rule)

# Simplification inference rule, aka conjunction elimination:
#   phi ∧ psi
#   ________
#   psi
#
# References:
#  - https://en.wikipedia.org/wiki/List_of_rules_of_inference
with as1.let_x_be_a_variable(formula_ts='phi') as phi, as1.let_x_be_a_variable(formula_ts='psi') as psi:
    simplification_2_rule: as1.WellFormedTransformationByVariableSubstitution = as1.let_x_be_a_transformation_by_variable_substitution(
        i=(
            cls1.is_a_proposition(phi),
            cls1.is_a_proposition(psi),
            phi | cls1.land | psi,),
        o=psi,
        v=(phi, psi,))
simplification_2_axiom: as1.WellFormedInferenceRule = as1.WellFormedInferenceRule(
    f=simplification_2_rule)

modus_ponens = as1.modus_ponens_inference_rule

axiomatization = as1.WellFormedAxiomatization(d=(
    conjunction_introduction,
    simplification_1_axiom,
    simplification_2_axiom,
    modus_ponens,))


def extend_theory_with_inference_rules_1(t: as1.FlexibleTheory) -> as1.WellFormedTheory:
    """Extends a theory with:
     - the catalog of foundational inference-rules found in inference-rules-1.
     - TODO: add some theory-specific heuristics?

    """
    global conjunction_introduction, simplification_1_axiom, simplification_2_axiom, modus_ponens_inference_rule
    t: as1.WellFormedTheory = as1.coerce_theory(t=t)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=conjunction_introduction)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=simplification_1_axiom)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=simplification_2_axiom)
    t, _ = as1.let_x_be_an_inference_rule(t=t, i=modus_ponens)
    return t
