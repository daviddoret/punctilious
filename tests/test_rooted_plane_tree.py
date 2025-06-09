import pytest

import punctilious as pu


class TestRootedPlaneTree:
    def test_is_leaf(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.is_leaf
        assert not rpt2.is_leaf
        assert not rpt6a.is_leaf
        assert not rpt12a.is_leaf

    def test_degree(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.degree == 0
        assert rpt2.degree == 1
        assert rpt6a.degree == 5
        assert rpt12a.degree == 4

    def test_size(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.size == 1
        assert rpt2.size == 2
        assert rpt6a.size == 6
        assert rpt12a.size == 12

    def test_ahu_unsorted_string(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.ahu_unsorted_string == "()"
        assert rpt2.ahu_unsorted_string == "(())"
        assert rpt6a.ahu_unsorted_string == "(()()()()())"
        assert rpt12a.ahu_unsorted_string == "(()(())(()()()()())(()))"

    def test_ahu_unsorted_inverted_binary_string(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.ahu_unsorted_inverted_binary_string == "10"
        assert rpt2.ahu_unsorted_inverted_binary_string == "1100"
        assert rpt6a.ahu_unsorted_inverted_binary_string == "110101010100"
        assert rpt12a.ahu_unsorted_inverted_binary_string == "110110011010101010011000"

    def test_ahu_unsorted_inverted_integer(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.ahu_unsorted_inverted_integer == 2
        assert rpt2.ahu_unsorted_inverted_integer == 12
        assert rpt6a.ahu_unsorted_inverted_integer == 3412
        assert rpt12a.ahu_unsorted_inverted_integer == 14264984

    def test_is_rooted_plane_tree_equivalent_to(self, rpt1, rpt2, rpt6a, rpt12a):
        # equivalence with self
        assert rpt1.is_rooted_plane_tree_equivalent_to(rpt1)
        assert rpt2.is_rooted_plane_tree_equivalent_to(rpt2)
        assert rpt6a.is_rooted_plane_tree_equivalent_to(rpt6a)
        assert rpt12a.is_rooted_plane_tree_equivalent_to(rpt12a)
        # non-equivalences
        assert not rpt1.is_rooted_plane_tree_equivalent_to(rpt2)
        assert not rpt1.is_rooted_plane_tree_equivalent_to(rpt6a)
        assert not rpt1.is_rooted_plane_tree_equivalent_to(rpt12a)
        assert not rpt2.is_rooted_plane_tree_equivalent_to(rpt1)
        assert not rpt2.is_rooted_plane_tree_equivalent_to(rpt6a)
        assert not rpt2.is_rooted_plane_tree_equivalent_to(rpt12a)
        assert not rpt6a.is_rooted_plane_tree_equivalent_to(rpt1)
        assert not rpt6a.is_rooted_plane_tree_equivalent_to(rpt2)
        assert not rpt6a.is_rooted_plane_tree_equivalent_to(rpt12a)
        assert not rpt12a.is_rooted_plane_tree_equivalent_to(rpt1)
        assert not rpt12a.is_rooted_plane_tree_equivalent_to(rpt2)
        assert not rpt12a.is_rooted_plane_tree_equivalent_to(rpt2)
        # equivalence with distinct instances
        assert rpt1.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree())
        assert rpt2.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(rpt1))
        assert rpt6a.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(rpt1, rpt1, rpt1, rpt1, rpt1))
        assert rpt12a.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(rpt1, rpt2, rpt6a, rpt2))

    def test_cache(self, rpt1, rpt2, rpt6a, rpt12a):
        t1_clone = pu.rpt.RootedPlaneTree()
        assert rpt1 == t1_clone
        assert rpt1 is t1_clone
        t2_clone = pu.rpt.RootedPlaneTree(t1_clone)
        assert rpt2 == t2_clone
        assert rpt2 is t2_clone
        t3_clone = pu.rpt.RootedPlaneTree(t1_clone, t1_clone, t1_clone, t1_clone, t1_clone)
        assert rpt6a == t3_clone
        assert rpt6a is t3_clone
        t4_clone = pu.rpt.RootedPlaneTree(t1_clone, t2_clone, t3_clone, t2_clone)
        assert rpt12a == t4_clone
        assert rpt12a is t4_clone
        pass

    def test_select_sub_rooted_plane_tree_from_path_sequence(self, rpt1, rpt2, rpt6a, rpt12a):
        assert rpt1.select_sub_tree_from_path_sequence((1,)) == rpt1
        assert rpt2.select_sub_tree_from_path_sequence((1,)) == rpt2
        assert rpt2.select_sub_tree_from_path_sequence((1, 1,)) == rpt1
        assert rpt6a.select_sub_tree_from_path_sequence((1,)) == rpt6a
        assert rpt6a.select_sub_tree_from_path_sequence((1, 1,)) == rpt1
        assert rpt6a.select_sub_tree_from_path_sequence((1, 2,)) == rpt1
        assert rpt6a.select_sub_tree_from_path_sequence((1, 3,)) == rpt1
        assert rpt6a.select_sub_tree_from_path_sequence((1, 4,)) == rpt1
        assert rpt6a.select_sub_tree_from_path_sequence((1, 5,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1,)) == rpt12a
        assert rpt12a.select_sub_tree_from_path_sequence((1, 1,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 2,)) == rpt2
        assert rpt12a.select_sub_tree_from_path_sequence((1, 2, 1,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3,)) == rpt6a
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3, 1,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3, 2,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3, 3,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3, 4,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 3, 5,)) == rpt1
        assert rpt12a.select_sub_tree_from_path_sequence((1, 4,)) == rpt2
        assert rpt12a.select_sub_tree_from_path_sequence((1, 4, 1,)) == rpt1

    def test_tuple_tree_constructor(self, rpt1, rpt2, rpt6a, rpt12a):
        t1b = pu.rpt.RootedPlaneTree(tuple_tree=())
        assert t1b == rpt1
        t2b = pu.rpt.RootedPlaneTree(tuple_tree=((),))
        assert t2b == rpt2
        t3b = pu.rpt.RootedPlaneTree(tuple_tree=((), (), (), (), (),))
        assert t3b == rpt6a
        t4b = pu.rpt.RootedPlaneTree(tuple_tree=((), ((),), ((), (), (), (), (),), ((),),))
        assert t4b == rpt12a

    def test_iterate_depth_first_ascending(self, rpt1, rpt2, rpt6a, rpt12a):
        l = tuple(t for t in rpt1.iterate_depth_first_ascending())
        assert l[0] == rpt1
        l = tuple(t for t in rpt2.iterate_depth_first_ascending())
        assert l[0] == rpt2
        assert l[1] == rpt1
        l = tuple(t for t in rpt6a.iterate_depth_first_ascending())
        assert l[0] == rpt6a
        assert l[1] == rpt1
        assert l[2] == rpt1
        assert l[3] == rpt1
        assert l[4] == rpt1
        assert l[5] == rpt1
        l = tuple(t for t in rpt12a.iterate_depth_first_ascending())
        assert l[0] == rpt12a
        assert l[1] == rpt1
        assert l[2] == rpt2
        assert l[3] == rpt1
        assert l[4] == rpt6a
        assert l[5] == rpt1
        assert l[6] == rpt1
        assert l[7] == rpt1
        assert l[8] == rpt1
        assert l[9] == rpt1
        assert l[10] == rpt2
        assert l[11] == rpt1

    def test_iterate_children(self, rpt1, rpt2, rpt6a, rpt12a):
        l = tuple(t for t in rpt1.iterate_children())
        assert len(l) == 0
        l = tuple(t for t in rpt2.iterate_children())
        assert l[0] == rpt1
        l = tuple(t for t in rpt6a.iterate_children())
        assert l[0] == rpt1
        assert l[1] == rpt1
        assert l[2] == rpt1
        assert l[3] == rpt1
        assert l[4] == rpt1
        l = tuple(t for t in rpt12a.iterate_children())
        assert l[0] == rpt1
        assert l[1] == rpt2
        assert l[2] == rpt6a
        assert l[3] == rpt2
