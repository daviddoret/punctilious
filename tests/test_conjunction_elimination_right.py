from unittest import TestCase
import punctilious as p
import random_data


class TestConjunctionEliminationRight(TestCase):
    def test_cer(self):
        u = p.UniverseOfDiscourse('conjunction-elimination-right-universe')
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t('conjunction-elimination-right-theory')
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(u.r.conjunction, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(◆₁(ℴ₁, ℴ₂) ∧ ◆₂(ℴ₃))', phi1.repr())
        phi2 = t.i.cer.infer_statement(phi1)
        self.assertEqual('◆₂(ℴ₃)', phi2.repr())
