from unittest import TestCase
import punctilious as pu
import random_data


class TestAbsorption(TestCase):
    def test_absorb(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.plaintext
        u = pu.UniverseOfDiscourse()
        o1 = u.o.declare()
        o2 = u.o.declare()
        t = u.t()
        a = u.declare_axiom(random_data.random_sentence())
        ap = t.include_axiom(a)
        phi1 = t.i.axiom_interpretation.infer_statement(ap, u.f(u.r.implies, o1, o2))
        phi2 = t.i.absorb.infer_statement(phi1)
        self.assertEqual('(o1 ==> (o1 and o2))', phi2.repr_as_formula(expand=True))
