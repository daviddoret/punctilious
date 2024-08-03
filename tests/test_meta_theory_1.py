import pytest
# import logging
import punctilious as pu


class TestMT1:
    def test_mt1(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t = pu.as1.let_x_be_a_theory()
        m = pu.as1.let_x_be_a_theory()
        m, i = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt1)
        c = pu.as1.connective_for_is_well_formed_formula(a)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(a,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        # TODO: BUG: Testing the inference-rule does not "work" because as a formula it contains
        #   the variable that it is itself using. This is an interesting case that must be
        #   further investigated and solved.
        # c = is_well_formed_formula_predicate(i)
        # m, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(pu.mt1.mt1,))
        # assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = pu.as1.connective_for_is_well_formed_formula(t)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        pass


class TestMT2:
    def test_mt2(self):
        m = pu.as1.let_x_be_a_theory()  # The meta-theory
        t = pu.as1.let_x_be_a_theory()
        m, i = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt2)

        # Test 1: an inference-rule is an inference-rule
        m, i2 = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt3)
        c = pu.as1.connective_for_is_well_formed_inference_rule(i2)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(i2,), raise_error_if_false=True)

        # Test 2: a simple-object is not an inference-rule
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        c = pu.as1.connective_for_is_well_formed_inference_rule(a)
        with pytest.raises(pu.u1.ApplicativeError) as error:
            m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=True)
        m, ok, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=False)
        assert not ok

        # Test 3: using is-well-formed-inference-rule on itself.
        # Test 1: an inference-rule is an inference-rule
        t, i3 = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt2)
        c = pu.as1.connective_for_is_well_formed_inference_rule(i3)  # This is a formula
        # m, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(i3,))
        # Raises: ERROR AS1-021: variable x is a sub-formula of phi.
        # TODO: Find a solution for the above.

        # TODO: Clarify semantically Derivation of type inference-rule and inference-rule

        pass


class TestMT3:
    def test_mt3(self):
        m = pu.as1.let_x_be_a_theory()  # meta-theory

        # Proper theory t allows to derive (is-well-formed-theory(t)).
        t = pu.as1.let_x_be_a_theory()  # target or object theory
        m, i = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt3)
        c = pu.as1.connective_for_is_well_formed_theory(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # Simple object a does not allow to derive (is-well-formed-theory(a)).
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')  # simple object
        c = pu.as1.connective_for_is_well_formed_theory(a)  # This is a formula
        with pytest.raises(pu.u1.ApplicativeError) as error:
            m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=True)

        m, ok, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=False)
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
        c = pu.as1.connective_for_is_well_formed_theory(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        c = t | pu.as1.connective_for_proves | a
        p = (pu.as1.connective_for_is_well_formed_theory(t),)
        a = (a,)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.t_proves_p, a=a,
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        b = pu.as1.let_x_be_a_simple_object(formula_ts='b')
        c = t | pu.as1.connective_for_proves | b
        p = (pu.as1.connective_for_is_well_formed_theory(t),)
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
        c = pu.as1.connective_for_is_well_formed_theory(t_inconsistent)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3, a=(t_inconsistent,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        t_proves_a = t_inconsistent | pu.as1.connective_for_proves | a
        p = (pu.as1.connective_for_is_well_formed_theory(t_inconsistent),)
        m, _, d = pu.as1.derive_1(t=m, c=t_proves_a, p=p, i=pu.mt1.t_proves_p, a=(a,),
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=t_proves_a, psi=d.valid_statement)

        not_a = pu.as1.connective_for_logical_negation(a)
        t_proves_not_a = t_inconsistent | pu.as1.connective_for_proves | not_a
        p = (pu.as1.connective_for_is_well_formed_theory(t_inconsistent),)
        m, _, d = pu.as1.derive_1(t=m, c=t_proves_not_a, p=p, i=pu.mt1.t_proves_p, a=(not_a,),
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=t_proves_not_a, psi=d.valid_statement)

        c = pu.as1.connective_for_is_inconsistent(t_inconsistent)
        p = (pu.as1.connective_for_is_well_formed_theory(t_inconsistent),
             t_proves_a,
             t_proves_not_a,)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.inconsistency_1, a=None,
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        pass

    class TestHypothesis:
        def test_hypothesis(self):
            t = pu.as1.let_x_be_a_theory()
            t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
            a, b = pu.as1.let_x_be_some_simple_objects(reps=('a', 'b',))
            t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
            t, _ = pu.as1.let_x_be_an_axiom(t=t, s=b | pu.csl1.implies | pu.csl1.lnot(a))
            # t, h = pu.as1.let_x_be_an_hypothesis(t=t, c=b)
            # h, ok, _ = pu.as1.derive_2(t=h, c=pu.csl1.lnot(a), i=pu.ir1.modus_ponens)
            # h_proves_a = t | pu.as1.connective_for_proves | a
            # h_proves_not_a = t | pu.as1.connective_for_proves | pu.csl1.lnot(a)
            # is_inconsistent_h = pu.csl1.is_inconsistent(h)
