from unittest import TestCase
import punctilious as p
import random_data


class TestModusPonens(TestCase):

    def test_modus_ponens_without_variable(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('modus-ponens-test-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        p_formula = u.f(r1, o1)
        self.assertEqual('◆₁(ℴ₁)', p_formula.repr_as_formula())
        q_formula = u.f(r2, o2)
        self.assertEqual('◆₂(ℴ₂)', q_formula.repr_as_formula())
        p_implies_q = t.dai(u.f(u.r.implies, p_formula, q_formula), ap=ap)
        p_statement = t.dai(p_formula, ap=ap)
        conclusion = t.i.mp.infer_statement(p_implies_q, p_statement)
        self.assertEqual('◆₂(ℴ₂)', conclusion.valid_proposition.repr_as_formula())

    def test_modus_ponens_with_variable(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        o4 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        t = u.t('modus-ponens-test-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        with u.v() as x, u.v() as y, u.v() as z:
            implication = t.dai(
                u.f(
                    u.r.implies,
                    u.f(u.r.land, u.f(r1, x, y), u.f(r1, y, z)),
                    u.f(r1, x, z)),
                ap=ap)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(r1, o2, o3), ap=ap)
        phi1_and_phi2 = t.i.ci.infer_statement(phi1, phi2)
        conclusion_1 = t.i.mp.infer_statement(implication, phi1_and_phi2)
        self.assertEqual('◆(ℴ₁, ℴ₃)', conclusion_1.valid_proposition.repr_as_formula())
