# formal-language constants

FORMULA_CONNECTOR_INDEX: int = 0
FORMULA_ARGUMENTS_INDEX: int = 1
FORMULA_FIXED_ARITY: int = 2

# meta-language formula structures

AXIOM_VALID_STATEMENT_INDEX: int = 0
AXIOM_FIXED_ARITY: int = 1

EXTENSION_MAP_DOMAIN_INDEX: int = 0  # The index-position of the `domain` element in the `arguments` tuple.
EXTENSION_MAP_CODOMAIN_INDEX: int = 1  # The index-position of the `codomain` element in the `arguments` tuple.
EXTENSION_MAP_FIXED_ARITY: int = 2  # A syntactic-rule.

NATURAL_INFERENCE_RULE_VARIABLES_INDEX: int = 0
NATURAL_INFERENCE_RULE_PREMISES_INDEX: int = 1
NATURAL_INFERENCE_RULE_CONCLUSION_INDEX: int = 2
NATURAL_INFERENCE_RULE_FIXED_ARITY: int = 3

THEOREM_STATEMENT_INDEX: int = 0
THEOREM_INPUTS_INDEX: int = 1
THEOREM_INFERENCE_RULE_INDEX: int = 2
THEOREM_FIXED_ARITY: int = 3
