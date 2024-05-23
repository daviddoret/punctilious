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
        lnot = pu.as1.connectives.lnot
        lor = pu.as1.connectives.lor
        implies = pu.as1.connectives.implies

        # elaborate a theory
        p = pu.as1.let_x_be_a_propositional_variable(rep='P')
        a1 = pu.as1.let_x_be_an_axiom(claim=p | is_a | propositional_variable)
        theory = pu.as1.Axiomatization(axioms=(pu.pls1.i1, a1,))

        # derive: p is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=p | is_a | proposition,
                               premises=(
                                   p | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=p | is_a | proposition)

        # derive: add i2: A is-a proposition ⊃ ¬A is a proposition
        # note that it is not necessary that either A or ¬A be valid
        theory = pu.as1.Derivation(valid_statements=(*theory, pu.pls1.i2,))
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition,),
            transformation_rule=pu.pls1.i2.transformation)
        claim = lnot(p) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(claim=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=lnot(p) | is_a | proposition, psi=isolated_theorem.claim)
        theory = pu.as1.Derivation(valid_statements=(*theory, isolated_theorem,))
        assert theory.has_theorem(phi=lnot(p) | is_a | proposition)

        # declare 1 as a propositional-variable
        with pu.as1.let_x_be_a_propositional_variable(rep='Q') as q:
            a2 = pu.as1.Axiom(claim=q | is_a | propositional_variable)
        theory = pu.as1.Derivation(valid_statements=(*theory, a2,))

        # derive q is-a proposition
        inference = pu.as1.Inference(
            premises=(a2.claim,),
            transformation_rule=pu.pls1.i1.transformation)
        claim = q | is_a | proposition
        isolated_theorem = pu.as1.Theorem(claim=claim, i=inference)
        theory = pu.as1.Derivation(valid_statements=(*theory, isolated_theorem,))

        # add i3: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)
        theory = pu.as1.Derivation(valid_statements=(*theory, pu.pls1.i3,))
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition, q | is_a | proposition,),
            transformation_rule=pu.pls1.i3.transformation)
        claim = (p | land | q) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(claim=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=claim, psi=isolated_theorem.claim)
        theory = pu.as1.Derivation(valid_statements=(*theory, isolated_theorem,))
        assert theory.has_theorem(phi=claim)

        pass
