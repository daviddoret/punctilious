from unittest import TestCase
import punctilious as pu
import random_data


# TODO: Proof by contradiction: design test
class TestProofByContradiction1(TestCase):
    def test_proof_by_contradiction_2(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_inferred_statement = True
        # Prepare the universe of discourse
        u = pu.UniverseOfDiscourse()
        blah_blah_blah = random_data.random_sentence(min_words=3)
        a1 = u.declare_axiom(blah_blah_blah)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        # Elaborate the parent theory
        t1 = u.t()
        t1_a2 = t1.include_axiom(a=a1)
        t1_p1 = t1.i.axiom_interpretation.infer_statement(axiom=t1_a2, formula=(o1 | u.r.eq | o2))
        t1_p2 = t1.i.axiom_interpretation.infer_statement(axiom=t1_a2, formula=(o2 | u.r.eq | o3))
        with u.v('x') as x, u.v('y') as y, u.v('z') as z:
            t1_p3_implication = t1.i.axiom_interpretation.infer_statement(axiom=t1_a2,
                formula=((x | u.r.eq | y) | u.r.land | (y | u.r.eq | z)))
        t1.stabilize()
        hypothetical_formula = (o1 | u.r.neq | o3)
        t1_h1 = t1.pose_hypothesis(hypothesis_formula=hypothetical_formula)
        # TODO: The hypothetical-theory must be stabilized immediately,
        #   otherwise new axioms or definitions may be introduced,
        #   leading to inconsistent results from the perspective of the
        #   base theory.
        t2 = t1_h1.hypothesis_child_theory
        t2_a1 = t1_h1.hypothesis_statement_in_child_theory
        t2_p5 = t2.i.conjunction_introduction.infer_statement(p=t1_p1, q=t1_p2)
        t2_p6 = t2.i.variable_substitution.infer_statement(p=t1_p3_implication, phi=(o1, o2, o3))
        # p7: 𝑟₁(𝑜₁, 𝑜₃) by modus ponens
        t2_p7 = t2.i.modus_ponens.infer_statement(p_implies_q=t2_p6, p=t2_p5)
        # p7 is in contradiction with the hypothetical_formula
        t1_p8 = t1.i.inconsistency_by_negation_introduction.infer_statement(p=t2_a1, not_p=t2_p7,
            inconsistent_theory=t2)
        t1_p9 = t1.i.proof_by_contradiction_2.infer_statement(p_hypothesis=t1_h1,
            inc_hypothesis=t1_p8)
        pass
