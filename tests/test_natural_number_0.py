import pytest

import punctilious as pu


class TestNaturalNumber0:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn0l.NN0(-1)

    def test_is_strictly_less_than(self):
        for i in range(0, 33):
            for j in range(0, 33):
                if i < j:
                    assert pu.nn0l.NN0(i).is_strictly_less_than(pu.nn0l.NN0(j))
                elif i >= j:
                    assert not pu.nn0l.NN0(i).is_strictly_less_than(pu.nn0l.NN0(j))

    def test_is_strictly_greater_than(self):
        for i in range(0, 33):
            for j in range(0, 33):
                if i > j:
                    assert pu.nn0l.NN0(i).is_strictly_greater_than(pu.nn0l.NN0(j))
                elif i <= j:
                    assert not pu.nn0l.NN0(i).is_strictly_greater_than(pu.nn0l.NN0(j))
