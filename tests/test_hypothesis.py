from unittest import TestCase
import punctilious as p
import random_data


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        p.configuration.echo_default = False
        u = p.UniverseOfDiscourse('original-theory')
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.axiom(blah_blah_blah)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r(2, signal_proposition=True)
        p.configuration.echo_default = True
        robust_theory = u.t(include_conjunction_introduction_inference_rule=True)
        robust_theory.modus_ponens_inference_rule = p.ModusPonensInferenceRule
        ap1 = robust_theory.postulate_axiom(a=a1)
        robust_theory.dai(
            valid_proposition=u.f(r1, o1, o2), ap=ap1)
        with u.v() as x, u.v() as y, u.v() as z:
            robust_theory.dai(
                valid_proposition=
                u.f(u.implies,
                    u.f(u.conjunction_relation, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap1)
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized, 'The stabilized property of the original-theory is not True.')

        hypothesis = robust_theory.pose_hypothesis(
            hypothetical_proposition=u.f(r1, o2, o3))
        hypothesis_theory = hypothesis.hypothetical_t
