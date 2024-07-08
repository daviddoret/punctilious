import pytest
import logging
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


class TestMT1:
    def test_mt1(self):
        t = as1.let_x_be_a_theory()
        m = as1.let_x_be_a_theory()
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=pu.mt1.mt1)
        c = is_well_formed_theory_predicate(t)
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(t,))
        pass


class TestMT2:
    def test_mt2(self):
        t = as1.let_x_be_a_theory(ref_ts='t')
        m = as1.let_x_be_a_theory(ref_ts='m')
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=pu.mt1.mt1)
        c = theory_predicate(t)
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(t,))
        pass
