from unittest import TestCase
import punctilious as p
import random_data


class TestDefinitionInclusion(TestCase):
    def test_definition_inclusion(self):
        p.configuration.echo_default = False
        p.configuration.echo_definition_inclusion = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        d1 = u.pose_definition(content1, header='foo')
        d2 = u.pose_definition(content2, header='bar')
        t1 = u.t(header='theory 1')
        t2 = u.t(header='theory 2')
        t1.endorse_definition(d1)
        t1.endorse_definition(d2)
        t2.endorse_definition(d1)
