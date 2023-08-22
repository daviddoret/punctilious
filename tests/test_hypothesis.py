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
        robust_theory = u.t()
        ap1 = robust_theory.include_axiom(a=a1)
        robust_theory.i.axiom_interpretation.infer_statement(axiom=ap1, formula=(o1 | r1 | o2))
        with u.v() as x, u.v() as y, u.v() as z:
            conditional = robust_theory.i.axiom_interpretation.infer_statement(axiom=ap1,
                formula=(((x | r1 | y) | u.r.land | (y | r1 | z)) | u.r.implies | (x | r1 | z)))
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized,
            'The stabilized property of the original-theory is not True.')
        hypothesis = robust_theory.pose_hypothesis(hypothesis_formula=(o2 | r1 | o3))
        hypothetical_proposition = hypothesis._hypothesis_statement_in_child_theory
        hypothetical_theory = hypothesis.hypothesis_child_theory
        hypothetical_conjunction = hypothetical_theory.i.ci.infer_statement((o1 | r1 | o2),
            hypothetical_proposition)
        proposition_1 = hypothetical_theory.i.vs.infer_statement(conditional, o1,  # x
            o2,  # y
            o3)  # z
        conclusion_1 = hypothetical_theory.i.mp.infer_statement(proposition_1,
            hypothetical_conjunction)
        self.assertEqual('𝑟₁(𝑜₁, 𝑜₃)',
            conclusion_1.valid_proposition.rep_formula(pu.encodings.unicode))
