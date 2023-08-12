from unittest import TestCase
import punctilious as pu
import random_data


class TestAxiomInterpretation(TestCase):

    def test_axiom_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.unicode
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        # Prepare the universe-of-discourse
        a1 = u.declare_axiom(natural_language=random_data.random_sentence())
        o1 = u.o.declare()
        o2 = u.o.declare()
        r1 = u.r.declare(arity=2, signal_proposition=True)
        phi1 = u.f(r1, o1, o2)
        # Elaborate the theory
        t = u.t()
        a2 = t.include_axiom(a1)
        p1 = t.i.axiom_interpretation.infer_statement(a2, phi1)
        self.assertTrue(p1.valid_proposition.is_syntactic_equivalent_to(u.f(r1, o1, o2)))
        print(p1.rep_report())
