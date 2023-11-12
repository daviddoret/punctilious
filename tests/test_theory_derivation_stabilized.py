from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestTheoryElaboration(TestCase):
    def test_theory_elaboration_stabilized(self):
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        blah_blah_blah = random_data.random_sentence(min_words=8)
        a1 = u.a.declare(blah_blah_blah)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(2, signal_proposition=True)
        pu.configuration.echo_default = True
        robust_theory = u.declare_theory()
        ap1 = robust_theory.include_axiom(a=a1)
        with u.with_variable() as x, u.with_variable() as y, u.with_variable() as z:
            implication = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
                p=u.declare_compound_formula(u.c1.implies,
                    u.declare_compound_formula(u.c1.land, u.declare_compound_formula(r1, x, y),
                        u.declare_compound_formula(r1, y, z)), u.declare_compound_formula(r1, x, z)), lock=False)
        r1o1o2 = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
            p=u.declare_compound_formula(r1, o1, o2), lock=False)
        r1o2o3 = robust_theory.i.axiom_interpretation.infer_formula_statement(a=ap1,
            p=u.declare_compound_formula(r1, o2, o3), lock=True)
        r1o1o2_and_r1o2o3 = robust_theory.i.ci.infer_formula_statement(r1o1o2, r1o2o3)
        implication_2 = robust_theory.i.variable_substitution.infer_formula_statement(p=implication,
            phi=u.c1.tupl(o1, o2, o3))
        robust_theory.i.mp.infer_formula_statement(p_implies_q=implication_2, p=r1o1o2_and_r1o2o3)
        robust_theory.stabilize()
        self.assertTrue(robust_theory.stabilized, 'The stabilized property of the original-theory is not True.')

        hypothesis = robust_theory.pose_hypothesis(hypothesis_formula=u.declare_compound_formula(r1, o2, o3))
        hypothesis_theory = hypothesis.hypothesis_child_theory
