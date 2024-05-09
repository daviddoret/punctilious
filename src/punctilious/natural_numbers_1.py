import collections

import axiomatic_system_1 as as1

# if x is a natural number, then x++ is a natural number
is_a = as1.connectives.is_a
x = as1.let_x_be_a_variable()
natural_number = as1.let_x_be_a_simple_object()
successor = as1.let_x_be_a_unary_connective()
