from unittest import TestCase
import punctilious as pu
import random_data


# TODO: Proof by contradiction: design test
class TestProofByContradiction(TestCase):
    def test_proof_by_contradiction(self):
        pu.configuration.echo_default = True
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
        a2 = t1.include_axiom(a=a1)
        p1 = t1.i.axiom_interpretation.infer_statement(axiom=a2, formula=u.f(r1, o1, o2))
        p2 = t1.i.axiom_interpretation.infer_statement(axiom=a2, formula=u.f(r1, o2, o3))
        with u.v() as x, u.v() as y, u.v() as z:
            p3_implication = t1.i.axiom_interpretation.infer_statement(
                axiom=a2,
                formula=u.f(u.r.implies,
                            u.f(u.r.land, u.f(r1, x, y),
                                u.f(r1, y, z)),
                            u.f(r1, x, z)))
        t1.stabilize()
        hypothetical_formula = u.f(u.r.lnot, u.f(r1, o1, o3))
        # H1: ¬(𝑟₁(𝑜₁, 𝑜₃))
        hypothesis = t1.pose_hypothesis(hypothetical_proposition=hypothetical_formula)
        # TODO: The hypothetical-theory must be stabilized immediately,
        #   otherwise new axioms or definitions may be introduced,
        #   leading to inconsistent results from the perspective of the
        #   base theory.
        hypothetical_theory = hypothesis.hypothetical_theory
        p5 = hypothetical_theory.i.conjunction_introduction.infer_statement(p=p1, q=p2)
        p6 = hypothetical_theory.i.variable_substitution.infer_statement(p3_implication, o1, o2, o3)
        # p7: 𝑟₁(𝑜₁, 𝑜₃) by modus ponens
        p7 = hypothetical_theory.i.modus_ponens.infer_statement(p_implies_q=p6, p=p5)
        # p7 is in contradiction with the hypothetical_formula
        # hypothetical_theory.i.inconsistency_introduction(!!!!!)
