from unittest import TestCase
import punctilious as p
import random_data


class TestTheoryElaboration(TestCase):
    def test_theory_elaboration_stabilized(self):
        p.configuration.echo_default = False
        u = p.UniverseOfDiscourse('original-theory')
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.axiom(blah_blah_blah)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        p.configuration.echo_default = True
        robust_theory = u.t()
        ap1 = robust_theory.postulate_axiom(a=a1)
        with u.v() as x, u.v() as y, u.v() as z:
            implication = robust_theory.dai(
                valid_proposition=
                u.f(u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap1)
        r1o1o2 = robust_theory.dai(
            valid_proposition=u.f(r1, o1, o2), ap=ap1)
        r1o2o3 = robust_theory.dai(
            valid_proposition=u.f(r1, o2, o3), ap=ap1)
        r1o1o2_and_r1o2o3 = robust_theory.i.ci.infer_statement(
            r1o1o2,
            r1o2o3)
        robust_theory.i.mp.infer_statement(
            implication,
            r1o1o2_and_r1o2o3)
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized, 'The stabilized property of the original-theory is not True.')

        hypothesis = robust_theory.pose_hypothesis(
            hypothetical_proposition=u.f(r1, o2, o3))
        hypothesis_theory = hypothesis.hypothetical_t
