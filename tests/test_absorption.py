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
        phi1_useless_noise = u.f(u.r.implies, o2, o1)
        phi2 = u.f(u.r.implies, o1, o2)
        phi3_useless_noise = u.f(u.r.implies, o2, o2)
        p1_useless_noise = t.i.axiom_interpretation.infer_statement(axiom=a2,
            formula=phi1_useless_noise)
        p2 = t.i.axiom_interpretation.infer_statement(axiom=a2, formula=phi2)
        p3 = t.i.axiom_interpretation.infer_statement(axiom=a2, formula=phi3_useless_noise)
        # Pass formula-statement as parameter
        p4 = t.i.absorb.infer_statement(p_implies_q=p2, echo=True)
        self.assertEqual('(o1 ==> (o1 and o2))', p4.rep_formula(expand=True))
        # Pass formula as parameter
        p5 = t.i.absorb.infer_statement(p_implies_q=phi2, echo=True)
        self.assertEqual('(o1 ==> (o1 and o2))', p5.rep_formula(expand=True))
        # Pass formula as tuple
        p6 = t.i.absorb.infer_statement(p_implies_q=(u.r.implies, o1, o2), echo=True)
        self.assertEqual('(o1 ==> (o1 and o2))', p6.rep_formula(expand=True))
        # Pass formula with pseudo-infix notation
        p7 = t.i.absorb.infer_statement(p_implies_q=o1 | u.r.implies | o2, echo=True)
        self.assertEqual('(o1 ==> (o1 and o2))', p7.rep_formula(expand=True))
