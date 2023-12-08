from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestAxiomInclusion(TestCase):
    def test_axiom_inclusion(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_axiom_declaration = True
        pu.configuration.echo_axiom_inclusion = True
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.a.declare(content1)
        ad2 = u.a.declare(content2)
        t = u.t.declare()
        ai1 = t.include_axiom(ad1)
        ai2 = t.include_axiom(ad2)
        pu.prnt(ai1.rep_report())

    def test_axiom_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.encoding = pu.encodings.unicode
        pu.configuration.echo_default = False
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.a.declare(content1)
        ad2 = u.a.declare(content2)
        t = u.t.declare()
        ai1 = t.include_axiom(ad1)
        ai2 = t.include_axiom(ad2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.c1.declare(1, symbol='r', signal_proposition=True)
        r2 = u.c1.declare(2, symbol='r', signal_proposition=True)
        aii1 = t.i.axiom_interpretation.infer_formula_statement(ai1, u.declare_compound_formula(r1, o1))
        self.assertTrue(
            aii1.valid_proposition.is_formula_syntactically_equivalent_to(u.declare_compound_formula(r1, o1)))
        print(aii1.rep_report())
