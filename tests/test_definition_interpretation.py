from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInterpretation(TestCase):
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
        dii1 = t.i.definition_interpretation.infer_statement(di1, u.f(u.r.equal, u.f(f, foo),
                                                                      u.f(g, bar, qux)),
                                                             echo=True)
        self.assertTrue(dii1.valid_proposition.is_formula_equivalent_to(
            u.f(u.r.equal, u.f(f, foo), u.f(g, bar, qux))))
