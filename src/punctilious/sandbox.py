import natural_number_sequence_library as nnsl

n = 10
t = ()
for n in range(1, n):
    t = nnsl.NaturalNumberSequence.get_o1_ordered_set_of_natural_number_sequences_of_sum_n(n)
    print(len(t))
