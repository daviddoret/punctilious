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
    a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
    a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
    a3 = pu.as1.let_x_be_an_axiom(claim=c | is_a | propositional_variable)
    theory = pu.as1.Axiomatization(axioms=(*pu.ir1.axioms, *pu.pls1.axioms, a1, a2, a3,))

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

    return theory


class TestPL1:
    def test_pl1(self, theory, a, b, c):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        assert theory.has_theorem(phi=a | is_a | proposition)
        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=a | implies | (a | land | a),
                               premises=(
                                   a | is_a | proposition,),
                               inference_rule=pu.ml1.pl01)
        assert theory.has_theorem(phi=a | implies | (a | land | a))

        # adapt the base theory
        a1 = pu.as1.let_x_be_an_axiom(claim=a)
        theory = pu.as1.Derivation(theorems=(*theory, a1,))


class TestPL2:
    def test_pl2(self):
        # PL2. (𝐴 ∧ 𝐵) ⊃ (𝐵 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land

        # elaborate a theory
        a, b = pu.as1.let_x_be_a_propositional_variable(rep=('A', 'B',))
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim, a3.claim,),
            transformation_rule=pu.ml1.pl02.transformation)
        isolated_theorem = pu.as1.TheoremByInference(claim=b | land | a, i=inference)
        assert pu.as1.is_formula_equivalent(phi=b | land | a, psi=isolated_theorem.claim)

        # extend the original theory with that new theorem
        extended_theory = pu.as1.Derivation(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=b | land | a)

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2,))
            pu.as1.Derivation(theorems=(*incomplete_axioms, isolated_theorem))


class TestPL3:
    def test_pl3(self):
        # PL3. (𝐴 ⊃ 𝐵) ⊃ [(𝐴 ∧ 𝐶) ⊃ (𝐵 ∧ 𝐶)]

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        implies = pu.as1.connectives.implies

        # elaborate a theory
        a, b, c = pu.as1.let_x_be_a_propositional_variable(rep=('A', 'B', 'C',))
        a1 = pu.as1.let_x_be_an_axiom(claim=a | is_a | propositional_variable)
        a2 = pu.as1.let_x_be_an_axiom(claim=b | is_a | propositional_variable)
        a3 = pu.as1.let_x_be_an_axiom(claim=c | is_a | propositional_variable)
        a4 = pu.as1.let_x_be_an_axiom(claim=a | implies | b)
        axioms = pu.as1.Axiomatization(axioms=(*pu.ml1.axioms, a1, a2, a3, a4,))

        # derive a new theorem
        inference = pu.as1.Inference(
            premises=(a1.claim, a2.claim, a3.claim, a4.claim,),
            transformation_rule=pu.ml1.pl03.transformation)
        isolated_theorem = pu.as1.TheoremByInference(claim=(a | land | c) | implies | (b | land | c), i=inference)
        assert pu.as1.is_formula_equivalent(phi=(a | land | c) | implies | (b | land | c), psi=isolated_theorem.claim)

        # extend the original theory with that new theorem
        extended_theory = pu.as1.Derivation(theorems=(*axioms, isolated_theorem,))
        assert extended_theory.has_theorem(phi=(a | land | c) | implies | (b | land | c))

        # show that wrong axiomatization fails to derive the theorems
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            incomplete_axioms = pu.as1.Axiomatization(axioms=(
                *pu.ir1.axioms, a1, a2, a3,))
            pu.as1.Derivation(theorems=(*incomplete_axioms, isolated_theorem))

        pass
