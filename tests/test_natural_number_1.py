import pytest
import punctilious as pu


class TestNaturalNumber1:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn1l.NN1(-1)
        with pytest.raises(Exception):
            pu.nn1l.NN1(0)

    def test_canonical_order(self):
        for i in range(1, 33):
            for j in range(1, 33):
                if i < j:
                    assert pu.nn1l.NN1(i).relates(pu.nn1l.NN1(j))
                elif i >= j:
                    assert not (pu.nn1l.NN1(i).relates(pu.nn1l.NN1(j)))

    def test_strict_greater_than(self):
        for i in range(1, 33):
            for j in range(1, 33):
                if i > j:
                    assert pu.nn1l.strictly_greater_than.relates(pu.nn1l.NN1(i), pu.nn1l.NN1(j))
                elif i <= j:
                    assert not pu.nn1l.strictly_greater_than.relates(pu.nn1l.NN1(i), pu.nn1l.NN1(j))
