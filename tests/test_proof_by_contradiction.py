from unittest import TestCase
import punctilious as pu
import random_data


# TODO: Proof by contradiction: design test
class TestProofByContradiction(TestCase):
    def test_proof_by_contradiction(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.declare_axiom(blah_blah_blah)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t1 = u.t()
        a2 = t1.include_axiom(a=a1)
        p1 = t1.i.axiom_interpretation.infer_statement(a2, u.f(r1, o1, o2))
        p2 = t1.i.axiom_interpretation.infer_statement(a2, u.f(r1, o2, o3))
        with u.v() as x, u.v() as y, u.v() as z:
            p3 = t1.i.axiom_interpretation.infer_statement(
                a2,
                u.f(u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y),
                        u.f(r1, y, z)),
                    u.f(r1, x, z)))
        t1.stabilize()
        h = u.f(u.r.lnot, u.f(r1, o1, o3))
        t2 = t1.pose_hypothesis(hypothetical_proposition=h)
        p4_hypothesis = t2._hypothetical_proposition
        hypothetical_theory = t2.hypothetical_theory
        hypothetical_conjunction = hypothetical_theory.i.ci.infer_statement(p1, p4_hypothesis)
        proposition_1 = hypothetical_theory.i.vs.infer_statement(
            p3,
            o1,  # x
            o2,  # y
            o3)  # z
        conclusion_1 = hypothetical_theory.i.mp.infer_statement(
            proposition_1,
            hypothetical_conjunction)
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₃)',
                         conclusion_1.valid_proposition.rep_formula(pu.encodings.unicode))
