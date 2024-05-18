import pytest
import punctilious.axiomatic_system_1 as as1
import punctilious.inference_rules_1 as ir1

is_a = as1.connectives.is_a
proposition = ir1.connectives.proposition
implies = ir1.connectives.implies


class TestModusPonens:
    def test_modus_ponens(self):
        a = as1.let_x_be_a_simple_object(rep='A')
        b = as1.let_x_be_a_simple_object(rep='B')
        t1 = as1.let_x_be_an_axiom(claim=a | is_a | proposition)
        t2 = as1.let_x_be_an_axiom(claim=b | is_a | proposition)
        t3 = as1.let_x_be_an_axiom(claim=a | implies | b)
        t4 = as1.let_x_be_an_axiom(claim=a)
        tb = as1.De
        theory = as1.union_enumeration(phi=ir1.inference_rules, psi=(t1, t2, t3, t4,))
        print(theory)
        pass
        # assert c1 is not c2
