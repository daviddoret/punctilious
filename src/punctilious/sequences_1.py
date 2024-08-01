import collections
import axiomatic_system_1 as as1

land = as1.connective_for_logical_conjunction
implies = as1.connective_for_logical_implication
is_a = as1.is_a_connective

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
