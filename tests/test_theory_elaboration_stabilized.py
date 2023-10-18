from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestTheoryElaboration(TestCase):
    def test_theory_elaboration_stabilized(self):
        pu.configuration.echo_default = False
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
        with u.v() as x, u.v() as y, u.v() as z:
            implication = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
                p=u.f(u.r.implies, u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)), u.f(r1, x, z)),
                lock=False)
        r1o1o2 = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
            p=u.f(r1, o1, o2), lock=False)
        r1o2o3 = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
            p=u.f(r1, o2, o3), lock=True)
        r1o1o2_and_r1o2o3 = robust_theory.i.ci.infer_formula_statement(r1o1o2, r1o2o3)
        implication_2 = robust_theory.i.variable_substitution.infer_formula_statement(p=implication,
            phi=u.r.tupl(o1, o2, o3))
        robust_theory.i.mp.infer_formula_statement(p_implies_q=implication_2, p=r1o1o2_and_r1o2o3)
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized,
            'The stabilized property of the original-theory is not True.')

        hypothesis = robust_theory.pose_hypothesis(hypothesis_formula=u.f(r1, o2, o3))
        hypothesis_theory = hypothesis.hypothesis_child_theory
