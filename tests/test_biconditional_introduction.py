from unittest import TestCase
import punctilious as pu
import random_data


class TestBiconditionalIntroduction(TestCase):
    def test_biconditional_introduction(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(arity=2, nameset='r', signal_proposition=True)
        r2 = u.r.declare(arity=1, nameset='r', signal_proposition=True)
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap,
            u.f(u.r.implies, u.f(r1, o1, o2), u.f(r2, o3)))
        phi2 = t.i.axiom_interpretation.infer_statement(ap,
            u.f(u.r.implies, u.f(r2, o3), u.f(r1, o1, o2)))
        phi3 = t.i.bi.infer_statement(phi1, phi2, echo=True)
        self.assertEqual('(r1(o1, o2) <==> r2(o3))', phi3.rep_formula())
