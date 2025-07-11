import punctilious.routed_plane_tree_generator as g

for i in range(1, 10):
    print(len(g.RootedPlaneTreeDatabase.get_ordered_set_of_rooted_plane_trees_of_size_n(i)))
