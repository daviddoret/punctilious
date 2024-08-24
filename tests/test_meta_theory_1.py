import pytest
# import logging
import punctilious as pu


class TestMT1:
    def test_mt1(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t = pu.as1.let_x_be_a_theory()
        m = pu.as1.let_x_be_a_theory()
        m, _ = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt1a)
        m, _ = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt1b)
        c = pu.as1.connective_for_is_well_formed_formula(a)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1a, a=(a,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        # TODO: BUG: Testing the inference-rule does not "work" because as a formula it contains
        #   the variable that it is itself using. This is an interesting case that must be
        #   further investigated and solved.
        # c = is_well_formed_formula_predicate(i)
        # m, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(pu.mt1.mt1,))
        # assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = pu.as1.connective_for_is_well_formed_formula(t)
        m, ok, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1a, a=(t,))
        assert ok
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = pu.as1.connective_for_is_a_proposition(c)
        m, ok, d = pu.as1.derive_2(t=m, c=c, i=pu.mt1.mt1b)
        assert ok
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        pass


class TestMT2:
    def test_mt2(self):
        t = pu.as1.let_x_be_a_theory()  # The meta-theory
        t, mt1a = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt1a)
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt2a)
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt2b)

        # Test 1: an inference-rule is an inference-rule
        c = pu.as1.connective_for_is_well_formed_inference_rule(pu.mt1.mt1a)  # This is a formula
        t, ok, d = pu.as1.derive_1(t=t, c=c, p=None, i=pu.mt1.mt2a, a=(pu.mt1.mt1a,), raise_error_if_false=True)
        assert ok

        # Test 2: a simple-object is not an inference-rule
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        c = pu.as1.connective_for_is_well_formed_inference_rule(a)
        t, ok, d = pu.as1.derive_1(t=t, c=c, p=None, i=pu.mt1.mt2a, a=(a,), raise_error_if_false=False)
        assert not ok

        # Test 3: using is-well-formed-inference-rule on itself.
        c = pu.as1.connective_for_is_well_formed_inference_rule(pu.mt1.mt2a)  # This is a formula
        t, ok, d = pu.as1.derive_1(t=t, c=c, p=None, i=pu.mt1.mt2a, a=(pu.mt1.mt2a,), raise_error_if_false=True)
        assert ok
        c = pu.as1.connective_for_is_a_proposition(c)
        m, ok, d = pu.as1.derive_2(t=t, c=c, i=pu.mt1.mt2b)
        assert ok
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        pass


class TestMT3:
    def test_mt3(self):
        t = pu.as1.let_x_be_a_theory()  # meta-theory

        # Proper theory t allows to derive (is-well-formed-theory(t)).
        t = pu.as1.let_x_be_a_theory()  # target or object theory
        t, i = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt3a)
        t, i2 = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt3b)
        c = pu.as1.connective_for_is_well_formed_theoretical_context(t)  # This is a formula
        t, ok, d = pu.as1.derive_1(t=t, c=c, p=None, i=i, a=(t,), raise_error_if_false=True)
        assert ok
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = pu.as1.connective_for_is_a_proposition(c)
        t, ok, d = pu.as1.derive_2(t=t, c=c, i=pu.mt1.mt3b)
        assert ok
        # assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # Simple object a does not allow to derive (is-well-formed-theory(a)).
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')  # simple object
        c = pu.as1.connective_for_is_well_formed_theoretical_context(a)  # This is a formula
        with pytest.raises(pu.u1.ApplicativeError) as error:
            t, _, d = pu.as1.derive_1(t=t, c=c, p=None, i=i, a=(a,), raise_error_if_false=True)

        t, ok, d = pu.as1.derive_1(t=t, c=c, p=None, i=i, a=(a,), raise_error_if_false=False)
        assert not ok


class TestTProvesP:
    def test_t_proves_p(self):
        t = pu.as1.let_x_be_a_theory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t, _ = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='A')
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)

        m = pu.as1.let_x_be_a_theory()  # Declare a meta-theory
        m = pu.mt1.extend_theory_with_meta_theory_1(t=m)  # Extend it with meta-theory-1 inference-rules
        c = pu.as1.connective_for_is_well_formed_theoretical_context(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3a, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        c = t | pu.as1.connective_for_proves | a
        p = (pu.as1.connective_for_is_well_formed_theoretical_context(t),)
        a = (a,)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.t_proves_p, a=a,
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        b = pu.as1.let_x_be_a_simple_object(formula_ts='b')
        c = t | pu.as1.connective_for_proves | b
        p = (pu.as1.connective_for_is_well_formed_theoretical_context(t),)
        m, ok, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.t_proves_p, a=(t, b,),
                                   raise_error_if_false=False)
        assert not ok


class TestInconsistency1:
    def test_inconsistency_1(self):
        t = pu.as1.let_x_be_a_theory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t, _ = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='A')
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        t_inconsistent, _ = pu.as1.let_x_be_an_axiom(t=t, s=pu.as1.connective_for_logical_negation(a))

        m = pu.as1.let_x_be_a_theory()  # Declare a meta-theory
        m = pu.mt1.extend_theory_with_meta_theory_1(t=m)  # Extend it with meta-theory-1 inference-rules
        c = pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3a, a=(t_inconsistent,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        t_proves_a = t_inconsistent | pu.as1.connective_for_proves | a
        p = (pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent),)
        m, _, d = pu.as1.derive_1(t=m, c=t_proves_a, p=p, i=pu.mt1.t_proves_p, a=(a,),
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=t_proves_a, psi=d.valid_statement)

        not_a = pu.as1.connective_for_logical_negation(a)
        t_proves_not_a = t_inconsistent | pu.as1.connective_for_proves | not_a
        p = (pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent),)
        m, _, d = pu.as1.derive_1(t=m, c=t_proves_not_a, p=p, i=pu.mt1.t_proves_p, a=(not_a,),
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=t_proves_not_a, psi=d.valid_statement)

        c = pu.as1.connective_for_is_inconsistent(t_inconsistent)
        p = (pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent),
             t_proves_a,
             t_proves_not_a,)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.inconsistency_1, a=None,
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        pass

    class TestHypothesis:
        def test_hypothesis(self):
            m = pu.as1.let_x_be_a_theory()  # Declare a meta-theory
            m = pu.mt1.extend_theory_with_meta_theory_1(t=m)  # Extend it with meta-theory-1 inference-rules
            m = pu.ml1.extend_theory_with_minimal_logic_1(t=m)
            m, p = pu.pls1.let_x_be_a_propositional_variable(t=m, formula_ts='P')
            m, q = pu.pls1.let_x_be_a_propositional_variable(t=m, formula_ts='Q')
            m, r = pu.pls1.let_x_be_a_propositional_variable(t=m, formula_ts='R')
            m, _, _ = pu.as1.auto_derive_2(t=m, c=pu.as1.connective_for_is_a_proposition(p))
            m, _, _ = pu.as1.auto_derive_2(t=m, c=pu.as1.connective_for_is_a_proposition(q))
            m, _, _ = pu.as1.auto_derive_2(t=m, c=pu.as1.connective_for_is_a_proposition(r))
            # Pose `P` and `Q` as true.
            m, _ = pu.as1.let_x_be_an_axiom(t=m, s=p)
            m, _ = pu.as1.let_x_be_an_axiom(t=m, s=q)
            # (Q, R) |-- not(P)
            m, i1 = pu.as1.let_x_be_an_inference_rule(
                t=m, f=pu.as1.WellFormedTransformationByVariableSubstitution(o=pu.csl1.lnot(p), v=None, i=(q, r,)))

            # Pose the `R` hypothesis
            # H |-- R
            h = pu.as1.WellFormedHypothesis(b=m, a=r)

            # Which leads to the `lnot(P)` theorem.
            # H |-- not(P) [I1]
            h, ok, _ = pu.as1.derive_2(t=h, c=pu.csl1.lnot(p), i=i1, raise_error_if_false=True)

            # T |-- H is wf-theory [I1]
            m, ok, d = pu.as1.derive_1(
                t=m, c=pu.as1.connective_for_is_well_formed_theoretical_context(h),
                p=None, i=pu.mt1.mt3a, a=(h,))
            assert ok
            m, _, _ = pu.as1.auto_derive_2(t=m, c=pu.as1.connective_for_is_a_proposition(
                pu.as1.connective_for_is_well_formed_theoretical_context(h)))

            h_proves_p = h | pu.as1.connective_for_proves | p
            p = (pu.as1.connective_for_is_well_formed_theoretical_context(h),)
            m, ok, d = pu.as1.derive_1(t=m, c=h_proves_p, p=p, i=pu.mt1.t_proves_p, a=(h,))
            assert ok

            not_a = pu.as1.connective_for_logical_negation(p)
            h_proves_not_p = h | pu.as1.connective_for_proves | not_a
            p = (pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent),)
            m, _, d = pu.as1.derive_1(t=m, c=h_proves_not_p, p=p, i=pu.mt1.t_proves_p, a=(not_a,),
                                      raise_error_if_false=True)
            assert pu.as1.is_formula_equivalent(phi=h_proves_not_p, psi=d.valid_statement)

            c = pu.as1.connective_for_is_inconsistent(t_inconsistent)
            p = (pu.as1.connective_for_is_well_formed_theoretical_context(t_inconsistent),
                 h_proves_p,
                 h_proves_not_p,)
            m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.inconsistency_1, a=None,
                                      raise_error_if_false=True)
            assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
            pass
