from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInterpretation(TestCase):
    def test_definition_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = True
        pu.configuration.echo_definition_inclusion = True
        u = pu.UniverseOfDiscourse()
        dd1 = u.declare_definition('f(foo) is defined as g(bar,qux).')
        t = u.t()
        di1 = t.include_definition(dd1)
        foo = u.o.declare('foo')
        bar = u.o.declare('bar')
        qux = u.o.declare('qux')
        f = u.r.declare(1, nameset='f', signal_proposition=True)
        g = u.r.declare(2, nameset='g', signal_proposition=True)
        dii1 = t.i.definition_interpretation.infer_statement(di1, u.f(u.r.equal, u.f(f, foo),
                                                                      u.f(g, bar, qux)),
                                                             echo=True)
        self.assertTrue(dii1.valid_proposition.is_formula_equivalent_to(
            u.f(u.r.equal, u.f(f, foo), u.f(g, bar, qux))))
