import pytest
import punctilious as pu

is_a = pu.axiomatic_system_1.connectives.is_a
proposition = pu.axiomatic_system_1.connectives.proposition
land = pu.axiomatic_system_1.connectives.land
implies = pu.axiomatic_system_1.connectives.implies
lor = pu.axiomatic_system_1.connectives.lor
lnot = pu.axiomatic_system_1.connectives.lnot


class TestHeuristic:
    def test_heuristic_basic(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='P')
        assert not pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=t)
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=p | is_a | proposition, t=t)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=t)
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Q')
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | land | q) | is_a | proposition, t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | implies | q) | is_a | proposition, t=t)
        assert success
        t, success = pu.as1.auto_derive_with_heuristics(conjecture=(p | lor | q) | is_a | proposition, t=t)
        assert success

    def test_heuristic_complex(self):
        t = pu.pls1.let_x_be_a_propositional_logic_syntax_1_theory()
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='P')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Q')
        t, success = pu.as1.auto_derive_with_heuristics(
            conjecture=((q | lor | q) | implies | (
                    (p | land | p) | land | (p | lor | (q | implies | lnot(q))))) | is_a | proposition, t=t)
        assert success


class TestAxioms:
    def test_pl1(self):
        # PL1. 𝐴 ⊃ (𝐴 ∧ 𝐴)

        # retrieve some basic vocabulary
        is_a = pu.as1.connectives.is_a
        proposition = pu.as1.connectives.proposition
        propositional_variable = pu.as1.connectives.propositional_variable
        land = pu.as1.connectives.land
        lnot = pu.as1.connectives.lnot
        lor = pu.as1.connectives.lor
        implies = pu.as1.connectives.implies

        # elaborate a theory
        theory, p = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')

        # derive: p is-a proposition
        theory, _, = pu.as1.derive_1(t=theory,
                                     c=p | is_a | proposition,
                                     p=(
                                         p | is_a | propositional_variable,),
                                     i=pu.pls1.i1)
        assert pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=theory)

        # derive: add i2: A is-a proposition ⊃ ¬A is a proposition
        # note that it is not necessary that either A or ¬A be valid
        theory = pu.as1.extend_theory(pu.pls1.i2, t=theory)
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition,),
            transformation_rule=pu.pls1.i2.transformation)
        claim = lnot(p) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=lnot(p) | is_a | proposition, psi=isolated_theorem.valid_statement)
        theory = pu.as1.extend_theory(isolated_theorem, t=theory)

        assert pu.as1.is_valid_statement_in_theory(phi=lnot(p) | is_a | proposition, t=theory)

        # declare 1 as a propositional-variable
        theory, q = pu.pls1.let_x_be_a_propositional_variable(t=theory, rep='Q')
        a2 = pu.as1.Axiom(valid_statement=q | is_a | propositional_variable)
        theory = pu.as1.extend_theory(a2, t=theory)

        # derive q is-a proposition
        inference = pu.as1.Inference(
            premises=(a2.valid_statement,),
            transformation_rule=pu.pls1.i1.transformation)
        claim = q | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        theory = pu.as1.extend_theory(isolated_theorem, t=theory)

        # add i3: (A is-a proposition, B is-a proposition) ⊃ ((A ∧ B) is a proposition)
        theory = pu.as1.extend_theory(pu.pls1.i3, t=theory)
        inference = pu.as1.Inference(
            premises=(p | is_a | proposition, q | is_a | proposition,),
            transformation_rule=pu.pls1.i3.transformation)
        claim = (p | land | q) | is_a | proposition
        isolated_theorem = pu.as1.Theorem(valid_statement=claim, i=inference)
        assert pu.as1.is_formula_equivalent(phi=claim, psi=isolated_theorem.valid_statement)
        theory = pu.as1.extend_theory(isolated_theorem, t=theory)
        assert pu.as1.is_valid_statement_in_theory(phi=claim, t=theory)

        pass

    def test_pl1_2(self):
        is_a = pu.as1.connectives.is_a
        proposition = pu.as1.connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='P')
        t, success, _, = pu.as1.auto_derive_2(t=t, conjecture=p | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=t)

    def test_pl1_3(self):
        is_a = pu.as1.connectives.is_a
        land = pu.as1.connectives.land
        proposition = pu.as1.connectives.proposition
        t, p = pu.pls1.let_x_be_a_propositional_variable(t=None, rep='X')
        t, q = pu.pls1.let_x_be_a_propositional_variable(t=t, rep='Y')
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=p | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=p | is_a | proposition, t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=q | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=q | is_a | proposition, t=t)
        t, success, _ = pu.as1.auto_derive_2(t=t, conjecture=(p | land | q) | is_a | proposition)
        assert success
        assert pu.as1.is_valid_statement_in_theory(phi=(p | land | q) | is_a | proposition, t=t)
        pass
