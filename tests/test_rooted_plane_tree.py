import pytest

import punctilious.rooted_plane_tree as rpt


@pytest.fixture
def t1():
    return rpt.RootedPlaneTree()


@pytest.fixture
def t2(t1):
    return rpt.RootedPlaneTree(t1)


@pytest.fixture
def t3(t1):
    return rpt.RootedPlaneTree(t1, t1, t1, t1, t1)


@pytest.fixture
def t4(t1, t2, t3):
    return rpt.RootedPlaneTree(t1, t2, t3, t2)


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
        assert t1.is_rooted_plane_tree_equivalent_to(rpt.RootedPlaneTree())
        assert t2.is_rooted_plane_tree_equivalent_to(rpt.RootedPlaneTree(t1))
        assert t3.is_rooted_plane_tree_equivalent_to(rpt.RootedPlaneTree(t1, t1, t1, t1, t1))
        assert t4.is_rooted_plane_tree_equivalent_to(rpt.RootedPlaneTree(t1, t2, t3, t2))
