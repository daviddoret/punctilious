import pytest
# import logging
import punctilious as pu


class TestMT1:
    def test_mt1(self):
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t = pu.as1.let_x_be_a_theory()
        m = pu.as1.let_x_be_a_theory()
        m, i = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt1)
        c = pu.as1.get_connectives().is_well_formed_formula_predicate(a)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(a,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        # TODO: BUG: Testing the inference-rule does not "work" because as a formula it contains
        #   the variable that it is itself using. This is an interesting case that must be
        #   further investigated and solved.
        # c = is_well_formed_formula_predicate(i)
        # m, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt1, a=(pu.mt1.mt1,))
        # assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)
        c = pu.as1.get_connectives().is_well_formed_formula_predicate(t)
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
        c = pu.as1.get_connectives().is_well_formed_inference_rule_predicate(i2)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(i2,), raise_error_if_false=True)

        # Test 2: a simple-object is not an inference-rule
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        c = pu.as1.get_connectives().is_well_formed_inference_rule_predicate(a)
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_MT1_001):
            m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=True)

        # Test 3: using is-well-formed-inference-rule on itself.
        # Test 1: an inference-rule is an inference-rule
        t, i3 = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.mt1.mt2)
        c = pu.as1.get_connectives().is_well_formed_inference_rule_predicate(i3)  # This is a formula
        # m, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(i3,))
        # Raises: ERROR AS1-021: variable x is a sub-formula of phi.
        # TODO: Find a solution for the above.

        # TODO: Clarify semantically Derivation of type inference-rule and inference-rule

        pass


class TestMT3:
    def test_mt3(self):
        # TODO: Implement strict connective constraints on theories and introduce a test
        #   checking that an atomic-object is not a theory.
        m = pu.as1.let_x_be_a_theory()  # meta-theory

        # Proper theory t allows to derive (is-well-formed-theory(t)).
        t = pu.as1.let_x_be_a_theory()  # target or object theory
        m, i = pu.as1.let_x_be_an_inference_rule(t=m, i=pu.mt1.mt3)
        c = pu.as1.get_connectives().is_well_formed_theory_predicate(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # Simple object a does not allow to derive (is-well-formed-theory(a)).
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')  # simple object
        c = pu.as1.get_connectives().is_well_formed_theory_predicate(a)  # This is a formula
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_MT1_002):
            m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=i, a=(a,), raise_error_if_false=True)

        pass


class TestTProvesP:
    def test_t_proves_p(self):
        t = pu.as1.let_x_be_a_theory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t, _ = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='A')
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)

        m = pu.as1.let_x_be_a_theory()  # Declare a meta-theory
        m = pu.mt1.extend_theory_with_meta_theory_1(t=m)  # Extend it with meta-theory-1 inference-rules
        c = pu.as1.get_connectives().is_well_formed_theory_predicate(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        c = t | pu.as1.get_connectives().proves | a
        p = (pu.as1.get_connectives().is_well_formed_theory_predicate(t),)
        m, _, d = pu.as1.derive_1(t=m, c=c, p=p, i=pu.mt1.t_proves_p, a=(t, a,),
                                  raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # TODO: derive: P is-a-proposition-in T
        # TODO: derive is-inconsistent(T)


class TestInconsistency1:
    def test_inconsistency_1(self):
        t = pu.as1.let_x_be_a_theory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        a = pu.as1.let_x_be_a_simple_object(formula_ts='a')
        t, _ = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='A')
        t, _ = pu.as1.let_x_be_an_axiom(t=t, s=a)
        t_inconsistent, _ = pu.as1.let_x_be_an_axiom(t=t, s=pu.as1.get_connectives().lnot(a))  # This is a contradiction

        m = pu.as1.let_x_be_a_theory()  # Declare a meta-theory
        m = pu.mt1.extend_theory_with_meta_theory_1(t=m)  # Extend it with meta-theory-1 inference-rules
        c = pu.as1.get_connectives().is_well_formed_theory_predicate(t)  # This is a formula
        m, _, d = pu.as1.derive_1(t=m, c=c, p=None, i=pu.mt1.mt3, a=(t,), raise_error_if_false=True)
        assert pu.as1.is_formula_equivalent(phi=c, psi=d.valid_statement)

        # TODO: derive: P is-a-proposition-in T
        # TODO: derive is-inconsistent(T)
