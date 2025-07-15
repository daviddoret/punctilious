import pytest

import punctilious as pu


class TestNaturalNumber0:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn0l.NN0(-1)

    def test_canonical_order(self):
        for i in range(0, 33):
            for j in range(0, 33):
                if i < j:
                    assert pu.nn0l.NN0(i).relates(pu.nn0l.NN0(j))
                elif i >= j:
                    assert not pu.nn0l.NN0(i).relates(pu.nn0l.NN0(j))

    def test_strict_greater_than(self):
        for i in range(0, 33):
            for j in range(0, 33):
                if i > j:
                    assert pu.nn0l.strict_greater_than.relates(pu.nn0l.NN0(i), pu.nn0l.NN0(j))
                elif i <= j:
                    assert not pu.nn0l.strict_greater_than.relates(pu.nn0l.NN0(i), pu.nn0l.NN0(j))
