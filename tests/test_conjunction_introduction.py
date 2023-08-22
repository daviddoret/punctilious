from unittest import TestCase
import punctilious as pu
import random_data


class TestConjunctionIntroduction(TestCase):
    def test_ci(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        t.i.axiom_interpretation.infer_statement(ap, r1(o1, o2))
        t.i.axiom_interpretation.infer_statement(ap, r2(o3))
        phi3 = t.i.ci.infer_statement(p=r1(o1, o2), q=r2(o3))
        self.assertTrue(phi3.is_formula_syntactically_equivalent_to(r1(o1, o2) | u.r.land | r2(o3)))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃))', phi3.rep_formula(encoding=pu.encodings.unicode))
        phi4 = t.i.ci.infer_statement(p=r1(o1, o2), q=r1(o1, o2))
        self.assertTrue(
            phi4.is_formula_syntactically_equivalent_to(r1(o1, o2) | u.r.land | r1(o1, o2)))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₁(𝑜₁, 𝑜₂))',
            phi4.rep_formula(encoding=pu.encodings.unicode))

    def test_ci_failure(self):
        pu.configuration.echo_default = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        t.i.axiom_interpretation.infer_statement(ap, r1(o1, o2))
        t.i.axiom_interpretation.infer_statement(ap, r2(o3))
        phi3 = t.i.ci.infer_statement(p=r1(o1, o2), q=r2(o3))
        self.assertTrue(phi3.is_formula_syntactically_equivalent_to(r1(o1, o2) | u.r.land | r2(o3)))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∧ 𝑟₂(𝑜₃))', phi3.rep_formula(encoding=pu.encodings.unicode))
        # Trying to pass a formula that is not a valid formula-statement must raise an Exception
        with self.assertRaises(pu.FailedVerificationException):
            phi4 = t.i.ci.infer_statement(p=r1(o1, o2), q=r1(o1, o3))
