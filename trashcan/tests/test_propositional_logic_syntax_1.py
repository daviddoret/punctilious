# import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


class TestHeuristic:
    def test_heuristic_basic(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='P')
        assert not pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p), t=t)
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=is_well_formed_proposition(p), t=t)
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p), t=t)
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=is_well_formed_proposition(p | land | q), t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=is_well_formed_proposition(p | implies | q), t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=is_well_formed_proposition(p | lor | q), t=t)
        assert success

    def test_heuristic_complex(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='P')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, success = pu.as1.auto_derive_with_heuristics(
            conjecture=is_well_formed_proposition((q | lor | q) | implies | (
                    (p | land | p) | land | (p | lor | (q | implies | lnot(q))))), t=t)
        assert success


class TestAxioms:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        # is_a = pu.as1.is_a_connective
        is_a_proposition = pu.as1.connective_for_is_well_formed_proposition
        is_a_propositional_variable = pu.as1.connective_for_is_a_propositional_variable
        land = pu.as1.connective_for_logical_conjunction
        lnot = pu.as1.connective_for_logical_negation
        lor = pu.as1.connective_for_logical_disjunction
        implies = pu.as1.connective_for_logical_implication

        # elaborate a theory
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')

        # derive: p is-a proposition
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_a_proposition(p),
                                  p=(
                                      is_a_propositional_variable(p),),
                                  i=pu.pls1.i1, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_a_proposition(p), t=t)

        # derive: add i2: A is-a proposition ⊃ ¬A is a proposition
        # note that it is not necessary that either A or ¬A be valid
        t = pu.as1.append_to_theory(pu.pls1.i2, t=t)
        inference_rule = pu.as1.WellFormedInferenceRule(f=pu.pls1.i2.transformation)
        inference = pu.as1.WellFormedInference(
            p=(is_a_proposition(p),),
            r=inference_rule)
        claim = is_a_proposition(lnot(p))
        isolated_theorem = pu.as1.WellFormedTheorem(p=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=is_a_proposition(lnot(p)), psi=isolated_theorem.valid_statement)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)

        assert pu.as1.is_valid_proposition_so_far_1(p=is_a_proposition(lnot(p)), t=t)

        # declare 1 as a propositional-variable
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        a2 = pu.as1.WellFormedAxiom(p=is_a_propositional_variable(q))
        t = pu.as1.append_to_theory(a2, t=t)

        # derive q is-a proposition
        inference_rule = pu.as1.WellFormedInferenceRule(f=pu.pls1.i1.transformation)
        inference = pu.as1.WellFormedInference(
            p=(a2.valid_statement,),
            r=inference_rule)
        claim = is_a_proposition(q)
        isolated_theorem = pu.as1.WellFormedTheorem(p=claim, i=inference)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)

        # add i3: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)
        t = pu.as1.append_to_theory(pu.pls1.i3, t=t)
        inference_rule = pu.as1.WellFormedInferenceRule(f=pu.pls1.i3.transformation)
        inference = pu.as1.WellFormedInference(
            p=(is_a_proposition(p), is_a_proposition(q),),
            r=inference_rule)
        claim = is_a_proposition(p | land | q)
        isolated_theorem = pu.as1.WellFormedTheorem(p=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=claim, psi=isolated_theorem.valid_statement)
        t = pu.as1.append_to_theory(isolated_theorem, t=t)
        assert pu.as1.is_valid_proposition_so_far_1(p=claim, t=t)

        pass

    def test_pl1_2(self):
        # is_a = pu.as1.is_a_connective
        proposition = pu.as1.connective_for_is_well_formed_proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, success, _, = pu.as1.auto_derive_2(t=t, c=proposition(p))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=proposition(p), t=t)

    def test_pl1_3(self):
        # is_a = pu.as1.is_a_connective
        # land = pu.as1.connective_for_logical_conjunction
        proposition = pu.as1.connective_for_is_well_formed_proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='X')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Y')
        t, success, _ = pu.as1.auto_derive_2(t=t, c=proposition(p))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=proposition(p), t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, c=proposition(q))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=proposition(q), t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, c=proposition(p | land | q))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=proposition(p | land | q), t=t)
        pass
