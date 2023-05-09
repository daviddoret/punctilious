
def traverse_two_tuple_trees(tree_1, tree_2):
    if isinstance(tree_1, tuple) and isinstance(tree_2, tuple):
        for component_1, component_2 in zip(tree_1, tree_2):
            for sub_component_1, sub_component_2 in traverse_two_tuple_trees(component_1, component_2):
                yield sub_component_1, sub_component_2
    else:
        yield tree_1, tree_2

t1 = (1, 2, 3, (5, 6, 7), 4, 2, 2)
t2 = (1, 2, 3, (5, 6, 7), 4, 1, 2)

for x, y in traverse_two_tuple_trees(t1, t2):
    print([x, y])

l1 = list([1,2,3])
l1.append(5)
print(l1)
