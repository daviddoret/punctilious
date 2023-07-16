from unittest import TestCase
import punctilious as pu
import random_data


class TestEqualTermsSubstitution(TestCase):
    def test_ets(self):
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
        phi1 = t.i.axiom_interpretation.infer_statement(
            ap, u.f(u.r.equal, u.f(r1, o1, o2), u.f(r2, o3)))
        self.assertEqual('(r1(o1, o2) = r2(o3))',
                         phi1.rep_formula(encoding=pu.encodings.plaintext))
        phi2 = t.i.axiom_interpretation.infer_statement(ap,
                                                        u.f(r1, u.f(r1, u.f(r1, u.f(r1, o1, o2),
                                                                            u.f(r1, o1, o2)), o2),
                                                            u.f(r2, u.f(r1, o1, o2))),
                                                        echo=True)
        self.assertEqual('r1(r1(r1(r1(o1, o2), r1(o1, o2)), o2), r2(r1(o1, o2)))',
                         phi2.rep_formula(encoding=pu.encodings.plaintext))
        phi3 = t.i.ets.infer_statement(phi2, phi1, echo=True)
        self.assertEqual('r1(r1(r1(r2(o3), r2(o3)), o2), r2(r2(o3)))',
                         phi3.rep_formula(encoding=pu.encodings.plaintext))
