import pytest
import punctilious.axiomatic_system_1 as as1
import punctilious.inference_rules_1 as ir1


class TestModusPonens:
    def test_modus_ponens(self):
        is_a = as1.connectives.is_a
        proposition = ir1.connectives.proposition
        implies = ir1.connectives.implies

        a = as1.let_x_be_a_simple_object(rep='A')
        b = as1.let_x_be_a_simple_object(rep='B')
        a1 = as1.let_x_be_an_axiom(claim=a | is_a | proposition)
        a2 = as1.let_x_be_an_axiom(claim=b | is_a | proposition)
        a3 = as1.let_x_be_an_axiom(claim=a | implies | b)
        a4 = as1.let_x_be_an_axiom(claim=a)
        t0 = [*ir1.inference_rules, a1, a2, a3, a4, ]
        theory = as1.Axiomatization(axioms=(ir1.adjunction_axiom, ir1.simplification_1_axiom,))
        # theory = as1.union_demonstration(phi=ir1.inference_rules, psi=(a1, a2, a3, a4,))
        print(theory)
        pass
        # assert c1 is not c2
