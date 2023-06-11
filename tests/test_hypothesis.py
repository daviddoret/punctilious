from unittest import TestCase
import punctilious as p
import random_data


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        """Elaborate a first theory that is insufficient to prove P.
        Then, make an hypothesis with a new proposition to would prove P.
        Finally, prove P under that hypothesis."""
        p.configuration.echo_default = False
        u = p.UniverseOfDiscourse('test-hypothesis-universe-of-discourse')
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.axiom(blah_blah_blah)
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r(2, signal_proposition=True)
        p.configuration.echo_default = True
        robust_theory = u.t(
            include_conjunction_introduction_inference_rule=True,
            include_modus_ponens_inference_rule=True)
        ap1 = robust_theory.postulate_axiom(a=a1)
        first_proposition = robust_theory.dai(
            valid_proposition=u.f(r1, o1, o2), ap=ap1)
        with u.v() as x, u.v() as y, u.v() as z:
            conditional = robust_theory.dai(
                valid_proposition=
                u.f(u.implies,
                    u.f(u.conjunction_relation, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap1)
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized, 'The stabilized property of the original-theory is not True.')
        hypothesis = robust_theory.pose_hypothesis(
            hypothetical_proposition=u.f(r1, o2, o3))
        hypothetical_proposition = hypothesis.proposition
        hypothetical_theory = hypothesis.hypothetical_t
        hypothetical_conjunction = hypothetical_theory.ci(first_proposition, hypothetical_proposition)
        conclusion_1 = hypothetical_theory.infer_by_modus_ponens(
            conditional=conditional,
            antecedent=hypothetical_conjunction)
        self.assertEqual('◆(ℴ₁, ℴ₃)', conclusion_1.valid_proposition.repr_as_formula())
