from unittest import TestCase
import punctilious as pu
import random_data


class TestDisjunctionIntroductionLeft(TestCase):

    def test_di(self):
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
        phi3 = t.i.disjunction_introduction_left.infer_statement(p=r1(o1, o2), q=r2(o3))
        self.assertTrue(phi3.is_formula_syntactically_equivalent_to(r2(o3) | u.r.lor | r1(o1, o2)))
        self.assertEqual('(𝑟₂(𝑜₃) ∨ 𝑟₁(𝑜₁, 𝑜₂))', phi3.rep_formula(encoding=pu.encodings.unicode))

    def test_di_failure(self):
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
        t.i.axiom_interpretation.infer_statement(ap, r2(o3))
        with self.assertRaises(pu.FailedVerificationException):
            phi3 = t.i.disjunction_introduction_left.infer_statement(p=r1(o1, o2), q=r2(o3))
