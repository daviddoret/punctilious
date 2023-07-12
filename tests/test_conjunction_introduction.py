from unittest import TestCase
import punctilious as pu
import random_data


class TestConjunctionIntroduction(TestCase):
    def test_ci(self):
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(r1, o1, o2))
        phi2 = t.i.axiom_interpretation.infer_statement(ap, u.f(r2, o3))
        phi3 = t.i.ci.infer_statement(phi1, phi2)
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃))',
                         phi3.rep_formula(text_format=pu.encodings.unicode))
        phi4 = t.i.ci.infer_statement(phi1, phi1)
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₁(𝑜₁, 𝑜₂))',
                         phi4.rep_formula(text_format=pu.encodings.unicode))
