import pytest
import punctilious as pu


class TestNaturalNumber1:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn1l.NN1(-1)
        with pytest.raises(Exception):
            pu.nn1l.NN1(0)

    def test_order_relation_o1(self):
        pu.nn1l.NN1.set_default_order_relation(pu.nn1l.o1)
        for i in range(1, 33):
            for j in range(1, 33):
                if i < j:
                    assert pu.nn1l.NN1(i) < pu.nn1l.NN1(j)
                elif i >= j:
                    assert not (pu.nn1l.NN1(i) < pu.nn1l.NN1(j))

    def test_order_relation_o2(self):
        pu.nn1l.NN1.set_default_order_relation(pu.nn1l.o2)
        for i in range(1, 33):
            for j in range(1, 33):
                if i > j:
                    assert pu.nn1l.NN1(i) < pu.nn1l.NN1(j)
                elif i <= j:
                    assert not (pu.nn1l.NN1(i) < pu.nn1l.NN1(j))
