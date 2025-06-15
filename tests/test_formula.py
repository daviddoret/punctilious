import pytest

import punctilious as pu


class TestFormula:
    def test_tree_size(self, phi1, phi2a, phi2b, phi6a):
        assert phi1.tree_size == 1
        assert phi2a.tree_size == 2
        assert phi2b.tree_size == 2
        assert phi6a.tree_size == 6
