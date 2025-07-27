import pytest

import punctilious as pu


class TestNaturalNumber1:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn1l.NN1(0)

    def test_is_strictly_less_than(self):
        for i in range(1, 33):
            for j in range(1, 33):
                if i < j:
                    assert pu.nn1l.NN1(i).is_strictly_less_than(pu.nn1l.NN1(j))
                elif i >= j:
                    assert not pu.nn1l.NN1(i).is_strictly_less_than(pu.nn1l.NN1(j))
