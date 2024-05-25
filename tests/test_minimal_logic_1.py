import pytest
import punctilious as pu

# retrieve some basic vocabulary
is_a = pu.as1.connectives.is_a
propositional_variable = pu.as1.connectives.propositional_variable
land = pu.as1.connectives.land
proposition = pu.as1.connectives.proposition
implies = pu.as1.connectives.implies


@pytest.fixture
def a():
    a = pu.as1.let_x_be_a_simple_object(rep='A')
    return a


@pytest.fixture
def b():
    b = pu.as1.let_x_be_a_simple_object(rep='B')
    return b


@pytest.fixture
def c():
    c = pu.as1.let_x_be_a_simple_object(rep='C')
    return c


@pytest.fixture
def theory(a, b, c):
    # elaborate a theory with 3 propositions: a, b, and c
    a1 = pu.as1.let_x_be_an_axiom_deprecated(claim=a | is_a | propositional_variable)
    a2 = pu.as1.let_x_be_an_axiom_deprecated(claim=b | is_a | propositional_variable)
    a3 = pu.as1.let_x_be_an_axiom_deprecated(claim=c | is_a | propositional_variable)
    theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3,))

    # derive: a is-a proposition
    theory = pu.as1.derive_OBSOLETE(theory=theory,
                                    claim=a | is_a | proposition,
                                    premises=(a | is_a | propositional_variable,),
                                    inference_rule=pu.pls1.i1)
    assert theory.is_valid_statement(phi=a | is_a | proposition)

    # derive: b is-a proposition
    theory = pu.as1.derive_OBSOLETE(theory=theory,
                                    claim=b | is_a | proposition,
                                    premises=(b | is_a | propositional_variable,),
                                    inference_rule=pu.pls1.i1)
    assert theory.is_valid_statement(phi=b | is_a | proposition)

    # derive: c is-a proposition
    theory = pu.as1.derive_OBSOLETE(theory=theory,
                                    claim=c | is_a | proposition,
                                    premises=(c | is_a | propositional_variable,),
                                    inference_rule=pu.pls1.i1)
    assert theory.is_valid_statement(phi=c | is_a | proposition)

    return theory


class TestPL1:
    def test_pl1(self):
        # Test PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # Elaborate a basic theory with P as a propositional-variable
        theory, p, = pu.pls1.let_x_be_a_propositional_variable(theory=None, rep='P')

        # Add axiom PL01 to the theory
        theory, _ = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ml1.pl01, )

        # Derive: P ⊃ (P ∧ P)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=p | implies | (p | land | p),
                                  premises=(
                                      p | is_a | proposition,),
                                  inference_rule=pu.ml1.pl01)
        assert theory.is_valid_statement(phi=p | implies | (p | land | p))
        pass

        # Derive: (P ∧ P) is-a proposition
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | land | p) | is_a | proposition,
                                  premises=(
                                      p | is_a | proposition,
                                      p | is_a | proposition,),
                                  inference_rule=pu.pls1.i3)
        assert theory.is_valid_statement(phi=(p | land | p) | is_a | proposition)

        # make P valid and add modus-ponens to the theory
        theory, _, = pu.as1.let_x_be_an_axiom(theory=theory, claim=p)
        theory, _, = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ir1.modus_ponens_axiom)

        # Derive: P ∧ P from P by modus-ponens
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=p | land | p,
                                  premises=(
                                      p | is_a | proposition,
                                      (p | land | p) | is_a | proposition,
                                      p | implies | (p | land | p),
                                      p,),
                                  inference_rule=pu.ir1.modus_ponens_axiom)
        assert theory.is_valid_statement(phi=p | land | p)
        pass


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # Elaborate a basic theory with P and Q as a propositional-variables
        theory, p, = pu.pls1.let_x_be_a_propositional_variable(theory=None, rep='P')
        theory, q, = pu.pls1.let_x_be_a_propositional_variable(theory=theory, rep='Q')

        # Add axiom PL02 to the theory
        theory, _ = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ml1.pl02, )

        # Derive: (P ∧ Q) ⊃ (Q ∧ P)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | land | q) | implies | (q | land | p),
                                  premises=(
                                      p | is_a | proposition,
                                      q | is_a | proposition,),
                                  inference_rule=pu.ml1.pl02)
        assert theory.is_valid_statement(phi=(p | land | q) | implies | (q | land | p))
        pass

        # Derive: (P ∧ Q) and (Q ∧ P) is-a proposition
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | land | q) | is_a | proposition,
                                  premises=(
                                      p | is_a | proposition,
                                      q | is_a | proposition,),
                                  inference_rule=pu.pls1.i3)
        assert theory.is_valid_statement(phi=(p | land | q) | is_a | proposition)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(q | land | p) | is_a | proposition,
                                  premises=(
                                      q | is_a | proposition,
                                      p | is_a | proposition,),
                                  inference_rule=pu.pls1.i3)
        assert theory.is_valid_statement(phi=(q | land | p) | is_a | proposition)

        # make (P ∧ Q) valid and add modus-ponens to the theory
        theory, _, = pu.as1.let_x_be_an_axiom(theory=theory, claim=p | land | q)
        theory, _, = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ir1.modus_ponens_axiom)

        # Derive: P ∧ P from P by modus-ponens
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=q | land | p,
                                  premises=(
                                      (p | land | q) | is_a | proposition,
                                      (q | land | p) | is_a | proposition,
                                      (p | land | q) | implies | (q | land | p),
                                      p | land | q,),
                                  inference_rule=pu.ir1.modus_ponens_axiom)
        assert theory.is_valid_statement(phi=q | land | p)
        pass


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # Elaborate a basic theory with P, Q, and R as a propositional-variables
        theory, p, = pu.pls1.let_x_be_a_propositional_variable(theory=None, rep='P')
        theory, q, = pu.pls1.let_x_be_a_propositional_variable(theory=theory, rep='Q')
        theory, r, = pu.pls1.let_x_be_a_propositional_variable(theory=theory, rep='R')

        # Add axiom PL03 to the theory
        theory, _ = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ml1.pl03, )

        # Derive: (P ⊃ Q) ⊃ ((P ∧ R) ⊃ (B ∧ R))
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
                                  premises=(
                                      p | is_a | proposition,
                                      q | is_a | proposition,
                                      r | is_a | proposition,),
                                  inference_rule=pu.ml1.pl03)
        assert theory.is_valid_statement(phi=(p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)))
        pass

        # Derive: propositions
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | land | r) | is_a | proposition,
                                  premises=(
                                      p | is_a | proposition,
                                      r | is_a | proposition,),
                                  inference_rule=pu.pls1.i3)
        assert theory.is_valid_statement(phi=(p | land | r) | is_a | proposition)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(q | land | r) | is_a | proposition,
                                  premises=(
                                      q | is_a | proposition,
                                      r | is_a | proposition,),
                                  inference_rule=pu.pls1.i3)
        assert theory.is_valid_statement(phi=(q | land | r) | is_a | proposition)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | implies | q) | is_a | proposition,
                                  premises=(
                                      p | is_a | proposition,
                                      q | is_a | proposition,),
                                  inference_rule=pu.pls1.i4)
        assert theory.is_valid_statement(phi=(p | implies | q) | is_a | proposition)
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=((p | land | r) | implies | (q | land | r)) | is_a | proposition,
                                  premises=(
                                      (p | land | r) | is_a | proposition,
                                      (q | land | r) | is_a | proposition,),
                                  inference_rule=pu.pls1.i4)
        assert theory.is_valid_statement(phi=((p | land | r) | implies | (q | land | r)) | is_a | proposition)

        # make (P implies Q) valid and add modus-ponens to the theory
        theory, _, = pu.as1.let_x_be_an_axiom(theory=theory, claim=p | implies | q)
        theory, _, = pu.as1.let_x_be_an_inference_rule(theory=theory, inference_rule=pu.ir1.modus_ponens_axiom)

        # Derive: (P ∧ R) implies (Q ∧ R)  from P by modus-ponens
        theory, _ = pu.as1.derive(theory=theory,
                                  claim=(p | land | r) | implies | (q | land | r),
                                  premises=(
                                      (p | implies | q) | is_a | proposition,
                                      ((p | land | r) | implies | (q | land | r)) | is_a | proposition,
                                      (p | implies | q) | implies | ((p | land | r) | implies | (q | land | r)),
                                      p | implies | q,),
                                  inference_rule=pu.ir1.modus_ponens_axiom)
        assert theory.is_valid_statement(phi=(p | land | r) | implies | (q | land | r))
        pass
