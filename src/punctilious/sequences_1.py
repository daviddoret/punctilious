import collections
import axiomatic_system_1 as as1

land = as1.connectives.land
implies = as1.connectives.implies
is_a = as1.connectives.is_a

sequence_of_numbers = as1.let_x_be_a_simple_object(formula_typesetter='sequence-of-numbers')
bounded_above = as1.let_x_be_a_simple_object(formula_typesetter='bounded-above')
bounded_below = as1.let_x_be_a_simple_object(formula_typesetter='bounded-below')
bounded = as1.let_x_be_a_simple_object(formula_typesetter='bounded')
unbounded = as1.let_x_be_a_simple_object(formula_typesetter='unbounded')
upper_bound = as1.let_x_be_a_simple_object(formula_typesetter='upper-bound')
lower_bound = as1.let_x_be_a_simple_object(formula_typesetter='lower-bound')

an = as1.let_x_be_a_simple_object(formula_typesetter='an')

axiom_1 = (an | is_a | sequence_of_numbers) | land | (
        (an | is_a | bounded_above)
        | land |
        (an | is_a | bounded_below)
) | implies | (an | is_a | bounded)
print(axiom_1)
