import pytest
import punctilious as pu
from punctilious.connectives_standard_library_1 import *


@pytest.fixture
def f1():
    t = pu.as1.WellFormedTheory()
    t = pu.ir1.extend_theory_with_inference_rules_1(t=t)
    t = pu.pls1.extend_theory_with_propositional_logic_syntax_1(t=t)
    t, a = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='A')
    t, b = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='B')
    t, c = pu.pls1.let_x_be_a_propositional_variable(t=t, formula_ts='C')

    # derive:(a is-a proposition)
    t, _, _ = pu.as1.derive_1(t=t,
                              c=is_a_proposition(a),
                              p=(is_a_propositional_variable(a),),
                              i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_so_far_1(p=is_a_proposition(a), t=t)

    # derive: (b is-a proposition)
    t, _, _ = pu.as1.derive_1(t=t,
                              c=is_a_proposition(b),
                              p=(is_a_propositional_variable(b),),
                              i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_so_far_1(p=is_a_proposition(b), t=t)

    # derive: (c is-a proposition)
    t, _, _ = pu.as1.derive_1(t=t,
                              c=is_a_proposition(c),
                              p=(is_a_propositional_variable(c),),
                              i=pu.pls1.i1, raise_error_if_false=True)
    assert pu.as1.is_valid_proposition_so_far_1(p=is_a_proposition(c), t=t)

    return t, a, b, c


class TestAdjunction:
    def test_adjunction(self, f1):
        t, a, b, c = f1
        # adapt the base theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=b)

        # derive a new theorem from the target inference-rule
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=a | land | b,
                                  p=(
                                      is_a_proposition(a),
                                      is_a_proposition(b),
                                      a,
                                      b,),
                                  i=pu.ir1.conjunction_introduction, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=a | land | b, t=t)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=t,
                            c=a | land | c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.conjunction_introduction, raise_error_if_false=True)


class TestSimplification1:
    def test_simplification_1(self, f1):
        t, a, b, c = f1

        # adapt the base theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a | land | b)

        # derive a new theorem from the target inference-rule
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=a,
                                  p=(
                                      is_a_proposition(a),
                                      is_a_proposition(b),
                                      a | land | b,),
                                  i=pu.ir1.simplification_1_axiom, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=a, t=t)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e105'):
            # wrong theory
            pu.as1.derive_1(t=t,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.simplification_1_axiom, raise_error_if_false=True)


class TestSimplification2:
    def test_simplification_2(self, f1):
        t, a, b, c = f1
        # adapt the base theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a | land | b)

        # derive a new theorem from the target inference-rule
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=b,
                                  p=(
                                      is_a_proposition(a),
                                      is_a_proposition(b),
                                      a | land | b,),
                                  i=pu.ir1.simplification_2_axiom, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=b, t=t)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(Exception):  # , match='e120'):
            # wrong theory
            pu.as1.derive_1(t=t,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | land | c,),
                            i=pu.ir1.simplification_2_axiom, raise_error_if_false=True)


class TestModusPonens:
    def test_modus_ponens(self, f1):
        t, a, b, c = f1
        # adapt the base theory
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a | implies | b)
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a)

        # derive a new theorem from the target inference-rule
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=b,
                                  p=(
                                      is_a_proposition(a),
                                      is_a_proposition(b),
                                      a | implies | b,
                                      a),
                                  i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=b, t=t)

        # extend the theory to perform a second test
        # using a single propositional-variable
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=a | implies | (a | land | a))
        t, _, = pu.as1.let_x_be_an_axiom(t=t, s=is_a_proposition(a | land | a))

        # derive a new theorem from the target inference-rule
        t, _, _ = pu.as1.derive_1(t=t,
                                  c=a | land | a,
                                  p=(
                                      is_a_proposition(a),
                                      is_a_proposition(a | land | a),
                                      a | implies | (a | land | a),
                                      a),
                                  i=pu.ir1.modus_ponens, raise_error_if_false=True)
        assert pu.as1.is_valid_proposition_so_far_1(p=a | land | a, t=t)

        # show that wrong premises fail to derive a theorem
        with pytest.raises(pu.u1.ApplicativeError, match=pu.c1.ERROR_CODE_AS1_041):
            # wrong theory
            pu.as1.derive_1(t=t,
                            c=c,
                            p=(
                                is_a_proposition(a),
                                is_a_proposition(c),
                                a | implies | c,
                                c),
                            i=pu.ir1.modus_ponens.transformation, raise_error_if_false=True)
