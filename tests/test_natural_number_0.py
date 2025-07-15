import pytest

import punctilious as pu


class TestNaturalNumber0:

    def test_constructor(self):
        with pytest.raises(Exception):
            pu.nn0l.NN0(-1)

    def test_order_relation_o1(self):
        pu.nn0l.NN0.set_default_order_relation(pu.nn0l.o1)
        for i in range(0, 33):
            for j in range(0, 33):
                if i < j:
                    assert pu.nn0l.NN0(i) < pu.nn0l.NN0(j)
                elif i >= j:
                    assert not (pu.nn0l.NN0(i) < pu.nn0l.NN0(j))

    def test_order_relation_o2(self):
        pu.nn0l.NN0.set_default_order_relation(pu.nn0l.o2)
        for i in range(0, 33):
            for j in range(0, 33):
                if i > j:
                    assert pu.nn0l.NN0(i) < pu.nn0l.NN0(j)
                elif i <= j:
                    assert not (pu.nn0l.NN0(i) < pu.nn0l.NN0(j))
