from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestEqualTermsSubstitution(TestCase):
    def test_equal_terms_substitution_simple(self):
        import sample.sample_equal_terms_substitution as test
        u: pu.UniverseOfDiscourse = test.u
        o1: pu.SimpleObjct = test.o1
        o2: pu.SimpleObjct = test.o2
        o3: pu.SimpleObjct = test.o3
        r1: pu.Connective = test.r1
        r2: pu.Connective = test.r2
        proposition_of_interest: pu.InferredStatement = test.proposition_of_interest
        self.assertTrue(proposition_of_interest.is_formula_syntactically_equivalent_to(
            phi=r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))))
        self.assertEqual('r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))',
                         proposition_of_interest.rep_formula(pu.encodings.plaintext))
        self.assertEqual('𝑟₁(𝑟₁(𝑟₁(𝑟₂(𝑜₃), 𝑟₂(𝑜₃)), 𝑜₂), 𝑟₂(𝑟₂(𝑜₃)))',
                         proposition_of_interest.rep_formula(pu.encodings.unicode_extended))

    def test_equal_terms_substitution_with_theory_extension(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_statement = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(2, signal_proposition=True)
        r2 = u.c1.declare(1, signal_proposition=True)
        t1 = u.t.declare()
        a = u.a.declare(random_data.random_sentence())
        ap = t1.include_axiom(a)
        q_equal_r = t1.i.axiom_interpretation.infer_formula_statement(ap,
                                                                      u.declare_compound_formula(u.c1.equal,
                                                                                                 u.declare_compound_formula(
                                                                                                     r1, o1, o2),
                                                                                                 u.declare_compound_formula(
                                                                                                     r2, o3)),
                                                                      lock=False)
        self.assertEqual('(r1(o1, o2) = r2(o3))', q_equal_r.rep_formula(encoding=pu.encodings.plaintext))
        p = t1.i.axiom_interpretation.infer_formula_statement(ap, u.declare_compound_formula(r1,
                                                                                             u.declare_compound_formula(
                                                                                                 r1,
                                                                                                 u.declare_compound_formula(
                                                                                                     r1,
                                                                                                     u.declare_compound_formula(
                                                                                                         r1, o1, o2),
                                                                                                     u.declare_compound_formula(
                                                                                                         r1, o1, o2)),
                                                                                                 o2),
                                                                                             u.declare_compound_formula(
                                                                                                 r2,
                                                                                                 u.declare_compound_formula(
                                                                                                     r1, o1, o2))),
                                                              lock=True)
        self.assertEqual('r1(r1(r1(r1(o1, o2), r1(o1, o2)), o2), r2(r1(o1, o2)))',
                         p.rep_formula(encoding=pu.encodings.plaintext))
        t2 = u.t.declare(extended_theory=t1, extended_theory_limit=p)
        p_prime = t2.i.ets.infer_formula_statement(p=p, x_equal_y=q_equal_r)
        self.assertEqual('r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))',
                         p_prime.rep_formula(encoding=pu.encodings.plaintext))