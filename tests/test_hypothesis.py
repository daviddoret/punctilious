from unittest import TestCase
import punctilious as p
import random_data


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        echo_hypothesis = p.configuration.echo_hypothesis
        p.configuration.echo_default = True
        u = p.UniverseOfDiscourse('original-theory')
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.axiom(blah_blah_blah)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r(2, signal_proposition=True)
        robust_theory = u.t()
        ap1 = robust_theory.postulate_axiom(a=a1)
        robust_theory.dai(valid_proposition=u.f(r1, o1, o2), ap=ap1)
        h = robust_theory.pose_hypothesis(hypothetical_proposition=u.f(r1, o2, o3))
        p.configuration.echo_hypothesis = echo_hypothesis
