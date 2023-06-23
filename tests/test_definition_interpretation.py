from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInterpretation(TestCase):
    def test_definition_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = True
        pu.configuration.echo_definition_inclusion = True
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        dd1 = u.declare_definition(content1)
        dd2 = u.declare_definition(content2)
        t = u.t()
        di1 = t.include_definition(dd1)
        di2 = t.include_definition(dd2)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(2, signal_proposition=True)
        dii1 = t.i.definition_interpretation.infer_statement(di1, u.f(u.r.equal, u.f(r1, o1), u.f(r2, o2, o3)),
                                                             echo=True)
        self.assertTrue(dii1.valid_proposition.is_formula_equivalent_to(u.f(u.r.equal, u.f(r1, o1), u.f(r2, o2, o3))))
