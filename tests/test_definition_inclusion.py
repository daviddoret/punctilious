from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInclusion(TestCase):
    def test_definition_inclusion(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_declaration = True
        pu.configuration.echo_definition_inclusion = True
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        ad1 = u.declare_definition(content1)
        ad2 = u.declare_definition(content2)
        t = u.t()
        ai1 = t.include_definition(ad1)
        ai2 = t.include_definition(ad2)
        pu.prnt(ai1.rep_report())
