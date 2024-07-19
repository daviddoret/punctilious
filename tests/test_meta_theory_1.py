import pytest
import logging
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


class TestMT1:
    def test_mt1(self):
        a = as1.let_x_be_a_simple_object(formula_ts='a')
        t = as1.let_x_be_a_theory()
        m = as1.let_x_be_a_theory()
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=pu.mt1.mt1)
        c = is_well_formed_formula(a)
        m, d = as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(a,))
        assert as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        # TODO: BUG: Testing the inference-rule does not "work" because as a formula it contains
        #   the variable that it is itself using. This is an interesting case that must be
        #   further investigated and solved.
        # c = is_well_formed_formula_predicate(i)
        # m, d = as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(pu.mt1.mt1,))
        # assert as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = is_well_formed_formula(t)
        m, d = as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(t,))
        assert as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        pass


class TestMT2:
    def test_mt2(self):
        a = as1.let_x_be_a_simple_object(formula_ts='a')
        t = as1.let_x_be_a_theory()
        m = as1.let_x_be_a_theory()
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=pu.mt1.mt2)
        x = as1.is_well_formed_inference_rule(i=a)
        # A simple-object formula is not an inference-rule
        c = pu.mt1.is_well_formed_inference_rule(a)
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(a,))
        # TODO: BUG: The derivation should return lnot(is_well_formed_inference_rule_predicate(a)).
        #   is_well_formed_inference_rule works properly, probably derive_1 returns c directly.
        assert as1.is_formula_equivalent(phi=lnot(c), psi=d.valid_statement)
        # A theory is not an inference-rule
        c = is_well_formed_inference_rule(t)
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(t,))
        assert as1.is_formula_equivalent(phi=lnot(c), psi=d.valid_statement)
        pass


class TestMT3:
    def test_mt3(self):
        # TODO: Implement strict connective constraints on theories and introduce a test
        #   checking that an atomic-object is not a theory.
        m = as1.let_x_be_a_theory()  # meta-theory

        # Proper theory t allows to derive (is-well-formed-theory(t)).
        t = as1.let_x_be_a_theory()  # target or object theory
        m, i = as1.let_x_be_an_inference_rule(t1=m, i=pu.mt1.mt3)
        c = is_well_formed_theory(t)  # This is a formula
        m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(t,))
        assert as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # Simple object a does not allow to derive (is-well-formed-theory(a)).
        a = as1.let_x_be_a_simple_object(formula_ts='a')  # simple object
        c = is_well_formed_theory(a)  # This is a formula
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_MT1_002):
            m, d = as1.derive_1(t=m, c=c, p=None, i=i, a=(a,))

        pass
