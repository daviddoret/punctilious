from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInterpretation(TestCase):
    def test_definition_interpretation(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = True
        pu.configuration.echo_definition_inclusion = True
        u = pu.UniverseOfDiscourse()
        t = u.t()
        # add an arbitrary definition
        content1 = random_data.random_sentence()
        def_declaration = u.declare_definition(content1)
        def_inclusion = t.include_definition(def_declaration)
        o1 = u.o.declare()
        o2 = u.o.declare()
        o3 = u.o.declare()
        r1 = u.r.declare(1, signal_proposition=True)
        r2 = u.r.declare(2, signal_proposition=True)
        def_interpretation = t.i.definition_interpretation.infer_statement(
            def_inclusion,
            u.f(u.r.equal, o1, u.f(r2, o3, o2)),
            echo=True)
        self.assertTrue(
            def_interpretation.valid_proposition.is_formula_equivalent_to(u.f(u.r.equal, o1, u.f(r2, o3, o2))))
