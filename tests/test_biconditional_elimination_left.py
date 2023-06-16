from unittest import TestCase
import punctilious as p
import random_data


class TestBiconditionalEliminationLeft(TestCase):
    def test_bel(self):
        u = p.UniverseOfDiscourse('biconditional-elimination-left-universe')
        o1 = u.o()
        o2 = u.o()
        o3 = u.o()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('biconditional-elimination-left-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(u.r.biconditional, u.f(r1, o1, o2), u.f(r2, o3)), ap=ap)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ⟺ ◆₂(ℴ₃))', phi1.repr_as_formula())
        phi2 = t.i.bel.infer_statement(phi1)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ⟹ ◆₂(ℴ₃))', phi2.repr_as_formula())
