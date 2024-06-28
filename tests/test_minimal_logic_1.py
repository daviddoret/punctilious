import pytest
import logging
import punctilious as pu
from punctilious.connectives_standard_library_1 import *

derive_0 = pu.as1.derive_0
derive_1 = pu.as1.derive_2
auto_derive_2 = pu.as1.auto_derive_2
auto_derive_3 = pu.as1.auto_derive_3
auto_derive_4 = pu.as1.auto_derive_4


@pytest.fixture
def a():
    a = pu.as1.let_x_be_a_simple_object(formula_typesetter='A')
    return a


@pytest.fixture
def b():
    b = pu.as1.let_x_be_a_simple_object(formula_typesetter='B')
    return b


@pytest.fixture
def c():
    c = pu.as1.let_x_be_a_simple_object(formula_typesetter='C')
    return c


@pytest.fixture
def theory(a, b, c):
    # elaborate a theory with 3 propositions: a, b, and c
    a1 = pu.as1.let_x_be_an_axiom_deprecated(valid_statement=a | is_a | propositional_variable)
    a2 = pu.as1.let_x_be_an_axiom_deprecated(valid_statement=b | is_a | propositional_variable)
    a3 = pu.as1.let_x_be_an_axiom_deprecated(valid_statement=c | is_a | propositional_variable)
    t = pu.as1.Axiomatization(derivations=(*pu.ir1.axioms, *pu.pls1.axiomatization, a1, a2, a3,))

    # derive: a is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=a | is_a | proposition,
                           p=(a | is_a | propositional_variable,),
                           i=pu.pls1.i1)
    assert as1.is_valid_statement_in_theory(phi=a | is_a | proposition, t=t)

    # derive: b is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=b | is_a | proposition,
                           p=(b | is_a | propositional_variable,),
                           i=pu.pls1.i1)
    assert as1.is_valid_statement_in_theory(phi=b | is_a | proposition, t=t)

    # derive: c is-a proposition
    t, m = pu.as1.derive_1(t=t,
                           c=c | is_a | proposition,
                           p=(c | is_a | propositional_variable,),
                           i=pu.pls1.i1)
    assert as1.is_valid_statement_in_theory(phi=c | is_a | proposition, t=t)

    return t


class TestPL1:
    def test_pl1(self):
        # Test PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # Elaborate a basic theory with P as a propositional-variable
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')

        # Add axiom PL01 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl01, )

        # Derive: P is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=p | is_a | proposition,
                               p=(
                                   p | is_a | propositional_variable,),
                               i=pu.pls1.i1)
        assert pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=t)
        pass

        # Derive: P ⊃ (P ∧ P)
        t, _ = pu.as1.derive_1(t=t,
                               c=p | implies | (p | land | p),
                               p=(
                                   p | is_a | proposition,),
                               i=pu.ml1.pl01)
        assert pu.as1.is_valid_statement_in_theory(phi=p | implies | (p | land | p), t=t)
        pass

        # Derive: (P ∧ P) is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | p) | is_a | proposition,
                               p=(
                                   p | is_a | proposition,
                                   p | is_a | proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | p) | is_a | proposition, t=t)

        # make P valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=p)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens_axiom)

        # Derive: P ∧ P from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=p | land | p,
                               p=(
                                   p | is_a | proposition,
                                   (p | land | p) | is_a | proposition,
                                   p | implies | (p | land | p),
                                   p,),
                               i=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=p | land | p, t=t)
        pass


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # Elaborate a basic theory with P and Q as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Q')
        t, _, _, _ = auto_derive_4(t=t, conjecture=p | is_a | proposition)
        t, _, _, _ = auto_derive_4(t=t, conjecture=q | is_a | proposition)

        # Add axiom PL02 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl02, )

        # Derive: (P ∧ Q) ⊃ (Q ∧ P)
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | q) | implies | (q | land | p),
                               p=(
                                   p | is_a | proposition,
                                   q | is_a | proposition,),
                               i=pu.ml1.pl02)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | q) | implies | (q | land | p), t=t)

        # Derive: (P ∧ Q) and (Q ∧ P) is-a proposition
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | q) | is_a | proposition,
                               p=(
                                   p | is_a | proposition,
                                   q | is_a | proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | q) | is_a | proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(q | land | p) | is_a | proposition,
                               p=(
                                   q | is_a | proposition,
                                   p | is_a | proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_statement_in_theory(phi=(q | land | p) | is_a | proposition, t=t)

        # make (P ∧ Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=p | land | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens_axiom)

        # Derive: P ∧ P from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=q | land | p,
                               p=(
                                   (p | land | q) | is_a | proposition,
                                   (q | land | p) | is_a | proposition,
                                   (p | land | q) | implies | (q | land | p),
                                   p | land | q,),
                               i=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=q | land | p, t=t)
        pass


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='R')
        t, _, _, _ = auto_derive_4(t=t, conjecture=p | is_a | proposition)
        t, _, _, _ = auto_derive_4(t=t, conjecture=q | is_a | proposition)
        t, _, _, _ = auto_derive_4(t=t, conjecture=r | is_a | proposition)

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl03, )

        # Derive: (P ⊃ Q) ⊃ ((P ∧ R) ⊃ (B ∧ R))
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | implies | q) | implies | (
                                       (p | land | r) | implies | (q | land | r)),
                               p=(
                                   p | is_a | proposition,
                                   q | is_a | proposition,
                                   r | is_a | proposition,),
                               i=pu.ml1.pl03)
        assert pu.as1.is_valid_statement_in_theory(
            phi=(p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
            t=t)
        pass

        # Derive: propositions
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | r) | is_a | proposition,
                               p=(
                                   p | is_a | proposition,
                                   r | is_a | proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | r) | is_a | proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(q | land | r) | is_a | proposition,
                               p=(
                                   q | is_a | proposition,
                                   r | is_a | proposition,),
                               i=pu.pls1.i3)
        assert pu.as1.is_valid_statement_in_theory(phi=(q | land | r) | is_a | proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | implies | q) | is_a | proposition,
                               p=(
                                   p | is_a | proposition,
                                   q | is_a | proposition,),
                               i=pu.pls1.i4)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | implies | q) | is_a | proposition, t=t)
        t, _ = pu.as1.derive_1(t=t,
                               c=((p | land | r) | implies | (q | land | r)) | is_a | proposition,
                               p=(
                                   (p | land | r) | is_a | proposition,
                                   (q | land | r) | is_a | proposition,),
                               i=pu.pls1.i4)
        assert pu.as1.is_valid_statement_in_theory(
            phi=((p | land | r) | implies | (q | land | r)) | is_a | proposition, t=t)

        # make (P implies Q) valid and add modus-ponens to the theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=p | implies | q)
        t, _, = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ir1.modus_ponens_axiom)

        # Derive: (P ∧ R) implies (Q ∧ R)  from P by modus-ponens
        t, _ = pu.as1.derive_1(t=t,
                               c=(p | land | r) | implies | (q | land | r),
                               p=(
                                   (p | implies | q) | is_a | proposition,
                                   ((p | land | r) | implies | (q | land | r)) | is_a | proposition,
                                   (p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
                                   p | implies | q,),
                               i=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | r) | implies | (q | land | r), t=t)
        pass


class TestPL4:
    def test_pl4_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL4. [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t, p, = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')
        t, q, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Q')
        t, r, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='R')
        t, _, _, _, = auto_derive_4(t=t, conjecture=p | is_a | proposition)
        t, _, _, _, = auto_derive_4(t=t, conjecture=q | is_a | proposition)
        t, _, _, _, = auto_derive_4(t=t, conjecture=r | is_a | proposition)

        # Add axiom PL03 to the theory
        t, _ = pu.as1.let_x_be_an_inference_rule(t=t, i=pu.ml1.pl04, )

        # Derive: [(𝐴 ⊃ 𝐵) ∧ (𝐵 ⊃ 𝐶)] ⊃ (𝐴 ⊃ 𝐶)
        phi = ((p | implies | q) | land | (q | implies | r)) | implies | (p | implies | r)
        t, _, _, _ = auto_derive_4(t=t, conjecture=phi)
        assert pu.as1.is_valid_statement_in_theory(
            phi=((p | implies | q) | land | (
                (q | implies | r)) | implies | (p | implies | r)),
            t=t)
        pass


class TestPL5:
    def test_pl5_with_auto_derivation(self, caplog):
        caplog.set_level(logging.INFO)

        # PL5. 𝐵 ⊃ (𝐴 ⊃ 𝐵).

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        t1 = pu.as1.Axiomatization(derivations=(*pu.ir1.axiomatization, *pu.pls1.axiomatization,))
        t1, x, = pu.pls1.let_x_be_a_propositional_variable(t=t1, rep='X')
        t1, y, = pu.pls1.let_x_be_a_propositional_variable(t=t1, rep='Y')
        t1, _, = pu.as1.let_x_be_an_axiom(t=t1, valid_statement=y)

        # Add axiom PL05 to the theory
        t1, _ = pu.as1.let_x_be_an_inference_rule(t=t1, i=pu.ml1.pl05, )

        # Derive: P ⊃ Q
        t2, success, _ = auto_derive_2(t=t1, conjecture=x | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=x | is_a | proposition, t=t2)

        t2, success, _ = auto_derive_2(t=t2, conjecture=y | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=y | is_a | proposition, t=t2)

        t2, success, _ = auto_derive_2(t=t2, conjecture=(x | implies | y) | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=(x | implies | y) | is_a | proposition, t=t2)

        t3, success, _, _ = auto_derive_4(t=t1, conjecture=(x | implies | y) | is_a | proposition,
                                          max_recursion=4)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=(x | implies | y) | is_a | proposition, t=t3)

        t2, success, _ = auto_derive_2(t=t2, conjecture=y | implies | (x | implies | y))
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=y | implies | (x | implies | y), t=t2)

        t4, _, = pu.as1.derive_1(
            t=t2,
            c=x | implies | y,
            p=(
                y | is_a | proposition,
                (x | implies | y) | is_a | proposition,
                y | implies | (x | implies | y),
                y,),
            i=pu.ir1.modus_ponens_axiom)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=x | implies | y, t=t4)

        t5, success, _ = derive_1(t=t2, c=x | implies | y, debug=True,
                                  i=pu.ir1.modus_ponens_axiom)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=x | implies | y, t=t5)
        pass

        # TODO: This automatic-derivation fails.
        # t6, success, _, _ = auto_derive_4(t=t3, conjecture=x | implies | y, debug=False, max_recursion=5)
        # assert success
        # assert pu.as1.is_valid_statement_in_theory(phi=x | implies | y, t=t6)
        # pass


class TestMancosu2021P20:
    def test_mancosu_2021_page_20_with_derivation_1(self, caplog):
        t = pu.as1.Axiomatization(
            derivations=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, p1, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='p1')
        t, p2, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='p2')
        t, success, _, = derive_1(c=p1 | is_a | proposition,
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_1(c=p2 | is_a | proposition,
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_1(c=(p1 | lor | p2) | is_a | proposition,
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_1(c=(p2 | lor | p1) | is_a | proposition,
                                  i=pu.pls1.i5, t=t)
        t, success, _, = derive_1(c=(p1 | implies | (p1 | lor | p2)) | is_a | proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_1(c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | is_a | proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_1(
            c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (
                    p1 | implies | (p1 | lor | p2)) | is_a | proposition,
            i=pu.pls1.i4, t=t)

        # 1. ⊢ 𝑝1 ⊃ (𝑝1 ∨ 𝑝2) (axiom PL7)
        t, success, _, = derive_1(t=t, c=p1 | implies | (p1 | lor | p2),
                                  i=pu.ml1.pl07)
        assert success

        # 2. ⊢ [𝑝1 ⊃ (𝑝1 ∨ 𝑝2)] ⊃ [((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2))] (axiom PL5)
        t, success, _, = derive_1(
            t=t,
            c=(p1 | implies | (p1 | lor | p2)) | implies | (
                    ((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (p1 | implies | (p1 | lor | p2))),
            i=pu.ml1.pl05)
        assert success

        # 3. ⊢ ((𝑝1 ∨ 𝑝2) ⊃ (𝑝2 ∨ 𝑝1)) ⊃ (𝑝1 ⊃ (𝑝1 ∨ 𝑝2)) (mp 1, 2)
        t, success, _, = derive_1(
            c=((p1 | lor | p2) | implies | (p2 | lor | p1)) | implies | (p1 | implies | (p1 | lor | p2)),
            i=pu.ir1.modus_ponens_axiom, t=t, debug=True)
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

    def test_mancosu_2021_page_21_with_derivation_1(self, caplog):
        t = pu.as1.Axiomatization(
            derivations=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, *pu.ml1.axiomatization,))
        t, c, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='C')
        t, d, = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='D')
        t, success, _, = derive_1(c=c | is_a | proposition,
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_1(c=d | is_a | proposition,
                                  i=pu.pls1.i1, t=t)
        t, success, _, = derive_1(c=(c | implies | d) | is_a | proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_1(c=(d | implies | c) | is_a | proposition,
                                  i=pu.pls1.i4, t=t)
        t, success, _, = derive_1(c=(d | land | d) | is_a | proposition,
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_1(c=(c | land | d) | is_a | proposition,
                                  i=pu.pls1.i3, t=t)
        t, success, _, = derive_1(c=((d | land | d) | implies | (c | land | d)) | is_a | proposition,
                                  i=pu.pls1.i4, t=t)
        # 1. ⊢ 𝐶(hypothesis)
        t, hypothesis = pu.as1.let_x_be_an_axiom(t=t, valid_statement=c)
        assert pu.as1.is_valid_statement_in_theory(phi=c, t=t)
        # 2. ⊢ 𝐶 ⊃ (𝐷 ⊃ 𝐶)(axiom PL5)
        t, success, _, = derive_1(c=c | implies | (d | implies | c),
                                  i=pu.ml1.pl05, t=t)
        assert success
        # 3. ⊢ 𝐷 ⊃ 𝐶 (mp 1, 2)
        t, success, _, = derive_1(c=d | implies | c,
                                  i=pu.ir1.modus_ponens_axiom, t=t)
        assert success
        # 4. ⊢ (𝐷 ⊃ 𝐶) ⊃ [(𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)] (axiom PL3)
        t, success, _, = derive_1(
            c=(d | implies | c) | implies | ((d | land | d) | implies | (c | land | d)),
            i=pu.ml1.pl03, t=t)
        assert success
        # 5. ⊢ (𝐷 ∧ 𝐷) ⊃ (𝐶 ∧ 𝐷)(mp 3, 4)
        t, success, _, = derive_1(
            c=(d | land | d) | implies | (c | land | d),
            i=pu.ir1.modus_ponens_axiom, t=t)
        assert success
        # 6. ⊢ 𝐷 ⊃ (𝐷 ∧ 𝐷)(axiom PL1)
        t, success, _, = derive_1(
            c=d | implies | (d | land | d),
            i=pu.ml1.pl01, t=t)
        assert success
        # 7. ⊢ 𝐷(hypothesis)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, valid_statement=d)
        # 8. ⊢ 𝐷 ∧ 𝐷(mp 6, 7)
        t, success, _, = derive_1(
            c=d | land | d,
            i=pu.ir1.modus_ponens_axiom, t=t)
        assert success
        # 9. ⊢ 𝐶 ∧ 𝐷(mp 5, 8)
        t, success, _, = derive_1(
            c=c | land | d,
            i=pu.ir1.modus_ponens_axiom, t=t, debug=True)
        assert success
