import pytest
import punctilious as pu


class TestPropositionalLogicMetaTheory:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.as1.connectives.proposition
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        lor = pu.as1.connectives.lor
        implies = pu.as1.connectives.implies

        # elaborate a theory
        p = pu.as1.let_x_be_a_propositional_variable(rep='P')
        a1 = pu.as1.let_x_be_an_axiom(claim=p | is_a | propositional_variable)
        axioms = pu.as1.Axiomatization(axioms=(a1,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim,),
            transformation_rule=pu.pls1.i1.transformation)
        claim = p | is_a | proposition
        isolated_theorem = pu.as1.TheoremByInference(claim=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=p | is_a | proposition, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=p | is_a | proposition)
        # REPRENDRE ICI!!!!!
