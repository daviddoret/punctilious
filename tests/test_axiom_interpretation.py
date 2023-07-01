from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomInterpretation(TestCase):
    def test_axiom_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.text_format = pu.text_formats.plaintext
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.declare_axiom(content1)
        ad2 = u.declare_axiom(content2)
        t = u.t()
        ai1 = t.include_axiom(ad1)
        ai2 = t.include_axiom(ad2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(2, signal_proposition=True)
        aii1 = t.i.axiom_interpretation.infer_statement(ai1, u.f(r1, o1))
        self.assertTrue(aii1.valid_proposition.is_formula_equivalent_to(u.f(r1, o1)))
        print(aii1.rep_report())
