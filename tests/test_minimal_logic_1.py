import pytest
import logging
import punctilious as pu
from punctilious.connectives_standard_library_1 import *

derive_0 = pu.as1.derive_0
derive_2 = pu.as1.derive_2
auto_derive_2 = pu.as1.auto_derive_2
auto_derive_3 = pu.as1.auto_derive_3
auto_derive_4 = pu.as1.auto_derive_4


@pytest.fixture
def a():
    a = pu.as1.let_x_be_a_simple_object(formula_ts='A')
    return a


@pytest.fixture
def b():
    b = pu.as1.let_x_be_a_simple_object(formula_ts='B')
    return b


@pytest.fixture
def c():
    c = pu.as1.let_x_be_a_simple_object(formula_ts='C')
    return c


@pytest.fixture
def theory(a, b, c):
    # elaborate a theory with 3 propositions: a, b, and c
    a1 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(a))
    a2 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(b))
    a3 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(c))
    t = pu.as1.Axiomatization(d=(*pu.ir1.axioms, *pu.pls1.axiomatization, a1, a2, a3,))

    # derive: a is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=is_a_proposition(a),
                           p=(is_a_propositional_variable(a),),
                           i=pu.pls1.i1)
    assert as1.is_valid_proposition_in_theory_1(p=is_a_proposition(a), t=t)

    # derive: b is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=is_a_proposition(b),
                           p=(is_a_propositional_variable(b),),
                           i=pu.pls1.i1)
    assert as1.is_valid_proposition_in_theory_1(p=is_a_proposition(b), t=t)

    # derive: c is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=is_a_proposition(c),
                           p=(is_a_propositional_variable(c),),
                           i=pu.pls1.i1)
    assert as1.is_valid_proposition_in_theory_1(p=is_a_proposition(c), t=t)

    return t


class TestPL1:
    def test_pl1(self):
        # Test PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)
        t = pu.as1.let_x_be_a_theory()

        # Elaborate a basic theory with P as a propositional-variable
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')

        # Add axiom PL01 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ml1.pl01, )

        # Derive: P is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=is_a_proposition(p),
                               p=(is_a_propositional_variable(p),),
                               i=pu.pls1.i1)
        assert pu.as1.is_valid_proposition_in_theory_1(p=is_a_proposition(p), t=t)
        pass

        # Derive: P ⊃ (P ∧ P)
        t, _ = pu.as1.derive_1(t=t,
                               c=p | implies | (p | land | p),
                               p=(
                                   is_a_proposition(p),),
                               i=pu.ml1.pl01)
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | implies | (p | land | p), t=t)
        pass

        # Derive: (P ∧ P) is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=is_a_proposition(p | land | p),
                               p=(
                                   is_a_proposition(p),
                                   is_a_proposition(p),),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_proposition_in_theory_1(p=is_a_proposition(p | land | p), t=t)

        # make P valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p)
        t, _, = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ir1.modus_ponens)

        # Derive: P ∧ P from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=p | land | p,
                               p=(
                                   is_a_proposition(p),
                                   (p | land | p) | is_a | is_a_proposition,
                                   p | implies | (p | land | p),
                                   p,),
                               i=pu.ir1.modus_ponens)
        assert pu.as1.is_valid_proposition_in_theory_1(p=p | land | p, t=t)
        pass


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # Elaborate a basic theory with P and Q as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, _, _, _ = auto_derive_4(t=t, conjecture=is_a_proposition(p))
        t, _, _, _ = auto_derive_4(t=t, conjecture=is_a_proposition(q))

        # Add axiom PL02 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ml1.pl02, )

        # Derive: (P ∧ Q) ⊃ (Q ∧ P)
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | q) | implies | (q | land | p),
                               p=(
                                   is_a_proposition(p),
                                   is_a_proposition(q),),
                               i=pu.ml1.pl02)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | land | q) | implies | (q | land | p), t=t)

        # Derive: (P ∧ Q) and (Q ∧ P) is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | q) | is_a | is_a_proposition,
                               p=(
                                   is_a_proposition(p),
                                   is_a_proposition(q),),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | land | q) | is_a | is_a_proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(q | land | p) | is_a | is_a_proposition,
                               p=(
                                   is_a_proposition(q),
                                   is_a_proposition(p),),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(q | land | p) | is_a | is_a_proposition, t=t)

        # make (P ∧ Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p | land | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ir1.modus_ponens)

        # Derive: P ∧ P from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=q | land | p,
                               p=(
                                   (p | land | q) | is_a | is_a_proposition,
                                   (q | land | p) | is_a | is_a_proposition,
                                   (p | land | q) | implies | (q | land | p),
                                   p | land | q,),
                               i=pu.ir1.modus_ponens)
        assert pu.as1.is_valid_proposition_in_theory_1(p=q | land | p, t=t)
        pass


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='R')
        t, _, _, _ = auto_derive_4(t=t, conjecture=is_a_proposition(p))
        t, _, _, _ = auto_derive_4(t=t, conjecture=is_a_proposition(q))
        t, _, _, _ = auto_derive_4(t=t, conjecture=r | is_a | is_a_proposition)

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ml1.pl03, )

        # Derive: (P ⊃ Q) ⊃ ((P ∧ R) ⊃ (B ∧ R))
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | implies | q) | implies | (
                                       (p | land | r) | implies | (q | land | r)),
                               p=(
                                   is_a_proposition(p),
                                   is_a_proposition(q),
                                   r | is_a | is_a_proposition,),
                               i=pu.ml1.pl03)
        assert pu.as1.is_valid_proposition_in_theory_1(
            p=(p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
            t=t)
        pass

        # Derive: propositions
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | r) | is_a | is_a_proposition,
                               p=(
                                   is_a_proposition(p),
                                   r | is_a | is_a_proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | land | r) | is_a | is_a_proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(q | land | r) | is_a | is_a_proposition,
                               p=(
                                   is_a_proposition(q),
                                   r | is_a | is_a_proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(q | land | r) | is_a | is_a_proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | implies | q) | is_a | is_a_proposition,
                               p=(
                                   is_a_proposition(p),
                                   is_a_proposition(q),),
                               i=pu.pls1.i4)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | implies | q) | is_a | is_a_proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=((p | land | r) | implies | (q | land | r)) | is_a | is_a_proposition,
                               p=(
                                   (p | land | r) | is_a | is_a_proposition,
                                   (q | land | r) | is_a | is_a_proposition,),
                               i=pu.pls1.i4)
        assert pu.as1.is_valid_proposition_in_theory_1(
            p=((p | land | r) | implies | (q | land | r)) | is_a | is_a_proposition, t=t)

        # make (P implies Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=p | implies | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ir1.modus_ponens)

        # Derive: (P ∧ R) implies (Q ∧ R)  from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | r) | implies | (q | land | r),
                               p=(
                                   (p | implies | q) | is_a | is_a_proposition,
                                   ((p | land | r) | implies | (q | land | r)) | is_a | is_a_proposition,
                                   (p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
                                   p | implies | q,),
                               i=pu.ir1.modus_ponens)
        assert pu.as1.is_valid_proposition_in_theory_1(p=(p | land | r) | implies | (q | land | r), t=t)
        pass


class TestPL4:
    def test_pl4_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, formula_ts='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='R')
        t, _, _, _, = auto_derive_4(t=t, conjecture=is_a_proposition(p))
        t, _, _, _, = auto_derive_4(t=t, conjecture=is_a_proposition(q))
        t, _, _, _, = auto_derive_4(t=t, conjecture=r | is_a | is_a_proposition)

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t1=t, i=pu.ml1.pl04, )

        # Derive: [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
        phi = ((p | implies | q) | land | (q | implies | r)) | implies | (p | implies | r)
        t, _, _, _ = auto_derive_4(t=t, conjecture=phi)
        assert pu.as1.is_valid_proposition_in_theory_1(
            p=((p | implies | q) | land | (
                (q | implies | r)) | implies | (p | implies | r)),
            t=t)
        pass


class TestPL5:
    def test_pl5_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵).

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t1 = pu.as1.Axiomatization(d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization,))
        t1, x, = pu.pls1.let_x_be_a_propositional_variable(t=t1, formula_ts='X')
        t1, y, = pu.pls1.let_x_be_a_propositional_variable(t=t1, formula_ts='Y')
        t1, _, = pu.as1.let_x_be_an_axiom(t=t1, s=y)

        # Add axiom PL05 to the theory
        t1, _ = pu.as1.let_x_be_an_inference_rule(t1=t1, i=pu.ml1.pl05, )

        # Derive: P ⊃ Q
        t2, success, _ = auto_derive_2(t=t1, conjecture=x | is_a | is_a_proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=x | is_a | is_a_proposition, t=t2)

        t2, success, _ = auto_derive_2(t=t2, conjecture=y | is_a | is_a_proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=y | is_a | is_a_proposition, t=t2)

        t2, success, _ = auto_derive_2(t=t2, conjecture=(x | implies | y) | is_a | is_a_proposition)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=(x | implies | y) | is_a | is_a_proposition, t=t2)

        t3, success, _, _ = auto_derive_4(t=t1, conjecture=(x | implies | y) | is_a | is_a_proposition,
                                          max_recursion=4)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=(x | implies | y) | is_a | is_a_proposition, t=t3)

        t2, success, _ = auto_derive_2(t=t2, conjecture=y | implies | (x | implies | y))
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=y | implies | (x | implies | y), t=t2)

        t4, _, = pu.as1.derive_1(
            t=t2,
            c=x | implies | y,
            p=(
                y | is_a | is_a_proposition,
                (x | implies | y) | is_a | is_a_proposition,
                y | implies | (x | implies | y),
                y,),
            i=pu.ir1.modus_ponens)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=x | implies | y, t=t4)

        t5, success, _ = derive_2(t=t2, c=x | implies | y, debug=False,
                                  i=pu.ir1.modus_ponens)
        assert success
        assert pu.as1.is_valid_proposition_in_theory_1(p=x | implies | y, t=t5)
        pass

        # TODO: This automatic-derivation fails.
        # t6, success, _, _ = auto_derive_4(t=t3, conjecture=x | implies | y, debug=False, max_recursion=5)
        # assert success
        # assert pu.as1.is_valid_statement_in_theory(phi=x | implies | y, t=t6)
        # pass


class TestMancosu2021P20:
    def test_mancosu_2021_page_20_with_derivation_1(self, caplog):
        t = pu.as1.Axiomatization(
            d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, p1, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='p1')
        t, p2, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='p2')
        t, success, _, = derive_2(c=is_a_proposition(p1),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_a_proposition(p2),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=is_a_proposition(p1 | lor | p2),
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_2(c=is_a_proposition(p2 | lor | p1),
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_2(c=(p1 | implies | (p1 | lor | p2)) | is_a | is_a_proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | is_a | is_a_proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(
            c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (
                    p1 | implies | (p1 | lor | p2)) | is_a | is_a_proposition,
            i=pu.pls1.i4, t=t)

        # 1. ⊢ 𝑝1 ⊃ (𝑝1 ∨ 𝑝2) (axiom PL7)
        t, success, _, = derive_2(t=t, c=p1 | implies | (p1 | lor | p2),
                                  i=pu.ml1.pl07)
        assert success

        # 2. ⊢ [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] (axiom PL5)
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
        t = pu.as1.Theory()
        t = pu.ml1.extend_theory_with_minimal_logic_1(t=t)
        t = pu.ml1.extend_theory_with_mancosu_2021_page_20(t=t)

    def test_mancosu_2021_page_21_with_derivation_1(self, caplog):
        t = pu.as1.Axiomatization(
            d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, c, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='C')
        t, d, = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='D')
        t, success, _, = derive_2(c=is_a_proposition(c),
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=d | is_a | is_a_proposition,
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_2(c=(c | implies | d) | is_a | is_a_proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(c=(d | implies | c) | is_a | is_a_proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_2(c=(d | land | d) | is_a | is_a_proposition,
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_2(c=(c | land | d) | is_a | is_a_proposition,
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_2(c=((d | land | d) | implies | (c | land | d)) | is_a | is_a_proposition,
                                  i=pu.pls1.i4, t=t)
        # 1. ⊢ 𝐶(hypothesis)
        t, hypothesis = pu.as1.let_x_be_an_axiom(t=t, s=c)
        assert pu.as1.is_valid_proposition_in_theory_1(p=c, t=t)
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
