from unittest import TestCase
import punctilious as p
import random_data


class TestDefinition(TestCase):
    def test_definition(self):
        echo_definition = p.configuration.echo_definition_declaration
        p.configuration.echo_definition_declaration = True
        u = p.UniverseOfDiscourse('white-sheet-of-paper')
        content1 = random_data.random_sentence()
        content2 = random_data.random_sentence(min_words=30)
        content3 = random_data.random_sentence()
        content4 = random_data.random_sentence()
        content5 = random_data.random_sentence()
        d1 = u.declare_definition(content1)
        d2 = u.declare_definition(content2)
        d3 = u.declare_definition(content3, header=p.ObjctHeader('1.1.1'))
        d4 = u.declare_definition(content4, header='1.1.2')
        d5 = u.declare_definition(content5, header='1.1.3', dashed_name='my-definition')
        self.assertEqual(f'𝐝₁: “{content1}”', d1.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐝₂: “{content2}”', d2.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐃𝐞𝐟𝐢𝐧𝐢𝐭𝐢𝐨𝐧 𝟏.𝟏.𝟏 (d₃): “{content3}”', d3.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐃𝐞𝐟𝐢𝐧𝐢𝐭𝐢𝐨𝐧 𝟏.𝟏.𝟐 (d₄): “{content4}”', d4.repr_as_statement(wrap=False))
        self.assertEqual(f'𝐃𝐞𝐟𝐢𝐧𝐢𝐭𝐢𝐨𝐧 𝟏.𝟏.𝟑 (d₅): “{content5}”', d5.repr_as_statement(wrap=False))
        p.configuration.echo_definition_declaration = echo_definition
