"""The connectives_standard_library_1 (aka csl1) module is a catalog of standardized mathematical connectives for easy
reference and reuse in theory development.

Provides short and user-friendly versions of the connectives.
"""

import axiomatic_system_1 as as1

algorithm = as1.algorithm_connective
axiom = as1.axiom_connective
axiomatization = as1.axiomatization_connective
enumeration = as1.enumeration_connective
derivation = as1.derivation_connective
implies = as1.implies_connective
inference = as1.inference_connective
inference_rule = as1.inference_rule_connective
is_a = as1.is_a_connective
is_well_formed_formula = as1.is_well_formed_formula_connective
is_well_formed_inference_rule = as1.is_well_formed_inference_rule_connective
is_well_formed_theory = as1.is_well_formed_theory_connective
land = as1.logical_conjunction_connective
lnot = as1.logical_negation_connective
lor = as1.logical_disjunction_connective
proves = as1.proves_connective
is_inconsistent = as1.is_inconsistent_connective

map_formula = as1.map_connective
"""The connective dedicated to signaling map formulas. Cf. Map python-class."""

natural_transformation = as1.transformation_by_variable_substitution_connective
is_a_proposition = as1.is_a_proposition_connective
is_a_propositional_variable = as1.is_a_propositional_variable_connective
theorem = as1.theorem_connective
theory_formula = as1.theory_connective
transformation = as1.transformation_by_variable_substitution_connective
tupl = as1.tupl_connective
