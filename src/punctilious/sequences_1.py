import collections
import axiomatic_system_1 as as1

land = as1._connectives.land
implies = as1._connectives.implies
is_a = as1._connectives.is_a

sequence_of_numbers = as1.let_x_be_a_simple_object(formula_ts='sequence-of-numbers')
bounded_above = as1.let_x_be_a_simple_object(formula_ts='bounded-above')
bounded_below = as1.let_x_be_a_simple_object(formula_ts='bounded-below')
bounded = as1.let_x_be_a_simple_object(formula_ts='bounded')
unbounded = as1.let_x_be_a_simple_object(formula_ts='unbounded')
upper_bound = as1.let_x_be_a_simple_object(formula_ts='upper-bound')
lower_bound = as1.let_x_be_a_simple_object(formula_ts='lower-bound')

an = as1.let_x_be_a_simple_object(formula_ts='an')

axiom_1 = (an | is_a | sequence_of_numbers) | land | (
        (an | is_a | bounded_above)
        | land |
        (an | is_a | bounded_below)
) | implies | (an | is_a | bounded)
print(axiom_1)
