# import pytest
import logging
import punctilious as pu
from punctilious.connectives_standard_library_1 import *

derive_0 = pu.as1.derive_0
derive_2 = pu.as1.derive_2
auto_derive_2 = pu.as1.auto_derive_2
auto_derive_3 = pu.as1.auto_derive_3
auto_derive_4 = pu.as1.auto_derive_4


class TestPL1:
    def test_pl1(self):
        # Test PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)
        t = pu.as1.let_x_be_a_theory()

        # Elaborate a basic theory with P as a propositional-variable
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')

        # Add axiom PL01 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl01, )

        # Derive: P is-a proposition
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(p),
                                  p=(is_a_propositional_variable(p),),
                                  i=pu.pls1.i1, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p), t=t)
        pass

        # Derive: P ⊃ (P ∧ P)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=p | implies | (p | land | p),
                                  p=(
                                      is_well_formed_proposition(p),),
                                  i=pu.ml1.pl01, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=p | implies | (p | land | p), t=t)
        pass

        # Derive: (P ∧ P) is-a proposition
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(p | land | p),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(p),),
                                  i=pu.pls1.i3, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p | land | p), t=t)

        # make P valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens)

        # Derive: P ∧ P from P by modus-ponens
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=p | land | p,
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(p | land | p),
                                      p | implies | (p | land | p),
                                      p,),
                                  i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=p | land | p, t=t)
        pass


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # Elaborate a basic theory with P and Q as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, _, _, _ = auto_derive_4(t=t, c=is_well_formed_proposition(p))
        t, _, _, _ = auto_derive_4(t=t, c=is_well_formed_proposition(q))

        # Add axiom PL02 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl02, )

        # Derive: (P ∧ Q) ⊃ (Q ∧ P)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=(p | land | q) | implies | (q | land | p),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(q),),
                                  i=pu.ml1.pl02, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=(p | land | q) | implies | (q | land | p), t=t)

        # Derive: (P ∧ Q) and (Q ∧ P) is-a proposition
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(p | land | q),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(q),),
                                  i=pu.pls1.i3, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p | land | q), t=t)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(q | land | p),
                                  p=(
                                      is_well_formed_proposition(q),
                                      is_well_formed_proposition(p),),
                                  i=pu.pls1.i3, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(q | land | p), t=t)

        # make (P ∧ Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p | land | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens)

        # Derive: P ∧ P from P by modus-ponens
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=q | land | p,
                                  p=(
                                      is_well_formed_proposition(p | land | q),
                                      is_well_formed_proposition(q | land | p),
                                      (p | land | q) | implies | (q | land | p),
                                      p | land | q,),
                                  i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=q | land | p, t=t)
        pass


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='R')
        t, _, _, _ = auto_derive_4(t=t, c=is_well_formed_proposition(p))
        t, _, _, _ = auto_derive_4(t=t, c=is_well_formed_proposition(q))
        t, _, _, _ = auto_derive_4(t=t, c=is_well_formed_proposition(r))

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl03, )

        # Derive: (P ⊃ Q) ⊃ ((P ∧ R) ⊃ (B ∧ R))
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=(p | implies | q) | implies | (
                                          (p | land | r) | implies | (q | land | r)),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(q),
                                      is_well_formed_proposition(r),),
                                  i=pu.ml1.pl03, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(
            p=(p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
            t=t)
        pass

        # Derive: propositions
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(p | land | r),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(r),),
                                  i=pu.pls1.i3, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p | land | r), t=t)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(q | land | r),
                                  p=(
                                      is_well_formed_proposition(q),
                                      is_well_formed_proposition(r),),
                                  i=pu.pls1.i3, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(q | land | r), t=t)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition(p | implies | q),
                                  p=(
                                      is_well_formed_proposition(p),
                                      is_well_formed_proposition(q),),
                                  i=pu.pls1.i4, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(p | implies | q), t=t)
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=is_well_formed_proposition((p | land | r) | implies | (q | land | r)),
                                  p=(
                                      is_well_formed_proposition(p | land | r),
                                      is_well_formed_proposition(q | land | r),),
                                  i=pu.pls1.i4, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(
            p=is_well_formed_proposition((p | land | r) | implies | (q | land | r)), t=t)

        # make (P implies Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p | implies | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens)

        # Derive: (P ∧ R) implies (Q ∧ R)  from P by modus-ponens
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=(p | land | r) | implies | (q | land | r),
                                  p=(
                                      is_well_formed_proposition(p | implies | q),
                                      is_well_formed_proposition((p | land | r) | implies | (q | land | r)),
                                      (p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
                                      p | implies | q,),
                                  i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=(p | land | r) | implies | (q | land | r), t=t)
        pass


class TestPL4:
    def test_pl4_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='R')
        t, _, _, _, = auto_derive_4(t=t, c=is_well_formed_proposition(p))
        t, _, _, _, = auto_derive_4(t=t, c=is_well_formed_proposition(q))
        t, _, _, _, = auto_derive_4(t=t, c=is_well_formed_proposition(r))

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl04, )

        # Derive: [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
        phi = ((p | implies | q) | land | (q | implies | r)) | implies | (p | implies | r)
        t, _, _, _ = auto_derive_4(t=t, c=phi)
        assert pu.as1.is_valid_proposition_so_far_1(
            p=((p | implies | q) | land | (
                (q | implies | r)) | implies | (p | implies | r)),
            t=t)
        pass


class TestPL5:
    def test_pl5_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵).

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t1 = pu.as1.WellFormedAxiomatization(d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization,))
        t1, x, = pu.pls1.let_x_be_a_propositional_variable(t=t1, formula_ts='X')
        t1, y, = pu.pls1.let_x_be_a_propositional_variable(t=t1, formula_ts='Y')
        t1, _, = pu.as1.let_x_be_an_axiom(t=t1, s=y)

        # Add axiom PL05 to the theory
        t1, _ = pu.as1.let_x_be_an_inference_rule(t=t1, i=pu.ml1.pl05, )

        # Derive: P ⊃ Q
        t2, success, _ = auto_derive_2(t=t1, c=is_well_formed_proposition(x))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(x), t=t2)

        t2, success, _ = auto_derive_2(t=t2, c=is_well_formed_proposition(y))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(y), t=t2)

        t2, success, _ = auto_derive_2(t=t2, c=is_well_formed_proposition(x | implies | y))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(x | implies | y), t=t2)

        t3, success, _, _ = auto_derive_4(t=t1, c=is_well_formed_proposition(x | implies | y),
                                          max_recursion=4)
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=is_well_formed_proposition(x | implies | y), t=t3)

        t2, success, _ = auto_derive_2(t=t2, c=y | implies | (x | implies | y))
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=y | implies | (x | implies | y), t=t2)

        t4, _, _ = pu.as1.derive_1(
            t=t2,
            c=x | implies | y,
            p=(
                is_well_formed_proposition(y),
                is_well_formed_proposition(x | implies | y),
                y | implies | (x | implies | y),
                y,),
            i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=x | implies | y, t=t4)

        t5, success, _ = derive_2(t=t2, c=x | implies | y, debug=False,
                                  i=pu.ir1.modus_ponens)
        assert success
        assert pu.as1.is_valid_proposition_so_far_1(p=x | implies | y, t=t5)
        pass

        # TODO: This automatic-derivation fails.
        # t6, success, _, _ = auto_derive_4(t=t3, conjecture=x | implies | y, debug=False, max_recursion=5)
        # assert success
        # assert pu.as1.is_valid_statement_in_theory(phi=x | implies | y, t=t6)
        # pass


class TestMancosu2021P20:
    def test_mancosu_2021_page_20_with_derivation_1(self, caplog):
        t = pu.as1.WellFormedAxiomatization(
            d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, p1, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='p1')
        t, p2, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='p2')
        t, success, _, = derive_2(c=is_well_formed_proposition(p1),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(p2),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(p1 | lor | p2),
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(p2 | lor | p1),
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(p1 | implies | (p1 | lor | p2)),
                                  i=pu.pls1.i4, t=t)

        # 1. ⊢ 𝑝1 ⊃ (𝑝1 ∨ 𝑝2) (axiom PL7)
        t, success, _, = derive_2(t=t, c=p1 | implies | (p1 | lor | p2),
                                  i=pu.ml1.pl07)
        assert success

        # 2. ⊢ [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] (axiom PL5)
        t, success, _, = derive_2(c=is_well_formed_proposition((p1 | lor | p2) | implies | (p2 | lor | p1)),
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(
            c=is_well_formed_proposition(((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (
                    p1 | implies | (p1 | lor | p2))),
            i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(
            t=t,
            c=(p1 | implies | (p1 | lor | p2)) | implies | (
                    ((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (p1 | implies | (p1 | lor | p2))),
            i=pu.ml1.pl05)
        assert success

        pass
        # 3. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) (mp 1, 2)
        t, success, _, = derive_2(
            c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (p1 | implies | (p1 | lor | p2)),
            i=pu.ir1.modus_ponens, t=t, debug=False)
        assert success

        # 4. ⊢ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] ⊃[{((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))}] (axiom PL3)
        # 5. ⊢ {((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} ⊃ {(𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))} (mp 3, 4)
        # 6. ⊢ [(𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] (axiom PL1)
        # 7. ⊢ (𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)(axiom PL8)
        # 8. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 6, 7)
        # 9. ⊢ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) (mp 5, 8)
        # 10. ⊢ [((𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) ∧ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1))] ⊃ (𝑝1 ⊃ (𝑝2 ∨ 𝑝1)) (axiom PL4)
        # 11. ⊢ 𝑝1 ⊃ (𝑝2 ∨ 𝑝1)(mp 9, 10)
        pass

    def test_mancosu_2021_page_20(self, caplog):
        t = pu.as1.WellFormedTheory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        t = pu.ml1.extend_theory_with_mancosu_2021_page_20(t=t)
        pass

    def test_mancosu_2021_page_21_with_derivation_1(self, caplog):
        t = pu.as1.WellFormedAxiomatization(
            d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, c, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='C')
        t, d, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='D')
        t, success, _, = derive_2(c=is_well_formed_proposition(c),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(d),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(c | implies | d),
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(d | implies | c),
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(d | land | d),
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition(c | land | d),
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_2(c=is_well_formed_proposition((d | land | d) | implies | (c | land | d)),
                                  i=pu.pls1.i4, t=t)
        # 1. ⊢ 𝐶(hypothesis)
        t, hypothesis = pu.as1.let_x_be_an_axiom(t=t, s=c)
        assert pu.as1.is_valid_proposition_so_far_1(p=c, t=t)
        # 2. ⊢ 𝐶 ⊃ (𝐷 ⊃ 𝐶)(axiom PL5)
        t, success, _, = derive_2(c=c | implies | (d | implies | c),
                                  i=pu.ml1.pl05, t=t)
        assert success
        # 3. ⊢ 𝐷 ⊃ 𝐶 (mp 1, 2)
        t, success, _, = derive_2(c=d | implies | c,
                                  i=pu.ir1.modus_ponens, t=t)
        assert success
        # 4. ⊢ (𝐷 ⊃ 𝐶) ⊃ [(𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)] (axiom PL3)
        t, success, _, = derive_2(
            c=(d | implies | c) | implies | ((d | land | d) | implies | (c | land | d)),
            i=pu.ml1.pl03, t=t)
        assert success
        # 5. ⊢ (𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)(mp 3, 4)
        t, success, _, = derive_2(
            c=(d | land | d) | implies | (c | land | d),
            i=pu.ir1.modus_ponens, t=t)
        assert success
        # 6. ⊢ 𝐷 ⊃ (𝐷 ∧ 𝐷)(axiom PL1)
        t, success, _, = derive_2(
            c=d | implies | (d | land | d),
            i=pu.ml1.pl01, t=t)
        assert success
        # 7. ⊢ 𝐷(hypothesis)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=d)
        # 8. ⊢ 𝐷 ∧ 𝐷(mp 6, 7)
        t, success, _, = derive_2(
            c=d | land | d,
            i=pu.ir1.modus_ponens, t=t)
        assert success
        # 9. ⊢ 𝐶 ∧ 𝐷(mp 5, 8)
        t, success, _, = derive_2(
            c=c | land | d,
            i=pu.ir1.modus_ponens, t=t, debug=False)
        assert success
