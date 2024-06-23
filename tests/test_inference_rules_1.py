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
    theory = pu.as1.Axiomatization(derivations=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, a1, a2, a3,))

    # derive: a is-a proposition
    theory, _, = pu.as1.derive_1(t=theory,
                                 conjecture=a | is_a | proposition,
                                 premises=(a | is_a | propositional_variable,),
                                 inference_rule=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=a | is_a | proposition, t=theory)

    # derive: b is-a proposition
    theory, _, = pu.as1.derive_1(t=theory,
                                 conjecture=b | is_a | proposition,
                                 premises=(b | is_a | propositional_variable,),
                                 inference_rule=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=b | is_a | proposition, t=theory)

    # derive: c is-a proposition
    theory, _, = pu.as1.derive_1(t=theory,
                                 conjecture=c | is_a | proposition,
                                 premises=(c | is_a | propositional_variable,),
                                 inference_rule=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=c | is_a | proposition, t=theory)

    return theory


class TestAdjunction:
    def test_adjunction(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     conjecture=a | land | b,
                                     premises=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a,
                                         b,),
                                     inference_rule=pu.ir1.adjunction_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=a | land | b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            conjecture=a | land | c,
                            premises=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            inference_rule=pu.ir1.adjunction_axiom)


class TestSimplification1:
    def test_simplification_1(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     conjecture=a,
                                     premises=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | land | b,),
                                     inference_rule=pu.ir1.simplification_1_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            conjecture=c,
                            premises=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            inference_rule=pu.ir1.simplification_1_axiom)


class TestSimplification2:
    def test_simplification_2(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     conjecture=b,
                                     premises=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | land | b,),
                                     inference_rule=pu.ir1.simplification_2_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e120'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            conjecture=c,
                            premises=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            inference_rule=pu.ir1.simplification_2_axiom)


class TestModusPonens:
    def test_modus_ponens(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a | implies | b)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     conjecture=b,
                                     premises=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | implies | b,
                                         a),
                                     inference_rule=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=b, t=theory)

        # extend the theory to perform a second test
        # using a single propositional-variable
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=a | implies | (a | land | a))
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, valid_statement=(a | land | a) | is_a | proposition)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     conjecture=a | land | a,
                                     premises=(
                                         a | is_a | proposition,
                                         (a | land | a) | is_a | proposition,
                                         a | implies | (a | land | a),
                                         a),
                                     inference_rule=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=a | land | a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.as1.CustomException, match='e123'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            conjecture=c,
                            premises=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | implies | c,
                                c),
                            inference_rule=pu.ir1.modus_ponens_rule)
