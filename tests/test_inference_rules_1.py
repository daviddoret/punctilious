import pytest
import punctilious as pu


class TestAdjunction:
    def test_adjunction(self):
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        land = pu.ir1.connectives.land

        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_axiom(claim=a)
        a4 = pu.as1.let_x_be_an_axiom(claim=b)
        r: pu.as1.Transformation = pu.as1.coerce_transformation(phi=pu.ir1.adjunction_axiom.claim)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.inference_rules, a1, a2, a3, a4,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))
        inference = pu.as1.Inference(
            p=(a1.claim, a2.claim, a3.claim, a4.claim,),
            f=r)
        proof = pu.as1.ProofByInference(claim=a | land | b, i=inference)
        assert pu.as1.is_formula_equivalent(phi=a | land | b, psi=proof.claim)
        theory_2 = pu.as1.Demonstration(proofs=(*theory, proof))
        assert theory_2.has_theorem(phi=a | land | b)
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            wrong_axiomatization = pu.as1.Axiomatization(axioms=(
                pu.ir1.simplification_1_axiom, pu.ir1.simplification_2_axiom, pu.ir1.modus_ponens_axiom, a1, a2, a3,
                a4,))
            wrong_theory_1 = pu.as1.Demonstration(proofs=(*wrong_axiomatization, proof))


class TestModusPonens:
    def test_modus_ponens(self):
        is_a = pu.as1.connectives.is_a
        proposition = pu.ir1.connectives.proposition
        implies = pu.ir1.connectives.implies

        a = pu.as1.let_x_be_a_simple_object(rep='A')
        b = pu.as1.let_x_be_a_simple_object(rep='B')
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | proposition)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | proposition)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | implies | b)
        a4 = pu.as1.let_x_be_an_axiom(claim=a)
        theory = pu.as1.Axiomatization(axioms=(*pu.ir1.inference_rules, a1, a2, a3, a4,))
        # theory = pu.as1.union_demonstration(phi=pu.ir1.inference_rules, psi=(a1, a2, a3, a4,))
        print(theory)
        proof = pu.as1.ProofByInference(claim=b,
                                        i=pu.as1.Inference(p=(a1.claim, a2.claim, a3.claim, a4.claim,),
                                                           f=pu.ir1.modus_ponens_axiom.claim))
        pass
        # assert c1 is not c2
