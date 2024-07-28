"""The connectives_standard_library_1 (aka csl1) module is a catalog of standardized mathematical connectives for easy
reference and reuse in theory development.

Provides short and user-friendly versions of the connectives.
"""

import axiomatic_system_1 as as1

algorithm = as1.get_connectives().algorithm
axiom = as1.axiom_connective
axiomatization = as1.axiomatization_connective
enumeration = as1.enumeration_connective
derivation = as1.get_connectives().derivation
implies = as1.get_connectives().implies
inference = as1.get_connectives().inference
inference_rule = as1.get_connectives().inference_rule
is_a = as1.get_connectives().is_a
is_well_formed_formula = as1.is_well_formed_formula_connective
is_well_formed_inference_rule = as1.is_well_formed_inference_rule_connective
is_well_formed_theory = as1.is_well_formed_theory_connective
land = as1.logical_conjunction_connective
lnot = as1.logical_negation_connective
lor = as1.logical_disjunction_connective
proves = as1.get_connectives().proves
is_inconsistent = as1.get_connectives().is_inconsistent

map_formula = as1.get_connectives().map_formula
"""The connective dedicated to signaling map formulas. Cf. Map python-class."""

natural_transformation = as1.get_connectives().transformation_by_variable_substitution
is_a_proposition = as1.get_connectives().is_a_proposition
is_a_propositional_variable = as1.get_connectives().is_a_propositional_variable
theorem = as1.get_connectives().theorem
theory_formula = as1.get_connectives().theory_formula
transformation = as1.get_connectives().transformation_by_variable_substitution
tupl = as1.get_connectives().tupl
