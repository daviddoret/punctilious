from unittest import TestCase
import punctilious as pu
import random_data


class TestAbsorption(TestCase):
    def test_absorption_1(self):
        pu.configuration.echo_default = True
        pu.configuration.encoding = pu.encodings.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        t = u.t()
        a1 = u.declare_axiom(random_data.random_sentence())
        a2 = t.include_axiom(a1)
        p1 = t.i.axiom_interpretation.infer_statement(a2, u.f(u.r.implies, o1, o2))
        p2 = t.i.absorb.infer_statement(p_implies_q=p1, echo=True)
        self.assertEqual('(o1 ==> (o1 and o2))', p2.rep_formula(expand=True))
