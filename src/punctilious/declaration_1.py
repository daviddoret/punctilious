# TODO: The idea is to develop here a meta-theory that allows the usage of the := connective to declare
#   definitions.

# import presentation_layer_1 as pl1
import axiomatic_system_1 as as1

is_defined_as: as1.Connective = as1.BinaryConnective(formula_ts=':=')

# inference-rule:
# premises:
#   - is-a-symbol(s)
#   - s := phi
# conclusion:
#   d is any derivation
#   substitute(d,s,phi)

# idea:
#  - a static conclusion is not adequate, perhaps we could use a dynamic conclusion,
#     like a python-function conclusion_is_potentially_compatible_with_target(...) ???
#     is this worthwhile? or are we better off just computing the effective conclusions?
