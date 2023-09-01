from unittest import TestCase
import punctilious as pu
import random_data


class TestDisjunctionIntroduction2(TestCase):

    def test_di2(self):
        import sample.code.disjunction_introduction_2 as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=r1(o1, o2) | u.r.lor | r2(o3)))
        self.assertEqual('(r1(o1, o2) or r2(o3))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₁(𝑜₁, 𝑜₂) ∨ 𝑟₂(𝑜₃))',
            proposition_of_interest.rep_formula(pu.encodings.unicode))

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
            phi3 = t.i.disjunction_introduction_2.infer_statement(p=r1(o1, o2), q=r2(o3))
