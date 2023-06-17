from unittest import TestCase
import punctilious as p
import random_data


class TestAbsorption(TestCase):
    def test_absorb(self):
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        o1 = u.o()
        o2 = u.o()
        t = u.t('testing-theory')
        a = u.elaborate_axiom(random_data.random_sentence())
        ap = t.postulate_axiom(a)
        phi1 = t.dai(u.f(u.r.implies, o1, o2), ap=ap)
        phi2 = t.i.absorb.infer_statement(phi1)
        self.assertEqual('(ℴ₁ ⟹ (ℴ₁ ∧ ℴ₂))', phi2.repr())