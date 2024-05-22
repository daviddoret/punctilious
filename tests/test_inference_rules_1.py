import pytest
import punctilious as pu


class TestAdjunction:
    def test_adjunction(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        proposition = pu.as1.connectives.proposition

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        c = pu.as1.let_x_be_a_simple_object(rep='C')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a5 = pu.as1.let_x_be_an_axiom(claim=c | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a)
        a4 = pu.as1.let_x_be_an_axiom(claim=b)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3, a4, a5,))

        # derive: a is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=a | is_a | proposition,
                               premises=(a | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=a | is_a | proposition)

        # derive: b is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=b | is_a | proposition,
                               premises=(b | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=b | is_a | proposition)

        # derive: c is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=c | is_a | proposition,
                               premises=(c | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=c | is_a | proposition)

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=a | land | b,
                               premises=(a | is_a | proposition, b | is_a | proposition, a, b,),
                               inference_rule=pu.ir1.adjunction_axiom)
        assert theory.has_theorem(phi=a | land | b)

        # show that wrong premises fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            pu.as1.derive(theory=theory,
                          claim=a | land | c,
                          premises=(a | is_a | proposition, c | is_a | proposition, a, c,),
                          inference_rule=pu.ir1.adjunction_axiom)


class TestSimplification1:
    def test_simplification_1(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        proposition = pu.as1.connectives.proposition
        land = pu.as1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3,))

        # derive: a is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=a | is_a | proposition,
                               premises=(a | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)

        # derive: b is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=b | is_a | proposition,
                               premises=(b | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a | is_a | proposition, b | is_a | proposition, a | land | b,),
            transformation_rule=pu.ir1.simplification_1_axiom.transformation)
        isolated_theorem = pu.as1.TheoremByInference(claim=a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=a, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Derivation(theorems=(*theory, isolated_theorem))
        assert extended_theory.has_theorem(phi=a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.adjunction_axiom, pu.ir1.simplification_2_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,))
            wrong_theory = pu.as1.Derivation(theorems=(*wrong_axiomatization, isolated_theorem))


class TestSimplification2:
    def test_simplification_2(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        proposition = pu.as1.connectives.proposition
        land = pu.as1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3,))

        # derive: a is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=a | is_a | proposition,
                               premises=(a | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)

        # derive: b is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=b | is_a | proposition,
                               premises=(b | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a | is_a | proposition, b | is_a | proposition, a | land | b,),
            transformation_rule=pu.ir1.simplification_2_axiom.transformation)
        isolated_theorem = pu.as1.TheoremByInference(claim=b, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b, psi=isolated_theorem.claim)
        extended_theory = pu.as1.Derivation(theorems=(*theory, isolated_theorem))
        assert extended_theory.has_theorem(phi=b)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.adjunction_axiom, pu.ir1.simplification_1_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,))
            wrong_theory = pu.as1.Derivation(theorems=(*wrong_axiomatization, isolated_theorem))


class TestModusPonens:
    def test_modus_ponens(self):
        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        proposition = pu.as1.connectives.proposition
        implies = pu.as1.connectives.implies
        land = pu.as1.connectives.land

        # elaborate a theory
        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | implies | b)
        a4 = pu.as1.let_x_be_an_axiom(claim=a)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3, a4,))

        # derive: a is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=a | is_a | proposition,
                               premises=(a | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=a | is_a | proposition)

        # derive: b is-a proposition
        theory = pu.as1.derive(theory=theory,
                               claim=b | is_a | proposition,
                               premises=(b | is_a | propositional_variable,),
                               inference_rule=pu.pls1.i1)
        assert theory.has_theorem(phi=b | is_a | proposition)

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=b,
                               premises=(a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | implies | b,
                                         a),
                               inference_rule=pu.ir1.modus_ponens_axiom)
        assert theory.has_theorem(phi=b)

        # show that wrong premises fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e117'):
            theory = pu.as1.derive(theory=theory,
                                   claim=a,
                                   premises=(a | is_a | proposition,
                                             b | is_a | proposition,
                                             b | implies | a,
                                             b),
                                   inference_rule=pu.ir1.modus_ponens_axiom)
