from unittest import TestCase
import punctilious as pu
import random_data


class TestEqualTermsSubstitution(TestCase):
    def test_equal_terms_substitution_simple(self):
        pu.configuration.echo_default = False
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
            u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(r1(o1, o2) = r2(o3))', phi1.rep_formula(encoding=pu.encodings.plaintext))
        phi2 = t.i.axiom_interpretation.infer_statement(ap,
            u.f(r1, u.f(r1, u.f(r1, u.f(r1, o1, o2), u.f(r1, o1, o2)), o2),
                u.f(r2, u.f(r1, o1, o2))), echo=True)
        self.assertEqual('r1(r1(r1(r1(o1, o2), r1(o1, o2)), o2), r2(r1(o1, o2)))',
            phi2.rep_formula(encoding=pu.encodings.plaintext))
        phi3 = t.i.ets.infer_statement(p=phi2, q_equal_r=phi1, echo=True)
        self.assertEqual('r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))',
            phi3.rep_formula(encoding=pu.encodings.plaintext))

    def test_equal_terms_substitution_with_theory_extension(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_statement = True
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t1 = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t1.include_axiom(a)
        q_equal_r = t1.i.axiom_interpretation.infer_statement(ap,
            u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(r1(o1, o2) = r2(o3))',
            q_equal_r.rep_formula(encoding=pu.encodings.plaintext))
        p = t1.i.axiom_interpretation.infer_statement(ap,
            u.f(r1, u.f(r1, u.f(r1, u.f(r1, o1, o2), u.f(r1, o1, o2)), o2),
                u.f(r2, u.f(r1, o1, o2))))
        self.assertEqual('r1(r1(r1(r1(o1, o2), r1(o1, o2)), o2), r2(r1(o1, o2)))',
            p.rep_formula(encoding=pu.encodings.plaintext))
        t2 = u.declare_theory(extended_theory=t1, extended_theory_limit=p)
        p_prime = t2.i.ets.infer_statement(p=p, q_equal_r=q_equal_r)
        self.assertEqual('r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))',
            p_prime.rep_formula(encoding=pu.encodings.plaintext))
