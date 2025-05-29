import pytest

import punctilious.rooted_plane_tree as rpt


class TestRootedPlaneTree:
    def test_sample_rooted_plane_trees(self):
        t1 = rpt.RootedPlaneTree()
        assert t1.is_leaf
        assert t1.degree == 0
        assert t1.ahu_unsorted_string == "()"
        assert t1.ahu_unsorted_inverted_binary_string == "10"
        assert t1.ahu_unsorted_inverted_integer == 2
        t2 = rpt.RootedPlaneTree(t1)
        assert not t2.is_leaf
        assert t2.degree == 1
        assert t2.ahu_unsorted_string == "(())"
        assert t2.ahu_unsorted_inverted_binary_string == "1100"
        assert t2.ahu_unsorted_inverted_integer == 12
        t3 = rpt.RootedPlaneTree(t1, t1, t1, t1, t1)
        assert not t3.is_leaf
        assert t3.degree == 5
        assert t3.ahu_unsorted_string == "(()()()()())"
        assert t3.ahu_unsorted_inverted_binary_string == "110101010100"
        assert t3.ahu_unsorted_inverted_integer == 3412
        t4 = rpt.RootedPlaneTree(t1, t2, t3, t2)
        assert not t4.is_leaf
        assert t4.degree == 4
        assert t4.ahu_unsorted_string == "(()(())(()()()()())(()))"
        assert t4.ahu_unsorted_inverted_binary_string == "110110011010101010011000"
        assert t4.ahu_unsorted_inverted_integer == 14264984
