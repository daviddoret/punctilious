import pytest

import punctilious as pu


class TestFormula:
    def test_tree_size(self, phi1, phi2a, phi2b, phi6a):
        assert phi1.tree_size == 1
        assert phi2a.tree_size == 2
        assert phi2b.tree_size == 2
        assert phi6a.tree_size == 6

    def test_iterate_connectives(self, phi1, phi2a, phi2b, phi6a):
        l = tuple(t for t in phi1.iterate_connectives())
        assert l[0] == pu.connective_library.one
        l = tuple(t for t in phi2a.iterate_connectives())
        assert l[0] == pu.connective_library.one
        assert l[1] == pu.connective_library.one
        l = tuple(t for t in phi2b.iterate_connectives())
        assert l[0] == pu.connective_library.minus
        assert l[1] == pu.connective_library.one
        l = tuple(t for t in phi6a.iterate_connectives())
        assert l[0] == pu.connective_library.set_by_extension
        assert l[1] == pu.connective_library.one
        assert l[2] == pu.connective_library.two
        assert l[3] == pu.connective_library.three
        assert l[4] == pu.connective_library.four
        assert l[5] == pu.connective_library.five
