from unittest import TestCase
import punctilious as p
import random_data


class TestConjunctionIntroduction(TestCase):
    def test_conjunction_introduction(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t(
            'testing-theory',
            include_conjunction_introduction_inference_rule=True)
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(r1, o1, o2), ap=ap)
        phi2 = t.dai(u.f(r2, o3), ap=ap)

        phi3 = t.ci(phi1, phi2)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ∧ ◆₂(ℴ₃))', phi3.repr())

        phi4 = t.ci(phi1, phi1)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ∧ ◆₁(ℴ₁, ℴ₂))', phi4.repr())
