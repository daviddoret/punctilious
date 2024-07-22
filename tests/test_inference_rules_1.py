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
    a1 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(a))
    a2 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(b))
    a3 = pu.as1.let_x_be_an_axiom_DEPRECATED(s=is_a_propositional_variable(c))
    theory = pu.as1.Axiomatization(d=(*pu.ir1.axiomatization, *pu.pls1.axiomatization, a1, a2, a3,))

    # derive:(a is-a proposition)
    theory, _, _ = pu.as1.derive_1(t=theory,
                                   c=is_a_proposition(a),
                                   p=(is_a_propositional_variable(a),),
                                   i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_in_theory_1(p=is_a_proposition(a), t=theory)

    # derive: (b is-a proposition)
    theory, _, _ = pu.as1.derive_1(t=theory,
                                   c=is_a_proposition(b),
                                   p=(is_a_propositional_variable(b),),
                                   i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_in_theory_1(p=is_a_proposition(b), t=theory)

    # derive: (c is-a proposition)
    theory, _, _ = pu.as1.derive_1(t=theory,
                                   c=is_a_proposition(c),
                                   p=(is_a_propositional_variable(c),),
                                   i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_in_theory_1(p=is_a_proposition(c), t=theory)

    return theory


class TestAdjunction:
    def test_adjunction(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=b)

        # derive a new theorem from the target inference-rule
        theory, _, _ = pu.as1.derive_1(t=theory,
                                       c=a | land | b,
                                       p=(
                                           is_a_proposition(a),
                                           is_a_proposition(b),
                                           a,
                                           b,),
                                       i=pu.ir1.conjunction_introduction, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_in_theory_1(p=a | land | b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=a | land | c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.conjunction_introduction, raise_error_if_false=True)


class TestSimplification1:
    def test_simplification_1(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, _ = pu.as1.derive_1(t=theory,
                                       c=a,
                                       p=(
                                           is_a_proposition(a),
                                           is_a_proposition(b),
                                           a | land | b,),
                                       i=pu.ir1.simplification_1_axiom, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_in_theory_1(p=a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.simplification_1_axiom, raise_error_if_false=True)


class TestSimplification2:
    def test_simplification_2(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | land | b)

        # derive a new theorem from the target inference-rule
        theory, _, _ = pu.as1.derive_1(t=theory,
                                       c=b,
                                       p=(
                                           is_a_proposition(a),
                                           is_a_proposition(b),
                                           a | land | b,),
                                       i=pu.ir1.simplification_2_axiom, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_in_theory_1(p=b, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e120'):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.simplification_2_axiom, raise_error_if_false=True)


class TestModusPonens:
    def test_modus_ponens(self, theory, a, b, c):
        # adapt the base theory
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | implies | b)
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a)

        # derive a new theorem from the target inference-rule
        theory, _, _ = pu.as1.derive_1(t=theory,
                                       c=b,
                                       p=(
                                           is_a_proposition(a),
                                           is_a_proposition(b),
                                           a | implies | b,
                                           a),
                                       i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_in_theory_1(p=b, t=theory)

        # extend the theory to perform a second test
        # using a single propositional-variable
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=a | implies | (a | land | a))
        theory, _, = pu.as1.let_x_be_an_axiom(t=theory, s=is_a_proposition(a | land | a))

        # derive a new theorem from the target inference-rule
        theory, _, _ = pu.as1.derive_1(t=theory,
                                       c=a | land | a,
                                       p=(
                                           is_a_proposition(a),
                                           is_a_proposition(a | land | a),
                                           a | implies | (a | land | a),
                                           a),
                                       i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_in_theory_1(p=a | land | a, t=theory)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_041):
            # wrong theory
            pu.as1.derive_1(t=theory,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | implies | c,
                                c),
                            i=pu.ir1.modus_ponens.transformation, raise_error_if_false=True)
