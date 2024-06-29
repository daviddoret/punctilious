import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


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
    a1 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=a | is_a | propositional_variable)
    a2 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=b | is_a | propositional_variable)
    a3 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=c | is_a | propositional_variable)
    theory = pu.as1.Axiomatization(derivations=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, a1, a2, a3,))

    # derive:(a is-a proposition)
    theory, _, = pu.as1.derive_1(t=theory,
                                 c=a | is_a | proposition,
                                 p=(a | is_a | propositional_variable,),
                                 i=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=a | is_a | proposition, t=theory)

    # derive: (b is-a proposition)
    theory, _, = pu.as1.derive_1(t=theory,
                                 c=b | is_a | proposition,
                                 p=(b | is_a | propositional_variable,),
                                 i=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=b | is_a | proposition, t=theory)

    # derive: (c is-a proposition)
    theory, _, = pu.as1.derive_1(t=theory,
                                 c=c | is_a | proposition,
                                 p=(c | is_a | propositional_variable,),
                                 i=pu.pls1.i1)
    assert pu.as1.is_valid_statement_in_theory(phi=c | is_a | proposition, t=theory)

    return theory


class TestAdjunction:
    def test_adjunction(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=a | land | b,
                                     p=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a,
                                         b,),
                                     i=pu.ir1.conjunction_introduction)
        assert pu.as1.is_valid_statement_in_theory(phi=a | land | b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=a | land | c,
                            p=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            i=pu.ir1.conjunction_introduction)


class TestSimplification1:
    def test_simplification_1(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=a,
                                     p=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | land | b,),
                                     i=pu.ir1.simplification_1_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            i=pu.ir1.simplification_1_axiom)


class TestSimplification2:
    def test_simplification_2(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=b,
                                     p=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | land | b,),
                                     i=pu.ir1.simplification_2_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e120'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | land | c,),
                            i=pu.ir1.simplification_2_axiom)


class TestModusPonens:
    def test_modus_ponens(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | implies | b)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=b,
                                     p=(
                                         a | is_a | proposition,
                                         b | is_a | proposition,
                                         a | implies | b,
                                         a),
                                     i=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=b, t=theory)

        # extend the theory to perform a second test
        # using a single propositional-variable
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | implies | (a | land | a))
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=(a | land | a) | is_a | proposition)

        # derive a new theorem from the target inference-rule
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=a | land | a,
                                     p=(
                                         a | is_a | proposition,
                                         (a | land | a) | is_a | proposition,
                                         a | implies | (a | land | a),
                                         a),
                                     i=pu.ir1.modus_ponens_axiom)
        assert pu.as1.is_valid_statement_in_theory(phi=a | land | a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.u1.ApplicativeException, match=pu.as1.ERROR_CODE_AS1_041):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                a | is_a | proposition,
                                c | is_a | proposition,
                                a | implies | c,
                                c),
                            i=pu.ir1.modus_ponens_rule)
