from unittest import TestCase
import punctilious as pu
import punctilious.random_data as random_data


class TestDefinitionInclusion(TestCase):
    def test_definition_inclusion(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = False
        pu.configuration.echo_definition_inclusion = False
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.a.declare(content1)
        ad2 = u.a.declare(content2)
        t = u.t.declare()
        ai1 = t.include_definition(ad1)
        ai2 = t.include_definition(ad2)
        pu.prnt(ai1.rep_report())

    def test_definition_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = False
        pu.configuration.echo_definition_inclusion = False
        u = pu.UniverseOfDiscourse()
        dd1 = u.d.declare(natural_language='Let f(foo) be defined as g(bar,qux).')
        t = u.t.declare()
        di1 = t.include_definition(dd1, echo=True)
        foo = u.o.declare(symbol='foo', auto_index=False)
        bar = u.o.declare(symbol='bar', auto_index=False)
        qux = u.o.declare(symbol='qux', auto_index=False)
        f = u.c1.declare(1, symbol='f', auto_index=False, signal_proposition=True)
        g = u.c1.declare(2, symbol='g', auto_index=False, signal_proposition=True)
        dii1 = t.i.definition_interpretation.infer_formula_statement(d=di1, x=u.declare_compound_formula(f, foo),
            y=u.declare_compound_formula(g, bar, qux), echo=True)
        self.assertTrue(dii1.valid_proposition.is_formula_syntactically_equivalent_to(
            u.declare_compound_formula(u.c1.equal, u.declare_compound_formula(f, foo),
                u.declare_compound_formula(g, bar, qux))))
