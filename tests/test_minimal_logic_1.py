import pytest
import punctilious as pu


class TestPL1:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land

        db = pu.as1.DemonstrationBuilder(theorems=None)

        # elaborate a theory
        p = pu.as1.let_x_be_a_propositional_variable(rep='P', db=db)
        a1 = pu.as1.let_x_be_an_axiom(claim=p | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=p)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim,),
            transformation_rule=pu.ml1.pl01.claim)
        claim = p | land | p
        isolated_theorem = pu.as1.TheoremByInference(claim=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=p | land | p, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=p | land | p)

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
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim, a3.claim,),
            transformation_rule=pu.ml1.pl02.claim)
        isolated_theorem = pu.as1.TheoremByInference(claim=b | land | a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b | land | a, psi=isolated_theorem.claim)

        # extend the original theory with that new theorem
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=b | land | a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2,))
            pu.as1.Demonstration(theorems=(*incomplete_axioms, isolated_theorem))
