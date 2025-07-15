import punctilious as pu

# n = 3

# a = tuple(pu.nnsl.get_sequences_of_natural_numbers_whose_sum_equals_n(n))
# b = tuple(
#    pu.nnsl.NaturalNumberSequence.get_o1_ordered_set_of_natural_number_sequences_of_sum_n(n))

# print(a)
# print(b)

c = pu.rptc.RootedPlaneTreeGenerator.get_ordered_set_of_rooted_plane_trees_of_size_n(4)
# print(c)
# for t in c:
#    s = tuple(x.size for x in t.immediate_subtrees)
#    print(s)
print(c[0])
print(c[0].represent_as_multiline_string_vertical_tree_representation())
print(c[1])
print(c[1].represent_as_multiline_string_vertical_tree_representation())
print(c[0].is_less_than_under_o1(c[1]))

x = c[0]
y = c[1]
print(x.immediate_subtrees[0])
print(y.immediate_subtrees[0])
print(x.immediate_subtrees[0].size)
print(y.immediate_subtrees[0].size)
print(x.immediate_subtrees[0] < y.immediate_subtrees[0])
pass

print("_____")

x = c[0][0]
y = c[1][0]
print(x.immediate_subtrees[0])
print(y.immediate_subtrees[0])
print(x.immediate_subtrees[0].size)
print(y.immediate_subtrees[0].size)
print(x.immediate_subtrees[0] < y.immediate_subtrees[0])
