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
        p = pu.as1.let_x_be_a_propositional_variable_OBSOLETE(rep='P')
        a1 = pu.as1.let_x_be_an_axiom_deprecated(valid_statement=p | is_a | propositional_variable)
        theory = pu.as1.Axiomatization(axioms=(pu.pls1.i1, a1,))

        # derive: p is-a proposition
        theory, _, = pu.as1.derive(theory=theory,
                                   valid_statement=p | is_a | proposition,
                                   premises=(
                                       p | is_a | propositional_variable,),
                                   inference_rule=pu.pls1.i1)
        assert pu.as1.is_valid_statement_with_regard_to_theory(phi=p | is_a | proposition, t=theory)

        # derive: add i2: A is-a proposition ⊃ ¬A is a proposition
        # note that it is not necessary that either A or ¬A be valid
        theory = pu.as1.Theory(derivations=(*theory, pu.pls1.i2,))
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition,),
            transformation_rule=pu.pls1.i2.transformation)
        claim = lnot(p) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=lnot(p) | is_a | proposition, psi=isolated_theorem.valid_statement)
        theory = pu.as1.Theory(derivations=(*theory, isolated_theorem,))
        assert pu.as1.is_valid_statement_with_regard_to_theory(phi=lnot(p) | is_a | proposition, t=theory)

        # declare 1 as a propositional-variable
        with pu.as1.let_x_be_a_propositional_variable_OBSOLETE(rep='Q') as q:
            a2 = pu.as1.Axiom(valid_statement=q | is_a | propositional_variable)
        theory = pu.as1.Theory(derivations=(*theory, a2,))

        # derive q is-a proposition
        inference = pu.as1.Inference(
            premises=(a2.valid_statement,),
            transformation_rule=pu.pls1.i1.transformation)
        claim = q | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        theory = pu.as1.Theory(derivations=(*theory, isolated_theorem,))

        # add i3: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)
        theory = pu.as1.Theory(derivations=(*theory, pu.pls1.i3,))
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition, q | is_a | proposition,),
            transformation_rule=pu.pls1.i3.transformation)
        claim = (p | land | q) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=claim, psi=isolated_theorem.valid_statement)
        theory = pu.as1.Theory(derivations=(*theory, isolated_theorem,))
        assert pu.as1.is_valid_statement_with_regard_to_theory(phi=claim, t=theory)

        pass

    def test_pl1_2(self):
        is_a = pu.as1.connectives.is_a
        proposition = pu.as1.connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')
        phi = p | is_a | proposition
        t, _, _, = pu.as1.auto_derive(t=t, phi=phi)
        assert pu.as1.is_valid_statement_with_regard_to_theory(phi=phi, t=t)

    def test_pl1_3(self):
        is_a = pu.as1.connectives.is_a
        land = pu.as1.connectives.land
        proposition = pu.as1.connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='X')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Y')
        phi = (p | land | q) | is_a | proposition
        t, _, _ = pu.as1.auto_derive(t=t, phi=phi)
        pass
