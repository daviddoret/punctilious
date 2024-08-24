"""The connectives_standard_library_1 (aka csl1) module is a catalog of standardized mathematical connectives for easy
reference and reuse in theory development.

Provides short and user-friendly versions of the connectives.
"""

import axiomatic_system_1 as as1

algorithm = as1.connective_for_algorithm_formula
axiom = as1.connective_for_axiom_formula
axiomatization = as1.connective_for_axiomatization_formula
enumeration = as1.connective_for_enumeration
derivation = as1.connective_for_theory_component
hypothesis = as1.connective_for_hypothesis
implies = as1.connective_for_logical_implication
inference = as1.connective_for_inference
inference_rule = as1.connective_for_inference_rule
# is_a = as1.is_a_connective
is_well_formed_formula = as1.connective_for_is_well_formed_formula
is_well_formed_inference_rule = as1.connective_for_is_well_formed_inference_rule
is_well_formed_theory = as1.connective_for_is_well_formed_theoretical_context
land = as1.connective_for_logical_conjunction
lnot = as1.connective_for_logical_negation
lor = as1.connective_for_logical_disjunction
proves = as1.connective_for_proves
"""
Synonyms:
 - proves
 - right-tack
 - turnstile
"""
right_tack = as1.connective_for_proves
"""
Synonyms:
 - proves
 - right-tack
 - turnstile
"""
turnstile = as1.connective_for_proves
"""
Synonyms:
 - proves
 - right-tack
 - turnstile
"""
is_inconsistent = as1.connective_for_is_inconsistent

map_formula = as1.connective_for_map
"""The connective dedicated to signaling map formulas. Cf. Map python-class."""

natural_transformation = as1.transformation_by_variable_substitution_connective
is_a_proposition = as1.connective_for_is_a_proposition
is_a_propositional_variable = as1.connective_for_is_a_propositional_variable
theorem = as1.connective_for_theorem
theory_formula = as1.connective_for_theory
transformation = as1.transformation_by_variable_substitution_connective
tupl = as1.connective_for_tupl
extends = as1.connective_for_extension
