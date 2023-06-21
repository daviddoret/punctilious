from unittest import TestCase
import punctilious as pu
import random_data


class TestBiconditionalEliminationLeft(TestCase):
    def test_bel(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.dai(u.f(u.r.biconditional, u.f(r1, o1, o2), u.f(r2, o3)), ap=ap)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ⟺ ◆₂(ℴ₃))', phi1.repr_as_formula())
        phi2 = t.i.bel.infer_statement(phi1)
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ⟹ ◆₂(ℴ₃))', phi2.repr_as_formula())
