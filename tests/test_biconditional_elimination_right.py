from unittest import TestCase
import punctilious as p
import random_data


class TestBiconditionalEliminationRight(TestCase):
    def test_ber(self):
        u = p.UniverseOfDiscourse('biconditional-elimination-right-universe')
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('biconditional-elimination-right-theory')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.dai(u.f(u.r.biconditional, u.f(r1, o1, o2), u.f(r2, o3)), ap=ap, echo=True)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ⟺ ◆₂(ℴ₃))', phi1.repr())
        phi2 = t.i.ber.infer_statement(phi1, echo=True)
        self.assertEqual('(◆₂(ℴ₃) ⟹ ◆₁(ℴ₁, ℴ₂))', phi2.repr())
