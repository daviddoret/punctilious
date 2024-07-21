import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


class TestHeuristic:
    def test_heuristic_basic(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='P')
        assert not pu.as1.is_valid_proposition_in_theory_1(p=p | is_a | proposition, t=t)
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=p | is_a | proposition, t=t)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | is_a | proposition, t=t)
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | land | q) | is_a | proposition, t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | implies | q) | is_a | proposition, t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | lor | q) | is_a | proposition, t=t)
        assert success

    def test_heuristic_complex(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='P')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, success = pu.as1.auto_derive_with_heuristics(
            conjecture=((q | lor | q) | implies | (
                    (p | land | p) | land | (p | lor | (q | implies | lnot(q))))) | is_a | proposition, t=t)
        assert success


class TestAxioms:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1._connectives.is_a
        proposition = pu.as1._connectives.proposition
        is_a_propositional_variable = pu.as1._connectives.is_a_propositional_variable
        land = pu.as1._connectives.land
        lnot = pu.as1._connectives.lnot
        lor = pu.as1._connectives.lor
        implies = pu.as1._connectives.implies

        # elaborate a theory
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')

        # derive: p is-a proposition
        t, _, = pu.as1.derive_1(t=t,
                                c=p | is_a | proposition,
                                p=(
                                    is_a_propositional_variable(p),),
                                i=pu.pls1.i1)
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | is_a | proposition, t=t)

        # derive: add i2: A is-a proposition ⊃ ¬A is a proposition
        # note that it is not necessary that either A or ¬A be valid
        t = pu.as1.append_to_theory(pu.pls1.i2, t=t)
        inference_rule = pu.as1.InferenceRule(t=pu.pls1.i2.transformation)
        inference = pu.as1.Inference(
            p=(p | is_a | proposition,),
            i=inference_rule)
        claim = lnot(p) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(s=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=lnot(p) | is_a | proposition, psi=isolated_theorem.valid_statement)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)

        assert pu.as1.is_valid_proposition_in_theory_1(p=lnot(p) | is_a | proposition, t=t)

        # declare 1 as a propositional-variable
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        a2 = pu.as1.Axiom(s=is_a_propositional_variable(q))
        t = pu.as1.append_to_theory(a2, t=t)

        # derive q is-a proposition
        inference_rule = pu.as1.InferenceRule(t=pu.pls1.i1.transformation)
        inference = pu.as1.Inference(
            p=(a2.valid_statement,),
            i=inference_rule)
        claim = q | is_a | proposition
        isolated_theorem = pu.as1.Theorem(s=claim, i=inference)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)

        # add i3: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)
        t = pu.as1.append_to_theory(pu.pls1.i3, t=t)
        inference_rule = pu.as1.InferenceRule(t=pu.pls1.i3.transformation)
        inference = pu.as1.Inference(
            p=(p | is_a | proposition, q | is_a | proposition,),
            i=inference_rule)
        claim = (p | land | q) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(s=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=claim, psi=isolated_theorem.valid_statement)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)
        assert pu.as1.is_valid_proposition_in_theory_1(p=claim, t=t)

        pass

    def test_pl1_2(self):
        is_a = pu.as1._connectives.is_a
        proposition = pu.as1._connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, success, _, = pu.as1.auto_derive_2(t=t, conjecture=p | is_a | proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | is_a | proposition, t=t)

    def test_pl1_3(self):
        is_a = pu.as1._connectives.is_a
        land = pu.as1._connectives.land
        proposition = pu.as1._connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='X')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Y')
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=p | is_a | proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | is_a | proposition, t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=q | is_a | proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=q | is_a | proposition, t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=(p | land | q) | is_a | proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | land | q) | is_a | proposition, t=t)
        pass
