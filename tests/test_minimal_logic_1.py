import pytest
import punctilious as pu


class TestPL1:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        implies = pu.as1.connectives.implies

        # elaborate a theory
        p = pu.as1.let_x_be_a_propositional_variable(rep='P')
        a1 = pu.as1.let_x_be_an_axiom(claim=p | is_a | propositional_variable)
        axioms = pu.as1.Axiomatization(axioms=(pu.ir1.modus_ponens_axiom, pu.ml1.pl01, a1,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim,),
            transformation_rule=pu.ml1.pl01.transformation)
        claim = p | implies | (p | land | p)
        isolated_theorem = pu.as1.TheoremByInference(claim=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=p | implies | (p | land | p), psi=isolated_theorem.claim)
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=p | implies | (p | land | p))

        # because the derived theorem is an implication, we can further apply modus ponens
        # make the premises true:
        a2 = pu.as1.let_x_be_an_axiom(claim=p)
        extended_theory = pu.as1.Demonstration(theorems=(*extended_theory, a2,))
        inference = pu.as1.Inference(
            # TODO: REPRENDRE ICI: IL FAUT QUE LES FORMULES PROPOSITIONNELLES
            #   SOIENT RECONNUES COMME TELLES. CELA PASSE PROBABLEMENT PAR UN MECANISME
            #   D'INFERENCE IMPLICITE, OU ALORS PAR LA GENERATION D'AXIOMES AUTOMATIQUES.
            #   IL FAUT PENSER A L'AJOUT ENSUITE D'AUTRES CLASSES, LES NATURELS, ETC.
            premises=(a2,),
            transformation_rule=pu.ir1.modus_ponens_rule)
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
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land

        # elaborate a theory
        a, b = pu.as1.let_x_be_a_propositional_variable(rep=('A', 'B',))
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim, a3.claim,),
            transformation_rule=pu.ml1.pl02.transformation)
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


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        implies = pu.as1.connectives.implies

        # elaborate a theory
        a, b, c = pu.as1.let_x_be_a_propositional_variable(rep=('A', 'B', 'C',))
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=c | is_a | propositional_variable)
        a4 = pu.as1.let_x_be_an_axiom(claim=a | implies | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim, a3.claim, a4.claim,),
            transformation_rule=pu.ml1.pl03.transformation)
        isolated_theorem = pu.as1.TheoremByInference(claim=(a | land | c) | implies | (b | land | c), i=inference)
        assert pu.as1.is_formula_equivalent(phi=(a | land | c) | implies | (b | land | c), psi=isolated_theorem.claim)

        # extend the original theory with that new theorem
        extended_theory = pu.as1.Demonstration(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=(a | land | c) | implies | (b | land | c))

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2, a3,))
            pu.as1.Demonstration(theorems=(*incomplete_axioms, isolated_theorem))

        pass
