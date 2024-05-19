import pytest
import punctilious as pu


class TestPL1:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        db = pu.as1.DemonstrationBuilder(theorems=None)

        # elaborate a theory
        a = pu.as1.let_x_be_a_propositional_variable(rep='A', db=db)
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=a)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim,),
            f=pu.ml1.pl01_rule)
        isolated_theorem = pu.as1.TheoremByInference(claim=a | land | a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=a | land | a, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=a | land | a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2,))
            wrong_theory_1 = pu.as1.Demonstration(theorems=(*incomplete_axioms, isolated_theorem))


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        db = pu.as1.DemonstrationBuilder(theorems=None)

        # elaborate a theory
        a, b = pu.as1.let_x_be_a_propositional_variable(rep=('A', 'B',), db=db)
        a1 = pu.as1.let_x_be_an_inference_rule(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_inference_rule(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_inference_rule(claim=a | land | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim,),
            f=pu.ml1.pl02_rule)
        isolated_theorem = pu.as1.TheoremByInference(claim=b | land | a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b | land | a, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=b | land | a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2,))
            pu.as1.Demonstration(theorems=(*incomplete_axioms, isolated_theorem))
