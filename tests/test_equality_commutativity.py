from unittest import TestCase
import punctilious as pu
import random_data


class TestEqualityCommutativity(TestCase):
    def test_ec(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(2, signal_proposition=True)
        r2 = u.r.declare(1, signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(u.r.equal, u.f(r1, o1, o2),
                                                                u.f(r2, o3)))
        self.assertEqual('(r1(o1, o2) = r2(o3))', phi1.rep_formula())
        phi2 = t.i.ec.infer_statement(phi1, echo=True)
        self.assertEqual('(r2(o3) = r1(o1, o2))', phi2.rep_formula())
