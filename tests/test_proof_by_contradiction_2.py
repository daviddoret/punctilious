from unittest import TestCase
import punctilious as pu
import random_data


# TODO: Proof by contradiction: design test
class TestProofByContradiction1(TestCase):
    def test_proof_by_contradiction_2(self):
        # Configuration
        pu.configuration.echo_default = False
        pu.configuration.echo_inferred_statement = True
        # Prepare the universe of discourse
        u = pu.UniverseOfDiscourse()
        dummy_axiom = u.declare_axiom('Dummy axiom for the sake of testing.')
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        # Elaborate the parent theory
        t = u.t()
        theory_axiom = t.include_axiom(a=dummy_axiom)
        t.i.axiom_interpretation.infer_statement(axiom=theory_axiom, formula=(o1 | u.r.eq | o2))
        t.i.axiom_interpretation.infer_statement(axiom=theory_axiom, formula=(o2 | u.r.eq | o3))
        with u.v('x') as x, u.v('y') as y, u.v('z') as z:
            implication_axiom = t.i.axiom_interpretation.infer_statement(axiom=theory_axiom,
                formula=(((x | u.r.eq | y) | u.r.land | (y | u.r.eq | z)) | u.r.implies | (
                        x | u.r.eq | z)))
        t.stabilize()
        hypothetical_formula = (o1 | u.r.neq | o3)
        h = t.pose_hypothesis(hypothesis_formula=hypothetical_formula)
        p_ci = h.child_theory.i.conjunction_introduction.infer_statement(p=(o1 | u.r.eq | o2),
            q=(o2 | u.r.eq | o3))
        p_vs = h.child_theory.i.variable_substitution.infer_statement(p=implication_axiom,
            phi=(o1, o2, o3))
        p_mp = h.child_theory.i.modus_ponens.infer_statement(p_implies_q=p_vs, p=p_ci)
        # Eureka: the previous proposition is in contradiction with the hypothetical_formula,
        # we may now infer the inconsistency of the hypothesis:
        t1_p8 = t.i.inconsistency_introduction_1.infer_statement(p=h.child_statement, not_p=p_mp,
            inconsistent_theory=h.child_theory)
        # and because the hypothesis is inconsistent,
        # we may complete the proof by contradiction:
        t.i.proof_by_contradiction_2.infer_statement(p_neq_q_hypothesis=h, inc_hypothesis=t1_p8)
        pass
