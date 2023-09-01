from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction1(TestCase):
    def test_inconsistency_introduction_1(self):
        import sample.code.inconsistency_introduction_1 as test
        u: pu.UniverseOfDiscourse = test.u
        t1: pu.TheoryElaborationSequence = test.t1
        inc_proof: pu.InferredStatement = test.inc_proof
        self.assertIs(pu.consistency_values.proved_inconsistent, t1.consistency)
        self.assertTrue(inc_proof.is_formula_syntactically_equivalent_to(u.r.inc(t1)))
        self.assertEqual('𝐼𝑛𝑐(𝒯₁)', inc_proof.rep_formula(encoding=pu.encodings.unicode))

    def test_inconsistency_introduction_1_with_hypothesis(self):
        """Inconsistency introduction in a hypothesis"""
        pu.configuration.echo_default = True
        # Prepare the universe of discourse
        u = pu.UniverseOfDiscourse()
        axiom = u.declare_axiom(natural_language='Dummy axiom for testing purposes')
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        # Elaborate the parent theory
        t1 = u.t()
        axiom_theory = t1.include_axiom(a=axiom)
        t1_p1 = t1.i.axiom_interpretation.infer_statement(axiom=axiom_theory, formula=r1(o1, o2))
        t1_p2 = t1.i.axiom_interpretation.infer_statement(axiom=axiom_theory, formula=r1(o2, o3))
        with u.v() as x, u.v() as y, u.v() as z:
            t1_p3_implication = t1.i.axiom_interpretation.infer_statement(axiom=axiom_theory,
                formula=((r1(x, y) | u.r.land | r1(y, z)) | u.r.implies | r1(x, z)))
        t1.stabilize()
        hypothetical_formula = u.f(u.r.lnot, u.f(r1, o1, o3))
        # H1: ¬(𝑟₁(𝑜₁, 𝑜₃))
        t1_h1 = t1.pose_hypothesis(hypothesis_formula=hypothetical_formula)
        t2 = t1_h1.hypothesis_child_theory
        t2_p5 = t1_h1.hypothesis_statement_in_child_theory
        t2_p6 = t2.i.conjunction_introduction.infer_statement(p=t1_p1, q=t1_p2)
        t2_p7 = t2.i.variable_substitution.infer_statement(p=t1_p3_implication, phi=(o1, o2, o3))
        # t2_p8: 𝑟₁(𝑜₁, 𝑜₃) by modus ponens
        t2_p8 = t2.i.modus_ponens.infer_statement(p_implies_q=t2_p7, p=t2_p6)
        # p5 is the negation of p8, which is a contradiction in t2
        p9 = t1.i.inconsistency_introduction_1.infer_statement(p=t2_p8, not_p=t2_p5,
            inconsistent_theory=t2)