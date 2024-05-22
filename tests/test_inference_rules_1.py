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


class TestAdjunction:
    def test_adjunction(self, theory, a, b, c):
        # adapt the base theory
        a1 = pu.as1.let_x_be_an_axiom(claim=a)
        a2 = pu.as1.let_x_be_an_axiom(claim=b)
        theory = pu.as1.Derivation(theorems=(*theory, a1, a2,))

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=a | land | b,
                               premises=(
                                   a | is_a | proposition,
                                   b | is_a | proposition,
                                   a,
                                   b,),
                               inference_rule=pu.ir1.adjunction_axiom)
        assert theory.has_theorem(phi=a | land | b)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.as1.CustomException, match='e117'):
            # wrong theory
            pu.as1.derive(theory=theory,
                          claim=a | land | c,
                          premises=(
                              a | is_a | proposition,
                              c | is_a | proposition,
                              a | land | c,),
                          inference_rule=pu.ir1.adjunction_axiom)


class TestSimplification1:
    def test_simplification_1(self, theory, a, b, c):
        # adapt the base theory
        a1 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        theory = pu.as1.Derivation(theorems=(*theory, a1,))

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=a,
                               premises=(
                                   a | is_a | proposition,
                                   b | is_a | proposition,
                                   a | land | b,),
                               inference_rule=pu.ir1.simplification_1_axiom)
        assert theory.has_theorem(phi=a)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.as1.CustomException, match='e105'):
            # wrong theory
            pu.as1.derive(theory=theory,
                          claim=c,
                          premises=(
                              a | is_a | proposition,
                              c | is_a | proposition,
                              a | land | c,),
                          inference_rule=pu.ir1.simplification_1_axiom)


class TestSimplification2:
    def test_simplification_2(self, theory, a, b, c):
        # adapt the base theory
        a1 = pu.as1.let_x_be_an_axiom(claim=a | land | b)
        theory = pu.as1.Derivation(theorems=(*theory, a1,))

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=b,
                               premises=(
                                   a | is_a | proposition,
                                   b | is_a | proposition,
                                   a | land | b,),
                               inference_rule=pu.ir1.simplification_2_axiom)
        assert theory.has_theorem(phi=b)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.as1.CustomException, match='e108'):
            # wrong theory
            pu.as1.derive(theory=theory,
                          claim=c,
                          premises=(
                              a | is_a | proposition,
                              c | is_a | proposition,
                              a | land | c,),
                          inference_rule=pu.ir1.simplification_2_axiom)


class TestModusPonens:
    def test_modus_ponens(self, theory, a, b, c):
        # adapt the base theory
        a1 = pu.as1.let_x_be_an_axiom(claim=a | implies | b)
        a2 = pu.as1.let_x_be_an_axiom(claim=a)
        theory = pu.as1.Derivation(theorems=(*theory, a1, a2,))

        # derive a new theorem from the target inference-rule
        theory = pu.as1.derive(theory=theory,
                               claim=b,
                               premises=(
                                   a | is_a | proposition,
                                   b | is_a | proposition,
                                   a | implies | b,
                                   a),
                               inference_rule=pu.ir1.modus_ponens_axiom)
        assert theory.has_theorem(phi=b)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.as1.CustomException, match='e123'):
            # wrong theory
            pu.as1.derive(theory=theory,
                          claim=c,
                          premises=(
                              a | is_a | proposition,
                              c | is_a | proposition,
                              a | implies | c,
                              c),
                          inference_rule=pu.ir1.modus_ponens_rule)
