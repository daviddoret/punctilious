import pytest

import punctilious as pu


@pytest.fixture
def t1():
    return pu.rpt.RootedPlaneTree()


@pytest.fixture
def t2(t1):
    return pu.rpt.RootedPlaneTree(t1)


@pytest.fixture
def t3(t1):
    return pu.rpt.RootedPlaneTree(t1, t1, t1, t1, t1)


@pytest.fixture
def t4(t1, t2, t3):
    return pu.rpt.RootedPlaneTree(t1, t2, t3, t2)


class TestRootedPlaneTree:
    def test_is_leaf(self, t1, t2, t3, t4):
        assert t1.is_leaf
        assert not t2.is_leaf
        assert not t3.is_leaf
        assert not t4.is_leaf

    def test_degree(self, t1, t2, t3, t4):
        assert t1.degree == 0
        assert t2.degree == 1
        assert t3.degree == 5
        assert t4.degree == 4

    def test_size(self, t1, t2, t3, t4):
        assert t1.size == 1
        assert t2.size == 2
        assert t3.size == 6
        assert t4.size == 12

    def test_ahu_unsorted_string(self, t1, t2, t3, t4):
        assert t1.ahu_unsorted_string == "()"
        assert t2.ahu_unsorted_string == "(())"
        assert t3.ahu_unsorted_string == "(()()()()())"
        assert t4.ahu_unsorted_string == "(()(())(()()()()())(()))"

    def test_ahu_unsorted_inverted_binary_string(self, t1, t2, t3, t4):
        assert t1.ahu_unsorted_inverted_binary_string == "10"
        assert t2.ahu_unsorted_inverted_binary_string == "1100"
        assert t3.ahu_unsorted_inverted_binary_string == "110101010100"
        assert t4.ahu_unsorted_inverted_binary_string == "110110011010101010011000"

    def test_ahu_unsorted_inverted_integer(self, t1, t2, t3, t4):
        assert t1.ahu_unsorted_inverted_integer == 2
        assert t2.ahu_unsorted_inverted_integer == 12
        assert t3.ahu_unsorted_inverted_integer == 3412
        assert t4.ahu_unsorted_inverted_integer == 14264984

    def test_is_rooted_plane_tree_equivalent_to(self, t1, t2, t3, t4):
        # equivalence with self
        assert t1.is_rooted_plane_tree_equivalent_to(t1)
        assert t2.is_rooted_plane_tree_equivalent_to(t2)
        assert t3.is_rooted_plane_tree_equivalent_to(t3)
        assert t4.is_rooted_plane_tree_equivalent_to(t4)
        # non-equivalences
        assert not t1.is_rooted_plane_tree_equivalent_to(t2)
        assert not t1.is_rooted_plane_tree_equivalent_to(t3)
        assert not t1.is_rooted_plane_tree_equivalent_to(t4)
        assert not t2.is_rooted_plane_tree_equivalent_to(t1)
        assert not t2.is_rooted_plane_tree_equivalent_to(t3)
        assert not t2.is_rooted_plane_tree_equivalent_to(t4)
        assert not t3.is_rooted_plane_tree_equivalent_to(t1)
        assert not t3.is_rooted_plane_tree_equivalent_to(t2)
        assert not t3.is_rooted_plane_tree_equivalent_to(t4)
        assert not t4.is_rooted_plane_tree_equivalent_to(t1)
        assert not t4.is_rooted_plane_tree_equivalent_to(t2)
        assert not t4.is_rooted_plane_tree_equivalent_to(t2)
        # equivalence with distinct instances
        assert t1.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree())
        assert t2.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(t1))
        assert t3.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(t1, t1, t1, t1, t1))
        assert t4.is_rooted_plane_tree_equivalent_to(pu.rpt.RootedPlaneTree(t1, t2, t3, t2))

    def test_cache(self, t1, t2, t3, t4):
        t1_clone = pu.rpt.RootedPlaneTree()
        assert t1 == t1_clone
        assert t1 is t1_clone
        t2_clone = pu.rpt.RootedPlaneTree(t1_clone)
        assert t2 == t2_clone
        assert t2 is t2_clone
        t3_clone = pu.rpt.RootedPlaneTree(t1_clone, t1_clone, t1_clone, t1_clone, t1_clone)
        assert t3 == t3_clone
        assert t3 is t3_clone
        t4_clone = pu.rpt.RootedPlaneTree(t1_clone, t2_clone, t3_clone, t2_clone)
        assert t4 == t4_clone
        assert t4 is t4_clone
        pass

    def test_select_sub_rooted_plane_tree_from_path_sequence(self, t1, t2, t3, t4):
        assert t1.select_sub_tree_from_path_sequence((1,)) == t1
        assert t2.select_sub_tree_from_path_sequence((1,)) == t2
        assert t2.select_sub_tree_from_path_sequence((1, 1,)) == t1
        assert t3.select_sub_tree_from_path_sequence((1,)) == t3
        assert t3.select_sub_tree_from_path_sequence((1, 1,)) == t1
        assert t3.select_sub_tree_from_path_sequence((1, 2,)) == t1
        assert t3.select_sub_tree_from_path_sequence((1, 3,)) == t1
        assert t3.select_sub_tree_from_path_sequence((1, 4,)) == t1
        assert t3.select_sub_tree_from_path_sequence((1, 5,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1,)) == t4
        assert t4.select_sub_tree_from_path_sequence((1, 1,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 2,)) == t2
        assert t4.select_sub_tree_from_path_sequence((1, 2, 1,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 3,)) == t3
        assert t4.select_sub_tree_from_path_sequence((1, 3, 1,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 3, 2,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 3, 3,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 3, 4,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 3, 5,)) == t1
        assert t4.select_sub_tree_from_path_sequence((1, 4,)) == t2
        assert t4.select_sub_tree_from_path_sequence((1, 4, 1,)) == t1

    def test_tuple_tree_constructor(self, t1, t2, t3, t4):
        t1b = pu.rpt.RootedPlaneTree(tuple_tree=())
        assert t1b == t1
        t2b = pu.rpt.RootedPlaneTree(tuple_tree=((),))
        assert t2b == t2
        t3b = pu.rpt.RootedPlaneTree(tuple_tree=((), (), (), (), (),))
        assert t3b == t3
        t4b = pu.rpt.RootedPlaneTree(tuple_tree=((), ((),), ((), (), (), (), (),), ((),),))
        assert t4b == t4

    def test_iterate_depth_first_ascending(self, t1, t2, t3, t4):
        l = tuple(t for t in t1.iterate_depth_first_ascending())
        assert l[0] == t1
        l = tuple(t for t in t2.iterate_depth_first_ascending())
        assert l[0] == t2
        assert l[1] == t1
        l = tuple(t for t in t3.iterate_depth_first_ascending())
        assert l[0] == t3
        assert l[1] == t1
        assert l[2] == t1
        assert l[3] == t1
        assert l[4] == t1
        assert l[5] == t1
        l = tuple(t for t in t4.iterate_depth_first_ascending())
        assert l[0] == t4
        assert l[1] == t1
        assert l[2] == t2
        assert l[3] == t1
        assert l[4] == t3
        assert l[5] == t1
        assert l[6] == t1
        assert l[7] == t1
        assert l[8] == t1
        assert l[9] == t1
        assert l[10] == t2
        assert l[11] == t1

    def test_iterate_children(self, t1, t2, t3, t4):
        l = tuple(t for t in t1.iterate_children())
        assert len(l) == 0
        l = tuple(t for t in t2.iterate_children())
        assert l[0] == t1
        l = tuple(t for t in t3.iterate_children())
        assert l[0] == t1
        assert l[1] == t1
        assert l[2] == t1
        assert l[3] == t1
        assert l[4] == t1
        l = tuple(t for t in t4.iterate_children())
        assert l[0] == t1
        assert l[1] == t2
        assert l[2] == t3
        assert l[3] == t2
