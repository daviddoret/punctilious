from unittest import TestCase
import punctilious as pu
import random_data


class TestDefinitionInclusion(TestCase):
    def test_definition_inclusion(self):
        pu.configuration.echo_default = False
        pu.configuration.echo_definition_inclusion = True
        u = pu.UniverseOfDiscourse()
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        d1 = u.declare_definition(content1, title='foo')
        d2 = u.declare_definition(content2, title='bar')
        t1 = u.t(title='theory 1')
        t2 = u.t(title='theory 2')
        t1.include_definition(d1)
        t1.include_definition(d2)
        t2.include_definition(d1)
