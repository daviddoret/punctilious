import pytest
import punctilious as pu


class TestAdjunction:
    def test_adjunction(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_inference_rule(claim=a)
        a4 = pu.as1.let_x_be_an_inference_rule(claim=b)
        r: pu.as1.Transformation = pu.as1.coerce_transformation(phi=pu.ir1.adjunction_axiom.claim)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, a1, a2, a3, a4,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim, a4.claim,),
            f=r)
        isolated_theorem = pu.as1.TheoremByInference(claim=a | land | b, i=inference)
        assert pu.as1.is_formula_equivalent(phi=a | land | b, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=a | land | b)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e123'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                pu.ir1.simplification_1_axiom, pu.ir1.simplification_2_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,
                a4,))
            wrong_theory_1 = pu.as1.Demonstration(theorems=(*incomplete_axioms, extended_theory))


class TestSimplification1:
    def test_simplification_1(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_inference_rule(claim=a | land | b)
        r: pu.as1.Transformation = pu.as1.coerce_transformation(phi=pu.ir1.simplification_1_axiom.claim)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, a1, a2, a3,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim,),
            f=r)
        isolated_theorem = pu.as1.TheoremByInference(claim=a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=a, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem))
        assert extended_theory.has_theorem(phi=a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.adjunction_axiom, pu.ir1.simplification_2_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,))
            wrong_theory = pu.as1.Demonstration(theorems=(*wrong_axiomatization, isolated_theorem))


class TestSimplification2:
    def test_simplification_2(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_inference_rule(claim=a | land | b)
        r: pu.as1.Transformation = pu.as1.coerce_transformation(phi=pu.ir1.simplification_2_axiom.claim)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, a1, a2, a3,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim,),
            f=r)
        isolated_theorem = pu.as1.TheoremByInference(claim=b, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem))
        assert extended_theory.has_theorem(phi=b)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.adjunction_axiom, pu.ir1.simplification_1_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,))
            wrong_theory = pu.as1.Demonstration(theorems=(*wrong_axiomatization, isolated_theorem))


class TestModusPonens:
    def test_modus_ponens(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        implies = pu.ir1.implies
        land = pu.ir1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_inference_rule(claim=a | implies | b)
        a4 = pu.as1.let_x_be_an_inference_rule(claim=a)
        r: pu.as1.Transformation = pu.as1.coerce_transformation(phi=pu.ir1.modus_ponens_axiom.claim)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim, a4.claim),
            f=r)
        isolated_theorem = pu.as1.TheoremByInference(claim=b, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem))
        assert extended_theory.has_theorem(phi=b)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.adjunction_axiom, pu.ir1.simplification_1_axiom, pu.ir1.simplification_2_axiom, a1, a2, a3,))
            wrong_theory = pu.as1.Demonstration(theorems=(*wrong_axiomatization, isolated_theorem))
