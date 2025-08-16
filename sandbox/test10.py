import punctilious as pu

s = pu.nn0sl.NaturalNumber0Sequence()
for i in range(32):
    r1 = pu.nn0sl.get_lexicographic_rank_within_adjusted_sum_and_length_class(s)
    r2 = pu.nn0sl.get_reverse_lexicographic_rank_within_adjusted_sum_and_length_class(s)
    print(f"{i} {s}     {r1}        {r2}")
    s = s.successor
