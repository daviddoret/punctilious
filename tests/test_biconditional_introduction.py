from unittest import TestCase
import punctilious as p
import random_data


class TestBiconditionalIntroduction(TestCase):
    def test_biconditional_introduction(self):
        p.configuration.echo_default = False
        p.configuration.echo_statement = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o2.declare()
        o2 = u.o2.declare()
        o3 = u.o2.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t(
            'testing-theory')
        a = u.axiom('The arbitrary axiom of testing.')
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(u.r.implies, u.f(r1, o1, o2), u.f(r2, o3)), ap=ap)
        phi2 = t.dai(u.f(u.r.implies, u.f(r2, o3), u.f(r1, o1, o2)), ap=ap)
        phi3 = t.i.bi.infer_statement(phi1, phi2, echo=True)
        self.assertEqual(
            '((◆₁(ℴ₁, ℴ₂) ⟹ ◆₂(ℴ₃)) ⟺ (◆₂(ℴ₃) ⟹ ◆₁(ℴ₁, ℴ₂)))', phi3.repr())
