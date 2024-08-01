"""The connectives_standard_library_1 (aka csl1) module is a catalog of standardized mathematical connectives for easy
reference and reuse in theory development.

Provides short and user-friendly versions of the connectives.
"""

import axiomatic_system_1 as as1

algorithm = as1.connective_for_algorithm
axiom = as1.connective_for_axiom
axiomatization = as1.connective_for_axiomatization
enumeration = as1.connective_for_enumeration
derivation = as1.connective_for_derivation
implies = as1.connective_for_logical_implication
inference = as1.connective_for_inference
inference_rule = as1.connective_for_inference_rule
is_a = as1.is_a_connective
is_well_formed_formula = as1.connective_for_is_well_formed_formula
is_well_formed_inference_rule = as1.connective_for_is_well_formed_inference_rule
is_well_formed_theory = as1.connective_for_is_well_formed_theory
land = as1.connective_for_logical_conjunction
lnot = as1.connective_for_logical_negation
lor = as1.connective_for_logical_disjunction
proves = as1.proves_connective
is_inconsistent = as1.is_inconsistent_connective

map_formula = as1.map_connective
"""The connective dedicated to signaling map formulas. Cf. Map python-class."""

natural_transformation = as1.transformation_by_variable_substitution_connective
is_a_proposition = as1.connective_for_is_a_proposition
is_a_propositional_variable = as1.is_a_propositional_variable_connective
theorem = as1.theorem_connective
theory_formula = as1.theory_connective
transformation = as1.transformation_by_variable_substitution_connective
tupl = as1.tupl_connective
