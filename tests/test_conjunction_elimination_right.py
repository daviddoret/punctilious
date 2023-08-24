from unittest import TestCase
import punctilious as pu
import random_data


class TestConjunctionEliminationRight(TestCase):
    def test_cer(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap,
            u.f(u.r.conjunction, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃))', phi1.rep_formula(pu.encodings.unicode))
        phi2 = t.i.cer.infer_statement(p_and_q=phi1)
        self.assertEqual('𝑟₂(𝑜₃)', phi2.rep_formula(encoding=pu.encodings.unicode))
