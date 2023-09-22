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
        ad1 = u.declare_definition(content1)
        ad2 = u.declare_definition(content2)
        t = u.t()
        ai1 = t.include_definition(ad1)
        ai2 = t.include_definition(ad2)
        pu.prnt(ai1.rep_report())

    def test_definition_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = False
        pu.configuration.echo_definition_inclusion = False
        u = pu.UniverseOfDiscourse()
        dd1 = u.declare_definition(natural_language='Let f(foo) be defined as g(bar,qux).')
        t = u.t()
        di1 = t.include_definition(dd1, echo=True)
        foo = u.o.declare(nameset=pu.NameSet(symbol='foo', index=None))
        bar = u.o.declare(nameset=pu.NameSet(symbol='bar', index=None))
        qux = u.o.declare(nameset=pu.NameSet(symbol='qux', index=None))
        f = u.r.declare(1, nameset=pu.NameSet(symbol='f', index=None), signal_proposition=True)
        g = u.r.declare(2, nameset=pu.NameSet(symbol='g', index=None), signal_proposition=True)
        dii1 = t.i.definition_interpretation.infer_formula_statement(di1,
            u.f(u.r.equal, u.f(f, foo), u.f(g, bar, qux)), echo=True)
        self.assertTrue(dii1.valid_proposition.is_formula_syntactically_equivalent_to(
            u.f(u.r.equal, u.f(f, foo), u.f(g, bar, qux))))
