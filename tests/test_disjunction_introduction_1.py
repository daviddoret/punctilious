from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDisjunctionIntroduction1(TestCase):

    def test_di1(self):
        import sample.sample_disjunction_introduction_1 as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Relation = test.r1
        r2: pu.Relation = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            o2=r2(o3) | u.r.lor | r1(o1, o2)))
        self.assertEqual('(r2(o3) or r1(o1, o2))',
            proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('(𝑟₂(𝑜₃) ∨ 𝑟₁(𝑜₁, 𝑜₂))',
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
        t.i.axiom_interpretation.infer_formula_statement(ap, r2(o3))
        with self.assertRaises(pu.PunctiliousException):
            phi3 = t.i.disjunction_introduction_1.infer_formula_statement(p=r1(o1, o2), q=r2(o3))
