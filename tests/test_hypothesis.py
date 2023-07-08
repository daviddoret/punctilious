from unittest import TestCase
import punctilious as pu
import random_data


class TestHypothesis(TestCase):
    def test_hypothesis(self):
        """Elaborate a first theory that is insufficient to prove P.
        Then, make an hypothesis with a new proposition to would prove P.
        Finally, prove P under that hypothesis."""
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.declare_axiom(blah_blah_blah)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        pu.configuration.echo_default = True
        robust_theory = u.t()
        ap1 = robust_theory.include_axiom(a=a1)
        first_proposition = robust_theory.i.axiom_interpretation.infer_statement(
            ap1, u.f(r1, o1, o2))
        with u.v() as x, u.v() as y, u.v() as z:
            conditional = robust_theory.i.axiom_interpretation.infer_statement(
                ap1,
                u.f(u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y),
                        u.f(r1, y, z)),
                    u.f(r1, x, z)))
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized,
                        'The stabilized property of the original-theory is not True.')
        hypothesis = robust_theory.pose_hypothesis(
            hypothetical_proposition=u.f(r1, o2, o3))
        hypothetical_proposition = hypothesis.proposition
        hypothetical_theory = hypothesis.hypothetical_t
        hypothetical_conjunction = hypothetical_theory.i.ci.infer_statement(first_proposition,
                                                                            hypothetical_proposition)
        proposition_1 = hypothetical_theory.i.vs.infer_statement(
            conditional,
            o1,  # x
            o2,  # y
            o3)  # z
        conclusion_1 = hypothetical_theory.i.mp.infer_statement(
            proposition_1,
            hypothetical_conjunction)
        self.assertEqual('𝑟₁(𝑜₂, 𝑜₄)',
                         conclusion_1.valid_proposition.rep_formula(pu.text_formats.unicode))
