from unittest import TestCase

import punctilious as pu
import random_data


class TestInconsistencyIntroduction(TestCase):
    def test_inconsistency_introduction(self):
        """Simple inconsistency introduction"""
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        t1 = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t1.include_axiom(a)
        p = t1.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2))
        not_p = t1.i.axiom_interpretation.infer_statement(ap, u.f(u.r.lnot, u.f(r1, o1, o2)))
        t2 = u.t()
        inc = t2.i.inconsistency_introduction.infer_statement(inc_p=p, p=not_p)
        self.assertEqual('𝐼𝑛𝑐(𝒯₁)', inc.rep_formula(encoding=pu.encodings.unicode))
        self.assertIs(pu.consistency_values.proved_inconsistent, t1.consistency)

    def test_inconsistency_introduction_2(self):
        """Inconsistency introduction in a hypothesis"""
        pu.configuration.echo_default = True
        # Prepare the universe of discourse
        u = pu.UniverseOfDiscourse()
        blah_blah_blah = random_data.random_sentence(min_words=3)
        a1 = u.declare_axiom(blah_blah_blah)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        # Elaborate the parent theory
        t1 = u.t()
        t1_a2 = t1.include_axiom(a=a1)
        t1_p1 = t1.i.axiom_interpretation.infer_statement(axiom=t1_a2, formula=u.f(r1, o1, o2))
        t1_p2 = t1.i.axiom_interpretation.infer_statement(axiom=t1_a2, formula=u.f(r1, o2, o3))
        with u.v() as t2_p5, u.v() as y, u.v() as z:
            t1_p3_implication = t1.i.axiom_interpretation.infer_statement(
                axiom=t1_a2,
                formula=u.f(u.r.implies,
                            u.f(u.r.land, u.f(r1, t2_p5, y),
                                u.f(r1, y, z)),
                            u.f(r1, t2_p5, z)))
        t1.stabilize()
        hypothetical_formula = u.f(u.r.lnot, u.f(r1, o1, o3))
        # H1: ¬(𝑟₁(𝑜₁, 𝑜₃))
        t1_h1 = t1.pose_hypothesis(hypothetical_proposition=hypothetical_formula)
        t2 = t1_h1.hypothetical_theory
        t2_p5 = t1_h1.hypothetical_proposition
        t2_p6 = t2.i.conjunction_introduction.infer_statement(inc_p=t1_p1, q=t1_p2)
        t2_p7 = t2.i.variable_substitution.infer_statement(t1_p3_implication, o1, o2, o3)
        # t2_p8: 𝑟₁(𝑜₁, 𝑜₃) by modus ponens
        t2_p8 = t2.i.modus_ponens.infer_statement(p=t2_p7, inc_p=t2_p6)
        # p5 is the negation of p8, which is a contradiction in t2
        p9 = t1.i.inconsistency_introduction.infer_statement(inc_p=t2_p8, p=t2_p5,
                                                             inconsistent_theory=t2)
